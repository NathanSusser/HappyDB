import os
import json
import pandas as pd

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_clean.csv'

# Output directory for split batches
output_dir = 'data/splits'
os.makedirs(output_dir, exist_ok=True)

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

# Parameters
max_batch_size_bytes = 10_000_000  # Target batch size (10 MB)

# Initialize batching
batch_num = 1
current_batch_size = 0
output_file_path = os.path.join(output_dir, f'batch_requests_{batch_num}.jsonl')
f = open(output_file_path, 'w')  # Open the first batch file

# Iterate over sentences and items to create requests
for index, row in sentences.iterrows():
    hmid = row['hmid']
    period = row['reflection_period']
    sentence = row['cleaned_hm']
    sent_id = hmid

    # Convert period to a descriptive time
    time_frame = {
        "24h": "24 hours",
        "3m": "3 months"
    }.get(period, "an unknown period")

    for idx, item_row in items.iterrows():  # Process all items
        item = item_row['Items']
        request_id = f"{str(sent_id) + '-' + str(idx)}"

        # Construct developer and user messages
        dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
        user_msg = (
            f"The following is a description of an experience ** {sentence} **. \n\n"
            f"How much does this experience indicate ** {item} ** "
            "Provide a response on a scale of 1 to 7. Respond with a low number if the experience "
            f"does not indicate that {item}. Respond with a high number if the experience strongly indicates "
            f"that {item}. Respond with only a number between 1 and 7. Do not provide any other response."
        )

        # Construct the JSON structure for each request
        request = {
            "custom_id": f"request-{request_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "developer", "content": [{"type": "text", "text": dev_msg}]},
                    {"role": "user", "content": [{"type": "text", "text": user_msg}]}
                ],
                "max_tokens": 1
            }
        }

        # Serialize the request and calculate its size
        request_json = json.dumps(request) + '\n'
        request_size = len(request_json.encode('utf-8'))

        # Check if adding this request exceeds the batch size
        if current_batch_size + request_size > max_batch_size_bytes:
            f.close()  # Close the current batch file
            print(f"Batch {batch_num} written to {output_file_path}")
            batch_num += 1
            current_batch_size = 0
            output_file_path = os.path.join(output_dir, f'batch_requests_{batch_num}.jsonl')
            f = open(output_file_path, 'w')  # Start a new batch file

        # Write the request to the current batch file
        f.write(request_json)
        current_batch_size += request_size

f.close()  # Close the final batch file
print(f"Batch {batch_num} written to {output_file_path}")
print(f"All batches written to {output_dir}")
