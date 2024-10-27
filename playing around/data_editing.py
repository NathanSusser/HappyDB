import csv

input_filename = '/Users/nsusser/Desktop/Github/happyDB/happydb/data/cleaned_hm.csv'   # Replace with your actual input file name
output_filename = '/Users/nsusser/Desktop/Github/happyDB/my_data/ngram_data.csv' # Replace with your desired output file name

with open(input_filename, 'r', newline='', encoding='utf-8') as infile, \
     open(output_filename, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ['cleaned_hm']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        writer.writerow({'cleaned_hm': row['cleaned_hm']})