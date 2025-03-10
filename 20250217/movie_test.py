# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:23:50 2025

@author: Admin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# 변수 저장
stock_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94'

res = requests.get(stock_url)
soup = BeautifulSoup(res.text, 'html.parser')

rows = soup.find_all('div', class_='data_box')


for i in range(0, len(rows)):
    movie_cells = rows[i].find_all('a')
    movie = movie_cells[0].text
    rank_cells = rows[i].find_all('span')
    rank = rank_cells[1].text
    print(movie, rank)




















