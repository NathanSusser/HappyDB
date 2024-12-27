import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

# File paths for test Parquet files
test_items_path = 'dataframes/test_items_with_embeddings.parquet'
test_sentences_path = 'dataframes/test_sentences_with_embeddings.parquet'

# Read in the Parquet files
test_items = pd.read_parquet(test_items_path)
test_sentences = pd.read_parquet(test_sentences_path)

# Extract embeddings as NumPy arrays
test_item_embeddings = np.vstack(test_items['embedding'].values)
test_sentence_embeddings = np.vstack(test_sentences['embedding'].values)

# Analyze contents
print("Length of item embeddings:", len(test_item_embeddings))
print("Length of sentence embeddings:", len(test_sentence_embeddings))

# Save indices for items and sentences to separate files
test_items[['Item-sit']].to_csv('dataframes/test_item_indices.csv', index_label='Item_Index')
test_sentences[['cleaned_hm']].to_csv('dataframes/test_sentence_indices.csv', index_label='Sentence_Index')

print("Item and sentence indices saved to 'test_item_indices.csv' and 'test_sentence_indices.csv'.")

# Compute cosine similarity between each item and sentence
cosine_similarities = []
for i, item_embedding in enumerate(test_item_embeddings):
    for j, sentence_embedding in enumerate(test_sentence_embeddings):
        similarity = 1 - cosine(item_embedding, sentence_embedding)  # Cosine similarity
        cosine_similarities.append({
            'Item_Index': i,
            'Sentence_Index': j,
            'Cosine_Similarity': similarity
        })

# Convert to DataFrame
cosine_similarities_df = pd.DataFrame(cosine_similarities)

# Write cosine similarities to CSV
cosine_similarities_df.to_csv('dataframes/cosine_similarities.csv', index=False)

print("Cosine similarity analysis completed and written to 'dataframes/cosine_similarities.csv'.")
