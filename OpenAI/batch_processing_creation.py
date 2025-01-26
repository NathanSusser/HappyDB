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
sentences_per_batch = 250  # Number of sentences per batch
num_sentences = len(sentences)  # Total number of sentences
num_batches = (num_sentences + sentences_per_batch - 1) // sentences_per_batch  # Calculate the number of batches

# Split sentences into batches
for batch_num in range(num_batches):
    batch_start = batch_num * sentences_per_batch
    batch_end = min((batch_num + 1) * sentences_per_batch, num_sentences)
    batch_sentences = sentences.iloc[batch_start:batch_end]

    # Output file for this batch
    output_file_path = os.path.join(output_dir, f'batch_requests_{batch_num + 1}.jsonl')

    with open(output_file_path, 'w') as f:
        for index, row in batch_sentences.iterrows():
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
                # Get the item and request ID
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

    print(f"Batch {batch_num + 1} written to {output_file_path}")

print(f"All batches written to {output_dir}")
