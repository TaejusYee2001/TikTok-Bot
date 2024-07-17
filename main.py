import os
import logging

from src.scraper import RedditScraper
                        
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

site_url = "https://www.reddit.com/r/AmItheAsshole/"
data_dir = "data"
audio_dir = "audio"
video_dir = "video"

for directory in [data_dir, audio_dir, video_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

scraper = RedditScraper(site_url)
scraper.scrape_posts(data_dir)

print("Success!")
