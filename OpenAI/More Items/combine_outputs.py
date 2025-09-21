#IMPORTS

#imports
import pandas
import os

#=========================================

#SETUP

#define the directory containing your CSV files
csv_dir = '/Users/nsusser/Desktop/Github/happyDB/dataframes/tests/gpt40-mini/More Items'

#list of CSV files to combine
csv_files = [
    'output - mini 0.csv',
    'output - mini 200.csv',
    'output - mini 400.csv'
]

#define the new column names
new_column_names = {
    'id': 'Index',
    'raw': 'hmid',
    'parsed': 'clean_hm',
}

#=========================================

#COMBINE AND SAVE

#combine the CSV files
combined_df = pandas.concat(
    [pandas.read_csv(os.path.join(csv_dir, f), index_col=0).reset_index(drop=True) for f in csv_files],
    ignore_index=True
)

#rename the columns
combined_df.rename(columns=new_column_names, inplace=True)

#save the combined dataframe
combined_output_path = os.path.join(csv_dir, 'output - merged.csv')
combined_df.to_csv(combined_output_path, index=False)

print(f"Combined CSV saved to {combined_output_path}")
