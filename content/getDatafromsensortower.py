#  SelectCategory-module__nestedItem--hA_4V css-nl43q0"
#00957146@mail.ntou.edu.tw
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.keys import Keys
# r = requests.get("https://play.google.com/store/games?device=phone&hl=zh-TW")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
def scroll_down(driver):
    for i in range(100):
        driver.find_element(By.ID, 'mainContent').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
try:
    # 打开网页
    driver.get("https://app.sensortower.com/top-charts?category=game&os=android&device=iphone&date=2024-05-02&country=TW")
    input() #login
    button = driver.find_element(By.CLASS_NAME, 'css-14xhkbs')
    button.click()
    time.sleep(1)
    button = driver.find_elements(By.CLASS_NAME, 'SelectCategory-module__expandableItem--smZQP')[1]
    button.click()
    game_category_list = list(range(34,68,2))
    for i in game_category_list:
        print(i)
        game_category = driver.find_elements(By.CLASS_NAME, 'css-1q16mk8')
        button = game_category[i]
        button.click()
        time.sleep(10)

        scroll_down(driver)
        
        elements = driver.find_elements(By.TAG_NAME,'table')
        links = elements[0].find_elements(By.TAG_NAME, 'a')

        # 写入文件
        with open('url.txt', 'a') as f:
            for index, link in enumerate(links):
                if (index + 3) % 4 == 0:
                    href = link.get_attribute('href')
                    if href:
                        f.write(href + '\n')

        button = driver.find_element(By.CLASS_NAME, 'css-14xhkbs')
        button.click()
        time.sleep(2)
finally:
    driver.quit()