#IMPORTS
import os, pandas as pd, numpy, json, random, time
from openai import OpenAI

#set current directory
os.chdir('/Users/nsusser/Desktop/Github/happyDB/playing around/my data/') #fill in

#specify dataset
dataset = 'clean_open_ai'

#load dataset
df = pd.read_csv('clean_open_ai.csv')

#=========================================

#GPT FUNCTIONS

#set up openai connection
OPENAI_API_KEY = "" #fill in
client = OpenAI(api_key=OPENAI_API_KEY) 

#gpt3 function
def chat3(system, user_assistant):
  assert isinstance(system, str), "`system` should be a string"
  assert isinstance(user_assistant, list), "`user_assistant` should be a list"
  system_msg = [{"role": "system", "content": system}]
  user_assistant_msgs = [
      {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
      for i in range(len(user_assistant))]
  msgs = system_msg + user_assistant_msgs
  response = client.chat.completions.create(model="gpt-3.5-turbo",
                                          messages=msgs)
  return response.choices[0].message.content 

#=========================================


for row_index, row in df[['hmid', 'reflection_period', 'cleaned_hm']].iterrows():
  #break up row into moment and time
  moment = row['cleaned_hm']
  time = row['reflection_period']
  print(moment, time) 
  for col_index, item in enumerate(df.columns[3:], start=1): 
    #specify which rows to code
    if  row_index > -1  and col_index > -1:
        #check the scale wording to use
        if 1 <= col_index <= 5 or 14 <= col_index <= 17:
           scale_0 = 'never'
           scale_10 = 'always'
        elif col_index == 6 or col_index == 18:
           scale_0 = 'terrible'
           scale_10 = 'excellent'
        elif 7 <=col_index <= 13 or 19 <= col_index <= 23:
            scale_0 = 'not at all'
            scale_10 = 'completely'
        print(col_index, item, scale_0, scale_10)
  # Remove the break statement to ensure all columns are processed for each row

'''
        
        #append and save
        coded_contexts.append([duty,intellect,adversity,mating,positivity,negativity,deception,sociality])
        dfout = pandas.DataFrame(coded_contexts[1:], columns = coded_contexts[0])
        dfout.to_csv('data - unmerged - ' + dataset + '.csv')
        print(index)

#=========================================

#MERGE
dfout= pandas.read_csv('data - unmerged - ' + dataset + '.csv')
dfout = pandas.concat([df,dfout], axis=1)
columns_to_drop = [col for col in dfout.columns if 'unnamed:' in col.lower()]
dfout.drop(columns=columns_to_drop, inplace=True)
dfout.to_csv('data - ' + dataset + '.csv')
'''