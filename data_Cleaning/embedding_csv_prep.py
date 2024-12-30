#IMPORTS
import pandas as pd
import os

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/') #fill in

'''
#read in the happyDB data
hbd_df = pd.read_csv('happydb/data/cleaned_hm.csv')
# Pull the clean sentences from the happyDB data
clean_sentences = hbd_df[['hmid', 'reflection_period', 'cleaned_hm']]
print(clean_sentences.head())

# Set 'hmid', 'reflection_period', and 'cleaned_hm' as multi-index
clean_sentences.set_index(['hmid', 'reflection_period', 'cleaned_hm'], inplace=True)

#save the clean_sentences dataframe to a csv
clean_sentences.to_csv('dataframes/clean_sentences.csv', index=True)
'''

#Create CSV for the dimensions and items

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

# rename the item columns to be consistent
PERMA_df = PERMA_df.rename(columns={'item-sit': 'Item-sit'})
WBP_df = WBP_df.rename(columns={'Item-sit': 'Item-sit'})
SWLS_df = SWLS_df.rename(columns={'item-sit': 'Item-sit'})
PWB_df = PWB_df.rename(columns={'Item-sit': 'Item-sit'})
PANAS_df = PANAS_df.rename(columns={'Item': 'Item-sit'})
WHO_5_df = WHO_5_df.rename(columns={'Items-Sit': 'Item-sit'})

# Add a 'Scale' column to each DataFrame to identify the source
PERMA_df['Scale'] = 'PERMA'
WBP_df['Scale'] = 'WBP'
SWLS_df['Scale'] = 'SWLS'
PWB_df['Scale'] = 'PWB'
PANAS_df['Scale'] = 'PANAS'
WHO_5_df['Scale'] = 'WHO-5'

# Concatenate vertically
combined_df = pd.concat([
    PERMA_df[['Scale', 'Dimension', 'Item-sit']],
    WBP_df[['Scale', 'Dimension', 'Item-sit']],
    SWLS_df[['Scale', 'Dimension', 'Item-sit']],
    PWB_df[['Scale', 'Dimension', 'Item-sit']],
    PANAS_df[['Scale', 'Dimension', 'Item-sit']],
    WHO_5_df[['Scale', 'Dimension', 'Item-sit']]
], axis=0).reset_index(drop=True)

# Remove leading and trailing whitespace from all string entries
combined_df = combined_df.map(lambda x: x.strip() if isinstance(x, str) else x)

#save the dim_items_df dataframe to a csv
combined_df.to_csv('dataframes/scales_df.csv', index=False)