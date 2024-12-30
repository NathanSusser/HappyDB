import google.generativeai as genai
import pandas as pd
import os
import time

# Set up file paths
os.chdir('/Users/nsusser/Desktop/Github/happyDB/')
sentences_path = 'dataframes/clean_sentences.csv'
items_path = 'dataframes/scales_df.csv'

# Load data
sentences = pd.read_csv(sentences_path)
items = pd.read_csv(items_path)

# Create hierarchical column structure
columns = list(zip(items['Scale'], items['Dimension'], items['Item-sit']))
columns = pd.MultiIndex.from_tuples(columns, names=["Scale", "Dimension", "Item-sit"])

# Create multi-index for rows using sentences and HMIDs
row_index = pd.MultiIndex.from_tuples(zip(sentences['hmid'], sentences['cleaned_hm']), names=["hmid", "cleaned_hm"])

# Initialize the DataFrame with None values
ratings = pd.DataFrame(None, index=row_index, columns=columns)

# Set up the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Constants for rate-limiting
RATE_LIMIT_TOKENS_PER_MINUTE = 1_000_000
MAX_REQUESTS_PER_MINUTE = 15
MAX_DAILY_REQUESTS = 1500
MODEL_NAME = "gemini-1.5-flash"

def wait_if_needed(total_tokens, start_time):
    """
    Wait if the number of tokens processed exceeds the rate limit.
    """
    elapsed_time = time.time() - start_time
    tokens_per_second = RATE_LIMIT_TOKENS_PER_MINUTE / 60
    expected_time = total_tokens / tokens_per_second
    if elapsed_time < expected_time:
        sleep_time = expected_time - elapsed_time
        print(f"Sleeping for {sleep_time:.2f} seconds to respect token rate limits...")
        time.sleep(sleep_time)

def enforce_rpm_limit(request_count, start_time):
    """
    Enforce the requests per minute (RPM) limit.
    """
    if request_count >= MAX_REQUESTS_PER_MINUTE:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            sleep_time = 60 - elapsed_time
            print(f"Sleeping for {sleep_time:.2f} seconds to respect RPM limits...")
            time.sleep(sleep_time)
        # Reset request count and start time for the next minute
        request_count = 0
        start_time = time.time()
    return request_count, start_time

def chat_with_retries(message, retries=3):
    """
    Send a message to the generative model with retry logic.
    """
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(message)
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Max retries reached. Skipping this request.")
                return None

# Iterate over sentences and items with rate-limiting
start_time = time.time()
total_tokens_used = 0  # Track the total tokens processed
request_count = 0
total_requests = 0

for _, row in sentences.iterrows():
    period = row['reflection_period']
    sentence = row['cleaned_hm']
    hmid = row['hmid']

    if total_requests >= MAX_DAILY_REQUESTS:
        print("Daily quota reached. Exiting...")
        break

    # Convert period to a descriptive time
    if period == "24h":
        time_frame = "24 hours"
    elif period == "3m":
        time_frame = "3 months"
    else:
        time_frame = "an unknown period"
    
    for _, item_row in items.iterrows():
        item = item_row['Item-sit']
        Dimension = item_row['Dimension']
        Scale = item_row['Scale']
        
        # Construct messages
        dev_msg = f"You are a helpful assistant who can help me code individual sentences written by people asked to describe what made them happy in the last {time_frame}."
        user_msg = f"On a scale of 0 to 7 where 0 is strongly agree and 7 is strongly disagree, please rate ** {item} ** This is the experience: ** {sentence} ** Please only return the number on a scale of 0 to 7 of ** {item} **."
        
        msg = dev_msg + '\n' + user_msg + '\n'

        # Estimate token count for the message (simplistic estimation: 1 word = 1 token)
        token_count = len(msg.split())
        total_tokens_used += token_count

        # Enforce RPM limit
        request_count, start_time = enforce_rpm_limit(request_count, start_time)
        
        # Wait if rate limit is exceeded
        wait_if_needed(total_tokens_used, start_time)

        # Get the response from the AI model with retries
        response = chat_with_retries(msg)

        if response is not None:
            try:
                # Strip whitespace and attempt to convert to an integer
                response_number = int(response.strip())
                print(f"Valid response: {response_number}")
                
                # Save the response to the ratings DataFrame
                ratings.loc[(hmid, sentence), (Scale, Dimension, item)] = response_number
            except ValueError:
                # Log unexpected responses
                print(f"Invalid response: {response}")
        else:
            print("No response received. Skipping.")
        
        # Update request counters
        request_count += 1
        total_requests += 1

# Fill missing values with a placeholder
ratings.fillna(-1, inplace=True)

# Save the result as a Parquet file
ratings.to_parquet('dataframes/tests/ratings.parquet')

print("Processing completed. Ratings saved to Parquet file.")
