#IMPORTS
import pandas as pd
import os

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/') #fill in

#read in the happyDB data
hbd_df = pd.read_csv('happydb/data/cleaned_hm.csv')

#read in PERMA items and dimensions
PERMA_df = pd.read_csv('Profiles/PERMA.csv')

#read in the WB-PRo items and dimensions
WBP_df = pd.read_csv('Profiles/WB-Pro.csv')

#read in the SWB items and dimensions
#SWB_df = pd.read_csv('/Profiles/SWB.csv')

#read in the PWB items and dimensions
#PWB_df = pd.read_csv('/Profiles/PWB.csv')

#read in the PANAS items and dimensions
#PANAS_df = pd.read_csv('/Profiles/PANAS.csv')

#pull the clean sentences from the happyDB data
clean_sentences = hbd_df['cleaned_hm']
print(clean_sentences.head())

# Extract the second column (Items) from PERMA_df and WBP_df
PERMA_items = PERMA_df.iloc[:, 1]  # Second column
WBP_items = WBP_df.iloc[:, 1]      # Second column

# Combine items from both dataframes to create the list of column names
column_names = list(PERMA_items) + list(WBP_items)

# Create the matrix with clean sentences as rows and combined items as columns
matrix = pd.DataFrame(0, index=clean_sentences, columns=column_names)

#download the matrix
matrix.to_csv('/Users/nsusser/Desktop/Github/happyDB/playing around/my data/clean_open_ai.csv', index=True)