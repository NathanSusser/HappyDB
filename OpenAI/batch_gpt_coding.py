import os
import time
import httpx
import re
from openai import OpenAI
from tqdm import tqdm

# Function to extract numeric value from a filename for proper sorting
def extract_numeric(filepath):
    filename = os.path.basename(filepath)
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
split_files_dir = 'data/splits/'
output_files_dir = 'data/outputs/'
log_files_dir = 'data/logs/'

# Create directories if they don't exist
os.makedirs(output_files_dir, exist_ok=True)
os.makedirs(log_files_dir, exist_ok=True)

# Retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key, timeout=httpx.Timeout(120.0))

# Get the list of split files and sort numerically
split_files = sorted(
    [f for f in os.listdir(split_files_dir) if f.endswith(".jsonl")],
    key=extract_numeric
)

# Batch creation
print("Starting batch creation...")
for i, split_file in enumerate(tqdm(split_files, desc="Creating Batches")):
    input_file_path = os.path.join(split_files_dir, split_file)
    output_file_path = os.path.join(output_files_dir, f"output_{split_file.replace('.jsonl', '.txt')}")
    log_file_path = os.path.join(log_files_dir, f"log_{split_file.replace('.jsonl', '')}.txt")

    # Check if a log file already exists for this batch
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            content = log_file.read()
            if "Batch ID:" in content:
                batch_id = content.split("Batch ID:")[1].splitlines()[0].strip()
                print(f"Skipping {split_file} (Batch ID: {batch_id})")
                continue  # Skip to the next split file

    # Upload the input JSONL file
    print(f"Uploading the input file: {split_file}...")
    with open(input_file_path, "rb") as file:
        uploaded_file = client.files.create(file=file, purpose="batch")
    input_file_id = uploaded_file.id
    print(f"File uploaded successfully with ID: {input_file_id}")

    # Create the batch
    print(f"Creating the batch for {split_file}...")
    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    batch_id = batch.id
    print(f"Batch created successfully with ID: {batch_id}")

    # Write file_id and batch_id to log file
    with open(log_file_path, "w") as log_file:
        log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"File ID: {input_file_id}\n")
        log_file.write(f"Batch ID: {batch_id}\n")

print("Batch creation completed.")
