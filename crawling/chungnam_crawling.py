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

def chungnam_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []
    
    driver.get("https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0703&site_dvs_cd=kr&menu_dvs_cd=0703")

    for page_num in range(1, 101):
        for title_num in range(1, 11):
            driver.find_element("xpath", f"""//*[@id="txt"]/div[2]/div[{title_num}]/div/h4/a""").click()
                
            # 제목
            title = driver.find_element("xpath", '//*[@id="txt"]/div[2]/h4')
            title = title.text

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", '//*[@id="txt"]/div[4]')
            content = content.text
            
            # semi-preprocessing_불필요한 문자 삭제
            content = content.replace("\n", "")
            content = content.replace("사진설명 : ", "")
            content = content.replace("사진 설명 : ", "")
            content = content.replace("[사진설명]", "")
            content = content.replace("※ 사진설명 : ", "")
            content = content.replace("※ 사진 설명 : ", "")
            content = content.replace("/* 사진 설명 : ", "")
            
            contents.append(content)

            driver.back()

        # 페이지 넘기기
        if page_num < 11: 
            if page_num == 10:
                driver.find_element("xpath", f"""//*[@id="txt"]/div[4]/p/a[10]""").click()
            else:
                for i in range(1, 10):
                    if page_num % 10 == i:
                        driver.find_element("xpath", f"""//*[@id="txt"]/div[4]/p/a[{page_num}]""").click()
        else : 
            if page_num % 10 == 0:
                driver.find_element("xpath", f"""//*[@id="txt"]/div[4]/p/a[12]""").click()
            else:
                for i in range(1, 10):
                    if page_num % 10 == i:
                        driver.find_element("xpath", f"""//*[@id="txt"]/div[4]/p/a[{i+2}]""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'chungnam_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    chungnam_crawling(config)