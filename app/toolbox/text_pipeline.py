# import pandas as pd
# import numpy as np
import re
# from datetime import datetime
import emoji


# Function: Clean & Preprocess Texts for Input
def text_preprocess(text):
    text=str(text)

    # Lower Case - Fasttext is case sensitive 
    text = text.lower()
    
    # Textify emoji's 
    text = re.sub(r'_', ' ', emoji.demojize(text) )

#     # Genericize website patterns
#     website_pattern = re.compile(r'http\S+')
#     text = re.sub(website_pattern, 'website_url', text)
    text = text.replace('https://', 'https_ ')
    text = text.replace('http://', 'http_ ')
    
#     # Genericize email address patterns
#     email_pattern = re.compile(r'\S*@\S*\s?')
#     text = re.sub(email_pattern, 'email_address', text)

    # Genericize Phone Number patterns
    phone_num_pattern = re.compile("(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")
    text = re.sub(phone_num_pattern, 'phone_number', text)

    # Remove HTML patterns
    html_pattern = re.compile('<.*?>')
    text = re.sub(html_pattern, '', text)

    # Remove punctuation and special chars
    my_char_remove_list = ['"', '%', '&', "'", '(', ')', '*', '+', ',', '.',
            ':', ';', '<', '=', '>', '[', '\\', ']', '^', 
           '`', '{', '|', '}', '~', '»', '«', '"', '"']
    punct_pattern = re.compile("[" + re.escape("".join(my_char_remove_list)) + "]")
    text = re.sub(punct_pattern, '', text)

    # ...but leave & separate question marks and exclamation marks since so meaningful in our use cases
    text = text.replace('?', ' ? ')
    text = text.replace('!', ' ! ') 
    # Correct all multiple white spaces to a single white space
    text = re.sub('[\s]+', ' ', text)
    # Remove any spaces at the beginning and the end of a text
    text = text.strip()
   
    
#     # Remove numbers
#     rem_num = re.sub('[0-9]+', '', rem_url)

#     tokenizer = RegexpTokenizer(r'\w+')
#     tokens = tokenizer.tokenize(text)  
#     filtered_words = [w for w in tokens if len(w) > 2 if not w in stop_words]
#     stem_words=[stemmer.stem(w) for w in filtered_words]
#     lemma_words=[lemmatizer.lemmatize(w) for w in stem_words]
#     text = " ".join(filtered_words)

    return text


def pretty_labels(fastext_label):

    text = str(fastext_label.lower())
    text = re.sub('__label__', '', text)
    text = text.replace('[','').replace(']','')
    text = re.sub('_', ' ', text)

    return text

