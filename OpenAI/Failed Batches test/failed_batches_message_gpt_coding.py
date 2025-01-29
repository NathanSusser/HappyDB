import os
import time
import pandas as pd
from openai import OpenAI

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# Directory for output and log files
output_files_dir = "dataframes/tests/gpt40-mini/outputs/"
log_files_dir = "dataframes/tests/gpt40-mini/logs/"
failed_batches_dir = "dataframes/tests/gpt40-mini/failed_batches/"  # Directory for failed batches

# Create output and log directories if they don't exist
os.makedirs(output_files_dir, exist_ok=True)
os.makedirs(log_files_dir, exist_ok=True)

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Get the list of failed batch files
failed_batch_files = [f for f in os.listdir(failed_batches_dir) if f.endswith(".jsonl")]

# Keep track of batch IDs for polling
batches = []

# Step 1: Process each failed batch
for failed_batch_file in failed_batch_files:
    input_file_path = os.path.join(failed_batches_dir, failed_batch_file)
    output_file_path = os.path.join(output_files_dir, f"output_{failed_batch_file}")
    log_file_path = os.path.join(log_files_dir, f"log_{failed_batch_file}.txt")

    # Upload the input JSONL file
    print(f"Uploading the input file: {failed_batch_file}...")
    with open(input_file_path, "rb") as file:
        uploaded_file = client.files.create(file=file, purpose="batch")
    input_file_id = uploaded_file.id
    print(f"File uploaded successfully with ID: {input_file_id}")

    # Create the batch
    print(f"Creating the batch for {failed_batch_file}...")
    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    batch_id = batch.id
    print(f"Batch created successfully with ID: {batch_id}")

    # Write file_id and batch_id to log file
    with open(log_file_path, "w") as log_file:
        log_file.write(f"File ID: {input_file_id}\n")
        log_file.write(f"Batch ID: {batch_id}\n")

    # Add batch ID to the list for polling later
    batches.append({"batch_id": batch_id, "output_file": output_file_path, "log_file": log_file_path})

print("Failed batches submitted. Polling for completion...")

# Step 2: Poll all batches for up to 5 minutes
start_time = time.time()
while time.time() - start_time < 300:  # Poll for up to 5 minutes (300 seconds)
    for batch in batches:
        batch_id = batch["batch_id"]
        output_file_path = batch["output_file"]
        log_file_path = batch["log_file"]

        # Retrieve batch status
        batch_status = client.batches.retrieve(batch_id)
        status = batch_status.status
        print(f"Batch {batch_id} status: {status}")

        # Log the status
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Batch {batch_id} status: {status}\n")

        # If completed, retrieve and save results
        if status == "completed":
            print(f"Batch {batch_id} completed. Retrieving results...")
            output_file_id = batch_status.output_file_id
            file_response = client.files.content(output_file_id)

            # Save results to the output file
            with open(output_file_path, "wb") as output_file:
                output_file.write(file_response.read())
            print(f"Results saved to {output_file_path}")

            # Remove the batch from polling
            batches.remove(batch)

        # Handle failed or expired batches
        elif status in ["failed", "expired"]:
            print(f"Batch {batch_id} {status}. Please check your input file or batch configuration.")
            batches.remove(batch)

    # Break the loop if all batches are completed
    if not batches:
        print("All batches processed.")
        break

    time.sleep(30)  # Wait before polling again

print("Batch polling completed.")
