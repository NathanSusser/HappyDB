import os
import time
from openai import OpenAI

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# File paths
input_file_path = "dataframes/tests/gpt40-mini/batch_requests_test_5.jsonl"  # Path to your JSONL input file
output_file_path = "dataframes/tests/gpt40-mini/batch_output_test_5.jsonl"  # Path to save the output file

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Step 1: Upload the input JSONL file
print("Uploading the input file...")
with open(input_file_path, "rb") as file:
    uploaded_file = client.files.create(file=file, purpose="batch")
input_file_id = uploaded_file.id
print(f"File uploaded successfully with ID: {input_file_id}")

# Step 2: Create the batch
print("Creating the batch...")
batch = client.batches.create(
    input_file_id=input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
batch_id = batch.id
print(f"Batch created successfully with ID: {batch_id}")

# Step 3: Poll for batch status
print("Checking batch status...")
while True:
    batch_status = client.batches.retrieve(batch_id)
    status = batch_status.status
    print(f"Batch status: {status}")

    # Break if the batch is completed, failed, or expired
    if status in ["completed", "failed", "expired"]:
        break

    # Wait before polling again
    time.sleep(30)

# Step 4: Retrieve and save results if completed
if status == "completed":
    print("Batch completed. Retrieving results...")
    output_file_id = batch_status.output_file_id
    file_response = client.files.content(output_file_id)

    # Save results to the output file
    with open(output_file_path, "wb") as output_file:
        output_file.write(file_response.read())
    print(f"Results saved to {output_file_path}")

# Step 5: Handle failed or expired batches
elif status in ["failed", "expired"]:
    print(f"Batch {status}. Please check your input file or batch configuration.")
