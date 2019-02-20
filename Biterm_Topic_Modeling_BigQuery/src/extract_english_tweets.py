""" Code to clean headlines so that it can be used
    as input for the biterm algorithm """
import os
import sys
import pandas as pd
from langdetect import detect

if __name__ == "__main__":

    # reading the tweets file
    tweets = pd.read_csv("/mnt/input/apple_complaints.csv", usecols = ['text'], encoding='utf-8')
    
    # lower casing all the data
    tweets = tweets.apply(lambda x: x.astype(str).str.lower())

    english_tweets = []
    for index, row in tweets.iterrows():
        try:
            language = detect(row['text'])
        except:
            language = "error"

        if language == 'en':
            english_tweets.append(row['text'])
    
    
    english_tweets_df = pd.DataFrame(english_tweets, columns=['text'])
    print('No of English tweets: {}'. format(len(english_tweets_df)))

    english_tweets_df.to_csv('/mnt/input/apple_complaints_english.csv', index=False)
