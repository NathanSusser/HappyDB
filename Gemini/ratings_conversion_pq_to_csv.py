import pandas as pd

# Specify the input and output file paths
parquet_file = "/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/ratings.parquet"  # Replace with your Parquet file path
csv_file = "/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/ratings2.csv"         # Replace with your desired CSV file path

# Read the Parquet file into a DataFrame
df = pd.read_parquet(parquet_file)

df.to_csv(csv_file, index=True)  # Preserve the multi-index in the CSV

print(f"First row saved to {csv_file}.")
