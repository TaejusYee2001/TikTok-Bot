import os 
import glob

data_dir = "../data/text"
srt_files_dir = "../data/text/srt_files"
audio_dir = "../data/audio"
video_dir = "../data/video"
raw_background_dir = "../background/raw"
overlaid_background_dir = "../background/audio_overlaid"

for directory in [
    data_dir, 
    audio_dir, 
    video_dir, 
    raw_background_dir, 
    overlaid_background_dir, 
    srt_files_dir
]:
    files = glob.glob(os.path.join(directory, '*'))
    for file in files:
        try:
            if os.path.isfile(file): 
                os.remove(file)
                print(f"Removed file: {file}")
        except Exception as e: 
            print(f"Failed to delete {file}. Reason: {e}")