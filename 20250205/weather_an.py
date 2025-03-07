# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:20:37 2025

@author: Admin
"""

# 사용 모듈 import
import pandas as pd
import matplotlib.pyplot as plt

# 분석할 데이터 읽기
weather = pd.read_csv('./data/csv/weather.csv', encoding='cp949')

weather.head()
weather.info()

# 분석시 필요한 데이터 저장 리스트 선언
# 월별로 구분된 12개 데이터를 저장할 리스트
monthly = [0 for x in range(12)]
# 각 월별 평균 풍속을 저장할 리스트
monthly_wind = [0 for x in range(12)]

# '일시' 컬럼의 데이터에서 2020-07-30부분을 
# DateTime형식의 index를 만들어서
# 데이터프레임에 신규컬럼('month')에 추가
weather['일시'] = pd.to_datetime(weather['일시'])
weather['month'] = weather['일시'].dt.month
weather.head()

# 월별로 분리하여 저장 테스트
# 모든 해의 1월에 해당하는 데이터 추출하여 저장

monthly[0] = weather[weather['month'] ==1]
monthly[0].mean()
weather.head()

# 전체 데이터를 이용하여 1~12월 까지의 평균 풍속을 저장
for i in range(12):
    monthly[i] = weather[weather['month']== i+1]
    monthly_wind[i] = monthly[i].mean()['평균 풍속(m/s)']
    
# matplotlib를 이용한 간단한 시각화
plt.plot(monthly_wind, 'red')
plt.show()

























