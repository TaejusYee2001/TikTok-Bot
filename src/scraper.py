import os
import random
import time
import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

# Specify Chrome webdriver options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create UserAgent with random user agent string
ua = UserAgent()
user_agent = ua.random
chrome_options.add_argument(f"user-agent={user_agent}")

# Initialize WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://www.reddit.com/r/AmItheAsshole/'
driver.get(url)

# Browser automation to cache more posts by scrolling to bottom of page
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

num_scrolls = 0
while(num_scrolls < 5): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME + random.uniform(0.5, 1.5))
    
    # Update Scroll heights
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    num_scrolls += 1
    
    # Random mouse movement to simulate human behavior
    action = ActionChains(driver)
    action.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()

# Parse HTML for links to article pages
soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article', class_='w-full m-0')

print(f"Number of articles found: {len(articles)}")

links = []
for article in articles:
    shreddit_post = article.find('shreddit-post')
    links.append(shreddit_post.get('content-href'))
    
# Perform a new fetch on each post link
posts_data = {}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
for index, link in enumerate(links):
    aita_post_req = requests.get(link, headers=headers)
    aita_post_soup = BeautifulSoup(aita_post_req.content, 'html.parser')
    post_container = aita_post_soup.find('div', class_='text-neutral-content')
    
    if post_container: 
        div1 = post_container.find('div')
        div2 = div1.find('div')
        p_elements = div2.find_all('p')
        post_text = '\n\n'.join(p.get_text(strip=True) for p in p_elements) # Concatenate text
        
        posts_data[index] = {'id': index, 'text': post_text}

directory = 'data'
file_path = os.path.join(directory, 'posts_data.json')

if not os.path.exists(directory): 
    os.makedirs(directory)
    
with open('data/posts_data.json', 'w') as json_file: 
    json.dump(posts_data, json_file, indent=4)
    
print("Hello World")
