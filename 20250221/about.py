# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:31:15 2025

@author: Jiyeon Baek


about.py

시계열 데이터의 특징과 전처리 방법
"""
import pandas as pd 


### date 형 변환 : to_datetime() ###
# info() => 날짜 : object일 경우
d = pd.DataFrame({'date':['2019-01-03',
                          '2021-11-22',
                          '2023-01-05'],
                  'name':['J', 'Y', 'O',]})
d.info() 

d['date'] = pd.to_datetime(d.date, format= '%Y-%m-%d')


### datetime 형의 컬럼을 인덱스로 설정 : set_index() ###
d.set_index(keys=['date'], inplace=True)




### 결측치 확인 : isnull(), sum 함수 사용 ###
import numpy as np

d = pd.DataFrame({'date':['2019-01-03',
                          '2021-11-22',
                          '2021-12-01',
                          '2023-01-05'],
                  'x1':[0.1, 2.0, np.nan, 1.2]})

d.isnull().sum() 
'''
date    0
x1      1
dtype: int64
'''

d['date'] = pd.to_datetime(d.date, format= '%Y-%m-%d')
d.set_index(keys=['date'], inplace=True)
d.isnull().sum() 
'''
x1    1
dtype: int64
'''




### 결측치 처리 : fillna(method='ffill') / drop() / interpolate() ###
d = d.fillna(method='ffill')

d = pd.DataFrame({'date':['2019-01-03',
                          '2021-11-22',
                          '2021-12-01',
                          '2023-01-05'],
                  'x1':[0.1, 2.0, np.nan, 1.2]})


d = d.dropna() # 행삭제, # axis = 열삭제
d = d.interpolate() # 결측치 전/후의 평균값으로 채움 # 선형보간법
'''
선형보간법 
시간에 따라 시스템이 동작하는 방식을 알고 있을 때와
연도에 따른 온도 변화에 대한 추세를 미리 알고 있을 때 유용
'''


### 빈도 설정 : index 속성 / asfreq() ###
# 빈도 설정 : 데이터 분석에서 설정하는 시간의 최소 단위
# index 속성을 이용하면 빈도가 설정되어 있는 지를 확인 가능

d = pd.DataFrame({'date':['2019-01-03',
                          '2019-11-22',
                          '2021-12-01',
                          '2023-01-05'],
                  'x1':[0.1, 2.0, np.nan, 1.2]})
d['date'] = pd.to_datetime(d.date, format= '%Y-%m-%d')
d.set_index(keys=['date'], inplace=True)

# 인덱스 속성 확인
print(d.index) 
'''
DatetimeIndex(['2019-01-03', '2019-11-22', '2021-12-01', '2023-01-05'],
              dtype='datetime64[ns]', name='date', freq=None)
'''

# 빈도 설정 : asfreq('Y', method='ffill')
    # 'Y' : 매년 마지막 date(1), 해당하는 연이 없다면 NaN으로 채워짐
    # method='' : 채우는 방식
d2 = d.asfreq('Y', method='ffill') # method='ffill' : 이전,  # 'bfill' : 이후





### 특징량 만들기 : rolling() ###
# 시계열 데이터에서 빈도 설정 범위를 넓게 잡고 한묶음으로 설정했을 경우,
# 패턴에 대한 본질이 묻힐 수 있다.
# 방지 : rolling() 데이터를 shift 하여 더 상세한 특징량을 생성
# shift : 부분 시계열 데이터를 추출 => 해당 부분의 통계량 => 특징량으로

d = pd.DataFrame({'date':['2021-01-06',
                          '2021-01-13',
                          '2021-01-20',
                          '2021-01-27',
                          '2021-02-03'],
                  'x1':[5, 4, 3, 2, 7]})
d['date'] = pd.to_datetime(d.date)
d.set_index(keys=['date'], inplace=True)

d.rolling(2).mean() 
'''
index   0   1       2       3       4
        5,  4,      3       2       7
(2)         5,      4,      3,      2
결과      (4+5)/2     (3+4)/2     (2+3)/2    d.rolling(2).mean()
'''
'''
             x1
date           
2021-01-06  NaN
2021-01-13  4.5
2021-01-20  3.5
2021-01-27  2.5
2021-02-03  4.5
'''

### 이전 값과 차이 계산 : diff() ###
d = pd.DataFrame({'date':['2021-01-06',
                          '2021-01-13',
                          '2021-01-20',
                          '2021-01-27',
                          '2021-02-03'],
                  'x1':[5, 4, 3, 2, 7]})
d['date'] = pd.to_datetime(d.date)
d.set_index(keys=['date'], inplace=True)

y_diff = d.diff()  # 이후값 - 이전값
'''
index   0      1       2       3       4
------------------------------------------
data    5,     4,      3,      2,      7
y_diff Nan    -1.0    -1.0    -1.0    -1.0
'''
'''
            x1
date           
2021-01-06  NaN
2021-01-13 -1.0
2021-01-20 -1.0
2021-01-27 -1.0
2021-02-03  5.0
'''
y_diff.columns = ['diff']
temp = pd.concat([d, y_diff], axis=1)


### 지연값 추출 : shift() ###
'''
지연값 : 시계열 데이터의 경우 특정 값이 미래의 값에 영향을 주는 경우가 있다
이런 특성을 반영하기 위해 shift() 를 사용
shift(2) : 데이터가 2개씩 뒤로 밀리는 것을 의미.
          결측치가 발생 => 결측치 처리가 반드시 필요
'''
d = pd.DataFrame({'date':['2021-01-06',
                          '2021-01-13',
                          '2021-01-20',
                          '2021-01-27',
                          '2021-02-03'],
                  'x1':[5, 4, 3, 2, 7]})
d['date'] = pd.to_datetime(d.date)
d.set_index(keys=['date'], inplace=True)

d['shift'] = d['x1'].shift(2) 
'''
            x1  shift
date                 
2021-01-06   5    NaN
2021-01-13   4    NaN
2021-01-20   3    5.0
2021-01-27   2    4.0
2021-02-03   7    3.0
'''


# 결측치 이후값으로 채움
d = d.fillna(method='bfill')
'''
            x1  shift
date                 
2021-01-06   5    5.0
2021-01-13   4    5.0
2021-01-20   3    5.0
2021-01-27   2    4.0
2021-02-03   7    3.0
''' 

### 원-핫 인코딩 : get_dummies() ###
'''
범주형 데이터를 컴퓨터가 처리할 수 있도록 형태를 변환하는 방법
텍스트 형태 => 
카테고리형 데이터의 각 범주를 하나의 열로 만들고, 
해당 데이터가 있는 곳만 1을 표시, 아닌 곳은 0으로 표시
 => 숫자형으로 인식 가능하게 하는 방법
'''
d = pd.DataFrame({'date':['2021-01-06',
                          '2021-01-13',
                          '2021-01-20',
                          '2021-01-27',
                          '2021-02-03'],
                  'x1':[5, 4, 3, 2, 7],
                  '과목':['a','b','c','d','e']})
d['date'] = pd.to_datetime(d.date)
d.set_index(keys=['date'], inplace=True)

x = pd.get_dummies(d['과목'])



















