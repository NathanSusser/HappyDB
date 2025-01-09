import openai
import pandas as pd
import numpy as np
import os
import time

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Validation checks
assert not sentences['cleaned_hm'].isnull().any(), "Cleaned sentences contain null values!"
assert not items['Item-sit'].isnull().any(), "Items contain null values!"

# Retrieve the OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Constants
BATCH_SIZE = 100
RATE_LIMIT_TOKENS_PER_MINUTE = 350_000
MODEL_NAME = "text-embedding-3-large"

def batch_process(texts, batch_size):
    for i in range(0, len(texts), batch_size):
        yield texts[i:i + batch_size]

def get_text_embeddings_batch(texts):
    response = openai.embeddings.create(
        model=MODEL_NAME,
        input=texts
    )
    embeddings = [np.array(data.embedding) for data in response.data]
    return embeddings

def wait_if_needed(total_tokens, start_time):
    elapsed_time = time.time() - start_time
    tokens_per_second = RATE_LIMIT_TOKENS_PER_MINUTE / 60
    expected_time = total_tokens / tokens_per_second
    if elapsed_time < expected_time:
        sleep_time = expected_time - elapsed_time
        print(f"Sleeping for {sleep_time:.2f} seconds to respect rate limits...")
        time.sleep(sleep_time)

# Incremental processing and saving for items
items_ls = items['Item-sit'].tolist()
item_embeddings = []

print("Processing items...")
start_time = time.time()
for batch in batch_process(items_ls, BATCH_SIZE):
    batch_embeddings = get_text_embeddings_batch(batch)
    item_embeddings.extend(batch_embeddings)
    wait_if_needed(len(batch) * 1000, start_time)

# Save items incrementally to Parquet
items['embedding'] = item_embeddings
items.to_parquet('dataframes/items_with_embeddings.parquet', index=False)

# Incremental processing and saving for sentences
sentences_ls = sentences['cleaned_hm'].tolist()
sentence_embeddings = []

print("Processing sentences...")
start_time = time.time()
for batch in batch_process(sentences_ls, BATCH_SIZE):
    batch_embeddings = get_text_embeddings_batch(batch)
    sentence_embeddings.extend(batch_embeddings)
    wait_if_needed(len(batch) * 1000, start_time)

# Save sentences incrementally to Parquet
sentences['embedding'] = sentence_embeddings
sentences.to_parquet('dataframes/sentences_with_embeddings.parquet', index=False)

print("Embedding process completed and saved incrementally as Parquet files.")
