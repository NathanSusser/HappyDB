import pandas as pd
import os

# Set working directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# Load the main data and reverse-coded items
results = pd.read_csv('merged.csv')  
reverse_coded_items_df = pd.read_csv('profiles/merged_reverse_coded_items_only.csv')

# Display the first few rows of both datasets
print(results.head())
print(reverse_coded_items_df.head())

# Step 1: Transform reverse-coded items
max_value = 7  # Max value in the dataset

# Create a lookup set of reverse-coded items including Scale, Dimension, and Item
reverse_coded_lookup = set(zip(
    reverse_coded_items_df['Scale'],
    reverse_coded_items_df['Dimension'],
    reverse_coded_items_df['Items']
))

# Reverse coding based on the flattened column names
for col in results.columns:
    # Extract the Scale, Dimension, and Item from the column name
    if col.startswith("("):  # Ensure we're only parsing relevant columns
        # Parse the column to extract Scale, Dimension, and Item
        parts = col.strip("()").split(", ", maxsplit=2)
        if len(parts) == 3:
            scale, dimension, item = [part.strip("'") for part in parts]  # Remove quotes
            print(scale, dimension, item)
            # Match against the reverse_coded_lookup
            if (scale, dimension, item) in reverse_coded_lookup:
                if pd.api.types.is_numeric_dtype(results[col]):  # Ensure column is numeric
                    results[col] = max_value + 1 - results[col]


# Step 2: Define specific groupings for analysis
groupings = {
    "Accomplishment and Mastery": [
        ("PERMA", "Accomplishment"),
        ("CIT", "Mastery - Accomplishment"),
        ("CIT", "Mastery - Learning"),
        ("CIT", "Mastery - Self-Efficacy"),
        ("CIT", "Mastery - Self-Worth"),
        ("CIT", "Mastery - Skills"),
        ("PWB", "Environmental Mastery"),
        ("WBP", "Competence"),
        ("WBP", "Accomplishment"),
    ],
    "Autonomy and Control": [
        ("PWB", "Autonomy"),
        ("WBP", "Autonomy"),
        ("CIT", "Autonomy - Control"),
    ],
    "Engagement and Flow": [
        ("PERMA", "Engagement"),
        ("WBP", "Engagement"),
        ("CIT", "Engagement"),
    ],
    "Positive Emotions": [
        ("PERMA", "Positive Emotion"),
        ("WBP", "Positive Emotions"),
        ("PANAS", "Positive"),
    ],
    "Negative Emotions": [
        ("PERMA", "Negative emotion"),
        ("PANAS", "Negative"),
        ("CIT", "Subjective Well-Being - Negative Feelings"),
    ],
    "Meaning and Purpose": [
        ("PERMA", "Meaning"),
        ("WBP", "Meaning"),
        ("PWB", "Purpose in Life"),
        ("CIT", "Meaning"),
    ],
    "Positive Relationships": [
        ("PERMA", "Relationships"),
        ("PWB", "Positive Relations"),
        ("WBP", "Positive Relationships"),
        ("CIT", "Relationship - Belonging"),
        ("CIT", "Relationship - Community"),
        ("CIT", "Relationship - Respect"),
        ("CIT", "Relationship - Support"),
        ("CIT", "Relationship - Trust"),
    ],
    "Life Satisfaction and Well-Being": [
        ("SWLS", "LS"),
        ("WHO-5", "Well-Being"),
        ("CIT", "Subjective Well-Being - Life Satisfaction"),
    ]
}



# Step 3: Compute correlation matrices for each grouping
for group_name, dimensions in groupings.items():
    group_items = []

    for scale, dimension in dimensions:
         # Match all items that belong to this scale and dimension
        items = [col for col in results.columns if f"('{scale}', '{dimension}')" in col]
        group_items.extend(items)

    if len(group_items) > 1:  # Only calculate if there are multiple items in the group
        group_data = results[group_items]

        # Compute the correlation matrix for this group
        corr_matrix = group_data.corr()

        # Save the correlation matrix for this group
        corr_matrix.to_excel(f'dataframes/tests/gpt40-mini/Correlations/Inter-Scales Dimension/Group/Improved/{group_name}_correlation_matrix.xlsx')

        # Print the correlation matrix for review
        #print(f"{group_name} Correlation Matrix:")
        #print(corr_matrix)
