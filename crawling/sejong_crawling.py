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

def sejong_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    driver.get("http://www.sejongpr.ac.kr/sejongnewspaperlist.do?boardType=2")

    for i in range(1, 101):
        for page_num in range(1, 11):
            driver.find_element("xpath", f"""//*[@id="container"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/a[{page_num}]/span""").click()

            for title_num in range(1, 11):
                driver.find_element("xpath", f"""//*[@id="container"]/div[2]/div[2]/div/div[2]/div/div[2]/form[2]/div/div[{title_num}]/div/div[2]/div[1]/a""").click()
                time.sleep(2)
                
                # 제목
                title = driver.find_element("xpath", '//*[@id="container"]/div[2]/div[2]/div/div[2]/form[1]/div/div[2]/div[1]/div[1]/div/div[1]/div')
                title = title.text
                
                titles.append(title)
                
                # 내용
                content = driver.find_element("xpath", '//*[@id="container"]/div[2]/div[2]/div/div[2]/form[1]/div/div[2]/div[1]/div[2]/div[2]')
                driver.implicitly_wait(1)

                content = content.text
                
                # semi-preprocessing_불필요한 문자 삭제
                content = content.replace("\n", "")
                content = content.replace("▲", "")
                content = content.replace("△", "")

                # semi-preprocessing_취재/ 삭제
                del_index = content.find('취재/')

                # 삭제할 부분
                content[del_index:] 
                content = content[:del_index]

                contents.append(content)

                driver.back()

            # 페이지 넘기기
            if page_num % 10 == 0 :
                driver.find_element("xpath", f"""//*[@id="container"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[3]/a[1]/span""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'sejong_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    sejong_crawling(config)