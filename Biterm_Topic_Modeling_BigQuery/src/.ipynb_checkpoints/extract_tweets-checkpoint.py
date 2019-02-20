""" Code to extract tweets for a particular company """

import os
import sys
import pandas as pd

class Tweets_Extractor():
    def __init__(self):
        """
        Checking whether the tweet file exists or not
        """
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(self.dir_path, "../input/tweets.csv")
        if not os.path.isfile(self.file_path):
            print("Input File {} doesn't exist".format(self.file_path))
            sys.exit()

        #df.to_csv(os.path.join(self.dir_path, '../input/headlines.txt'), index=False)
        
    def extract_tweets(self, company_twitter_id):
        """ Function to get tweets for a particular company

    Returns:
        DataFrame: containing the tweets for that particular company
    """
        tweets_df = pd.read_csv(self.file_path)
        print('Total # of tweets: {}'.format(len(tweets_df)))
        print(tweets_df.dtypes)
        
        inbound_tweets = tweets_df.loc[(tweets_df['inbound'] == True) & (tweets_df['in_response_to_tweet_id'].isnull())]
        self.relevant_tweets = inbound_tweets.loc[inbound_tweets['text'].str.contains(company_twitter_id)]
        print('Relevant Number of Tweets: {}'.format(len(self.relevant_tweets)))
    
    def save_tweets(self, output_file_name):
        self.relevant_tweets.to_csv(os.path.join(self.dir_path, '../input/' + output_file_name), index=False)
        
if __name__ == "__main__":
    tw = Tweets_Extractor()
    tw.extract_tweets('@AppleSupport')
    tw.save_tweets('apple_complaints.csv')
    
    #tw.extract_tweets('@AmazonHelp')
    #tw.save_tweets('amazon.csv')