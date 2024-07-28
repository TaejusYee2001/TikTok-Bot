import os
import torch
import logging

from src.scraper import RedditScraper
from src.tts import TTS
#from src.background import Download
#from src.subtitles import Subtitles
                        
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

site_url = "https://www.reddit.com/r/AmItheAsshole/"
data_dir = "data"
audio_dir = "audio"
video_dir = "video"
background_dir = "background"

for directory in [data_dir, audio_dir, video_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

#scraper = RedditScraper(site_url)
#scraper.scrape_posts(data_dir)

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(device)
tts.convert_to_audio(os.path.join(data_dir, 'posts_data.json'), audio_dir)

#download_path = "background"
#if not os.path.exists(download_path):
#    os.makedirs(download_path)

#downloader = Download(download_path)
#downloader.download_files_from_dropbox()

#subtitles = Subtitles()
#subtitles.generate_srt_file(audio_dir, data_dir)
#subtitles.overlay_audio(background_dir, audio_dir)
#subtitles.overlay_subtitles("background+audio", data_dir, video_dir)

print("Success!")
