import pandas as pd
import torch
import torch.nn.functional as F
from transformers import AutoModel
import numpy as np
from tqdm import tqdm
import os
import gc

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
db_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
db = pd.read_csv(db_path)  # Cleaned sentences
items = pd.read_csv(items_path)  # Items for comparison

# Validation checks
assert not db['cleaned_hm'].isnull().any(), "Cleaned sentences contain null values!"
assert not items['Item-sit'].isnull().any(), "Items contain null values!"

# Define task instructions
query_prefix = "Compare this question to moments of happiness and evaluate their semantic similarity."
sentence_prefix = "Compare this moment of happiness to each question and evaluate their semantic similarity."

#set Device
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Load model
model = AutoModel.from_pretrained('nvidia/NV-Embed-v2', trust_remote_code=True)

# Function to batch encode with instruction
def batch_encode(texts, instruction, model, device, batch_size=32, max_length=512):
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Encoding batches", leave=True):
        batch_texts = texts[i:i + batch_size]
        batch_embeddings = model._do_encode(
            batch_texts,
            batch_size=batch_size,
            instruction=instruction,
            max_length=max_length,
            return_numpy=False
        ).to(device)
        embeddings.append(batch_embeddings)
        gc.collect()  # Free up memory
    return torch.cat(embeddings)

# Process DB and items in batches
batch_size = 32
max_length = 32768

# Extract queries (questions)
queries = items['Item-sit'].tolist()

# Extract sentences (cleaned happiness moments)
sentences = db['cleaned_hm'].tolist()

# Encode queries and sentences
print("Encoding queries...")
query_embeddings = batch_encode(queries, query_prefix, model, batch_size, max_length)

print("Encoding sentences...")
sentence_embeddings = batch_encode(sentences, sentence_prefix, model, batch_size, max_length)

# Normalize embeddings
query_embeddings = F.normalize(torch.tensor(query_embeddings), p=2, dim=1)
sentence_embeddings = F.normalize(torch.tensor(sentence_embeddings), p=2, dim=1)

# Compute cosine similarity scores
print("Computing similarity scores...")
similarity_scores = query_embeddings @ sentence_embeddings.T

# Convert to a readable DataFrame
similarity_df = pd.DataFrame(
    similarity_scores.numpy(),
    index=db['cleaned_hm'],  # Rows are sentences
    columns=items['Item-sit']  # Columns are items
)

# Save similarity scores
output_path = '/Users/nsusser/Desktop/Github/happyDB/similarity_scores.parquet'
similarity_df.to_parquet(output_path, index=True)
print(f"Similarity scores saved to {output_path}")
