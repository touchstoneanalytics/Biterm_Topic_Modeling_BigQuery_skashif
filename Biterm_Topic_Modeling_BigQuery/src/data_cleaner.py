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

        self.output_file_name = output_file_name            
        self.clean_data()
        
    def sentence_to_words(self, sentences):
        for sentence in sentences:
            # convert sentence (string) to list of words ignoring any words
            # that are too small (len 2) or too large (len 15)
            #print(sentence)
            yield (gensim.utils.simple_preprocess(str(sentence)))
        
    def clean_data(self):
        """
        Main function where all the cleaning of code will occur
        """
        # downloading the stop words dictionary
        stop = stopwords.words('english')
        # adding custom words from our datasets that we want to ignore
        stop.extend(['cnet', '-', '|', 'says', '@AppleSupport', '@AmazonHelp'])

        # reading the headlines file
        headlines = pd.read_csv(self.file_path)
        # lower casing all the data
        headlines = headlines.apply(lambda x: x.astype(str).str.lower())
        
        # removing all the stop words
        headlines['article_title_clean'] = headlines['article_title'].apply(lambda x: ' '.join([word for word in x.split() 
                                                                                                if word not in (stop)]))
        headlines['article_title_cleaner'] = list(self.sentence_to_words(headlines['article_title_clean']))
        headlines['article_title_cleaner'] = headlines['article_title_cleaner'].apply(lambda x: ' '.join(x))
        
        sentence_stream = [doc.split(" ") for doc in headlines['article_title_cleaner'].tolist()]
        bigram = Phrases(sentence_stream, min_count=10, threshold=100)
        sentences_with_bigrams = [bigram[sent] for sent in sentence_stream]
        #print(sentences_with_bigrams)
        headlines['article_title_cleanerer'] = [' '.join(sent) for sent in sentences_with_bigrams]
        headlines['article_title_cleanerer'].to_csv(os.path.join(self.dir_path, "../input/" + self.output_file_name), index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Cleaner')
    
    parser.add_argument("-i", dest="input_file", help="Path of the file containing data to be cleaned data", required=True)
    parser.add_argument("-o", dest="output_file", help="Name of the output file that will be generated", required=True)
    
    args = parser.parse_args()
    Data_Cleaner(args.input_file, args.output_file)