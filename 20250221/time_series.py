# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:31:39 2025

@author: Jiyeon Baek

time_series.py

주식 시세 예측 분석

문제 정의
    주식을 팔아야 할지, 팔지 말아야 할지 고민한다.
    고민한 끝에 앞으로 상승한다면 계속 가지고 있기로 마음먹었다.
    주식은 상승할 것인가 아니면 하강할 것인가?

pip install finance-DataReader
"""
import FinanceDataReader as fdr

df = fdr.StockListing('KRX') # 미국 증시 : NASDAQ

# DataReader('종목코드', 시작일자, 종료일자)

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

# 애플 주식 데이터 수집
df = fdr.DataReader('AAPL', '2022') 

# 주식 가격 시각화 
plt.figure(figsize=(10, 6))
sns.lineplot(x=df.index, y=df['Close'])
plt.title("Apple Stock Closed Price in 2022")
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()


# 샘플링 : 시간간격
# 다운 샘플링 : 샘플링 데이터 축소 (ex. 년 단위로 집약해서 보여줌)
# 업 샘플링 : 샘플링 데이터 확대 (ex. 월이나 일 단위로 많은 데이터)
# 데이터들이 매일 기록 => 시간 구간으로 묶어서 기존 데이터를 집약
# resample('BM') : B 영업일 / M 월 / S 초 / M 분 / H 시 / Q 분기 / Y 연도
# 한달 간격으로 다운샘플링

df_month = df.resample("BM").mean() 

# 수익률 = (매도가격 - 매수가격)/매수가격 : pct_change()

df_month['rtn'] = df_month['Close'].pct_change() 

# 수익률 시각화 
plt.figure(figsize=(10, 6))
sns.lineplot(x=df_month.index, y=df_month['rtn'])
plt.title("Apple Stock Returns in 2022-2023")
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()



# 주가 흐름 파악
# 이동평균선 : 과거 주식 가격의 흐름을 바탕으로 
#                                   미래 주식가격을 예측하는데 사용되는 선
# 일정 기간동안 주식 가격의 흐름을 평균내어 선들을 연결
# 예) 5일 이동평균선 : 최근 5일간의 주가를 종가기준으로 합하여 
#                                               5로 나누어 평균을 구하는 것
# rolling() 
# 한달 단위로 집약된 데이터
# rolling(2).mean()  =>  2달씩 종가에 대한 평균
df_month['MA'] = df_month['Close'].rolling(2).mean()

df_month.iloc[:, [3,7]].plot(figsize=(15,8))
plt.show()


# 최근 종가를 이용하여 이동평균선과 비교 => 상승/하락 판단
# 이동평균선 60일 전 종가
last_close = df_month['MA'].iloc[-2] 

# 오늘 종가
price = df_month['Close'].iloc[-1] 


if price > last_close:
    print('상승 장')
elif price < last_close:
    print('하락 장')
else:
    print('변화없음')

df_month.to_csv('apple_data_pra.csv')



# -------------------------------------------------------
# ----------------------번외-----------------------------
# ARIMA : 머신러닝 모델 

import statsmodels.api as sm 
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("C:/Users/Admin/Desktop/JY/Python/20250221_2/data/apple_data_pra.csv")
model = ARIMA(df['Close'].values, order=(0,1,2))
model_fit = model.fit() 
model_fit.summary()
















