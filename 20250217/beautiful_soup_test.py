# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:02:38 2025

@author: Admin
"""

# 웹 스크래핑을 하기 위한 HTTP 요청에 사용할 리퀘스트
# HTML 구조 파싱에 사용할 뷰티풀수프 라이브러리

import requests
from bs4 import BeautifulSoup

'''
1. BeautifulSoup(읽은 html 문자열, 파싱하는 parser)
    파싱하는 parser: html / xml
2. BeautifulSoup 객체를 변수에 저장.
    BeautifulSoup 객체의 함수를 이용하여 데이터 추출 가능
'''

# 문자열을 줄바꿈해서 변수에 할당 하고자 할 때 """ """ 사용
html = '''
<html>
    <body>
        <h1 id='title'>파이썬 데이터 분석가 되기</h1>
        <p id='body'>오늘의 주제는 웹 데이터 수집</p>
        <p class='scraping'>삼성전자 일별 시세 불러오기</p>
        <p class='scraping'>이해 쏙쏙</p>
    </body>
</html>
'''

# html.parser로 앞에서 입력한 HTML 코드를 파싱하여 그 결과를 soup에 저장
soup = BeautifulSoup(html, 'html.parser')
soup
'''
<html>
<body>
<h1 id="title">파이썬 데이터 분석가 되기</h1>
<p id="body">오늘의 주제는 웹 데이터 수집</p>
<p class="scraping">삼성전자 일별 시세 불러오기</p>
<p class="scraping">이해 쏙쏙</p>
</body>
</html>
'''
# html은 단순 문자열임
# soup은 각각의 요소 기능을 갖는 html 문서

# 텍스트 추출: .soup.stripped_strings
for stripped_text in soup.stripped_strings:
    print(stripped_text)
'''
파이썬 데이터 분석가 되기
오늘의 주제는 웹 데이터 수집
삼성전자 일별 시세 불러오기
이해 쏙쏙
'''

# 태그명으로 검색: find() / find_all()
# find(): 맨 처음 1개만 / find_all(): 모두 다
first_p = soup.find('p')
first_p # <p id="body">오늘의 주제는 웹 데이터 수집</p>
all_p = soup.find_all('p')
all_p
'''
[<p id="body">오늘의 주제는 웹 데이터 수집</p>,
 <p class="scraping">삼성전자 일별 시세 불러오기</p>,
 <p class="scraping">이해 쏙쏙</p>]
'''

# id 값이 title인 조건에 해당하는 첫번째 정보만 검색
title = soup.find(id='title')  # <h1 id="title">파이썬 데이터 분석가 되기</h1>

# class값이 scraping인 첫번째 정보만 검색
scraping = soup.find(class_='scraping')  # <p class="scraping">삼성전자 일별 시세 불러오기</p>

# class값이 scraping인 모든 정보 검색
scraping_all = soup.find_all(class_='scraping')
# [<p class="scraping">삼성전자 일별 시세 불러오기</p>, <p class="scraping">이해 쏙쏙</p>]

# attrs 매개변수 사용 => 속성으로 검색 attrs ={'속성명': '값'}
# class가 scraping인 첫 번째 요소 검색
first_scraping = soup.find(attrs={'class': 'scraping'})

# id 속성이 body인 요소 검색
body_elemnet = soup.find(attrs={'id': 'body'})





### 야후 파이낸스 주가 데이터 웹 스크래핑 ###
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# 변수 저장
stock_url = 'https://finance.yahoo.com/quote/005930.KS/history/'

# 웹 페이지 요청
res = requests.get(stock_url)
# res에서 HTML 문서만 가져오기
html = res.text
# 'Edge: Too Many Requests' 오류 뜸. 
# 이를 해결하기 위해 header를 가져옴
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

# 헤더를 담아 요청
res = requests.get(stock_url, headers= headers)
html = res.text
soup = BeautifulSoup(html, 'html.parser')

# tr 요소가 있을 경우, 클래스 정보를 가져옴
first_tr = soup.find('tr')
first_class = first_tr.get('class')[0] # [0]: 맨 처음 있는 클래스 값을 의미
# 'yf-1jecxey'

# tr 태그에 있는 td 태그 중 class == first_class인 애들 찾기
soup.find_all('td', class_ = first_class)

# Jul 26, 2024 -> 2024년 7월 26일 
# 81,600.00-> 81,600원
# 위 형태로 데이터 뽑기

# YYYY년 MM월 DD일인 형식으로 날짜 처리: strftime('%Y년 %m월 %d일')
datef = pd.to_datetime(soup.find_all('td',class_=first_class)[0].text).strftime('%Y년 %m월 %d일')
# '2025년 02월 17일'
    
# .00을 '원'으로 대체하여 종가(Colse) 처리: replace('.00', '원')
CloseP = soup.find_all('td', class_=first_class)[4].text.replace('.00', '원')
# '56,000원'

'''
for문으로 순회하면서 전체 날짜, 종가 데이터 가져와서 그래프 그리기
'''
rows = soup.find_all('tr') # tr,td 다 들어가있음
rows[1]
dates = []
prices = []
for i in range(1, len(rows)): # 첫 번째 tr태그 제외
    cells = rows[i].find_all('td')
    if len(cells) == 7:
        date = pd.to_datetime(cells[0].text, format='%b %d, %Y')
        close_price = cells[4].text.replace(',', '').replace('.00', '')
        dates.append(date)
        prices.append(int(close_price))

stock_data = pd.DataFrame({'data': dates, 'price': prices})

# y축  눈금 간격 설정
min_price = min(stock_data['price'])
max_price = max(stock_data['price'])
y_ticks = range(min_price, max_price, 3000)

plt.figure(figsize=(10,5))
plt.plot(stock_data['data'],
         stock_data['price'],
         marker='o',
         label='price')

plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Samsung Electronics Stock Price')
plt.legend()
plt.grid(True)
plt.yticks(y_ticks)
plt.show()


# 표형태로 되어있는 HTML 페이지에서 데이터를 읽은 후, 데이터 프레임으로 바로 변경
from io import StringIO

response = requests.get(stock_url, headers=headers)
stock_data = pd.read_html(StringIO(str(response.text)), header=0)[0]















