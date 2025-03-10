# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 12:41:06 2025

@author: Admin
"""
'''
미세먼지와 날씨의 상관관계
-> 미세먼지와 초미세먼지관계?
-> 미세먼지 변수 중 대기오염과 관련된 변수?
-> 일산화탄소와 이산화질소 관계?
-> 오존과 바람 관계?
-> 기온과 미세먼지 관계?
'''

import pandas as pd

dust = pd.read_excel('data/dust.xlsx')
weather = pd.read_excel('data/weather.xlsx')
dust=dust.fillna(method = 'bfill')
dust.isnull().sum()

dust.head()
'''
        날짜     아황산가스  일산화탄소   오존  이산화질소  PM10  PM2.5
0  2021-01-01 01  0.004         0.4     0.021  0.018    NaN     12.0
1  2021-01-01 02  0.004         0.4     0.019  0.020    20.0    13.0
2  2021-01-01 03  0.004         0.5     0.017  0.023    23.0    13.0
3  2021-01-01 04  0.004         0.5     0.015  0.024    17.0    12.0
4  2021-01-01 05  0.004         0.5     0.010  0.026    NaN     14.0

미세먼지(PM10): 지름 10㎛(마이크로미터) 이하의 먼지
초미세먼지(PM2.5): 지름 2.5㎛ 이하의 더 작은 먼지
'''
## 미세먼지와 초미세먼지 관계는?
dust_pm = dust[['PM10', 'PM2.5']]
dust_pm = dust_pm.dropna()
dust_pm.corr()
'''
           PM10     PM2.5
PM10   1.000000  0.830959
PM2.5  0.830959  1.000000
양의 상관 관계를 가짐
'''
# 미세먼지와 초미세먼지 산점도
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    
sns.scatterplot(x='PM10', y = 'PM2.5', data = dust_pm)
plt.xlabel("PM10 (미세먼지)")
plt.ylabel("PM2.5 (초미세먼지)")
plt.title("미세먼지 vs 초미세먼지 관계")
plt.show() # 우상향하는 패턴


## 미세먼지 변수 중 대기오염과 관련된 변수?
dust_pm10 = dust.drop(['날짜', 'PM2.5'], axis = 1)
dust_pm10=dust_pm10.dropna()
dust_pm10.corr()
'''
          아황산가스     일산화탄소     오존     이산화질소    PM10
아황산가스  1.000000     0.148473    -0.066222  0.084078  0.156999
일산화탄소  0.148473     1.000000    -0.763945  0.846364  0.529966
오존      -0.066222   -0.763945       1.000000 -0.924462 -0.345387
이산화질소  0.084078     0.846364    -0.924462  1.000000  0.416201
PM10        0.156999    0.529966    -0.345387  0.416201  1.000000

일산화탄소(CO) (0.529966)
이산화질소(NO₂) (0.416201)
'''
plt.figure(figsize=(8,6))
sns.heatmap(dust_pm10.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)


plt.title("대기오염 물질과 미세먼지(PM10) 상관관계 히트맵")
plt.show()

## -> 일산화탄소와 이산화질소 관계?
# 상관계수: 0.846364
plt.figure(figsize=(8,6))
sns.regplot(x=dust_pm10['일산화탄소'], y=dust_pm10['이산화질소'], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})

plt.xlabel("일산화탄소 (CO) 농도")
plt.ylabel("이산화질소 (NO₂) 농도")
plt.title("일산화탄소 vs 이산화질소 (회귀선 포함)")
plt.show() # 우상향하는 패턴

## 오존과 바람 관계?
weather.head()
'''
    지점 지점명                  일시  기온(°C)  풍속(m/s)  강수량(mm)  습도(%)
0  400  강남 2021-01-01 01:00:00    -7.2      0.6      0.0   57.5
1  400  강남 2021-01-01 02:00:00    -7.6      0.7      0.0   57.5
2  400  강남 2021-01-01 03:00:00    -8.2      0.6      0.0   62.0
3  400  강남 2021-01-01 04:00:00    -8.1      0.5      0.0   60.5
4  400  강남 2021-01-01 05:00:00    -8.7      1.3      0.0   66.4
'''
dust.info() # 날짜 object 2021-01-01 01
weather.info() # 일시 datetime 2021-01-01 01:00:00

dust.loc[dust['날짜'].str.endswith(' 24'), '날짜'] = (
    (pd.to_datetime(dust['날짜'].str[:10]) + pd.Timedelta(days=1)).astype(str) + " 00"
)

dust['일시'] = pd.to_datetime(dust['날짜'], format="%Y-%m-%d %H")

# dust weather 병합
du_we = dust.merge(weather, how = 'left', on = '일시')
du_we = du_we.dropna()

o_wind = du_we[['풍속(m/s)', '오존']]
o_wind.corr()
'''
          풍속(m/s)        오존
풍속(m/s)  1.000000  0.632415
오존       0.632415  1.000000
양의 상관 관계
'''
o_wind['풍속(m/s)'].min() # 0.0
o_wind['풍속(m/s)'].max() # 5.2

bins = [0, 1, 2, 3, 4, 5, 6]  # 최대값보다 큰 5.5까지 포함
labels = ['0~1', '1~2', '2~3', '3~4', '4~5', '5~6']

# `right=True` (기본값) → 오른쪽 경계 포함
o_wind['풍속 구간'] = pd.cut(o_wind['풍속(m/s)'], bins=bins, labels=labels, include_lowest=True)

plt.figure(figsize=(8,6))
o_wind.groupby('풍속 구간')['오존'].mean().plot(kind='bar', color='cornflowerblue')
plt.xlabel("풍속 구간 (m/s)")
plt.ylabel("오존 농도")
plt.title("풍속 구간별 평균 오존 농도")
plt.show()

# 온도와 미세먼지 상관관계 

























































