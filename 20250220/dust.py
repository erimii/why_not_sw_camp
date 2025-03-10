# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:01:11 2025

@author: Admin
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

dust = pd.read_excel('data/dust.xlsx')
dust.info()
dust.columns = ['date', 'so2','co', 'o3', 'no2', 'PM10', 'PM2.5']

# 날짜 데이터 년도-월-일 만 추출 후 날짜형으로 변경
# dust['date'][0] '2021-01-01 01'
dust['date'] = dust['date'].str[:11]
dust['date'] = pd.to_datetime(dust['date'])

# y, m, d 각각 추출 후 새로운 칼럼으로 추가
dust['year'] = dust['date'].dt.year
dust['month'] = dust['date'].dt.month
dust['day'] = dust['date'].dt.day

# 컬럼 순서 재정렬
dust = dust[['date', 'year', 'month', 'day', 'so2', 'co', 'o3', 'no2', 'PM10', 'PM2.5']]

### 데이터 전처리
dust.isnull().sum()
# 결측값을 앞 방향 혹은 뒷 방향으로 채우기
dust=dust.fillna(method = 'pad')

# 이전값이 없는 경우 20으로
dust.fillna(20, inplace = True)

# _-----------------------------------------------------
# 날씨 데이터
weather = pd.read_excel('data/weather.xlsx')
# 컬럼 제거
weather = weather.drop(['지점', '지점명'], axis = 1)
weather.info()
weather.columns = ['date','temp','wind','rain','humid']

# dust의 date와 동일하게 만들기
weather['date'] = pd.to_datetime(weather['date']).dt.date
weather['date'] = weather['date'] .astype('datetime64[ns]')

# 좀 더 세부적인 값을 측정하기 위해
weather['rain'] = weather['rain'].replace(0, 0.01)

# 데이터 병합
dust.shape # (744, 10)
weather.shape # (743, 5)

dust=dust.drop(index=743)
df = pd.merge(dust, weather, left_index=True, right_index=True, how="inner")

# 데이터 분석 및 시각화
# 모든 데이터 요소별 상관관계 확인
corr = df.corr()
corr['PM10'].sort_values(ascending = False)

# 히스토그램으로 시각화
df.hist(bins = 50, figsize =(20,15))
plt.show()

# 일별 미세먼지 평균 현황
plt.figure(figsize=(15,10))
sns.barplot(x= 'day',
            y= 'PM10',
            data=df,
            palette='Set1'
            )
plt.show()

# 각 변수간의 상관 관계
plt.figure(figsize=(15,12))
sns.heatmap(data = corr,
            annot = True,
            fmt = '.2f',
            cmap = 'hot')
plt.show()

# 온도와 미세먼지 상관관계 
plt.figure(figsize=(15,12))

x = df['temp']
y = df['PM10']

plt.plot(x,y,marker='o', linestyle='none', alpha=0.5)

plt.title('온도와 미세먼지')
plt.show()









































