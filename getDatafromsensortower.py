from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(600,1080)
try:
    # 打开网页
    driver.get("https://app.sensortower.com/top-charts?country=TW&category=all&date=2024-04-13&device=iphone&os=android")
    input()
    elements = driver.find_elements(By.TAG_NAME,'table')
    # print(len(elements))
    links = elements[0].find_elements(By.TAG_NAME, 'a')
    count = 0

    # 写入文件
    with open('topgrossing.txt', 'w') as f:
        for link in links:
            if count >= 100:
                break

            href = link.get_attribute('href')
            if href:
                f.write(href + '\n')
                count += 1

finally:
    # 关闭浏览器
    driver.quit()