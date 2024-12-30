import openai
import numpy as np
import pandas as pd
import os

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
items_path = 'dataframes/scales_df.csv'
parquet_path = 'dataframes/items_with_embeddings.parquet'

# Load data
items = pd.read_csv(items_path)
item = items.loc[47]
scale = item['Scale']
dimension = item['Dimension']
item_sit = item['Item-sit']
print(f"Scale: {scale}, Dimension: {dimension}, Item-sit: {item_sit}")

# Ensure the OpenAI API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Constants
MODEL_NAME = "text-embedding-3-large"

# Function to get embeddings for a single text
def get_single_text_embedding(text):
    response = openai.embeddings.create(
        model=MODEL_NAME,
        input=text
    )
    embedding = np.array(response.data[0].embedding)  # Extract the embedding
    return embedding

# Generate embedding for the single item
item_to_embed = item_sit  # Use the text from row 47
print("Generating embedding for the specific item...")
single_embedding = get_single_text_embedding([item_to_embed])  # Note: Input must be a list

# Output or save the embedding
print("Embedding generated successfully.")
print(single_embedding)

# Load the Parquet file with embeddings
items_embedding = pd.read_parquet(parquet_path)

# Replace row 47 in the DataFrame
items_embedding.at[47, 'Scale'] = scale
items_embedding.at[47, 'Dimension'] = dimension
items_embedding.at[47, 'Item-sit'] = item_sit
items_embedding.at[47, 'embedding'] = single_embedding.tolist()  # Ensure embedding is stored as a list

# Save the updated DataFrame back to Parquet
items_embedding.to_parquet(parquet_path, index=False)

print("Row 47 replaced in the Parquet file with the updated embedding.")
