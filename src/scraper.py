import os
import time
import json
import random
import string
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class RedditScraper: 
    def __init__(self, url, scrolls=2, pause_time=2):
        print("Initializing WebScraper...")
        self.url = url
        self.scrolls = scrolls
        self.pause_time = pause_time
        self.posts_data = {}

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless=new')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--enable-javascript')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Initialize WebDriver
        try: 
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e: 
            print(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def scrape_posts(self, output_dir):
        try: 
            print(f"Navigating to URL: {self.url}")
            self.driver.get(self.url)
            
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page loaded successfully")
            
            # Browser automation to cache more posts by scrolling
            num_scrolls = 0
            while num_scrolls < self.scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.pause_time + random.uniform(0.5, 1.5))
                
                num_scrolls += 1
                print(f"Completed scroll {num_scrolls}")
                
            # Parse HTML for links to article pages
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            articles = soup.find_all('article', class_='w-full m-0')
            
            print(f"Number of articles found: {len(articles)}")
            
            if not articles:
                print("No articles found. The HTML structure might have changed.")
                return
            
            links = []
            for article in articles:
                shreddit_post = article.find('shreddit-post')
                links.append(shreddit_post.get('content-href'))
            
            # Perform a new fetch on each post link
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
            allowed_chars = set(string.printable)
            for index, link in enumerate(links):
                aita_post_req = requests.get(link, headers=headers)
                aita_post_soup = BeautifulSoup(aita_post_req.content, 'html.parser')
                post_container = aita_post_soup.find('div', class_='text-neutral-content')
                
                if post_container: 
                    div1 = post_container.find('div')
                    div2 = div1.find('div')
                    p_elements = div2.find_all('p')
                    post_text = '\n\n'.join(p.get_text(strip=True) for p in p_elements)  # Concatenate text
                    post_text = ''.join(filter(lambda x: x in allowed_chars, post_text))
                    self.posts_data[index] = {'text': post_text}
                    
            # Write text data to json file
            file_path = os.path.join(output_dir, 'posts_data.json')
            with open(file_path, 'w') as json_file:
                json.dump(self.posts_data, json_file, indent=4)
            
            print(f"Saved article text to {file_path}")

        except Exception as e:
            print(f"An error occurred during scraping: {str(e)}")
            raise
        finally:
            self.driver.quit()
            print("WebDriver closed")

        return len(articles)