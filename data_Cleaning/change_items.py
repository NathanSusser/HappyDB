import pandas as pd
import os

# Set the working directory and file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
input_path = 'Profiles/CIT_reverse_coded.csv'
output_path = 'Profiles/CIT_reverse_coded.csv'

# Load the CSV file
df = pd.read_csv(input_path)

# Rename the column
df.rename(columns={'Items-Sit': 'Items'}, inplace=True)

# Remove the specific string from the 'Items' column
string_to_remove = 'How much does this experience indicate '
df['Items'] = df['Items'].str.replace(string_to_remove, '', regex=False)

# Save the cleaned data, ensuring special characters are escaped properly
df.to_csv(output_path, index=False)
