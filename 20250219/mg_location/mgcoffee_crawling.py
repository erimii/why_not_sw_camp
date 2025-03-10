# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:25:14 2025

@author: Admin
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()
url = 'https://www.mega-mgccoffee.com/store/find/'
driver.get(url)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
## webdriver로 서울에 잇는 매장 찾기
# 입력 필드 찾기 (id 사용)
input_box = driver.find_element(By.ID, "store_search")
# '서울' 입력
input_box.send_keys("서울")
# Enter 키 입력 (필요할 경우)
input_box.send_keys(Keys.RETURN)

time.sleep(2)

# 현재 페이지에 대한 HTML 파서 만들기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 원하는 HTML 태그 찾아오기
mg_soup_list = soup.select('#store_search_list > li')
mg_store = mg_soup_list[1]

name = mg_store.select('b')[0].text.strip() # '동서울터미널점'
address = mg_store.select('div.cont_text_inner.cont_text_info')[0].text.split()[1] # '광진구'



mg_list = []

for item in mg_soup_list:
    name = item.select('b')[0].text.strip()
    address = item.select('div.cont_text_inner.cont_text_info')[0].text.split()[1]
    
    mg_list.append([name, address])

columns = ['매장명','시군구명']

seoul_mg_df = pd.DataFrame(mg_list, columns = columns)

seoul_mg_df.to_excel('mg_location/files/seoul_mg_list.xlsx', index = False)





# 매장수와 한국인 인구수 비교

# 데이터 불러오기
seoul_mg = pd.read_excel('mg_location/files/seoul_mg_list.xlsx')
seoul_pop = pd.read_excel('mg_location/files/sgg_pop.xlsx')

mgs_sgg_count = seoul_mg.pivot_table(index = '시군구명', values='매장명', aggfunc='count').rename(columns={'매장명':'메가커피_매장수'})

# 데이터 통합
seoul_pop = seoul_pop.merge(mgs_sgg_count, how = 'left', on = '시군구명')


import pandas as pd
import folium
import json

sgg_geojson_file_path = 'mg_location/maps/seoul_sgg.geojson'
seoul_sgg_geo = json.load(open(sgg_geojson_file_path, encoding = 'utf-8'))

mg_choropleth = folium.Map(location=[37.573050, 126.979189],
                              tiles = 'CartoDB dark_matter',
                              zoom_start=11)

folium.Choropleth(geo_data=seoul_sgg_geo,
                  data = seoul_pop,
                  columns=['시군구명', '메가커피_매장수'],
                  fill_color = 'YlGn',
                  fill_opacity=0.7,
                  line_opacity=0.5,
                  key_on = 'properties.SIG_KOR_NM').add_to(mg_choropleth)

mg_choropleth.save('mg_choropleth.html')










