from openai import OpenAI
import os
import time

# File paths
log_files_dir = "dataframes/tests/gpt40-mini/CIT/logs/"  # Directory containing log files with batch IDs
output_files_dir = "dataframes/tests/gpt40-mini/CIT/outputs/"  # Directory to save output files

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Get the list of log files
log_files = [f for f in os.listdir(log_files_dir) if f.endswith(".txt")]

# Process each log file
for log_file in log_files:
    log_file_path = os.path.join(log_files_dir, log_file)

    # Load the batch ID from the log file
    try:
        with open(log_file_path, "r") as log:
            for line in log:
                if line.startswith("Batch ID:"):
                    batch_id = line.split(":")[1].strip()
                    break
        print(f"Loaded Batch ID from {log_file}: {batch_id}")
    except FileNotFoundError:
        print(f"Log file not found: {log_file_path}. Skipping...")
        continue

    # Poll for batch status
    print(f"Checking batch status for Batch ID: {batch_id}...")
    while True:
        batch_status = client.batches.retrieve(batch_id)
        status = batch_status.status
        print(f"Batch {batch_id} status: {status}")

        # Break if the batch is completed, failed, or expired
        if status in ["completed", "failed", "expired"]:
            break

        # Wait before polling again
        time.sleep(30)

    # Handle completed batches
    if status == "completed":
        print(f"Batch {batch_id} completed. Retrieving results...")
        output_file_id = batch_status.output_file_id
        file_response = client.files.content(output_file_id)

        # Save results to an output file
        output_file_path = os.path.join(output_files_dir, f"output_{log_file.replace('.txt', '.jsonl')}")
        with open(output_file_path, "wb") as output_file:
            output_file.write(file_response.read())
        print(f"Results saved to {output_file_path}")

    # Handle failed or expired batches
    elif status in ["failed", "expired"]:
        print(f"Batch {batch_id} {status}. Please check your input file or batch configuration.")

print("All batch content retrieval completed.")
