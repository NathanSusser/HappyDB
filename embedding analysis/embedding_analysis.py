import pandas as pd
import numpy as np
import os

os.chdir('/Users/nsusser/Desktop/Github/happyDB/dataframes')

# Load Parquet files
sentences_df = pd.read_parquet('sentences_with_embeddings.parquet')  # Contains sentence embeddings
items_df = pd.read_parquet('items_with_embeddings.parquet')          # Contains item embeddings

# Convert embeddings to NumPy arrays
sentence_embeddings = np.array(sentences_df['embedding'].tolist())  
item_embeddings = np.array(items_df['embedding'].tolist())          
     

# Compute cosine similarities using matrix multiplication
similarity_matrix = np.dot(sentence_embeddings, item_embeddings.T)

# Create hierarchical column structure for dimensions, scale, and items
columns = list(zip(items_df['Scale'], items_df['Dimension'], items_df['Item-sit']))
similarity_df = pd.DataFrame(similarity_matrix, columns=pd.MultiIndex.from_tuples(columns, names=["Scale", "Dimension", "Item-sit"]))

# Add sentence and hmid information to the DataFrame
sentences = sentences_df['cleaned_hm'].tolist()  # List of sentences
hmids = sentences_df['hmid'].tolist()  # List of HMIDs (assuming it's in the DataFrame)

# Create a MultiIndex for sentences and HMIDs
row_multi_index = pd.MultiIndex.from_tuples(zip(sentences, hmids), names=["hmid", "cleaned_hm"])
similarity_df.index = row_multi_index

print(similarity_df.head())
print(similarity_df.columns)

# Save the result as a Parquet file
similarity_df.to_parquet('cos_similarity_embeddings.parquet')

print("Cosine similarity matrix calculated and saved as 'cos_similarity_embeddings.parquet'")
