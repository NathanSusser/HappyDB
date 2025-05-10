import pandas as pd
import re

reverse_coded_items_df = pd.read_csv('profiles/merged_reverse_coded_items_only.csv')

items_path = 'dataframes/scales_clean.csv'
items = pd.read_csv(items_path)


def clean_df(df):
    df['Scale'] = df['Scale'].str.strip()
    df['Dimension'] = df['Dimension'].str.strip()
    df['Items'] = df['Items'].str.strip()
    return df

scales_clean = clean_df(items)
reverse_coded_items_df = clean_df(reverse_coded_items_df)

# Inner join to match only the reverse-coded items that exist in scales_clean
merged = reverse_coded_items_df.merge(
    scales_clean,
    on=["Scale", "Dimension", "Items"],
    how="inner",
    suffixes=("", "_clean")
)
merged['flat_name'] = merged.apply(
    lambda row: f"{row['Scale'].replace(' ', '_')}_{row['Dimension'].replace(' ', '_')}_{row['Items'].replace(' ', '_')}",
    axis=1
)


# Save reversed column names to a CSV
merged[['flat_name']].to_csv("profiles/reversed_column_names.csv", index=False)
