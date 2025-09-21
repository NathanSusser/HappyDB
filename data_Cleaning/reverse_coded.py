#IMPORTS

#imports
import pandas

#=========================================

#LOAD DATA

#load the uploaded CSV file to process it
file_path = "Profiles/PWB.csv"
data = pandas.read_csv(file_path)

#=========================================

#REVERSE CODED ITEMS

#list of reverse-coded items based on the previous analysis
reverse_coded_items = [
    "I am not afraid to voice my opinions, even when they are in opposition to others.",
    "For me, life has been a continuous process of learning, changing, and growth.",
    "In general, I feel I am in charge of the situation in which I live.",
    "People would describe me as a giving person, willing to share my time with others.",
    "I enjoy making plans for the future and working to make them a reality.",
    "Most people see me as loving and affectionate.",
    "When I look at the story of my life, I am pleased with how things have turned out.",
    "My decisions are not usually influenced by what everyone else is doing.",
    "I think it is important to have new experiences that challenge how you think about yourself.",
    "I have a sense of direction and purpose in life.",
    "I judge myself by what I think is important, not by others' values.",
    "In general, I feel confident and positive about myself.",
    "I have been able to build a living environment and a lifestyle for myself.",
    "I know that I can trust my friends, and they know they can trust me.",
    "Some people wander aimlessly through life, but I am not one of them.",
    "When I compare myself to friends, it makes me feel good about who I am.",
    "I have confidence in my opinions, even if contrary to the general consensus.",
    "I am quite good at managing the responsibilities of daily life.",
    "I have developed significantly as a person over time.",
    "I enjoy personal and mutual conversations with family and friends.",
    "I like most parts of my personality."
]

#add a new column to mark if an item is reverse coded
data['Reverse Coded'] = data['Items'].apply(lambda x: 'Yes' if x in reverse_coded_items else 'No')
data.drop(columns=['Items'], inplace=True)

#=========================================

#CLEAN ITEMS

#rename the column
data.rename(columns={'Item-sit': 'Items'}, inplace=True)

#remove the specific string from the 'Items' column
string_to_remove = 'How much does this experience indicate '
data['Items'] = data['Items'].str.replace(string_to_remove, '', regex=False)

#=========================================

#SAVE DATA

#save the updated data to a new CSV file
output_file_path = "Profiles/PWB_reverse_coded.csv"
data.to_csv(output_file_path, index=False)
