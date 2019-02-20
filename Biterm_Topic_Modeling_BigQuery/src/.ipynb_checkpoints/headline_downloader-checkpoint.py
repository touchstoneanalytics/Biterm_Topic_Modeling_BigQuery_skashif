""" Code to download headlines from Bigquery Dataset """

from google.cloud import bigquery
import os
import sys
import pandas

class Headline_Downloader():
    def __init__(self):
        """
        Setting the path for the Bigquery Access file
        and checking that it exists
        """
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.key_path = os.path.join(self.dir_path, "../input/bigquery_access.json")
        if not os.path.isfile(self.key_path):
            print("Bigquery Service Account File {} doesn't exist".format(self.key_path))
            sys.exit()

        df = self.download_headlines()
        df.to_csv(os.path.join(self.dir_path, '../input/headlines.txt'), index=False)
        
    def download_headlines(self):
        """ Function to get headlines from big query table

    Returns:
        DataFrame: containing the headlines for all the news
    """
        return pandas.read_gbq(
            "SELECT article_title FROM `sandbox-211511.Rss_Dataset.rss_articles` where rss_link in ('https://www.technologyreview.com/stories.rss', 'https://www.techradar.com/rss/news/computing', 'https://www.theverge.com/tech/rss/index.xml', 'http://feeds.feedburner.com/TechCrunchIT', 'http://feeds.mashable.com/Mashable', 'https://www.cnet.com/rss/news/')",
            project_id="sandbox-211511",
            private_key=self.key_path,
            dialect="standard"
        )
    
if __name__ == "__main__":
    Headline_Downloader()