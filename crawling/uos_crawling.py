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

def uos_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    for page_num in range(33):
        url = f'https://www.uos.ac.kr/korColumn/list.do?list_id=about02&seq=0&sort=&pageIndex={page_num}&searchCnd=&searchWrd=&viewAuth=Y&lpageCount=10&menuid=2000001009005000000'
        response = requests.get(url)
        response = BeautifulSoup(response.text, 'html.parser')
        
        # 제목
        html_title = response.find_all("div", class_="ti")
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
    df.to_csv(config.save_path, 'uos_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    uos_crawling(config)