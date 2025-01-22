import pandas as pd
import os

# Set working directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

# Load the main data and reverse-coded items
results = pd.read_csv('dataframes/tests/gpt40-mini/updated_ratings_matrix.csv', header=[0, 1, 2])  # Adjust to load multi-index
rev_items = pd.read_csv('Profiles/merged_reverse_coded_items.csv')

# Normalize text for matching
results_items = {item.strip().lower() for item in [col[2] for col in results.columns]}
rev_items['Items'] = rev_items['Items'].str.strip().str.lower()
reverse_coded_items = set(rev_items['Items'].tolist())

# Identify unmatched items
unmatched_items = results_items - reverse_coded_items
print(f"Unmatched items (treated as non-reverse-coded): {unmatched_items}")

# Filter columns
reverse_items = [col for col in results.columns if col[2].strip().lower() in reverse_coded_items]
non_reverse_items = [col for col in results.columns if col[2].strip().lower() not in reverse_coded_items]

# Separate reverse-coded and non-reverse-coded data
reverse_items_data = results[reverse_items]
non_reverse_items_data = results[non_reverse_items]

# Compute correlation matrices for all scales
scales = set([col[0] for col in results.columns])

for scale in scales:
    scale_items = [col for col in results.columns if col[0] == scale]
    if len(scale_items) > 1:  # Only process scales with multiple items
        scale_data = results[scale_items]

        # Compute correlation matrix for the entire scale
        corr_matrix = scale_data.corr()
        corr_matrix.to_excel(f'dataframes/tests/gpt40-mini/Correlations/{scale}_correlation_matrix.xlsx')
        print(f"{scale} correlation matrix saved.")

        # Special handling for PWB
        if scale == 'PWB'or scale == 'CIT':
            reverse_items = [col for col in scale_items if col[2].strip().lower() in reverse_coded_items]
            non_reverse_items = [col for col in scale_items if col[2].strip().lower() not in reverse_coded_items]

            # Reverse-coded PWB
            if len(reverse_pwb_items) > 1:
                reverse_pwb_data = scale_data[reverse_pwb_items]
                reverse_pwb_corr = reverse_pwb_data.corr()
                reverse_pwb_corr.to_excel(f'dataframes/tests/gpt40-mini/Correlations/PWB_reverse_correlation_matrix.xlsx')
                print("PWB reverse-coded correlation matrix saved.")

            # Non-reverse-coded PWB
            if len(non_reverse_pwb_items) > 1:
                non_reverse_pwb_data = scale_data[non_reverse_pwb_items]
                non_reverse_pwb_corr = non_reverse_pwb_data.corr()
                non_reverse_pwb_corr.to_excel(f'dataframes/tests/gpt40-mini/Correlations/PWB_non_reverse_correlation_matrix.xlsx')
                print("PWB non-reverse-coded correlation matrix saved.")
