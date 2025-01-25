import pandas as pd
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity

# Load the dataset (multi-index columns)
results = pd.read_csv('dataframes/tests/gpt40-mini/updated_ratings_matrix.csv', header=[0, 1, 2])

# Step 1: Flatten multi-index columns
results.columns = ['_'.join(col).strip() for col in results.columns.values]

# Step 2: Define the columns for factor analysis
# Include only the relevant scales (e.g., PERMA, WBP, etc.)
scales_to_include = ['PERMA', 'WBP', 'SWLS', 'PWB', 'PANAS', 'WHO-5']
cols = [col for col in results.columns if any(scale in col for scale in scales_to_include)]
df_subset = results[cols]

# Step 3: Standardize the subset
scaler = StandardScaler()
df_standardized = pd.DataFrame(scaler.fit_transform(df_subset), columns=df_subset.columns)

# Step 4: Perform KMO and Bartlett's test
kmo_all, kmo_model = calculate_kmo(df_standardized)
chi_square_value, p_value = calculate_bartlett_sphericity(df_standardized)

print(f"KMO Model: {kmo_model}")
print(f"Bartlett’s Test: Chi-Square = {chi_square_value}, p-value = {p_value}")

# Step 5: Determine optimal number of factors
fa = FactorAnalyzer(rotation=None)
fa.fit(df_standardized)
eigenvalues, _ = fa.get_eigenvalues()

# Scree plot for visualization (optional)
import matplotlib.pyplot as plt
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.title('Scree Plot')
plt.grid()
plt.show()

optimal_factors = sum(eigenvalues > 1)
print(f"Optimal Number of Factors: {optimal_factors}")

# Step 6: Fit factor analysis with optimal factors
fa = FactorAnalyzer(n_factors=optimal_factors, rotation='varimax')
fa.fit(df_standardized)

# Step 7: Project columns onto factors
factor_scores = fa.transform(df_standardized)
for i in range(factor_scores.shape[1]):
    results[f'Factor_{i+1}'] = factor_scores[:, i]

# Save results to a CSV
results.to_csv('dataframes/tests/gpt40-mini/Correlations/data - final 1000 - factors.csv', index=False)

# Step 8: Print top 10 variables per factor
items = df_subset.columns.tolist()  # Map back to original variable names
factor_loadings = pd.DataFrame(fa.loadings_, index=items)

for i in range(factor_loadings.shape[1]):
    sorted_loadings = factor_loadings.iloc[:, i].abs().sort_values(ascending=False)
    top_variables = sorted_loadings.head(10).index.tolist()
    print(f'\nFactor {i+1}:')
    for var in top_variables:
        print(f"- {var}")
