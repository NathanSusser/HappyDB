import pandas as pd
import json
import os

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_clean.csv'
output_files_dir = 'dataframes/tests/gpt40-mini/CIT/outputs/'  # Directory containing batch output files
failed_responses_file = 'dataframes/tests/gpt40-mini/CIT/failed_responses.csv'  # File to log invalid responses

# Load sentences and items
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Create hierarchical column structure
columns = list(zip(items['Scale'], items['Dimension'], items['Items']))
columns = pd.MultiIndex.from_tuples(columns, names=["Scale", "Dimension", "Items"])

# Create multi-index for rows using sentences and HMIDs
row_index = pd.MultiIndex.from_tuples(zip(sentences['hmid'], sentences['cleaned_hm']), names=["hmid", "cleaned_hm"])

# Initialize the DataFrame with None values
ratings = pd.DataFrame(None, index=row_index, columns=columns)

# Prepare a DataFrame to log failed responses
failed_responses = []

# Process all batch output files
output_files = [f for f in os.listdir(output_files_dir) if f.endswith(".jsonl")]

for output_file in output_files:
    output_file_path = os.path.join(output_files_dir, output_file)
    print(f"Processing output file: {output_file_path}")

    # Parse the JSONL results
    with open(output_file_path, 'r') as results_file:
        for line in results_file:
            response = json.loads(line)

            # Extract custom_id and response value
            custom_id = response["custom_id"]  # E.g., "request-123-45"
            result_body = response.get("response", {}).get("body", {})
            choice = result_body.get("choices", [{}])[0]
            response_text = choice.get("message", {}).get("content", "").strip()

            # Split the custom_id into sentence ID and item index
            try:
                sent_id, item_idx = custom_id.split("-")[1:]
                sent_id = int(sent_id)
                item_idx = int(item_idx)

                # Map to the sentence and item
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
                print(f"Error processing custom_id {custom_id}: {e}")

# Save the ratings matrix as a CSV file
output_matrix_path = 'dataframes/tests/gpt40-mini/CIT/ratings_matrix.csv'
ratings.to_csv(output_matrix_path)
print(f"Ratings matrix saved to {output_matrix_path}.")

# Save failed responses to a CSV file
if failed_responses:
    failed_responses_df = pd.DataFrame(failed_responses)
    failed_responses_df.to_csv(failed_responses_file, index=False)
    print(f"Failed responses logged to {failed_responses_file}.")
else:
    print("No failed responses to log.")
