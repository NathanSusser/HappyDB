#IMPORTS

#imports
import os
import json
import pandas

#=========================================

#SETUP

#set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_clean.csv'

#output directory for split batches
output_dir = 'data/splits'
os.makedirs(output_dir, exist_ok=True)

#load data
sentences = pandas.read_csv(sentences_path)
items = pandas.read_csv(items_path)

#model configuration
MODEL_NAME = "gpt-4o-mini-2024-07-18"

#parameters
max_batch_size_bytes = 10_000_000  #target batch size (10 MB)

#initialize batching
batch_num = 1
current_batch_size = 0
output_file_path = os.path.join(output_dir, f'batch_requests_{batch_num}.jsonl')
f = open(output_file_path, 'w')  #open the first batch file

#=========================================

#CREATE BATCH REQUESTS

#iterate over sentences and items to create requests
for index, row in sentences.iterrows():
    hmid = row['hmid']
    period = row['reflection_period']
    sentence = row['cleaned_hm']
    sent_id = hmid

    #convert period to a descriptive time
    time_frame = {
        "24h": "24 hours",
        "3m": "3 months"
    }.get(period, "an unknown period")

    for idx, item_row in items.iterrows():  #process all items
        item = item_row['Items']
        request_id = f"{str(sent_id) + '-' + str(idx)}"

        #construct developer and user messages
        dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
        user_msg = (
            f"The following is a description of an experience ** {sentence} **. \n\n"
            f"How much does this experience indicate ** {item} ** "
            "Provide a response on a scale of 1 to 7. Respond with a low number if the experience "
            f"does not indicate that {item}. Respond with a high number if the experience strongly indicates "
            f"that {item}. Respond with only a number between 1 and 7. Do not provide any other response."
        )

        #construct the JSON structure for each request
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

        #serialize the request and calculate its size
        request_json = json.dumps(request) + '\n'
        request_size = len(request_json.encode('utf-8'))

        #check if adding this request exceeds the batch size
        if current_batch_size + request_size > max_batch_size_bytes:
            f.close()  #close the current batch file
            print(f"Batch {batch_num} written to {output_file_path}")
            batch_num += 1
            current_batch_size = 0
            output_file_path = os.path.join(output_dir, f'batch_requests_{batch_num}.jsonl')
            f = open(output_file_path, 'w')  #start a new batch file

        #write the request to the current batch file
        f.write(request_json)
        current_batch_size += request_size

#close the final batch file
f.close()
print(f"Batch {batch_num} written to {output_file_path}")
print(f"All batches written to {output_dir}")
