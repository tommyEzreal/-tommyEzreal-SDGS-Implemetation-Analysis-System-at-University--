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

def jeju_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []
    
    driver.get("https://jnuhongbo.jejunu.ac.kr/boards/hongbo_jnunews")

    for page_num in range(1, 67):
        for title_num in range(1, 16):
            driver.find_element("xpath", f"""//*[@id="board"]/ul/li[{title_num}]/div[3]/a/span""").click()

            # 제목
            title = driver.find_element("xpath", """//*[@id="board"]/table/tbody/tr[1]/td""")
            title = title.text

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", """//*[@id="board"]/table/tbody/tr[3]/td""")
            content = content.text
            
            content = content.replace("\n", "")

            contents.append(content)

            driver.back()

        # 페이지 넘기기
        if page_num < 8:
            driver.find_element("xpath", f"""//*[@id="board"]/div/ul/li[{page_num+2}]/a""").click()
        else:
            driver.find_element("xpath", f"""//*[@id="board"]/div/ul/li[9]/a""").click()
        
    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'jeju_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    jeju_crawling(config)