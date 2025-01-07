from openai import OpenAI
import os
import time

# File paths
output_file_path = "dataframes/tests/gpt40-mini/batch_output_test_5.jsonl"  # Path to save the output file

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Load the batch ID
batch_id = "batch_677aeddee5908190a54261855c2ea060"
print(f"Checking status for Batch ID: {batch_id}")

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
