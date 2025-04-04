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

#read in SWLS items and dimensions
SWLS_df = pd.read_csv('Profiles/SWLS.csv')

#read in PWB items and dimensions
PWB_df = pd.read_csv('Profiles/PWB.csv')

#read in PERMA items and dimensions
PANAS_df = pd.read_csv('Profiles/PANAS.csv')

#read in the WHO-5 items and dimensions
WHO_5_df = pd.read_csv('Profiles/WHO-5.csv')
# Pull the clean sentences from the happyDB data
clean_sentences = hbd_df[['hmid', 'reflection_period', 'cleaned_hm']]
print(clean_sentences.head())

# Set 'hmid', 'reflection_period', and 'cleaned_hm' as multi-index
clean_sentences.set_index(['hmid', 'reflection_period', 'cleaned_hm'], inplace=True)

# Extract the third column (Items) from PERMA_df
PERMA_items = PERMA_df.iloc[:, [0, 2]]  

# Extract the third column (Items) from WBP_df
WBP_items = WBP_df.iloc[:, [0, 2]]

# Extract the third column (Items) from SWLS_df
SWLS_items = SWLS_df.iloc[:, [0, 2]]

# Extract the fourth column (Items) from PWB_df
PWB_items = PWB_df.iloc[:, [0, 2]]  

# Extract the third column (Items) from PANAS_df
PANAS_items = PANAS_df.iloc[:, [0, 2]]  

# Extract the third column (Items) from WHO_5_df
WHO_5_items = WHO_5_df.iloc[:, [0, 2]]  

# Combine items from PERMA_df to create the list of column names
column_names = list(PERMA_items) + list(WBP_items) + list(SWLS_items) + list(PWB_items) + list(PANAS_items) + list(WHO_5_items)

# Create the matrix with 'cleaned_hm' as rows and combined items as columns
matrix = pd.DataFrame(0, index=clean_sentences.index, columns=column_names)

print(matrix.columns[1:])
#download the matrix
matrix.to_csv('/Users/nsusser/Desktop/Github/happyDB/dataframes/dim_items_matrix.csv', index=True)