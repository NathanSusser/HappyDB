import openai
import pandas as pd
import os


# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Shuffle sentences DataFrame for random order
sentences = sentences.sample(frac=1).reset_index(drop=True)

# Output file
output_file = 'messages_output.txt'

# Open the file to write messages
with open(output_file, 'w') as f:
    # Iterate over sentences and items
    for _, row in sentences.iterrows():
        period = row['reflection_period']
        sentence = row['cleaned_hm']
        
        # Convert period to a descriptive time
        if period == "24h":
            time_frame = "24 hours"
        elif period == "3m":
            time_frame = "3 months"
        else:
            time_frame = "an unknown period"
        
        for _, item_row in items.iterrows():
            item = item_row['Item-sit']
            
            # Construct messages
            dev_msg = f"You are a helpful assistant who can help me code individual sentences written by people asked to describe what made them happy in the last {time_frame}."
            user_msg =  f"On a scale of 0 to 7 where 0 is strongly agree and 7 is strongly disagree, please rate ** {item} ** This is the experience: ** {sentence} ** Please only return the number on a scale of 0 to 7 of ** {item} **."
            
            msg = dev_msg + '\n' + user_msg + '\n'
            
           
            
        break

print(f"Messages written to {output_file}.")
