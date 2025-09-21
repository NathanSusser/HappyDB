#IMPORTS

#imports
import pandas
import os

#set working directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

#=========================================

#LOAD DATA

#set file paths
input_path = 'Profiles/CIT_reverse_coded.csv'
output_path = 'Profiles/CIT_reverse_coded.csv'

#load the csv file
df = pandas.read_csv(input_path)

#=========================================

#CLEAN ITEMS

#rename the column
df.rename(columns={'Items-Sit': 'Items'}, inplace=True)

#remove the specific string from the 'Items' column
string_to_remove = 'How much does this experience indicate '
df['Items'] = df['Items'].str.replace(string_to_remove, '', regex=False)

#=========================================

#SAVE DATA

#save the cleaned data
df.to_csv(output_path, index=False)
