import os
import json
from TTS.api import TTS as text_to_speech

class TTS: 
    def __init__(self, device):
        self.device = device
        self.tts = text_to_speech("tts_models/en/ljspeech/fast_pitch", False).to(device)
        
    def convert_to_audio(self, posts_data, audio_dir):
        with open(posts_data, 'r') as file:
            data = json.load(file)
            
        if not os.path.exists(audio_dir):
            os.makedir(audio_dir)

        for key, value in data.items():
            text = value['text']
            audio_path = os.path.join(audio_dir, f"{key}.wav")
            
            self.tts.tts_to_file(text=text, file_path=audio_path)
 