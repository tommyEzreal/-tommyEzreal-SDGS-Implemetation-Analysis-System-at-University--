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

def chonnam_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []
    
    driver.get("https://today.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=146")

    for page_num in range(1, 101):
        for title_num in range(1, 20):
            if title_num % 2 == 1:
                driver.find_element("xpath", f"""//*[@id="tbBoard"]/tbody/tr[1]/td/table/tbody/tr/td/div[2]/div[{title_num}]/a/h1""").click()

                # 제목
                title = driver.find_element("xpath", '//*[@id="tbBoard"]/tbody/tr/td/table/tbody/tr[2]/td/div[1]/h1')
                title = title.text
                
                titles.append(title)

                # 내용
                content = driver.find_element("xpath", '//*[@id="tbBoard"]/tbody/tr/td/table/tbody/tr[2]/td/div[1]')
                content = content.text
                
                content = content.replace("\n\n", "")
                content = content.replace("\n", " ")
                
                # semi-preprocessing_취재/ 삭제
                del_index = content.find(']')

                # 삭제할 부분
                content[:del_index] 
                content = content[del_index+1:]

                contents.append(content)

                driver.back()
                
        # 페이지 넘기기
        if page_num % 10 == 0:           
            driver.find_element("xpath", f"""//*[@id="tbBoard"]/tbody/tr[1]/td/table/tbody/tr/td/div[3]/a[4]/img""").click()
        else:
            for i in range(1, 10):
                    if page_num % 10 == i:
                        driver.find_element("xpath", f"""//*[@id="tbBoard"]/tbody/tr[1]/td/table/tbody/tr/td/div[3]/span[{i+1}]""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'chonnam_crawlin.csv')

if __name__ == "__main__":
    config = define_argparser()
    chonnam_crawling(config)