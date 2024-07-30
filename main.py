import os
#import torch

#from src.scraper import RedditScraper
#from src.tts import TTS
from src.download import Download
#from src.subtitles import Subtitles
                        
print("Starting the application")

site_url = "https://www.reddit.com/r/AmItheAsshole/"
data_dir = "data/text"
srt_files_dir = "data/text/srt_files"
audio_dir = "data/audio"
video_dir = "data/video"
raw_background_dir = "background/raw"
overlaid_background_dir = "background/audio_overlaid"

for directory in [
    data_dir, 
    audio_dir, 
    video_dir, 
    raw_background_dir, 
    overlaid_background_dir, 
    srt_files_dir
]:
    if not os.path.exists(directory):
        os.makedirs(directory)

#scraper = RedditScraper(site_url)
#scraper.scrape_posts(data_dir)

#device = "cuda" if torch.cuda.is_available() else "cpu"
#tts = TTS(device)
#tts.convert_to_audio(os.path.join(data_dir, 'posts_data.json'), audio_dir)

download_path = "background"
if not os.path.exists(download_path):
    os.makedirs(download_path)

downloader = Download(download_path)

id = 'hxxhhbo5xnmuezt'
secret = 'c9nqi9kd41zc2x1'
refresh = 'XQVWVuGGTxoAAAAAAAAAAcalkCxpBqmHsuXlv5u2BM9c_C5BGmz7UCZiA8-6pOci'

access_token = downloader.refresh_access_token(refresh_token= refresh, client_id= id, client_secret= secret )
downloader.download_files_from_dropbox(access_token = access_token)

#subtitles = Subtitles()
#subtitles.generate_srt_file(audio_dir, srt_files_dir)
#subtitles.overlay_audio(raw_background_dir, audio_dir, overlaid_background_dir)
#subtitles.overlay_subtitles(overlaid_background_dir, data_dir, video_dir)

print("Success!")
