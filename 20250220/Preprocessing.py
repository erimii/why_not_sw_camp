# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:10:38 2025

@author: Admin
"""

import pandas as pd

data = pd.read_excel("files/danawa_crawling_result.xlsx")

data.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 300 entries, 0 to 299
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   상품명     300 non-null    object
 1   스펙 목록   300 non-null    object
 2   가격      300 non-null    int64 
dtypes: int64(1), object(2)
memory usage: 7.2+ KBv
'''

# 1. 상품명 데이터를 회사명과 상품명으로 분리
data['상품명'][:5]
'''
0                                샤오미 드리미 V10
1                              원더스리빙 다이나킹 Z9
2                          LG전자 코드제로 A9 A978
3    샤오미 SHUNZAO 차량용 무선청소기 2세대 Z1 PRO (해외구매)
4                            델로라 V11 파워 300W
Name: 상품명, dtype: object
'''
#-----------------------------------------------------------
# test code
title = data['상품명'][0] # '샤오미 드리미 V10'
info = title.split(' ') # => ['샤오미', '드리미', 'V10']
info = title.split(' ', 1) # => ['샤오미', '드리미 V10']

#-----------------------------------------------------------
company_list = []
product_list = []

for title in data['상품명']:
    title_info = title.split(' ', 1)
    company_name = title_info[0]
    product_name = title_info[1]
    
    company_list.append(company_name)
    product_list.append(product_name)


# 2. 분석에 필요한 요소만 추출 - 카테고리, 사용시간, 흡입력
data['스펙 목록'][0].split(' / ')
'''
['핸디/스틱청소기', <- 카테고리 명
 '핸디+스틱형',
 '무선형',
 '전압: 25.2V',
 '헤파필터',
 'H12급',
 '5단계여과',
 '흡입력: 140AW', <- 흡입력
 '흡입력: 22000Pa', <- 흡입력
 '먼지통용량: 0.5L',
 '충전시간: 3시간30분',
 '사용시간: 1시간', <- 사용시간
 '용량: 2500mAh',
 '브러쉬: 바닥, 솔형, 틈새, 침구, 연장관',
 '거치대',
 '무게: 1.5kg',
 '색상:화이트',
 '소비전력: 450W']
'''

# 스펙 목록에 대한 패턴 분석
'''
카테고리 : 첫 번째 항목에 위치
사용 시간: 00분 / 00시간 
흡입력 : 000pa / 000AW
'''
#-----------------------------------------------------------
# test code
# 카테고리
spec_list = data['스펙 목록'][0].split(' / ')
category = spec_list[0] # '핸디/스틱청소기'

# 흡입력 / 사용시간
use_time_spec = '' # '사용시간: 1시간'
suction_spec='' # '흡입력: 22000Pa'

for spec in spec_list:
    if '사용시간' in spec:
        use_time_spec = spec
    elif '흡입력' in spec:
        suction_spec = spec

use_time_value = use_time_spec.split()[1].strip() # '1시간'
suction_value = suction_spec.split()[1].strip() # '22000Pa'

#------------------------------------------------------------

category_list = []
use_time_list = []
suction_ilst = []

for spec_data in data['스펙 목록']:
    spec_list = spec_data.split(' / ')
    
    category = spec_list[0]
    category_list.append(category)
    
    use_time_value = None
    suction_value = None
    
    for spec in spec_list:
        if '사용시간' in spec:
            use_time_value = spec.split()[1].strip()
        elif '흡입력' in spec:
            suction_value = spec.split()[1].strip()
    
    use_time_list.append(use_time_value)
    suction_ilst.append(suction_value)
            
# 3. 무선 청소기 사용시간 단위 통일
use_time_list[:5]
# ['1시간', '1시간5분', '80분', '30분', '1시간10분']
'''
'시간' 단어가 있으면
1. '시간'앞의 숫자를 추출 한 뒤, *60
2. '시간'뒤 '분' 앞의 숫자 추출후 더하기

'시간' 단어가 없으면
'분' 글자 앞의 숫자 추출

예외처리
'''
#-----------------------------------------------------------
# test code
times = use_time_list[:5]
# ['1시간', '1시간5분', '80분', '30분', '1시간10분']
def convert_time_minute(time):
    try:
        if '시간' in time:
            hour = time.split('시간')[0]
            if '분' in time:
                minute = time.split('시간')[-1].split('분')[0]
            else:
                minute = 0
        else:
            hour = 0
            minute = time.split('분')[0]
        return int(hour)*60 + int(minute)
    except:
        return None

for time in times:
    time_value = convert_time_minute(time)
    print(f'{time} = {time_value}')
#-----------------------------------------------------------
# 모델별 사용시간을 분 단위로 통일
new_use_time_list = []

for time in use_time_list:
    value = convert_time_minute(time)
    new_use_time_list.append(value)


# 4. 무선 청소기 흡입력 단위 통일
'''
AW: 진공 청소기의 전력량(airwatt)
W: 모터의 소비 전력 단위(watt)
PA: 흡입력 단위(pascal)

(1W == 1AW == 100PA)
'''
# 흡입력 단위를 통일시키는 함수
def get_suction(value):
    try:
        value = value.upper()
        if 'AW' in value or 'W' in value:
            result = value.replace('A','').replace('W','')
            result = int(result.replace(',',''))
        elif 'PA' in value:
            result = value.replace(',','')/100
        else:
            result = None
        return result
        
    except:
        return None

# 흡입력 단위 통일
new_suction_list=[]

for power in suction_ilst:
    value = get_suction(power)
    new_suction_list.append(value)
#----------------------전처리 완료-----------------------

pd_data = pd.DataFrame()

pd_data['카테고리'] = category_list
pd_data['회사명'] = company_list
pd_data['제품'] = product_list
pd_data['가격'] = data['가격']
pd_data['사용시간'] = new_use_time_list
pd_data['흡입력'] = new_suction_list

pd_data['카테고리'].value_counts()
'''
카테고리
핸디/스틱청소기    241
물걸레청소기       39
차량용청소기       13
침구청소기         5
업소용청소기        1
진공청소기         1
Name: count, dtype: int64
'''

# 핸디/스틱청소기만 선택
pd_data_final = pd_data[pd_data['카테고리'].isin(['핸디/스틱청소기'])]


pd_data_final.to_excel("files/danawa_data_final.xlsx", index=False)






















