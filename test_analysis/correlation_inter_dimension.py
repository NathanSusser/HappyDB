import pandas as pd
import os

# Set working directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# Load the main data and reverse-coded items
results = pd.read_csv('dataframes/tests/gpt40-mini/updated_ratings_matrix.csv', header=[0, 1, 2])  # Adjust to load multi-index
rev_items = pd.read_csv('profiles/PWB_reverse_coded.csv')

# Display the first few rows of both datasets
print(results.head())
print(rev_items.head())
'''
# Step 1: Transform reverse-coded items for PWB scale only
reverse_coded_items = rev_items['Items'].tolist()  # Assuming column 'Items' lists reverse-coded items
max_value = 7  # Max value in the dataset

for col in results.columns:
    if col[0] == 'PWB' and col[2] in reverse_coded_items:  # Check if scale is PWB
        if pd.api.types.is_numeric_dtype(results[col]):  # Ensure column is numeric
            results[col] = max_value + 1 - results[col]'''

# Step 2: Define specific groupings for analysis
groupings = {
    "Negative Emotion": [
        ("PERMA", "Negative emotion"),
        ("PANAS", "Negative")
    ],
    "Positive Emotions": [
        ("PERMA", "Positive Emotion"),
        ("WBP", "Positive Emotions"),
        ("PANAS", "Positive")
    ],
    "Positive Relationships": [
        ("PWB", "Positive Relations"),
        ("WBP", "Positive Relationships"),
        ("PERMA", "Relationships")
    ],
    "Meaning and Purpose": [
        ("PWB", "Purpose in Life"),
        ("PERMA", "Meaning"),
        ("WBP", "Meaning")
    ],
    "Life Satisfaction and Well-Being": [
        ("SWLS", "LS"),
        ("WHO-5", "Well-Being"),
        ("PERMA", "Happiness")
    ]
}

# Step 3: Compute correlation matrices for each grouping
for group_name, dimensions in groupings.items():
    group_items = []

    for scale, dimension in dimensions:
        items = [col for col in results.columns if col[0] == scale and col[1] == dimension]
        group_items.extend(items)

    if len(group_items) > 1:  # Only calculate if there are multiple items in the group
        group_data = results[group_items]

        # Compute the correlation matrix for this group
        corr_matrix = group_data.corr()

        # Save the correlation matrix for this group
        corr_matrix.to_excel(f'dataframes/tests/gpt40-mini/Correlations/Inter-Scales Dimension/Group/{group_name}_correlation_matrix.xlsx')

        # Print the correlation matrix for review
        print(f"{group_name} Correlation Matrix:")
        print(corr_matrix)
