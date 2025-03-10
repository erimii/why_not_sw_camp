# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:01:00 2025

@author: Admin
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()
url1 = 'http://www.genie.co.kr/chart/top200' # 50까지
driver.get(url1)
html1 = driver.page_source

url2 = 'https://www.genie.co.kr/chart/top200?ditc=D&ymd=20250218&hh=11&rtm=Y&pg=2' # 51~100 까지
driver.get(url2)
html2 = driver.page_source

soup1 = BeautifulSoup(html1, 'html.parser')
soup2 = BeautifulSoup(html2, 'html.parser')

# 곡과 가수명을 song_data에 저장
song_data = []

songs1 = soup1.select('table > tbody> tr')
songs2 = soup2.select('table > tbody> tr')

rank = 1

for song in songs1:
    title = song.select('td.info > a.title')[0].text.strip()
    singer = song.select('td.info > a.artist')[0].text
    song_data.append(['Genie', rank, title, singer])
    rank += 1

for song in songs2:
    title = song.select('td.info > a.title')[0].text.strip()
    singer = song.select('td.info > a.artist')[0].text
    song_data.append(['Genie', rank, title, singer])
    rank += 1

song_data[4]    # ['Genie', 5, 'Whiplash', 'aespa']

# song_data로 데이터프레임 만들기
columns = ['서비스', '순위', '타이틀', '가수']
pd_data = pd.DataFrame(song_data, columns = columns)

# 엑셀 파일에 저장
pd_data.to_excel('./files/genie.xlsx', index = False)




