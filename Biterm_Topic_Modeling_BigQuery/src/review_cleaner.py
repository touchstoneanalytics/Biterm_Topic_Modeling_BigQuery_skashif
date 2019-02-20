""" Code to clean headlines so that it can be used
    as input for the biterm algorithm """
import os
import sys
import pandas as pd
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
from gensim.models import Phrases
import argparse
import re
import spacy

class Data_Cleaner():
    def __init__(self, input_file_name, output_file_name):
        """
        Checking if the headlines file exist or not
        """
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(self.dir_path, "../input/" + input_file_name)
        if not os.path.isfile(self.file_path):
            print("File {} doesn't exist".format(self.file_path))
            sys.exit()

        # making sure that the resources have been downloaded before running the code
        nltk.download('wordnet')
        nltk.download('stopwords')
        #loading spacy 'english i.e en module'
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        
        self.output_file_name = output_file_name
        self.clean_data()
        
    def sentence_to_words(self, sentences):
        for sentence in sentences:
            # convert sentence (string) to list of words ignoring any words
            # that are too small (len 2) or too large (len 15)
            #print(sentence)
            yield (gensim.utils.simple_preprocess(str(sentence)))
    
    # lemmatization keeping only noun, adjective, verb and adverb
    def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags]
            )
        return texts_out

    def clean_data(self):
        """
        Main function where all the cleaning of code will occur
        """
        
        # using wordnet lemmatizer for stemming
        lemma = nltk.wordnet.WordNetLemmatizer()
        
        # downloading the stop words dictionary
        stop = stopwords.words(['english'])
        
        # reading the tweets file
        tweets = pd.read_csv(self.file_path, usecols = ['Body'], encoding='utf-8')

        # lower casing all the data
        tweets = tweets.apply(lambda x: x.astype(str).str.lower())
        
        # removing all the stop words and performing stemming
        tweets['text_clean'] = tweets['Body'].apply(lambda x: ' '.join([lemma.lemmatize(word) for word in x.split() 
                                                                                                if word not in (stop)]))
        # selecting words that have one of the following POS tags
        allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]
        tweets['text_clean'] = tweets['text_clean'].apply(lambda x: ' '.join([token.lemma_ for token in self.nlp(x) if token.pos_ in allowed_postags]))
        
        # removing all links from tweets
        tweets['text_clean'] = tweets['text_clean'].apply(lambda x: re.sub(r'http\S+', '', x, flags=re.MULTILINE))
        tweets['text_cleaner'] = list(self.sentence_to_words(tweets['text_clean']))
        tweets['text_cleaner'] = tweets['text_cleaner'].apply(lambda x: ' '.join(x))
        
        sentence_stream = [doc.split(" ") for doc in tweets['text_cleaner'].tolist()]
        bigram = Phrases(sentence_stream, min_count=10, threshold=100)
        sentences_with_bigrams = [bigram[sent] for sent in sentence_stream]
        #print(sentences_with_bigrams)
        tweets['text_cleanerer'] = [' '.join(sent) for sent in sentences_with_bigrams]
        tweets['text_cleanerer'].to_csv(os.path.join(self.dir_path, "../input/" + self.output_file_name), index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Cleaner')
    
    parser.add_argument("-i", dest="input_file", help="Path of the file containing data to be cleaned data", required=True)
    parser.add_argument("-o", dest="output_file", help="Name of the output file that will be generated", required=True)
    
    args = parser.parse_args()
    Data_Cleaner(args.input_file, args.output_file)