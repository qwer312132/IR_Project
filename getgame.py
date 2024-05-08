from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import requests
from bs4 import BeautifulSoup

# Specify the path to the Chrome driver executable
chromedriver = '/usr/bin/chromedriver'

# Create an instance of Options
options = Options()

# Add any desired options here, for example:
# options.add_argument("--headless")  # Run Chrome in headless mode

# Initialize the Chrome driver service
service = Service(chromedriver)

# Pass the service and options to the Chrome webdriver constructor
driver = webdriver.Chrome(service=service, options=options)

category = "https://play.google.com/store/apps/category/"

cateList = ["GAME_CASUAL", "GAME_ROLE_PLAYING", "GAME_ADVENTURE", "GAME_WORD", "GAME_MUSIC", "GAME_PUZZLE", "GAME_CARD", "GAME_ACTION", "GAME_EDUCATIONAL", "GAME_CASINO", "GAME_BOARD", "GAME_STRATEGY", "GAME_ARCADE", "GAME_TRIVIA", "GAME_SIMULATION", "GAME_RACING", "GAME_SPORTS"]


# for cateName in cateList[0]:
# driver open http---------------------------------------------------------------------
driver.get(category + cateList[0] + "?hl=zh-tw")

# 先找到包含滾動區域的父元素
scroll_area = driver.find_element(By.XPATH, "//*[@id='yDmH0d']/c-wiz[2]/div/div/div[1]")

# 遍歷所有的 i.google-material-icons.B1yxdb 元素
icons = scroll_area.find_elements(By.CSS_SELECTOR, 'i.google-material-icons.B1yxdb')
for icon in icons:
    try:
        # 等待元素可見
        WebDriverWait(driver, 10).until(EC.visibility_of(icon))
        
        # 點擊元素
        icon.click()
        
        # 取得當前頁面的HTML代碼
        page_source = driver.page_source
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(page_source, "html.parser")
        
        # 取得所有的 <div class="Epkrse">
        divs = soup.find_all('div', class_='Epkrse')
        for div in divs:
            print(div.text)

        # 處理divs...
    except TimeoutException:
        print("Element is not visible within the specified time.")

    # 关闭WebDriver
driver.quit()

   


# # 點擊查看所有評論
# see = driver.find_element(by = By.XPATH, value = '//c-wiz/section/div/div/div/div/div/button')
# see.click()



# for i in range(50):
#     iframe = driver.find_element(By.CSS_SELECTOR, "div[class='odk6He']")
#     scroll_origin = ScrollOrigin.from_element(iframe)
#     ActionChains(driver)\
#         .scroll_from_origin(scroll_origin, 0, 1000000000)\
#         .perform()
#     sleep(1)

# post_details = []
# pageSource = driver.page_source
# soup = BeautifulSoup(pageSource, "lxml")
# results = soup.find_all('div', class_='RHo1pe')
# for result in results:
#     name = result.find('div', class_ = 'X5PpBb').text.strip()
#     comment = result.find('div', class_ = 'h3YV2d')
#     if comment != None:
#         comment = comment.text.strip()
#     else:
#         comment = 'None'
#     reply = result.find('div', class_ = 'ras4vb')
#     if reply != None:
#         reply = reply.text.strip()
#     else:
#         reply = 'None'
    
#     post_dict = {
#         'name': name,
#         'comment': comment,
#         'reply': reply
#     }
    
#     # Add the dictionary to the list
#     post_details.append(post_dict)

# # 關閉瀏覽器
# # driver.close() 

# print(len(post_details))

# import json

# # Convert the list to JSON
# json_output = json.dumps(post_details, ensure_ascii=False)

# # Print the JSON output
# with open('gamecomment.json', 'w', encoding='utf-8') as f:
#     json.dump(post_details, f, ensure_ascii=False, indent=4)