import openai
import pandas as pd
import os
import json

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Output file path
output_path = 'dataframes/tests/gpt40-mini/batch_requests_test_5.jsonl'

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

# Open the file to write JSONL
with open(output_path, 'w') as f:
    for index, row in sentences.iterrows():
        
        if index == 50:
            print(f"Hit row: {index}")
            break

        hmid = row['hmid']
        period = row['reflection_period']
        sentence = row['cleaned_hm']
        sent_id = hmid
        # Convert period to a descriptive time
        if period == "24h":
            time_frame = "24 hours"
        elif period == "3m":
            time_frame = "3 months"
        else:
            time_frame = "an unknown period"
        
        for idx, item_row in items.iterrows():
            item = item_row['Item-sit']
            request_id = f"{str(sent_id) + "-" + str(idx)}"
            
            # Construct developer and user messages
            dev_msg = f"You are a helpful assistant who can help me code individual sentences written by people asked to describe what made them happy in the last {time_frame}."
            user_msg = f"On a scale of 0 to 7 where 0 is strongly agree and 7 is strongly disagree, please rate ** {item} ** This is the experience: ** {sentence} ** Please only return the number on a scale of 0 to 7 of ** {item} **."
            
            # Construct the JSON structure for each request
            request = {
                "custom_id": f"request-{request_id}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": MODEL_NAME,
                    "messages": [
                        {
                            "role": "developer",
                            "content": [
                                {"type": "text", "text": dev_msg}
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_msg}
                            ]
                        }
                    ],
                    "max_tokens": 1
                }
            }
            # Write to JSONL file
            f.write(json.dumps(request) + '\n')

print(f"Batch requests written to {output_path}.")
