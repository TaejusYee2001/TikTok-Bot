import random
import time
from selenium import webdriver
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
    

print("Hello World")
