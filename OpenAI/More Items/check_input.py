
#IMPORTS

#imports
import os, pandas, numpy, json, random, time

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

#=========================================

#SETUP

#file paths
sentences_path = 'dataframes/clean_sentences.csv'
prompts_path = 'OpenAI/More Items/misc - prompts.csv'

#output directory for split batches
output_dir = 'dataframes/tests/gpt40-mini/More Items/'
os.makedirs(output_dir, exist_ok=True)

#load dataset
sentences = pandas.read_csv(sentences_path)

#=========================================

#SPECIFY QUESTIONS

dfq = pandas.read_csv(prompts_path)
questions = list(dfq['Prompt'])
questionnames = list(dfq['Tag'])

#=========================================

#CODE

allratings = [['id','raw','parsed'] + questionnames]

#processing parameters
istart = 0
max_sentences = 1000
processed_count = 0

for index, row in sentences.iterrows():
    
    #specify which rows to code
    if  index >= istart  and index < istart + 5000:
        #stop after processing the first 1000 rows
        if processed_count >= max_sentences:
            print("Processed 1000 sentences. Stopping.")
            break
        
        #specify system message
        dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
        
        hmid = row['hmid']
        period = row['reflection_period']
        sentence = row['cleaned_hm']
        sent_id = hmid
        
        #iterate over the questions
        ratings = [index, sent_id, sentence]
        for q in questions:
            user_msg = (
                    f"The following is a description of an experience ** {sentence} **. \n\n"
                    f"{q}"
                )
            assistant_msg = dev_msg + user_msg
            ratings.append(assistant_msg)
        allratings.append(ratings)
        processed_count += 1
        print(f"Processed index: {index} ({processed_count}/{max_sentences})")
        
        if processed_count%100 == 0:
            #convert to pandas and save
            dfout = pandas.DataFrame(allratings[1:],columns = allratings[0])
            dfout.to_csv('output - mini ' + str(istart) + '.csv')
            print('save')

#convert to pandas and save
dfout = pandas.DataFrame(allratings[1:],columns = allratings[0])
dfout.to_csv('output - mini ' + str(istart) + '.csv')
print('save')