from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait


edge_options = Options()
# 使用无头模式
edge_options.add_argument('--headless')
# 禁用GPU，防止无头模式出现莫名的BUG
edge_options.add_argument('--disable-gpu')
driver = webdriver.Edge(options=edge_options)
url = input("输入url网址:   ")
driver.get(url)
try:
    # 等待页面中的元素加载完毕，这里设置了10秒的等待时间
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    content = driver.find_element(By.XPATH, '//*[@class="article"]').text  # 提取内容

    print("内容:", content)

except TimeoutException:
    print("加载页面元素超时")
finally:
    # 关闭浏览器
    driver.quit()
