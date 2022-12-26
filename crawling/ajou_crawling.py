import os
import time
import requests
import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from config import define_argparser

def ajou_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    driver.get("https://www.ajou.ac.kr/kr/ajou/news.do?mode=list&&articleLimit=12&article.offset=0")

    for page_num in range(1, 84):
        for title_num in range(1, 13):            
            driver.find_element("xpath", f"""//*[@id="cms-content"]/div/div/div[2]/ul/li[{title_num}]/div[2]/div[1]/a[1]""").click()

            # 제목
            title = driver.find_element("xpath", """//*[@id="cms-content"]/div/div/div[1]/div[1]/div[1]/p/span[2]""")
            time.sleep(0.5)
            title = title.text

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", """//*[@id="cms-content"]/div/div/div[1]/div[1]/div[3]""")
            time.sleep(0.5)
            content = content.text
            
            # semi-preprocessing_불필요한 문자 삭제
            content = content.replace("\n", "")
            content = content.replace("▲", "")

            contents.append(content)

            driver.back()

    # 페이지 넘기기
    if page_num == 1:
        driver.find_element("xpath", f"""//*[@id="cms-content"]/div/div/div[3]/div/ul/li[2]/a""").click()
    elif page_num > 5:
        driver.find_element("xpath", f"""//*[@id="cms-content"]/div/div/div[3]/div/ul/li[9]/a""").click()
    else:
        driver.find_element("xpath", f"""//*[@id="cms-content"]/div/div/div[3]/div/ul/li[{page_num + 3}]/a""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'ajou_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    ajou_crawling(config)