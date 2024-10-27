import csv
import pandas as pd
import json

count = 0
# This is the function you need to implement
def process_input(input_filename: str, n: int):
    final = {}

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_filename)
    '''
    
    # Extract the 'cleaned_hm' and 'predicted_category' columns
    text = df[['predicted_category']]
    categories = df[['predicted_category']].unique()
    for row in df:
            line = text[row]
            words = line.strip().split()
            for word in words:
                final[categories].add(word)
    '''
    # Assume 'df' is your DataFrame
    # Initialize an empty dictionary to store categories and their words
    final = {}

    # Iterate over the DataFrame rows
    for index, row in df.iterrows():
        # Get the category for this row
        category = row['predicted_category']  # Replace with your category column name
        # Get the text for this row
        line = row['cleaned_hm']  # Replace with your text column name

        # Skip rows with missing data
        if pd.isnull(category) or pd.isnull(line):
            continue

        # Preprocess the line (optional)
        line = line.strip().lower()
        words = line.split()

        # Initialize the set for this category if it doesn't exist
        if category not in final:
            final[category] = set()

        # Add words to the set for this category
        for word in words:
            global count 
            count += 1
            final[category].add(word)
    # Convert sets to lists for JSON serialization
    categories_serializable = {category: list(keywords) for category, keywords in final.items()}

    # Write the dictionary to a JSON file
    with open('my data/categories.json', 'w', encoding='utf-8') as json_file:
        json.dump(categories_serializable, json_file, indent=4)

    print("The categories dictionary has been saved to 'categories.json'.")
    return final


'''
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Ensure NLTK data is downloaded
nltk.download('punkt')


def analyze_row(row):
    text = row['cleaned_hm']  # Replace with your column name
    tokens = word_tokenize(text.lower())
    word_count = len(tokens)
    category_counts = defaultdict(int)
    
    for word in tokens:
        for category, words in categories.items():
            if word in words:
                category_counts[category] += 1
                
    # Calculate frequencies
    category_frequencies = {category: (count / word_count) * 100 
                            for category, count in category_counts.items()}
    return pd.Series(category_frequencies)

# Apply the function to each row
results = df.apply(analyze_row, axis=1)

# Combine results with original DataFrame
df = pd.concat([df, results], axis=1)

# Save to CSV
df.to_csv('output_with_liwc_analysis.csv', index=False)
'''
#process_input('data.tiny-sample.txt', 2)
#print(create_dict_line(["Start","hi", "nate", "End"], 2, {}, 0))
# This code is helpful for when you are testing / debugging your work.
# You may edit or remove the code below.

if __name__ == '__main__':
    filename = input('Enter a filename:')
    n = int(input('Enter an ngram size:'))
    print(process_input(filename,n))
    print(count)


