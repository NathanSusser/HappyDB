import pandas as pd

# Specify the input and output file paths
parquet_file = "/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/ratings.parquet"  # Replace with your Parquet file path
csv_file = "/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/ratings.csv"         # Replace with your desired CSV file path

# Read the Parquet file into a DataFrame
df = pd.read_parquet(parquet_file)

# Extract the first row
first_row = df.iloc[[0]]  # Selects the first row of the DataFrame

# Display the first row
print(first_row)

# Save the first row to a CSV file
first_row.to_csv(csv_file, index=True)  # Preserve the multi-index in the CSV

print(f"First row saved to {csv_file}.")
