# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:22:02 2025

@author: tuesv

크롤링을 이용한 서울시 스벅 매장 목록 데이터 생성
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()
url = 'https://www.istarbucks.co.kr/store/store_map.do?disp=locale'
driver.get(url)

## webdriver로 ‘서울’ 버튼 요소를 찾아 클릭
# 1. ‘서울’ 버튼 요소를 찾아
seoul_btn = '#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a'
# 2. 클릭하기
driver.find_element('css selector', seoul_btn).click()

# webdriver로 ‘전체’ 버튼 요소를 찾아 클릭
all_btn = '#mCSB_2_container > ul > li:nth-child(1) > a'
driver.find_element('css selector', all_btn).click()

# 현재 페이지에 대한 HTML 파서 만들기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 원하는 HTML 태그 찾아오기
starbucks_soup_list = soup.select('li.quickResultLstCon')
starbucks_store = starbucks_soup_list[0]
'''
<li class="quickResultLstCon" data-code="3762" data-hlytag="null" data-index="0" 
 data-lat="37.501087" data-long="127.043069" data-name="역삼아레나빌딩" data-storecd="1509" style="background:#fff"> 
    <strong data-my_siren_order_store_yn="N" data-name="역삼아레나빌딩" data-store="1509" data-yn="N">
        역삼아레나빌딩  
    </strong> 
    <p class="result_details">
        서울특별시 강남구 언주로 425 (역삼동)
        <br/>
        1522-3232
    </p> 
    <i class="pin_general">
        리저브 매장 2번
    </i>
</li>
'''
# 스타벅스 매장 정보 샘플 확인
name = starbucks_store.select('strong')[0].text.strip() # '역삼아레나빌딩'
lat = starbucks_store['data-lat'].strip()   # '37.501087'
long = starbucks_store['data-long'].strip() # '127.043069'
store_type = starbucks_store.select('i')[0]['class'][0][4:] # 'general'
address = str(starbucks_store.select('p.result_details')[0]).split('<br/>')[0].split('>')[1]    # '서울특별시 강남구 언주로 425 (역삼동)'
tel = str(starbucks_store.select('p.result_details')[0]).split('<br/>')[1].split('<')[0]    # '1522-3232'

### 서울시 스타벅스 매장 목록 데이터 ###
# 매장명, 위도, 경도, 매장 타입, 주소, 전화번호

starbucks_list = []

for item in starbucks_soup_list:
    name = item.select('strong')[0].text.strip() # '역삼아레나빌딩'
    lat = item['data-lat'].strip()   # '37.501087'
    lng = item['data-long'].strip() # '127.043069'
    store_type = item.select('i')[0]['class'][0][4:] # 'general'
    address = str(item.select('p.result_details')[0]).split('<br/>')[0].split('>')[1]    # '서울특별시 강남구 언주로 425 (역삼동)'
    tel = str(item.select('p.result_details')[0]).split('<br/>')[1].split('<')[0]    # '1522-3232'
    
    starbucks_list.append([name, lat, lng, store_type, address, tel])

columns = ['매장명', '위도', '경도', '매장타입', '주소', '전화번호']

seoul_starbucks_df = pd.DataFrame(starbucks_list, columns = columns)

seoul_starbucks_df.to_excel('starbucks_location/files/seoul_starbucks_list.xlsx', index = False)

