import openai
import pandas as pd
import os
import tiktoken
import numpy as np

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Create empty columns for token counts in the DataFrame
sentences['token_count_input'] = 0
sentences['token_count_output'] = 0

# Initialize tokenizer
def calculate_tokens(text, model="gpt-4o-mini"):
    tokenizer = tiktoken.encoding_for_model(model)
    return len(tokenizer.encode(text))

# Iterate over sentences and items
for idx, row in sentences.iterrows():
    period = row['reflection_period']
    sentence = row['cleaned_hm']
    '''
    if idx == 1000:
        print(f"Processing row: {idx}")
        break'''
    
    # Convert period to a descriptive time
    if period == "24h":
        time_frame = "24 hours"
    elif period == "3m":
        time_frame = "3 months"
    else:
        time_frame = "an unknown period"
    
    # Initialize counters for token counts
    total_token_count_input = 0
    total_token_count_output = 0
    
    for _, item_row in items.iterrows():
        item = item_row['Item-sit']
        
        dev_msg = f"You are a helpful research assistant who can help me code the psychological properties of people's experiences."
        user_msg = f"The following is a description of an experience ** {sentence} **. \n \n How much does this experience indicate ** {item} **? Provide a response on a scale of 1 to 7. Respond with a low number if the experience does not indicate that {item}. Respond with a high number if the experience strongly indicates that {item}. Respond with only a number between 1 and 7. Do not provide any other response."
            
        # Calculate token counts
        token_count_input = calculate_tokens(dev_msg) + calculate_tokens(user_msg)
        simulated_output = np.random.randint(0, 7)  # Placeholder for model output
        token_count_output = calculate_tokens(str(simulated_output))
        
        # Aggregate token counts
        total_token_count_input += token_count_input
        total_token_count_output += token_count_output
    
    # Assign aggregated counts to the DataFrame
    sentences.loc[idx, 'token_count_input'] = total_token_count_input
    sentences.loc[idx, 'token_count_output'] = total_token_count_output


# Calculate aggregate token statistics
average_tokens_input = sentences['token_count_input'].mean()
max_tokens_input = sentences['token_count_input'].max()
min_tokens_input = sentences['token_count_input'].min()
total_tokens_input = sentences['token_count_input'].sum()

# Display the token statistics for input
print("Input Token Statistics:")
print(f"Average Tokens: {average_tokens_input}")
print(f"Max Tokens: {max_tokens_input}")
print(f"Min Tokens: {min_tokens_input}")
print(f"Total Tokens: {total_tokens_input}")

average_tokens_output = sentences['token_count_output'].mean()
max_tokens_output = sentences['token_count_output'].max()
min_tokens_output = sentences['token_count_output'].min()
total_tokens_output = sentences['token_count_output'].sum()

# Display the token statistics for output
print("Output Token Statistics:")
print(f"Average Tokens: {average_tokens_output}")
print(f"Max Tokens: {max_tokens_output}")
print(f"Min Tokens: {min_tokens_output}")
print(f"Total Tokens: {total_tokens_output}")
