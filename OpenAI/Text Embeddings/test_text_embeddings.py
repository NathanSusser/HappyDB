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

# Test function to process a few batches and write to test Parquet files
def test_embedding_batches(items_ls, sentences_ls, batch_size=2):
    """
    Test the embedding process with one or two batches of items and sentences.
    Writes the results to test Parquet files.
    """
    print("Testing item embedding with a few batches...")
    item_batches = list(batch_process(items_ls, batch_size))
    test_item_embeddings = []
    for batch in item_batches[:2]:  # Process only the first two batches
        item_embeddings = get_text_embeddings_batch(batch)
        test_item_embeddings.extend(item_embeddings)
        print(f"Item Batch: {batch}")
        print(f"Item Embeddings: {item_embeddings}\n")

    # Create a test DataFrame for items and write to Parquet
    test_items_df = pd.DataFrame({
        'Item-sit': items_ls[:len(test_item_embeddings)],
        'embedding': test_item_embeddings
    })
    test_items_df.to_parquet('dataframes/test_items_with_embeddings.parquet', index=False)

    print("Testing sentence embedding with a few batches...")
    sentence_batches = list(batch_process(sentences_ls, batch_size))
    test_sentence_embeddings = []
    for batch in sentence_batches[:2]:  # Process only the first two batches
        sentence_embeddings = get_text_embeddings_batch(batch)
        test_sentence_embeddings.extend(sentence_embeddings)
        print(f"Sentence Batch: {batch}")
        print(f"Sentence Embeddings: {sentence_embeddings}\n")

    # Create a test DataFrame for sentences and write to Parquet
    test_sentences_df = pd.DataFrame({
        'cleaned_hm': sentences_ls[:len(test_sentence_embeddings)],
        'embedding': test_sentence_embeddings
    })
    test_sentences_df.to_parquet('dataframes/test_sentences_with_embeddings.parquet', index=False)

    print("Test embeddings saved to test Parquet files.")

# Run the test
items_ls = items['Item-sit'].tolist()
sentences_ls = sentences['cleaned_hm'].tolist()
test_embedding_batches(items_ls, sentences_ls, batch_size=2)
