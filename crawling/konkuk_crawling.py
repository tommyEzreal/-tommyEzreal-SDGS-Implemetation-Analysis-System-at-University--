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

def konkuk_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    driver.get("https://popkon.konkuk.ac.kr/news/articleList.html?sc_sub_section_code=S2N1&view_type=sm")

    for page_num in range(1, 45):
        for title_num in range(1, 21):
            try:
                driver.find_element("xpath", f"""//*[@id="section-list"]/ul/li[{title_num}]/div/h4/a""").click()
            except:
                driver.find_element("xpath", f"""//*[@id="section-list"]/ul/li[{title_num}]/h4/a""").click()
                
            # 제목
            title = driver.find_element("xpath", """//*[@id="article-view"]/div/header/h3""")
            title = title.text

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", """//*[@id="article-view-content-div"]""")
            content = content.text
            
            contents.append(content)

            driver.back()

        # 페이지 넘기기
        if page_num < 11: 
            if page_num == 1:
                driver.find_element("xpath", f"""//*[@id="sections"]/section/nav/ul/li[3]/a""").click()
            elif page_num == 10:
                driver.find_element("xpath", f"""//*[@id="sections"]/section/nav/ul/li[14]/a""").click()
            else:
                driver.find_element("xpath", f"""//*[@id="sections"]/section/nav/ul/li[{page_num+3}]/a""").click()
            
        else : 
            if page_num % 10 == 0:
                driver.find_element("xpath", f"""//*[@id="sections"]/section/nav/ul/li[15]/a""").click()
            else:
                driver.find_element("xpath", f"""//*[@id="sections"]/section/nav/ul/li[{(page_num%10)+4}]/a""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'konkuk_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    konkuk_crawling(config)