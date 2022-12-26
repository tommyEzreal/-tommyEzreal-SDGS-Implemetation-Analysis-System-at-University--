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

def ewha_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []
    
    driver.get("https://www.ewha.ac.kr/ewha/news/ewha-news.do?mode=list&&articleLimit=10&article.offset=0")

    for page_num in range(1, 101):
        for title_num in range(1, 11):   
            # 제목
            title = driver.find_element("xpath", f'//*[@id="jwxe_main_content"]/div/div/div[3]/ul/li[{title_num}]/div[2]/div[1]/a/span')
            title = title.text
            
            title = title.replace('\n',"")
            title = title.replace('\t',"")
            title = title.replace(' N',"")

            titles.append(title)

            # 내용
            content = driver.find_element("xpath", f'//*[@id="jwxe_main_content"]/div/div/div[3]/ul/li[{title_num}]/div[2]/div[2]/a')
            content = content.text
            
            content = content.replace("\n", "")
            content = content.replace("\t","")
            content = content.strip()
            
            contents.append(content)
        
        # 페이지 넘기기 
        if page_num == 1:
            driver.find_element("xpath", """//*[@id="jwxe_main_content"]/div/div/div[4]/div/ul/li[2]/a""").click()
        elif page_num < 6:
            driver.find_element("xpath", f"""//*[@id="jwxe_main_content"]/div/div/div[4]/div/ul/li[{page_num + 3}]/a""").click()
        else:
            driver.find_element("xpath", """//*[@id="jwxe_main_content"]/div/div/div[4]/div/ul/li[9]/a""").click()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'ewha_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    ewha_crawling(config)