from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from time import sleep
import json
# Specify the path to the Chrome driver executable
chromedriver = 'D:\\Users\\ntou-nlp\\Downloads\\chromedriver-win64\\chromedriver.exe'


# Create an instance of Options
options = Options()

# Add any desired options here, for example:
# options.add_argument("--headless")  # Run Chrome in headless mode

# Initialize the Chrome driver service
service = Service(chromedriver)

# Pass the service and options to the Chrome webdriver constructor
driver = webdriver.Chrome(service=service, options=options)


# driver open http---------------------------------------------------------------------
driver.get('https://play.google.com/store/apps/details?id=com.gamania.lineagem&hl=zh-TW')


# 點擊查看所有評論
see = driver.find_element(by = By.XPATH, value = '//c-wiz/section/div/div/div/div/div/button')
see.click()

import requests
from bs4 import BeautifulSoup

for i in range(500):
    iframe = driver.find_element(By.CSS_SELECTOR, "div[class='odk6He']")
    scroll_origin = ScrollOrigin.from_element(iframe)
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 1000000000)\
        .perform()
    sleep(1)

post_details = []
pageSource = driver.page_source
soup = BeautifulSoup(pageSource, "lxml")
results = soup.find_all('div', class_='RHo1pe')
for result in results:
    name = result.find('div', class_ = 'X5PpBb').text.strip()
    comment = result.find('div', class_ = 'h3YV2d')
    if comment != None:
        comment = comment.text.strip()
    else:
        comment = 'None'
    reply = result.find('div', class_ = 'ras4vb')
    if reply != None:
        reply = reply.text.strip()
    else:
        reply = 'None'
    
    post_dict = {
        'name': name,
        'comment': comment,
        'reply': reply
    }
    
    # Add the dictionary to the list
    post_details.append(post_dict)

# 關閉瀏覽器
# driver.close() 

print(len(post_details))

# Convert the list to JSON
json_output = json.dumps(post_details, ensure_ascii=False)

# Print the JSON output
with open('gamecomment.json', 'w', encoding='utf-8') as f:
    json.dump(post_details, f, ensure_ascii=False, indent=4)