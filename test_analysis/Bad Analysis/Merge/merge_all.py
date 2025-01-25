import pandas as pd
import os

# Set working directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# Load the main data and reverse-coded items
results = pd.read_csv('dataframes/tests/gpt40-mini/updated_ratings_matrix.csv', header=[0, 1, 2])  # Adjust to load multi-index
rev_items = pd.read_csv('profiles/PWB_reverse_coded.csv')
more_items = pd.read_csv('/Users/nsusser/Desktop/Nathan happy/data - merged - alldim.csv')
items = pd.read_csv('dataframes/scales_clean.csv') 

# Display the first few rows of both datasets
print(results.head())
print(rev_items.head())
print(more_items.head())

# Step 1: Transform reverse-coded items for PWB scale only
reverse_coded_items = rev_items['Items'].tolist()  # Assuming column 'Items' lists reverse-coded items
max_value = 7  # Max value in the dataset

for col in results.columns:
    if col[0] == 'PWB' and col[2] in reverse_coded_items:  # Check if scale is PWB
        if pd.api.types.is_numeric_dtype(results[col]):  # Ensure column is numeric
            results[col] = max_value + 1 - results[col]  # Reverse the coding logic


# Step 1: Reset index to expose `hmid` and `cleaned_hm`
results.reset_index(inplace=True)

# Step 2: Flatten the multi-index columns
results.columns = [
    f"{col[0]}_{col[1]}_{col[2]}" if isinstance(col, tuple) else col
    for col in results.columns
]

# Step 3: Rename the columns correctly
results.rename(
    columns={
        "index__": "index",  # Optional: Drop later if unnecessary
        "Scale_Dimension_Items": "hmid",
        "Unnamed: 1_level_0_Unnamed: 1_level_1_Unnamed: 1_level_2": "cleaned_hm",
    },
    inplace=True,
)
# Remove the 0th row
results = results.iloc[1:].reset_index(drop=True)

# Step 4: Drop the numerical index if not needed
results.drop(columns=["index"], inplace=True, errors="ignore")

# Step 5: Verify column names and structure
print("Updated columns in results:")
print(results.columns)


# Step 6: Drop unnecessary columns from `more_items`
more_items = more_items.drop(
    columns=[col for col in more_items.columns if "Unnamed" in col or col == "Index"],
    errors="ignore",
)

# Step 7: Rename the columns to match the main dataset

more_items.rename(columns={"clean_hm": "cleaned_hm"}, inplace=True)

print("Unique values in 'results[hmid]':", results['hmid'].unique())
print("Unique values in 'more_items[hmid]':", more_items['hmid'].unique())
print("Unique values in 'results[cleaned_hm]':", results['cleaned_hm'].unique())
print("Unique values in 'more_items[cleaned_hm]':", more_items['cleaned_hm'].unique())


# Step 9: Merge the DataFrames
merged_df = pd.merge(
    results,
    more_items,
    on=["hmid", "cleaned_hm"],
    how="inner",
)

# Print the resulting DataFrame
print(merged_df.head())

# Step 10: Save the merged DataFrame to a new CSV file
output_dir = 'dataframes/tests/gpt40-mini/More Items/'
os.makedirs(output_dir, exist_ok=True)
merged_df.to_csv(os.path.join(output_dir, "merged_data_1000.csv"), index=False)
