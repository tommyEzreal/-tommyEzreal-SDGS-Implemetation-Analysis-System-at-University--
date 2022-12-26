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

def kangwon_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    driver.get("https://www.kangwon.ac.kr/www/selectBbsNttList.do?bbsNo=21&&pageUnit=10&key=99&pageIndex=1")

    for page_num in range(1, 101):
        for title_num in range(1, 11):
            driver.find_element("xpath", f"""//*[@id="board"]/div[3]/ul[{title_num}]/li/a/div/div/strong""").click()
            
            # 제목
            title = driver.find_element("xpath", """//*[@id="board"]/table/thead/tr/th""")
            title = title.text
            
            # semi-preprocessing_조회수 삭제
            del_index = title.find('\n')

            # 삭제할 부분
            title[del_index:] 
            title = title[:del_index]

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", """//*[@id="board"]/table/tbody/tr/td""")
            content = content.text
            
            # semi-preprocessing_불필요한 문자 삭제
            content = content.replace("\n", "")
            content = content.replace("▲", "")
            content = content.replace("사진 확대보기", "")
            
            contents.append(content)

            driver.back()

        # 페이지 넘기기
        if page_num % 10 == 0:
            driver.find_element("xpath", f"""//*[@id="board"]/div[4]/span[3]/a[2]""").click()
        else:
            driver.find_element("xpath", f"""//*[@id="board"]/div[4]/span[2]/span/a[{(page_num%10)}]""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'kangwon_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    kangwon_crawling(config)