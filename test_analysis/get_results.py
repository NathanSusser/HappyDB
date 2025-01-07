import pandas as pd
import json
import os

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'
results_file_path = 'dataframes/tests/gpt40-mini/batch_output_test_5.jsonl'  

# Load sentences and items
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Create hierarchical column structure
columns = list(zip(items['Scale'], items['Dimension'], items['Item-sit']))
columns = pd.MultiIndex.from_tuples(columns, names=["Scale", "Dimension", "Item-sit"])

# Create multi-index for rows using sentences and HMIDs
row_index = pd.MultiIndex.from_tuples(zip(sentences['hmid'], sentences['cleaned_hm']), names=["hmid", "cleaned_hm"])

# Initialize the DataFrame with None values
ratings = pd.DataFrame(None, index=row_index, columns=columns)

# Parse the JSONL results
with open(results_file_path, 'r') as results_file:
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
            scale, dimension, item_text = item["Scale"], item["Dimension"], item["Item-sit"]

            # Store the response in the DataFrame
            ratings.loc[(sent_id, sentence), (scale, dimension, item_text)] = response_text

        except Exception as e:
            print(f"Error processing custom_id {custom_id}: {e}")

# Fill missing values with a placeholder
ratings.fillna(-1, inplace=True)

# Save the ratings matrix as a Parquet file
output_matrix_path = 'dataframes/tests/gpt40-mini/ratings_matrix.csv'
ratings.to_csv(output_matrix_path)

print(f"Ratings matrix saved to {output_matrix_path}.")
