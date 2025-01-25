import os
import json
import pandas as pd

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
ratings_matrix_path = 'dataframes/tests/gpt40-mini/CIT/ratings_matrix.csv'  # Existing ratings matrix
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_clean.csv'
failed_outputs_dir = 'dataframes/tests/gpt40-mini/CIT/outputs/failed_outputs'  # Directory containing failed output files
failed_responses_file = 'dataframes/tests/gpt40-mini/CIT/failed_responses.csv'  # File to log invalid responses

# Load existing ratings matrix
ratings = pd.read_csv(ratings_matrix_path, index_col=[0, 1], header=[0, 1, 2])  # Multi-index for rows and columns

# Load sentences and items
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Prepare a DataFrame to log failed responses
failed_responses = []

# Validate directory and list all JSONL files
if not os.path.exists(failed_outputs_dir):
    raise FileNotFoundError(f"Directory not found: {failed_outputs_dir}")
failed_output_files = [f for f in os.listdir(failed_outputs_dir) if f.endswith(".jsonl")]

if not failed_output_files:
    print("No failed output files found to process.")
else:
    print(f"Found {len(failed_output_files)} failed output files to process.")

# Process each failed output file
for failed_output_file in failed_output_files:
    failed_output_file_path = os.path.join(failed_outputs_dir, failed_output_file)
    print(f"Processing failed output file: {failed_output_file_path}")

    # Check if the file is non-empty
    if os.stat(failed_output_file_path).st_size == 0:
        print(f"Skipping empty file: {failed_output_file}")
        continue

    # Parse the JSONL file
    with open(failed_output_file_path, "r") as results_file:
        for line_num, line in enumerate(results_file, start=1):
            try:
                response = json.loads(line)

                # Extract custom_id and response value
                custom_id = response.get("custom_id")
                result_body = response.get("response", {})
                response_text = (
                    result_body.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )

                # Split custom_id to locate sentence ID and item index
                sent_id, item_idx = custom_id.split("-")[1:]
                sent_id = int(sent_id)
                item_idx = int(item_idx)

                # Map to sentence and item
                sentence = sentences.loc[sentences['hmid'] == sent_id, 'cleaned_hm'].values[0]
                item = items.iloc[item_idx]
                scale, dimension, item_text = item["Scale"], item["Dimension"], item["Items"]

                # Validate the response
                try:
                    # Strip whitespace and attempt to convert to an integer
                    response_number = int(response_text.strip())
                    ratings.loc[(sent_id, sentence), (scale, dimension, item_text)] = response_number
                except ValueError:
                    # Log unexpected responses
                    failed_responses.append({
                        "custom_id": custom_id,
                        "hmid": sent_id,
                        "sentence": sentence,
                        "scale": scale,
                        "dimension": dimension,
                        "item": item_text,
                        "response": response_text
                    })
                    print(f"Invalid response logged: {response_text}")

            except Exception as e:
                print(f"[File: {failed_output_file}, Line: {line_num}] Error processing line: {line.strip()}. Error: {e}")

# Save the updated ratings matrix
updated_ratings_matrix_path = 'dataframes/tests/gpt40-mini/updated_ratings_matrix.csv'
ratings.to_csv(updated_ratings_matrix_path)
print(f"Updated ratings matrix saved to {updated_ratings_matrix_path}.")

# Save failed responses to a CSV file
if failed_responses:
    failed_responses_df = pd.DataFrame(failed_responses)
    failed_responses_df.to_csv(failed_responses_file, index=False)
    print(f"Failed responses logged to {failed_responses_file}.")
else:
    print("No failed responses to log.")
