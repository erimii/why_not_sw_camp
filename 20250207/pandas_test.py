# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:30:47 2025

@author: Admin
"""

import pandas as pd

path = 'https://github.com/dongupak/DataML/raw/main/csv/'
file = path+'vehicle_prod.csv'
df = pd.read_csv(file, index_col=0)
# index_col= : 데이터프레임에서 인덱스로 사용할 열을 지정하는 역할

df.head()
'''
        2007   2008   2009   2010   2011
China   7.71   7.95  11.96  15.84  16.33
EU     19.02  17.71  15.00  16.70  17.48
US     10.47   8.45   5.58   7.60   8.40
Japan  10.87  10.83   7.55   9.09   7.88
Korea   4.04   3.78   3.45   4.20   4.62
'''

df['total'] = df.sum(axis = 1)


df['2009'].plot(kind='bar',
                color = ('orange', 'r', 'b', 'm', 'c','k'))


df['2009'].plot(kind='pie')
df.plot.line()
df.plot.bar()

df = df.T

df.plot.line()

df.loc['Korea']

df.iloc[4]


'''
그룹핑과 필터링

'''

path = 'https://github.com/dongupak/DataML/raw/main/csv/'
weather_file = path +  'weather.csv'
weather = pd.read_csv(weather_file, encoding='cp949')

weather.head()

#weather['month'] = pd.DatetimeIndex(weather['일시']).month
weather['일시'] = pd.to_datetime(weather['일시'])
weather['month'] = weather['일시'].dt.month

'''
groupby('기준 컬럼')
'''
month_mean = weather.groupby('month').mean()

'''
데이터 구조를 변경하는 pivot()
index = 어떤 컬럼을 index
columns = 어떤 컬럼을 열로 하는
values = 어떤 컬럼을 값으로 쓰겠다

fillna() : 존재하지 않는 값을 지정값으로 채움
value =
'''

df = pd.DataFrame({'상품': ['시게', '반지', '반지', '목걸이', '팔찌'],
                   '재질': ['금', '은', '백금', '금', '은'],
                   '가격': [550, 200, 350, 300, 600]})
'''
    상품  재질   가격
0   시게   금  550
1   반지   은  200
2   반지  백금  350
3  목걸이   금  300
4   팔찌   은  600
'''
new_df = df.pivot(index='상품', columns = '재질', values ='가격')
new_df.fillna(value=0)
'''
재질       금     백금      은
상품                      
목걸이  300.0    0.0    0.0
반지     0.0  350.0  200.0
시게   550.0    0.0    0.0
팔찌     0.0    0.0  600.0
'''

# 두 개의 데이터프레임을 하나로 합치는 concat() / merge()




































