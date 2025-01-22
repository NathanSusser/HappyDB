import os
import json
import pandas as pd

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_clean.csv'
failed_responses_file = 'dataframes/tests/gpt40-mini/CIT/failed_responses.csv'

# Output directory for failed batch requests
failed_output_dir = 'dataframes/tests/gpt40-mini/CIT/failed_batches/'
os.makedirs(failed_output_dir, exist_ok=True)

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)
failed_responses = pd.read_csv(failed_responses_file)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

# Group failed responses by sentence and batch them
failed_responses_grouped = failed_responses.groupby("hmid")

batch_counter = 0

for hmid, group in failed_responses_grouped:
    batch_counter += 1
    sentence_row = sentences[sentences['hmid'] == hmid].iloc[0]
    sentence = sentence_row['cleaned_hm']
    period = sentence_row['reflection_period']

    # Convert period to a descriptive time
    if period == "24h":
        time_frame = "24 hours"
    elif period == "3m":
        time_frame = "3 months"
    else:
        time_frame = "an unknown period"

    # Output file for this batch
    output_file_path = os.path.join(failed_output_dir, f'failed_batch_requests_{batch_counter}.jsonl')

    with open(output_file_path, 'w') as f:
        for _, failed_row in group.iterrows():
            item = failed_row['item']
            scale = failed_row['scale']
            dimension = failed_row['dimension']
            request_id = failed_row['custom_id'].split('-')[-1]

            # Construct developer and user messages
            dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
            user_msg = (
                f"The following is a description of an experience ** {sentence} **. \n\n"
                f"How much does this experience indicate ** {item} **? "
                "Provide a response on a scale of 1 to 7. Respond with a low number if the experience "
                f"does not indicate that {item}. Respond with a high number if the experience strongly indicates "
                f"that {item}. Respond with only a number between 1 and 7. Do not provide any other response."
            )

            # Construct the JSON structure for each failed request
            request = {
                "custom_id": f"request-{hmid}-{request_id}",
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

    print(f"Failed batch {batch_counter} written to {output_file_path}")

print(f"All failed batches written to {failed_output_dir}")
