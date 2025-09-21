
#IMPORTS

#imports
import os, pandas, numpy, json, random, time
from openai import OpenAI

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')

#=========================================

#SETUP

#file paths
sentences_path = 'dataframes/clean_sentences.csv'
prompts_path = 'OpenAI/More Items/misc - prompts.csv'

#output directory for split batches
output_dir = 'data/context output/'
os.makedirs(output_dir, exist_ok=True)

#load dataset
sentences = pandas.read_csv(sentences_path)

#=========================================

#SPECIFY QUESTIONS

dfq = pandas.read_csv(prompts_path)
questions = list(dfq['Prompt'])
questionnames = list(dfq['Tag'])

#=========================================

#GPT FUNCTIONS

#set up openai connection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) 

MODEL_NAME = "gpt-4o-mini-2024-07-18"

#gpt4 function
def chat4(system, user_assistant):
  assert isinstance(system, str), "`system` should be a string"
  assert isinstance(user_assistant, list), "`user_assistant` should be a list"
  system_msg = [{"role": "system", "content": system}]
  user_assistant_msgs = [
      {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
      for i in range(len(user_assistant))]
  msgs = system_msg + user_assistant_msgs
  response = client.chat.completions.create(model=MODEL_NAME,
                                          messages=msgs)
  return response.choices[0].message.content 

#=========================================

#CODE

allratings = [['id','raw','parsed'] + questionnames]

#processing parameters
istart = 0
processed_count = 0

for index, row in sentences.iterrows():
    
    #specify which rows to code
    if  index >= istart  and index < istart + 5000:
        
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
            assistant_msg = chat4(dev_msg, [user_msg])
            ratings.append(assistant_msg)
        allratings.append(ratings)
        processed_count += 1
        print(f"Processed index: {index} ({processed_count})")
        
        if processed_count%100 == 0:
            #convert to pandas and save
            dfout = pandas.DataFrame(allratings[1:],columns = allratings[0])
            dfout.to_csv('output - mini ' + str(istart) + '.csv')
            print('save')

#convert to pandas and save
dfout = pandas.DataFrame(allratings[1:],columns = allratings[0])
dfout.to_csv('output - mini ' + str(istart) + '.csv')
print('save')