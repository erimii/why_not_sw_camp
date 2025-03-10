# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:00:26 2025

@author: Admin

MelOn_Crawling -> Excel 파일로 저장
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()
url = 'http://www.melon.com/chart/index.htm'
driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

# 곡과 가수명을 song_data에 저장
song_data = []

rank = 1

songs = soup.select('table > tbody> tr')
len(songs) # 100

for song in songs:
    title = song.select('div.rank01 > span > a')[0].text
    singer = song.select('div.rank02 > span > a')[0].text
    
    song_data.append(['Melon', rank, title, singer])
    rank += 1

song_data[4]    # ['Melon', 5, 'APT.', '로제 (ROSÉ)']

# song_data로 데이터프레임 만들기
columns = ['서비스', '순위', '타이틀', '가수']
pd_data = pd.DataFrame(song_data, columns = columns)

# 엑셀 파일에 저장
pd_data.to_excel('./files/melon.xlsx', index = False)





































