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

def pusan_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    for page_num in range(51):
        url = f'https://www.pusan.ac.kr/kor/CMS/Board/Board.do?robot=Y&mCode=MN109&mgr_seq=12&page={page_num}'
        response = requests.get(url)
        response = BeautifulSoup(response.text, 'html.parser')
        
        # 제목
        html_title = response.find_all("span", class_="tit-main")
        # 내용
        html_contents = response.find_all("p", class_="inf")
        
        for i in html_title:
            titles.append(i.get_text().strip())
        for i in html_contents:
            contents.append(i.get_text().replace(u'\xa0', u'').lstrip('- '))
    
    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'pusan_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    pusan_crawling(config)