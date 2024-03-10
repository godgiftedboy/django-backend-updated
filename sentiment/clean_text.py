
import re
import string
import numpy as np 


import nltk
from nltk.corpus import stopwords,wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    # Get the set of English stopwords from NLTK
    stop_words = set(stopwords.words('english'))

    # Additional words to be added to the stop words set
    additional_stop_words = {'u', 'im'}

    # Concatenate the stop words set with additional words
    stop_words |= additional_stop_words


    text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Lemmatize tokens with proper POS tagging
    lemmatizer = WordNetLemmatizer()

    tagged_tokens = nltk.pos_tag(tokens)
    lemmatized_tokens = []
    for token, tag in tagged_tokens:
        if tag.startswith('NN'):  # Noun
            pos = 'n'
        elif tag.startswith('VB'):  # Verb
            pos = 'v'
        else:
            pos = 'a'  # Adjective (default)s
        lemmatized_token = lemmatizer.lemmatize(token, pos=pos)
        lemmatized_tokens.append(lemmatized_token)
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text
