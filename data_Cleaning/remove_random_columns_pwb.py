#IMPORTS

#imports
import pandas

#=========================================

#LOAD DATA

#read the CSV file into a dataframe
input_file = "/Users/nsusser/Desktop/Github/happyDB/Profiles/PWB.csv"
df = pandas.read_csv(input_file)

#=========================================

#REMOVE COLUMNS

#drop the specified columns
columns_to_remove = ["Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6", "Unnamed: 7"]
df = df.drop(columns=columns_to_remove)

#=========================================

#SAVE DATA

#write the updated dataframe to a new CSV file
output_file = "/Users/nsusser/Desktop/Github/happyDB/Profiles/PWB.csv"
df.to_csv(output_file, index=False)

#print confirmation message
print("Updated DataFrame saved to:", output_file)
print(df.head())  #display the first few rows
