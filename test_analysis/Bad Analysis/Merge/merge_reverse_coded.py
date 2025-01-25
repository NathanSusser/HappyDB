import pandas as pd

# Load the two files
file1_path = "Profiles/CIT_reverse_coded.csv"
file2_path = "Profiles/PWB_reverse_coded.csv"

# Read the files
CIT_df = pd.read_csv(file1_path)
PWB_df = pd.read_csv(file2_path)

#select the ones with yes
CIT_df = CIT_df[CIT_df['Reverse Coded'] == 'Yes']
PWB_df = PWB_df[PWB_df['Reverse Coded'] == 'Yes']

# Drop the 'Reverse Coded' column
CIT_df.drop(columns=['Reverse Coded'], inplace=True)  
PWB_df.drop(columns=['Reverse Coded'], inplace=True)

# Add column for Scale
CIT_df['Scale'] = 'CIT'
PWB_df['Scale'] = 'PWB'

# change the column order
CIT_df = CIT_df[['Scale', 'Dimension','Items']]
PWB_df = PWB_df[['Scale', 'Dimension','Items']]

# Merge the files along the same columns
merged_df = pd.concat([CIT_df, PWB_df], axis=0, ignore_index=True)

# Display the merged DataFrame
print(merged_df)

# Optionally save the merged file
merged_df.to_csv("Profiles/merged_reverse_coded_items_only.csv", index=False)
