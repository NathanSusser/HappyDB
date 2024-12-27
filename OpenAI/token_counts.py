import pandas as pd
import os
import tiktoken

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
sentences = pd.read_csv(sentences_path)  # Cleaned sentences
items = pd.read_csv(items_path)  # Items for comparison

# Validation checks
assert not sentences['cleaned_hm'].isnull().any(), "Cleaned sentences contain null values!"
assert not items['Item-sit'].isnull().any(), "Items contain null values!"

# Initialize tokenizer
def calculate_tokens(text, model="gpt-4o"):
    tokenizer = tiktoken.encoding_for_model(model)
    return len(tokenizer.encode(text))

# Extract items (well-being measurements)
items_ls = items['Item-sit'].tolist()

# Extract sentences (cleaned happiness moments)
sentences_ls = sentences['cleaned_hm'].tolist()

# Create empty columns for token counts in the DataFrame
sentences['token_count'] = None

# Loop through sentences to calculate token counts
for i, sentence in sentences.iterrows():
    token_count = calculate_tokens(sentence['cleaned_hm'])
    sentences.at[i, 'token_count'] = token_count  # Assign token count

# Calculate aggregate token statistics
average_tokens = sentences['token_count'].mean()
max_tokens = sentences['token_count'].max()
min_tokens = sentences['token_count'].min()
total_tokens = sentences['token_count'].sum()


# Display the token statistics
print("Sentence Token Statistics:")
print(f"Average Tokens: {average_tokens}")
print(f"Max Tokens: {max_tokens}")
print(f"Min Tokens: {min_tokens}")
print(f"Total Tokens: {total_tokens}")


# Create empty columns for token counts in the DataFrame
items['token_count'] = None

# Loop through sentences to calculate token counts
for i, item in items.iterrows():
    token_count = calculate_tokens(item['Item-sit'])
    items.at[i, 'token_count'] = token_count  # Assign token count

# Calculate aggregate token statistics
average_tokens = items['token_count'].mean()
max_tokens = items['token_count'].max()
min_tokens = items['token_count'].min()
total_tokens = items['token_count'].sum()

print("\nitem Token Statistics:")
print(f"Average Tokens: {average_tokens}")
print(f"Max Tokens: {max_tokens}")
print(f"Min Tokens: {min_tokens}")
print(f"Total Tokens: {total_tokens}")
