# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:01:28 2025

@author: Admin

"""
# 라이브러리
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# 크롬 브라우저 실행
browser = webdriver.Chrome()
url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube'
browser.get(url)

# 페이지 정보 가져오기
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

channel_list = soup.select('form > table > tbody > tr')
channel = channel_list[0]
len(channel_list) # 100

# 카테고리 추출
category = channel.select('p.category')[0].text.strip()   # '[음악/댄스/가수]'

# 채널명 추출
title = channel.select('h1 > a')[0].text.strip()   # 'BLACKPINK'

# 구독자 수 추출
subscriber = channel.select('.subscriber_cnt')[0].text

# View 수 추출
view = channel.select('.view_cnt')[0].text

# 동영상 수 추출
video = channel.select('.video_cnt')[0].text


# --------------------------------------------------------------------

## page url 10개
page = 1
url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page={}'.format(page)
# --------------------------------------------------------------------



# youtube 채널 랭킹 데이터(10 페이지) 크롤링 및 시각화
# 라이브러리
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

browser = webdriver.Chrome()

results = [] # [title, category, subscriber, view, video]

for page in range(1,11):
    url = f'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page={page}'
    browser.get(url)
    
    # 2초 기다리기
    time.sleep(2)
    
    # 페이지 정보 가져오기
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # channel 리스트 추출
    channel_list = soup.select('form > table > tbody > tr')
    
    for channel in channel_list:
        # 채널명 추출
        title = re.sub(r'[^\w\s가-힣]', '', channel.select('h1 > a')[0].text.strip())
        # 카테고리 추출
        category = channel.select('p.category')[0].text.strip()
        # 구독자 수 추출
        subscriber = channel.select('.subscriber_cnt')[0].text
        # View 수 추출
        view = channel.select('.view_cnt')[0].text
        # 동영상 수 추출
        video = channel.select('.video_cnt')[0].text
        
        data = [title, category, subscriber, view, video]
        results.append(data)

# 데이터 칼러몀을 설정하고 엑셀 파일로 저장
df = pd.DataFrame(results)
df.columns = ['title', 'category', 'subscriber', 'view', 'video']
df.to_excel('./files/youtube_rank.xlsx', index = False)


















