import pandas as pd

# Load the Parquet file
parquet_path = 'dataframes/items_with_embeddings.parquet'
items = pd.read_parquet(parquet_path)

# Define the values to match
scale_value = "WBP"
dimension_value = "Optimism"

# Find the indices matching the conditions
matching_indices = items[(items['Scale'] == scale_value) & (items['Dimension'] == dimension_value)].index

# Print the matching indices
print("Matching indices:")
print(matching_indices)

# Print the clean values for the specific columns
# Print the matching rows cleanly
print("Matching rows:")
for i in matching_indices:
    scale = items.loc[i, 'Scale']
    dimension = items.loc[i, 'Dimension']
    item_sit = items.loc[i, 'Item-sit']
    print(f"Scale: {scale}, Dimension: {dimension}, Item-sit: {item_sit}")

import numpy as np

# Extract embeddings for rows 45 and 47
embedding_45 = items.loc[45, 'embedding']
embedding_47 = items.loc[47, 'embedding']

# Convert embeddings to NumPy arrays (if they are stored as lists)
embedding_45 = np.array(embedding_45)
embedding_47 = np.array(embedding_47)

# Check if embeddings are equivalent
are_equal = np.array_equal(embedding_45, embedding_47)
print(f"Are embeddings for rows 45 and 47 equivalent? {are_equal}")

# Optionally, check the difference (for debugging)
difference = np.linalg.norm(embedding_45 - embedding_47)
print(f"Euclidean distance between the embeddings: {difference}")
