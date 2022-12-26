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

def hufs_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []
    
    driver.get("http://www.hufsnews.co.kr/news/articleList.html?sc_section_code=S1N1&sc_sub_section_code=S2N1&view_type=tm")

    for page_num in range(1, 84):
        for title_num in range(1, 13):
            driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/section/div/div[{title_num}]/div/a""").click()
            
            # 제목
            title = driver.find_element("xpath", """//*[@id="user-container"]/div[3]/header/header/div""")
            title = title.text

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", """//*[@id="article-view-content-div"]""")
            content = content.text
            
            # semi-preprocessing_불필요한 문자 삭제
            content = content.replace("\n", "")
            content = content.replace("■", "")
            content = content.replace("▲", "")
            content = content.replace("\n저작권자 © HUFS NEWS 무단전재 및 재배포 금지\nHUFSNEWS\n다른기사 보기", "")
            
            contents.append(content)

            driver.back()

        # 페이지 넘기기
        if page_num < 11: 
            if page_num == 1:
                driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/div/ul/li[3]/a""").click()
            elif page_num == 10:
                driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/div/ul/li[14]/a/i""").click()
            else:
                driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/div/ul/li[{page_num+3}]/a""").click()
            
        else : 
            if page_num % 10 == 0:
                driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/div/ul/li[15]/a""").click()
            else:
                driver.find_element("xpath", f"""//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/div/ul/li[{(page_num%10)+4}]/a""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'hufs_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    hufs_crawling(config)