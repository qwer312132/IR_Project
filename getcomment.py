from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from time import sleep
import json
# Specify the path to the Chrome driver executable
chromedriver = '/usr/bin/chromedriver'

# Create an instance of Options
options = Options()
# options.add_argument('--headless')
# options.add_argument('--user-agent=%s' % user_agent)

# Add any desired options here, for example:
# options.add_argument("--headless")  # Run Chrome in headless mode

# Initialize the Chrome driver service
service = Service(chromedriver)

# Pass the service and options to the Chrome webdriver constructor
driver = webdriver.Chrome(service=service, options=options)


# driver open http---------------------------------------------------------------------
driver.get('https://play.google.com/store/apps/details?id=com.gamania.lineagem&hl=zh-TW')
# # print(pageSource)
# # # 關閉瀏覽器
# driver.close() 

# def click_text(obj):
# #尋找「查看所有評論」的字串並點擊
#     try:
#         obj.find_element_by_xpath("//span[contains(text(),'查看所有評論')]").click()       
#     except:
#         pass

# move = driver.find_element_by_tag_name('body')
# click_text(move)

# 點擊查看所有評論
# sees = driver.find_element(by=By.CSS_SELECTOR, value="button")
# see = driver.find_element(by = By.CSS_SELECTOR, value = 'span[class="VfPpkd-vQzf8d"][jsname="V67aGc"][text()="查看所有評論"]')
see = driver.find_element(by = By.XPATH, value = '//c-wiz/section/div/div/div/div/div/button')
see.click()

# reviews = driver.find_element(by = By.CSS_SELECTOR, value = 'div[class='']')

# # 取得網頁原始碼
# driver.find_element_by_xpath("//span[contains(text(),'查看所有評論')]").click() 
# # for ranking in rankings:
#     if rankings.aria-label == "營收最高的項目":
#         ranking.click()   # 點擊登入按鈕d
#         print("切換到營收最高的項目")
# D3Qfie VfPpkd-ksKsZd-XxIAqe kofMvc EFMXQ VfPpkd-ksKsZd-mWPk3d

import requests
from bs4 import BeautifulSoup

# # # # tag = input("請輸入定位元素，class前面加上.，id前面加上# ")
# # # res = requests.get('https://play.google.com/store/games?hl=zh_TW&gl=US')
for i in range(50):
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

print(len(post_details))

# Convert the list to JSON
json_output = json.dumps(post_details, ensure_ascii=False)

# Print the JSON output
with open('gamecomment.json', 'w', encoding='utf-8') as f:
    json.dump(post_details, f, ensure_ascii=False, indent=4)