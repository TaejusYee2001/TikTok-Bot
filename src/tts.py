import os
import re
import json
import string
import logging
from TTS.api import TTS as text_to_speech

class TTS: 
    def __init__(self, device):
        self.device = device
        self.tts = text_to_speech("tts_models/en/ljspeech/fast_pitch", False).to(device)
        
    def preprocess_text(self, text):
        # Expand contractions (simple example)
        contractions = {
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            # Add more contractions as needed
        }
        for contraction, expanded in contractions.items():
            text = text.replace(contraction, expanded)

        # Replace special characters or emojis if necessary
        # You may choose to remove or handle them differently depending on your model's capability
        text = re.sub(r'[^\w\s.,!?]', '', text)  # Keep alphanumeric characters, spaces, and basic punctuation

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text
        
    def convert_to_audio(self, posts_data, audio_dir):
        with open(posts_data, 'r') as file:
            data = json.load(file)

        for key, value in data.items():
            text = value['text']
            text = self.preprocess_text(text)
            print(text)
            
            #audio_path = os.path.join(audio_dir, f"{key}.wav")
            
            #try:
            #    self.tts.tts_to_file(text=text, file_path=audio_path)
            #except Exception as e:
            #    print(f"Error processing text for key {key}: {e}")
 