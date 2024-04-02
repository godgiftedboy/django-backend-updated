
import re
import string
import numpy as np 


import nltk
from nltk.corpus import stopwords,wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



stop_words = set(stopwords.words('english'))
additional_stop_words = {'u', 'im', 'not', 'no', 'never', 'neither', 'nor'}
stop_words |= additional_stop_words
# Dictionary for common typos and slangs
typos_slangs = {
    "lol": "laugh out loud",
    "brb": "be right back",
    "jk": "just kidding",
}
def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    
    # Replace typos and slangs
    for typo, correction in typos_slangs.items():
        text = text.replace(typo, correction)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = nltk.pos_tag(tokens)
    lemmatized_tokens = [lemmatizer.lemmatize(token, pos=pos[0].lower()) if pos[0].lower() in ['n', 'v', 'a'] else lemmatizer.lemmatize(token) for token, pos in tagged_tokens]
    processed_tokens = []
    
    negation = False
    for token in lemmatized_tokens:
        if token in {'not', 'no', 'never', 'neither', 'nor', "cannot", "won't"}:
            negation = True
        elif negation:
            token = 'not_' + token
            negation = False
        processed_tokens.append(token)  
    processed_text = ' '.join([word for word in processed_tokens if word not in stop_words]) 
    return processed_text

