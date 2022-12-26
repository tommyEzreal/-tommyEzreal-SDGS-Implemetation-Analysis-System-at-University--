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

def kyunghee_crawling(config):

    path = config.load_chromedriver_path
    driver = webdriver.Chrome(path)
    
    titles = []
    contents = []

    for page_num in range(1, 201):
        
        driver.get(f"https://www.khu.ac.kr/kor/focus/list.do?page={page_num}&pageSize=5")
        time.sleep(2)
        
        for click_num in range(1, 6):
            driver.find_element("xpath", f"""//*[@id="contents"]/ul[1]/li[{click_num}]/div[2]/a""").click()
            
            time.sleep(2)
            
            # 제목
            title = driver.find_element("xpath", '//*[@id="printArea"]/div/div[1]/h4')
            titles.append(title)
            
            # 내용
            content = driver.find_element("xpath", '//*[@id="printArea"]/div/div[2]')
            driver.implicitly_wait(1)
            
            content = content.text
            
            # semi-preprocessing_불필요한 문자 삭제
            content = content.replace("\n", "")
            content = content.replace("ⓒ 경희대학교 커뮤니케이션센터 communication@khu.ac.kr", "")
            
            # semi-preprocessing_글/사진/영상+이름+이메일 삭제
            del_index = content.find('글 ')

            # 삭제할 부분
            content[del_index:] 
            content = content[:del_index]

            contents.append(content)
            
            driver.back()

    # 데이터프레임 생성
    list_sum = list(zip(titles, contents))    
    col = ["제목", "내용"]
    df = pd.DataFrame(list_sum, columns=col)

    # csv 파일로 내보내기
    df.to_csv(config.save_path, 'kyunghee_crawling.csv')

if __name__ == "__main__":
    config = define_argparser()
    kyunghee_crawling(config)