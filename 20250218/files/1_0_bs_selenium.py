# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:00:07 2025

@author: Admin

pip install selenium
로 설치

"""
'''
from selenium import webdriver
# 크롬 브라우저 실행
driver = webdriver.Chrome()

# url 접속
url = 'https://www.naver.com/'
driver.get(url)

# 웹페이지 html 다운로드
html = driver.page_source
'''


### BeautifulSoup.select() ###
html = '''
<html>
    <head>
    </head>
    <body>
        <h1> 우리동네시장</h1>
            <div class = 'sale'>
                <p id='fruits1' class='fruits'>
                    <span class = 'name'> 바나나 </span>
                    <span class = 'price'> 3000원 </span>
                    <span class = 'inventory'> 500개 </span>
                    <span class = 'store'> 가나다상회 </span>
                    <a href = 'http://bit.ly/forPlaywithData' > 홈페이지 </a>
                </p>
            </div>
            <div class = 'prepare'>
                <p id='fruits2' class='fruits'>
                    <span class ='name'> 파인애플 </span>
                </p>
            </div>
    </body>
</html>
'''

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# 태그명으로 태그 찾기
tags_span = soup.select('span')
'''  list로 만들어짐
[<span class="name"> 바나나 </span>,
 <span class="price"> 3000원 </span>,
 <span class="inventory"> 500개 </span>,
 <span class="store"> 가나다상회 </span>,
 <span class="name"> 파인애플 </span>]
'''
tags_p = soup.select('p')
''' p 태그 안에 있는 것들도 선택 됨
[<p class="fruits" id="fruits1">
 <span class="name"> 바나나 </span>
 <span class="price"> 3000원 </span>
 <span class="inventory"> 500개 </span>
 <span class="store"> 가나다상회 </span>
 <a href="http://bit.ly/forPlaywithData"> 홈페이지 </a>
 </p>,
 <p class="fruits" id="fruits2">
 <span class="name"> 파인애플 </span>
 </p>]
'''

 # 태그 구조로 위치 찾기
tags_name = soup.select('span.name')
'''
[<span class="name"> 바나나 </span>, <span class="name"> 파인애플 </span>]
'''
# 상위 구조 활용
tags_banana1 = soup.select('#fruits1 > span.name')
tags_banana2 = soup.select('div.sale > #fruits1 > span.name')
'''
[<span class="name"> 바나나 </span>]
'''
tags_banana3 = soup.select('div.sale span.name')
# div.sale 내부에서 span.name 찾아라


# 태그 그룹에서 하나의 태그만 선택
tags = soup.select('span.name')[0]
# <span class="name"> 바나나 </span>

# 태그에서 정보 가져오기
content = tags.text    # ' 바나나 '


'''
멜론 노래 순위 정보 크롤링
'''
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
url = 'http://www.melon.com/chart/index.htm'
driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

# 첫번째는 제외하고, 두 번째 부터 끝까지만 선택
songs = soup.select('tr')[1:]

song = songs[0]
title = song.select('div.ellipsis.rank01 > span > a')[0].text
# 'REBEL HEART'

# 가수 찾기
singer =  song.select('div.ellipsis.rank02 > span > a')[0].text
# 'IVE (아이브)'




































