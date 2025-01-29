import os
import json
import time
from openai import OpenAI

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
failed_batches_dir = "dataframes/tests/gpt40-mini/CIT/failed_batches/"  # Directory for failed JSONL batches
output_files_dir = "dataframes/tests/gpt40-mini/CIT/outputs/"  # Directory to save output files

# Ensure directories exist
os.makedirs(output_files_dir, exist_ok=True)

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Get the list of failed batch files
failed_batch_files = [f for f in os.listdir(failed_batches_dir) if f.endswith(".jsonl")]

# Process each failed batch file
for failed_batch_file in failed_batch_files:
    input_file_path = os.path.join(failed_batches_dir, failed_batch_file)
    output_file_path = os.path.join(output_files_dir, f"output_{failed_batch_file}")

    # Prepare to write responses
    responses = []

    # Parse the JSONL file and send API requests
    print(f"Processing file: {failed_batch_file}...")
    with open(input_file_path, "r") as infile:
        for line in infile:
            try:
                # Parse JSON entry
                request_data = json.loads(line)
                custom_id = request_data["custom_id"]
                body = request_data["body"]
                model = body["model"]
                messages = body["messages"]

                # Prepare the API call
                print(f"Sending request for custom_id: {custom_id}")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": message["role"],
                            "content": "".join(content["text"] for content in message["content"])
                        }
                        for message in messages
                    ],
                    max_tokens=body["max_tokens"]
                )

                # Extract relevant response content
                response_data = {
                    "custom_id": custom_id,
                    "response": response.to_dict()  # Convert response to dictionary for serialization
                }

                # Add to responses list
                responses.append(response_data)

                # Optional: Sleep to avoid rate limits
                time.sleep(1)
            except Exception as e:
                print(f"Error processing request for custom_id {custom_id}: {e}")

    # Save responses to the output file
    with open(output_file_path, "w") as outfile:
        for response in responses:
            outfile.write(json.dumps(response) + "\n")
    print(f"Responses saved to {output_file_path}")
