import pandas as pd

# Load the two matrices
matrix1_path = "dataframes/tests/gpt40-mini/updated_ratings_matrix.csv"
matrix2_path = "dataframes/tests/gpt40-mini/CIT/ratings_matrix.csv"

# Read the matrices (adjust for Excel files if needed)
matrix1 = pd.read_csv(matrix1_path, header=[0, 1], index_col=0)
matrix2 = pd.read_csv(matrix2_path, header=[0, 1], index_col=0)

# Ensure both matrices have the same multi-index structure
matrix1 = matrix1.reindex_like(matrix2, method=None)
matrix2 = matrix2.reindex_like(matrix1, method=None)

# Combine the matrices
merged_matrix = pd.concat([matrix1, matrix2], axis=1).groupby(level=0, axis=1).first()


# Save the merged matrix to a new file
merged_matrix.to_csv("dataframes/tests/gpt40-mini/merged_matrix.csv")

# Display the result
print(merged_matrix)
