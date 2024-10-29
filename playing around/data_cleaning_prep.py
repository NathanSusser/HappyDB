#IMPORTS
import pandas as pd
import os

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/') #fill in

#read in the happyDB data
hbd_df = pd.read_csv('happydb/data/cleaned_hm.csv')

#read in PERMA items and dimensions
PERMA_df = pd.read_csv('Profiles/PERMA.csv')

#read in PERMA_subject items and dimensions
PERMA_sub_df = pd.read_csv('Profiles/PERMA-SUBJECT.csv')

#read in the WB-PRo items and dimensions
WBP_df = pd.read_csv('Profiles/WB-Pro.csv')

#read in the SWB items and dimensions
#SWB_df = pd.read_csv('/Profiles/SWB.csv')

#read in the PWB items and dimensions
#PWB_df = pd.read_csv('/Profiles/PWB.csv')

#read in the PANAS items and dimensions
#PANAS_df = pd.read_csv('/Profiles/PANAS.csv')

# Pull the clean sentences from the happyDB data
clean_sentences = hbd_df[['hmid', 'reflection_period', 'cleaned_hm']]
print(clean_sentences.head())

# Get distinct items in 'reflection_period'
distinct_reflection_periods = clean_sentences['reflection_period'].unique()
print(distinct_reflection_periods)

# Set 'hmid', 'reflection_period', and 'cleaned_hm' as multi-index
clean_sentences.set_index(['hmid', 'reflection_period', 'cleaned_hm'], inplace=True)

# Extract the second column (Items) from PERMA_df
#PERMA_items = PERMA_df.iloc[:, 1]  

# Extract the second column (Items) from PERMA_df
#WBP_items = WBP_df.iloc[:, 1]  

# Extract the second column (Items) from PERMA_df
PERMA_sub_items = PERMA_sub_df.iloc[:, 1]  

# Combine items from PERMA_df to create the list of column names
column_names = list(PERMA_sub_items)  # + list(WBP_items)

# Create the matrix with 'cleaned_hm' as rows and combined items as columns
matrix = pd.DataFrame(0, index=clean_sentences.index, columns=column_names)

print(matrix.columns[1:])
#download the matrix
matrix.to_csv('/Users/nsusser/Desktop/Github/happyDB/playing around/my data/clean_open_ai.csv', index=True)