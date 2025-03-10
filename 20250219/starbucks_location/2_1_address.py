# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:22:02 2025

@author: tuesv
"""

import pandas as pd

seoul_starbucks = pd.read_excel('starbucks_location/files/seoul_starbucks_list.xlsx', header=0)

# 주소 정보에서 시군구명 추출
sgg_name =[]

for adress in seoul_starbucks['주소']:
    sgg = adress.split()[1]
    sgg_name.append(sgg)

seoul_starbucks['시군구명'] = sgg_name

seoul_starbucks.to_excel('starbucks_location/files/seoul_starbucks_list.xlsx', index = False)








































