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

# Step 1: Separate reverse-coded and non-reverse-coded items
reverse_coded_items = rev_items['Items'].tolist()  # Assuming column 'Items' lists reverse-coded items
regular_items_data = results[[col for col in results.columns if col[2] not in reverse_coded_items]]
reverse_items_data = results[[col for col in results.columns if col[2] in reverse_coded_items]]

# Step 2: Separate data by scales and dimensions to compute correlation matrices
scales = set([col[0] for col in results.columns])

for scale in scales:
    scale_items = [col for col in results.columns if col[0] == scale]
    if len(scale_items) > 1:  # Only calculate if there are multiple items in the scale
        scale_data = results[scale_items]

        # Group items by dimension (2nd level of index)
        dimensions = set([col[1] for col in scale_data.columns])

        for dimension in dimensions:
            dimension_items = [col for col in scale_data.columns if col[1] == dimension]
            if len(dimension_items) > 1:  # Only calculate if there are multiple items for the dimension
                dimension_data = scale_data[dimension_items]

                # Compute the correlation matrix for this dimension
                corr_matrix = dimension_data.corr()

                # Save the correlation matrix for this dimension within the scale
                corr_matrix.to_excel(f'dataframes/tests/gpt40-mini/Correlations/Dimension/{scale}_{dimension}_correlation_matrix.xlsx')

                # Print the correlation matrix for review
                print(f"{scale} - {dimension} Correlation Matrix:")
                print(corr_matrix)

        # Special handling for PWB reverse-coded and non-reverse-coded items
        if scale == 'PWB':
            reverse_pwb_items = [col for col in scale_items if col[2] in reverse_coded_items]
            non_reverse_pwb_items = [col for col in scale_items if col[2] not in reverse_coded_items]

            # Reverse-coded PWB items
            if len(reverse_pwb_items) > 1:
                reverse_pwb_data = scale_data[reverse_pwb_items]
                reverse_pwb_corr = reverse_pwb_data.corr()
                reverse_pwb_corr.to_excel(f'dataframes/tests/gpt40-mini/Correlations/Dimension/PWB_reverse_correlation_matrix.xlsx')
                print("PWB - Reverse-Coded Correlation Matrix:")
                print(reverse_pwb_corr)

            # Non-reverse-coded PWB items
            if len(non_reverse_pwb_items) > 1:
                non_reverse_pwb_data = scale_data[non_reverse_pwb_items]
                non_reverse_pwb_corr = non_reverse_pwb_data.corr()
                non_reverse_pwb_corr.to_excel(f'dataframes/tests/gpt40-mini/Correlations/Dimension/PWB_non_reverse_correlation_matrix.xlsx')
                print("PWB - Non-Reverse-Coded Correlation Matrix:")
                print(non_reverse_pwb_corr)
