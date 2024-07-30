import os
import ffmpeg
import random
import whisper
import logging
import subprocess

class Subtitles: 
    def __init__(self): 
        self.model = whisper.load_model('base', in_memory=True)
        print("Whisper model loaded successfully.")
        
    def seconds_to_srt_time(self, seconds):
        millisec = int((seconds - int(seconds)) * 1000)
        time_str = f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02},{millisec:03}"
        return time_str

    def generate_srt_file(self, audio_dir, data_dir):
        audio_files = sorted(os.listdir(audio_dir))
        for index, file in enumerate(audio_files):
            file_path = os.path.join(audio_dir, file)
            print(f"Processing audio file: {file_path}")
            transcript_dict = self.model.transcribe(word_timestamps=True, audio=file_path)
            print(f"Transcription completed for: {file_path}")

            srt_content = ""
            counter = 1
            for segment in transcript_dict['segments']:
                for word in segment['words']: 
                    start_time = self.seconds_to_srt_time(word['start'])
                    end_time = self.seconds_to_srt_time(word['end'])
                    text = word['word']
                    srt_content += f"{counter}\n{start_time} --> {end_time}\n{text.strip()}\n\n"
                    counter += 1
            
            srt_file_path = os.path.join(data_dir, f"{index}.srt")
            with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt_content)
            print(f"SRT file created at: {srt_file_path}")

    def overlay_audio(self, raw_background_dir, audio_dir, output_dir):
        num_raw_background = len(os.listdir(raw_background_dir))
        for index, _ in enumerate(os.listdir(audio_dir)):
            background_index = random.randint(0, num_raw_background - 1)
            background_video = f"{raw_background_dir}/{background_index}.mp4"
            audio_file = f"{audio_dir}/{index}.wav"
            overlaid_background_video = f"{output_dir}/{index}.mp4"
            
            add_audio_command = [
                'ffmpeg',
                '-i', background_video,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',  # You can change this to 'copy' if you want to keep the original audio codec
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-y',
                overlaid_background_video
            ]
            try:
                add_audio_result = subprocess.run(add_audio_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"Video with audio created at: {overlaid_background_video}")
                print(add_audio_result.stdout)
                print(add_audio_result.stderr)
            except subprocess.CalledProcessError as e:
                print(f"Failed to overlay audio: {e.stderr}")
                
    def overlay_subtitles(self, background_dir, data_dir, video_dir):
        for index, file in enumerate(os.listdir(background_dir)):
            background_video = f"{background_dir}/{index}.mp4"
            subtitles_file = f"{data_dir}/srt_files/{index}.srt"
            subtitled_video_file = f"{video_dir}/{index}.mp4"
            
            add_subtitles_command = [
                'ffmpeg',
                '-i', background_video,
                '-vf', f"subtitles={subtitles_file}:force_style='FontName=Arial,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=3'", # TODO: format 
                '-c:a', 'copy',
                '-y',
                subtitled_video_file
            ]
            
            try:
                add_subtitles_result = subprocess.run(add_subtitles_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"Subtitled video created at: {subtitled_video_file}")
                print(add_subtitles_result.stdout)
                print(add_subtitles_result.stderr)
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to overlay subtitles: {e.stderr}")
            