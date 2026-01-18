import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Download necessary NLTK data ---
# We use a try-except block to make sure it works on both your PC and GitHub Actions
def download_nltk_resources():
    resources = ['punkt', 'wordnet', 'omw-1.4', 'punkt_tab']
    for res in resources:
        try:
            nltk.data.find(f'tokenizers/{res}')
        except (LookupError, ValueError):
            try:
                nltk.data.find(f'corpora/{res}')
            except (LookupError, ValueError):
                nltk.download(res, quiet=True)

download_nltk_resources()

from nltk.stem import WordNetLemmatizer

# --- 2. The Knowledge Base ---
# You can edit this text to change what the bot knows!
raw_text = """
A chatbot is artificial intelligence software that can simulate a conversation.
Chatbots are important because they automate interaction between humans and machines.
Natural Language Processing (NLP) helps computers understand human language.
Python is a popular programming language for building chatbots.
NLTK is a leading platform for building Python programs to work with human language data.
The Final Year Project is a crucial part of the engineering curriculum.
"""

# --- 3. Preprocessing Functions ---
lemmatizer = WordNetLemmatizer()

def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def normalize(text):
    return lemmatize_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Prepare the sentence list
sentence_list = nltk.sent_tokenize(raw_text)

# --- 4. Main Chat Function ---
def get_bot_response(user_input):
    user_input = user_input.lower()
    
    # Simple greetings
    greetings_in = ("hello", "hi", "greetings", "sup", "what's up", "hey")
    greetings_out = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
    
    if user_input in greetings_in:
        return random.choice(greetings_out)

    # TF-IDF Logic
    sentence_list.append(user_input)
    
    # Create the vectorizer
    tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    
    try:
        tfidf = tfidf_vectorizer.fit_transform(sentence_list)
        
        # Calculate similarity
        vals = cosine_similarity(tfidf[-1], tfidf)
        
        # Get the second most similar sentence (the most similar is the user input itself)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        
        response = ""
        if req_tfidf == 0:
            response = "I am sorry! I don't understand you."
        else:
            response = sentence_list[idx]
            
    except Exception as e:
        response = "Error processing input."
        
    finally:
        sentence_list.remove(user_input) # Clean up to keep list size constant
        
    return response
