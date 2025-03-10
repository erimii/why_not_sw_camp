# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:22:02 2025

@author: tuesv
"""

import pandas as pd
import folium
import json

seoul_starbucks = pd.read_excel('starbucks_location/files/seoul_starbucks_list.xlsx')

starbucks_map = folium.Map(location=[37.573050, 126.979189], zoom_start=11)


for idx in seoul_starbucks.index:
    lat = seoul_starbucks.loc[idx, '위도']
    lng = seoul_starbucks.loc[idx, '경도']
    
    folium.CircleMarker(location=[lat, lng],
                        fill= True,
                        fill_color = 'green',
                        fill_opacity = 1,
                        color = 'yellow',
                        weight = 1,
                        radius = 3).add_to(starbucks_map)

starbucks_map.save('starbucks_map.html')

# 스타벅스 매장 타입별 위치

starbucks_map2 = folium.Map(location=[37.573050, 126.979189], zoom_start=11)

for idx in seoul_starbucks.index:
    lat = seoul_starbucks.loc[idx, '위도']
    lng = seoul_starbucks.loc[idx, '경도']
    
    store_type = seoul_starbucks.loc[idx, '매장타입']
    
    fillColor = ''
    if store_type == 'general':
        fillColor = 'green'
        size=2
    elif store_type == 'reserve':
        fillColor = 'blue'
        size=5
    elif store_type == 'generalDT':
        fillColor = 'red'
        size=5
        
    folium.CircleMarker(location=[lat, lng],
                        color = fillColor,
                        fill= True,
                        fill_color = fillColor,
                        fill_opacity = 1,
                        weight = 1,
                        radius = size).add_to(starbucks_map2)

starbucks_map2.save('starbucks_map2.html')









































