import pandas as pd

# Step 1: Read the CSV file into a DataFrame
input_file = "/Users/nsusser/Desktop/Github/happyDB/Profiles/PWB.csv"  # Replace with your file name
df = pd.read_csv(input_file)

# Step 2: Drop the specified columns
columns_to_remove = ["Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6", "Unnamed: 7"]
df = df.drop(columns=columns_to_remove)

# Step 3: Write the updated DataFrame to a new CSV file
output_file = "/Users/nsusser/Desktop/Github/happyDB/Profiles/PWB.csv"  # Replace with your desired output file name
df.to_csv(output_file, index=False)

# Print a message or preview the DataFrame
print("Updated DataFrame saved to:", output_file)
print(df.head())  # Display the first few rows of the updated DataFrame
