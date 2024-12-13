# TikTok-Bot
Welcome to the new project!

## 🤖 Social Media Automation Tool
Developers: Calvin Yee, Taejus Yee

Technologies: Python, Selenium, BeautifulSoup, FFmpeg, Docker, OpenAI (Whisper)

## 🚀 Project Overview
This Social Media Automation Tool automates the process of web scraping, TTS conversion, and subtitle generation, aimed at enhancing the accessibility and content delivery for social media platforms like Reddit. The tool can efficiently bypass anti-bot protocols, scrape data, and create customizable voiceovers, while leveraging AI to streamline subtitle creation.

## 🛠️ Features
### Automated Web Scraping:
Utilizes Selenium and BeautifulSoup to scrape Reddit posts while bypassing anti-bot mechanisms using browser automation techniques.

### Text-to-Speech (TTS) Integration:
Supports multiple TTS Options, originally using the free version of 11Labs, then moving to the TTS and gtts libraries.

### AI-Driven Subtitle Generation:
Uses OpenAI's Whisper model to automatically generate subtitle files from TTS audio. 

### Optimized Subtitle Preprocessing:
Improved text preprocessing pipelines, decreasing hallucination rates in Whisper model outputs.


## 🛠️ Technologies Used
Python: Core scripting language used for web scraping, API integration, and subtitle processing.
Selenium & BeautifulSoup: For automating the web scraping process and parsing HTML data.
FFmpeg: For handling and processing audio/video files.
Docker: To containerize the application, ensuring smooth deployments across different environments.
OpenAI Whisper: AI model for converting TTS-generated audio into accurate subtitle files.

## 💡 How It Works
Web Scraping: The tool launches a browser instance using Selenium and collects Reddit posts, bypassing any anti-bot measures using browser-based automation.
Text-to-Speech Conversion: It then sends the scraped data to the text-to-speech modules, producing audio mp3 files. 
Subtitle Generation: The tool employs OpenAI's Whisper model to infer subtitles from the TTS-generated audio, ensuring accurate and timely captioning in the form of .srt subtitles. 
Optimization: Text preprocessing pipelines optimize the subtitle creation process by reducing interpolation times and minimizing hallucination errors, helping adapt Reddit posting formats to social-media appropriate content. 
