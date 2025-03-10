# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:22:02 2025

@author: tuesv
"""

import pandas as pd
import folium
import json

seoul_sgg_stat = pd.read_excel('starbucks_location/files/seoul_sgg_stat2.xlsx', 
                               thousands=',')

sgg_geojson_file_path = 'starbucks_location/maps/seoul_sgg.geojson'
seoul_sgg_geo = json.load(open(sgg_geojson_file_path, encoding = 'utf-8'))

seoul_sgg_geo['features'][0]['properties']
'''
{'SIG_CD': '11320',
 'SIG_KOR_NM': '도봉구',
 'SIG_ENG_NM': 'Dobong-gu',
 'ESRI_PK': 0,
 'SHAPE_AREA': 0.00210990544544,
 'SHAPE_LEN': 0.239901251347}
'''

# 지도 생성
starbucks_bubble = folium.Map(location=[37.573050, 126.979189],
                              tiles = 'CartoDB positron',
                              zoom_start=11)

starbucks_bubble.save('starbucks_bubble.html')

# 서울시 시군구 경계 지도 그리기
def style_function(feature):
    return {
            'opacity':0.4,
            'weight': 1,
            'color': 'black',
            'fillOpacity':0,
            'dashArray': '5, 5'}

folium.GeoJson(seoul_sgg_geo, style_function=style_function).add_to(starbucks_bubble)

starbucks_bubble.save('starbucks_bubble_bound.html')

# 평균 매장 수 계산
starbucks_mean = seoul_sgg_stat['스타벅스_매장수'].mean()

# 평균 매장 수에 따라 크기가 다른 버블 지도로 시각화
for idx in seoul_sgg_stat.index:
    lat = seoul_sgg_stat.loc[idx, '위도']
    lng = seoul_sgg_stat.loc[idx, '경도']
    count = seoul_sgg_stat.loc[idx, '스타벅스_매장수']
    
    if count > starbucks_mean:
        fillColor = 'red'
    else: fillColor = 'blue'
    
    folium.CircleMarker(
        location = [lat, lng],
        dolor='#FFFF00',
        fill_color=fillColor,
        fill_opacity=0.7,
        weight = 1.5,
        radius = count/2).add_to(starbucks_bubble)
    
starbucks_bubble.save('starbucks_bubble_mean.html')


# 매장 수를 단계구분도로 시각화
sgg_geojson_file_path = 'starbucks_location/maps/seoul_sgg.geojson'
seoul_sgg_geo = json.load(open(sgg_geojson_file_path, encoding = 'utf-8'))

starbucks_choropleth = folium.Map(location=[37.573050, 126.979189],
                              tiles = 'CartoDB dark_matter',
                              zoom_start=11)

folium.Choropleth(geo_data=seoul_sgg_geo,
                  data = seoul_sgg_stat,
                  columns=['시군구명', '스타벅스_매장수'],
                  fill_color = 'YlGn',
                  fill_opacity=0.7,
                  line_opacity=0.5,
                  key_on = 'properties.SIG_KOR_NM').add_to(starbucks_choropleth)

starbucks_choropleth.save('starbucks_choropleth.html')














































