#IMPORTS

#imports
import os
import pandas
import concurrent.futures
from openai import OpenAI

#=========================================

#SETUP

#setup paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
prompts_path = 'OpenAI/More Items/misc - prompts.csv'

output_file = 'data/context output/final_output.csv'
os.makedirs('data/context output/', exist_ok=True)

#load datasets
sentences = pandas.read_csv(sentences_path)
dfq = pandas.read_csv(prompts_path)
questions = list(dfq['Prompt'])
questionnames = list(dfq['Tag'])

#setup OpenAI connection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

#=========================================

#GPT FUNCTIONS

#GPT-4 function
def chat4(system, user_msg):
    """calls the OpenAI API with the given system and user messages"""
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [{"role": "user", "content": user_msg}]
    msgs = system_msg + user_assistant_msgs
    response = client.chat.completions.create(model=MODEL_NAME, messages=msgs)
    return response.choices[0].message.content

#process a single question for a given sentence
def process_question(dev_msg, sentence, question):
    """processes a single question for the given sentence using the API"""
    user_msg = (
        f"The following is a description of an experience: ** {sentence} **. \n\n"
        f"{question}"
    )
    return chat4(dev_msg, user_msg)

#process a single sentence
def process_sentence(index, row):
    """processes one sentence with all questions"""
    dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
    sentence = row['cleaned_hm']
    hmid = row['hmid']

    #use ThreadPoolExecutor to process questions concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=33) as executor:
        future_to_question = {
            executor.submit(process_question, dev_msg, sentence, q): q for q in questions
        }
        results = ["No response"] * len(questions)  #default to "No response" for missing values
        for future in concurrent.futures.as_completed(future_to_question):
            question_index = questions.index(future_to_question[future])  #get the index
            try:
                results[question_index] = future.result()  #insert result in the correct position
            except Exception as e:
                print(f"Error processing question: {future_to_question[future]} - {e}")
                results[question_index] = "Error"  #placeholder for failed calls

    #return data in the correct order
    return [index, hmid, sentence] + results

#=========================================

#MAIN FUNCTION

def main():
    """main processing function"""
    #resume from last processed index
    if os.path.exists(output_file):
        completed_data = pandas.read_csv(output_file)
        istart = completed_data['id'].max() + 1
    else:
        #write header if the file doesn't exist
        with open(output_file, 'w') as f:
            header = ['id', 'raw', 'parsed'] + questionnames
            f.write(','.join(header) + '\n')
        istart = 0

    iend = len(sentences)
    rows_to_process = sentences.iloc[istart:iend]

    print(f"Resuming from index {istart}...")

    #initialize the results container
    allratings = []
    processed_count = 0

    #process sentences sequentially, with each sentence having multiple threads
    for index, row in rows_to_process.iterrows():
        ratings = process_sentence(index, row)
        allratings.append(ratings)
        processed_count += 1

        #append results to file every 10 sentences
        if processed_count % 10 == 0:
            with open(output_file, 'a') as f:
                for rating in allratings:
                    f.write(','.join(map(str, rating)) + '\n')
            allratings = []  #clear intermediate results
            print(f"Appended {processed_count} sentences to {output_file}")

    #save any remaining results
    if allratings:
        with open(output_file, 'a') as f:
            for rating in allratings:
                f.write(','.join(map(str, rating)) + '\n')
    print("Processing complete and final results saved.")

if __name__ == "__main__":
    main()
