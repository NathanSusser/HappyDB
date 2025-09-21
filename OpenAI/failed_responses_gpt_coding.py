#IMPORTS

#imports
import os
import json
import time
import pandas
from openai import OpenAI

#=========================================

#SETUP

#set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
failed_responses_file = 'data/failure/failed_responses4.csv'
items_path = 'dataframes/scales_clean.csv'

#output directory and file for storing responses
output_files_dir = "data/failure/outputs/"
os.makedirs(output_files_dir, exist_ok=True)
output_file_path = os.path.join(output_files_dir, "failed_responses_4.jsonl")  #single JSONL file

#load data
sentences = pandas.read_csv(sentences_path)
items = pandas.read_csv(items_path)
failed_responses = pandas.read_csv(failed_responses_file)

#initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

#=========================================

#PROCESS FAILED RESPONSES

#open JSONL file for appending responses
with open(output_file_path, "a") as outfile:
    #process each failed response using request_id to fetch the correct item
    for index, failed_row in failed_responses.iterrows():
        hmid = failed_row['hmid']
        sentence_row = sentences[sentences['hmid'] == hmid]

        if sentence_row.empty:
            print(f"Warning: No sentence found for hmid {hmid}. Skipping.")
            continue

        sentence = sentence_row.iloc[0]['cleaned_hm']

        #extract request_id and validate against items.csv
        try:
            request_id = int(failed_row['custom_id'].split('-')[-1])  #extract index from custom_id
        except ValueError:
            print(f"Error: Invalid request_id format in custom_id: {failed_row['custom_id']}. Skipping.")
            continue

        if request_id >= len(items):
            print(f"Warning: No corresponding item found for request_id {request_id}. Skipping.")
            continue

        item = items.iloc[request_id]['Items']  #pull correct item from items.csv

        #construct developer and user messages
        dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
        user_msg = (
            f"The following is a description of an experience ** {sentence} **. \n\n"
            f"How much does this experience indicate ** {item} ** "
            "Provide a response on a scale of 1 to 7. Respond with a low number if the experience "
            f"does not indicate that {item}. Respond with a high number if the experience strongly indicates "
            f"that {item}. Respond with only a number between 1 and 7. Do not provide any other response."
        )

        print(f"Processing hmid {hmid}, custom_id: {request_id}")
        print(f"Dev message: {dev_msg}")
        print(f"User message: {user_msg}")

        try:
            #send API request
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": dev_msg},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=1
            )

            #format response for JSONL
            response_data = {
                "custom_id": f"request-{hmid}-{request_id}",
                "response": response.to_dict()
            }

            #write response as a new line in the JSONL file
            outfile.write(json.dumps(response_data) + "\n")

            #avoid hitting rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Error processing hmid {hmid}, custom_id {request_id}: {e}")

print(f"All responses have been reprocessed and saved in {output_file_path}")
