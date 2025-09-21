#IMPORTS

#imports
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

#=========================================

#SETUP

#file paths
log_files_dir = "data/logs/"  #directory containing log files with batch IDs
invalid_batches_file = "invalid_batches.txt"  #file to log batches with invalid statuses

#retrieve the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

#initialize the OpenAI client
client = OpenAI(api_key=api_key)

#get the list of log files
log_files = [f for f in os.listdir(log_files_dir) if f.endswith(".txt")]

#allowed statuses
allowed_statuses = ["validated", "in_progress", "completed"]

#=========================================

#BATCH STATUS CHECKING

#function to process a single batch
def check_batch_status(log_file):
    try:
        #extract the Batch ID
        log_file_path = os.path.join(log_files_dir, log_file)
        with open(log_file_path, "r") as log:
            for line in log:
                if line.startswith("Batch ID:"):
                    batch_id = line.split(":")[1].strip()
                    break
        #retrieve batch status
        batch_status = client.batches.retrieve(batch_id)
        status = batch_status.status
        if status not in allowed_statuses:
            return {"batch_id": batch_id, "status": status}
        return None  #valid status, no issue
    except Exception as e:
        return {"batch_id": f"Error in {log_file}", "status": str(e)}

#=========================================

#PARALLEL PROCESSING

#parallel processing
invalid_batches = []
with ThreadPoolExecutor(max_workers=20) as executor:  #adjust the number of workers based on your system
    futures = {executor.submit(check_batch_status, log_file): log_file for log_file in log_files}

    for future in as_completed(futures):
        result = future.result()
        if result:  #only keep invalid batches or errors
            invalid_batches.append(result)

#log invalid batches to a file
if invalid_batches:
    with open(invalid_batches_file, "w") as invalid_log:
        for batch in invalid_batches:
            invalid_log.write(f"Batch ID: {batch['batch_id']}, Status: {batch['status']}\n")
    print(f"Invalid batches logged to {invalid_batches_file}")
else:
    print("All batches are in valid statuses.")

print("Batch status verification completed.")
