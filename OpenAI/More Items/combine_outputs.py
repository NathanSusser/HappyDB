import pandas as pd
import os

# Define the directory containing your CSV files
csv_dir = '/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/gpt40-mini/More Items'

# List of CSV files to combine
csv_files = [
    'output - mini 0.csv',
    'output - mini 200.csv',
    'output - mini 400.csv'
]

# Define the new column names
new_column_names = {
    'id': 'Index',
    'raw': 'hmid',
    'parsed': 'clean_hm',
}

# Combine the CSV files
combined_df = pd.concat(
    [pd.read_csv(os.path.join(csv_dir, f), index_col=0).reset_index(drop=True) for f in csv_files],
    ignore_index=True
)

# Rename the columns
combined_df.rename(columns=new_column_names, inplace=True)

# Save the combined DataFrame
combined_output_path = os.path.join(csv_dir, 'output - merged.csv')
combined_df.to_csv(combined_output_path, index=False)

print(f"Combined CSV saved to {combined_output_path}")
