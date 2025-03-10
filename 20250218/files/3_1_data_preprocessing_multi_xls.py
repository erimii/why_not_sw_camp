# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:01:53 2025

@author: Admin

여러개의 엑셀 파일(125개)을 전처리하여 통합..

# 월별 외국인 관광객 통게에 대한 데이터 수집: 한국관광데이터랩
"""

import pandas as pd

kto_201901 = pd.read_excel('./data/kto_201901.xlsx',
                           header=1,
                           usecols='A:G',
                           skipfooter = 4)

kto_201901.head()
'''
     국적      관광     상용    공용  유학/연수      기타       계
0  아시아주  765082  10837  1423  14087  125521  916950
1    일본  198805   2233   127    785    4576  206526
2    대만   86393     74    22    180    1285   87954
3    홍콩   34653     59     2     90    1092   35896
4   마카오    2506      2     0     17      45    2570
'''

# data 전처리
kto_201901.info()
'''
RangeIndex: 67 entries, 0 to 66
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   국적      67 non-null     object
 1   관광      67 non-null     int64 
 2   상용      67 non-null     int64 
 3   공용      67 non-null     int64 
 4   c   67 non-null     int64 
 5   기타      67 non-null     int64 
 6   계       67 non-null     int64 
 '''

# 기준년월 칼럼 추가
kto_201901['기준년월'] = '2019-01'

# continents_list에 해당하는 값 제외
continents_list=['아시아주','미주','구주','대양주','아프리카주','기타대륙','교포소계']
condition = (kto_201901.국적.isin(continents_list) == False)
kto_201901_country = kto_201901[condition]

# index 재설정
kto_201901_country_newindex = kto_201901_country.reset_index(drop=True)

# 대륙 칼럼 추가
continents = ['아시아']*25 + ['아메리카']*5 + ['유럽']*23 + ['오세아니아']*3 + ['아프리카']*2 + ['기타대륙'] + ['교포']
kto_201901_country_newindex['대륙'] = continents


# 관광객비율(%) 컬럼 추가 : .1
ratio = round(kto_201901_country_newindex['관광'] / kto_201901_country_newindex['계'] * 100, 1)
kto_201901_country_newindex['관광객비율(%)'] = ratio

kto_201901_country_newindex.head(1)

#---------------------------------------------------------
# 파일 읽은 후 데이터 전처리 과정 함수로 선언
def create_kto_data(yy,mm):
    file_path = './data/kto_{}{}.xlsx'.format(yy,mm)
    
    df = pd.read_excel(file_path, header=1, skipfooter=4, usecols='A:G')
    
    # 기준년월 칼럼 추가
    df['기준년월'] = '{}-{}'.format(yy,mm)
    
    # ignore_list에 해당하는 값 제외 후 index  재설정
    ignore_list=['아시아주','미주','구주','대양주','아프리카주','기타대륙','교포소계']
    condition = (df['국적'].isin(ignore_list) == False)
    df_country = df[condition].reset_index(drop=True)
    
    # 대륙 컬럼 추가
    continents = ['아시아']*25 + ['아메리카']*5 + ['유럽']*23 + ['오세아니아']*3 + ['아프리카']*2 + ['기타대륙'] + ['교포']
    df_country['대륙'] = continents
    
    # 관광객비율(%) 컬럼 추가
    ratio1 = round(df_country['관광'] / df_country['계'] * 100, 1)
    df_country['관광객비율(%)'] = ratio1
    
    # 전체비율(%) 컬럼 추가
    tourist_sum = sum(df_country['관광'])
    ratio2 = round(df_country['관광'] / tourist_sum * 100, 1)
    df_country['전체비율(%)'] = ratio2
    
    return(df_country)



kto_test = create_kto_data(2018, 12)
kto_test.head()
'''
    국적      관광    상용   공용  유학/연수    기타       계     기준년월   대륙  관광객비율(%)  전체비율(%)
0   일본      252461  1698  161    608        3593    258521      2018-12  아시아      97.7     22.7
1   대만      85697    71   22    266         1252    87308       2018-12  아시아      98.2      7.7
2   홍콩      58355    41    3    208         939     59546       2018-12  아시아      98.0      5.2
3  마카오      6766     0    1     20          36      6823       2018-12  아시아      99.2      0.6
4   태국      47242    42  302     58         6382    54026       2018-12  아시아      87.4      4.2
'''


df = pd.DataFrame()

for yy in range(2010, 2021):
    for mm in range(1, 13):
        try:
            temp = create_kto_data(str(yy), str(mm).zfill(2))
            df = pd.concat([df, temp], ignore_index=True)
            
        except:
            pass

df.info()

df.to_excel('./files/kto_total.xlsx', index = False)





# 과제
# 국적별 관광객 데이터를 개별 엑셀 파일로 저장하기
# [국적별 관광객 데이터] 스위스.xlsx

# 국가별 데이터 저장 하기
cntry_list = df['국적'].unique()

for cntry in cntry_list:
    
    df_filtered = df[df['국적'] == cntry]
    
    # 파일명 생성
    file_name = f'./files/[국적별 관광객 데이터] {cntry}.xlsx'
    
    # 저장
    df_filtered.to_excel(file_name, index=False)








