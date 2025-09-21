#IMPORTS

#imports
import pandas
import re

#=========================================

#LOAD DATA

#read reverse coded items
reverse_coded_items_df = pandas.read_csv('profiles/merged_reverse_coded_items_only.csv')

#read scales clean data
items_path = 'dataframes/scales_clean.csv'
items = pandas.read_csv(items_path)

#=========================================

#CLEAN DATA FUNCTION

def clean_df(df):
    """clean and standardize dataframe strings"""
    df['Scale'] = df['Scale'].str.strip()
    df['Dimension'] = df['Dimension'].str.strip()
    df['Items'] = df['Items'].str.strip()
    return df

#apply cleaning function
scales_clean = clean_df(items)
reverse_coded_items_df = clean_df(reverse_coded_items_df)

#=========================================

#MERGE AND CREATE COLUMN NAMES

#inner join to match only the reverse-coded items that exist in scales_clean
merged = reverse_coded_items_df.merge(
    scales_clean,
    on=["Scale", "Dimension", "Items"],
    how="inner",
    suffixes=("", "_clean")
)

#create flattened column names
merged['flat_name'] = merged.apply(
    lambda row: f"{row['Scale'].replace(' ', '_')}_{row['Dimension'].replace(' ', '_')}_{row['Items'].replace(' ', '_')}",
    axis=1
)

#=========================================

#SAVE DATA

#save reversed column names to a CSV
merged[['flat_name']].to_csv("profiles/reversed_column_names.csv", index=False)
