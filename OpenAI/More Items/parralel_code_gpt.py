import os
import pandas as pd
import concurrent.futures
from openai import OpenAI

# Setup paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
prompts_path = 'OpenAI/More Items/misc - prompts.csv'

output_file = 'data/context output/final_output.csv'
os.makedirs('data/context output/', exist_ok=True)

# Load datasets
sentences = pd.read_csv(sentences_path)
dfq = pd.read_csv(prompts_path)
questions = list(dfq['Prompt'])
questionnames = list(dfq['Tag'])

# Setup OpenAI connection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-4o-mini-2024-07-18"

# GPT-4 function
def chat4(system, user_msg):
    """Calls the OpenAI API with the given system and user messages."""
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [{"role": "user", "content": user_msg}]
    msgs = system_msg + user_assistant_msgs
    response = client.chat.completions.create(model=MODEL_NAME, messages=msgs)
    return response.choices[0].message.content

# Process a single question for a given sentence
def process_question(dev_msg, sentence, question):
    """Processes a single question for the given sentence using the API."""
    user_msg = (
        f"The following is a description of an experience: ** {sentence} **. \n\n"
        f"{question}"
    )
    return chat4(dev_msg, user_msg)

# Process a single sentence
def process_sentence(index, row):
    """Processes one sentence with all 33 questions."""
    dev_msg = "You are a helpful research assistant who can help me code the psychological properties of people's experiences."
    sentence = row['cleaned_hm']
    hmid = row['hmid']

    # Use ThreadPoolExecutor to process 33 questions concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=33) as executor:
        future_to_question = {
            executor.submit(process_question, dev_msg, sentence, q): q for q in questions
        }
        results = ["No response"] * len(questions)  # Default to "No response" for missing values
        for future in concurrent.futures.as_completed(future_to_question):
            question_index = questions.index(future_to_question[future])  # Get the index
            try:
                results[question_index] = future.result()  # Insert result in the correct position
            except Exception as e:
                print(f"Error processing question: {future_to_question[future]} - {e}")
                results[question_index] = "Error"  # Placeholder for failed calls

    # Return data in the correct order
    return [index, hmid, sentence] + results

# Main function
def main():
    # Resume from last processed index
    if os.path.exists(output_file):
        completed_data = pd.read_csv(output_file)
        istart = completed_data['id'].max() + 1
    else:
        # Write header if the file doesn't exist
        with open(output_file, 'w') as f:
            header = ['id', 'raw', 'parsed'] + questionnames
            f.write(','.join(header) + '\n')
        istart = 0

    iend = len(sentences)
    rows_to_process = sentences.iloc[istart:iend]

    print(f"Resuming from index {istart}...")

    # Initialize the results container
    allratings = []
    processed_count = 0

    # Process sentences sequentially, with each sentence having 33 threads
    for index, row in rows_to_process.iterrows():
        ratings = process_sentence(index, row)
        allratings.append(ratings)
        processed_count += 1

        # Append results to file every 10 sentences
        if processed_count % 10 == 0:
            with open(output_file, 'a') as f:
                for rating in allratings:
                    f.write(','.join(map(str, rating)) + '\n')
            allratings = []  # Clear intermediate results
            print(f"Appended {processed_count} sentences to {output_file}")

    # Save any remaining results
    if allratings:
        with open(output_file, 'a') as f:
            for rating in allratings:
                f.write(','.join(map(str, rating)) + '\n')
    print("Processing complete and final results saved.")

if __name__ == "__main__":
    main()
