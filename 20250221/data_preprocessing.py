# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 08:59:23 2025

@author: Admin
"""

'''
모델 정확도 저하 방지
1. 데이터 타입의 일관성 유지
2. 결측치
3. 이상치
4. 목적에 맞는 특징(변수) 추출 방법

### 1. 데이터 타입의 일관성 유지 ###
### 2. 결측치 ###
### 3. 이상치 ###
### 4. 목적에 맞는 특징(변수) 추출 방법 ###

'''
import pandas as pd 


data = pd.DataFrame({'A' : ['1', '2', '3'],
                     'B' : ['4', '5', '6'],
                     'C' : ['7', '8', '9']})

data.info() 

# A, B, C 열의 데이터 타입을 int로 변경
data[['A', 'B', 'C']] = data[['A', 'B', 'C']].apply(pd.to_numeric)

### 2. 결측치 ###
# 1. 결측값 제거 : DataFrame.dropna() axis=0 / axis = 1
data = pd.DataFrame({'A' : ['1', '2', '3', None],
                     'B' : ['4', None, '5', '6'],
                     'C' : [None, '7', '8', '9']})

# 결측값이 있는 행을 제거 
data_dropna = data.dropna(axis=1) 

# 2. 결측값 0으로 채우기 : DataFrame.fillna()
data_fillna = data.fillna(0)

# 3. 결측값 평균으로 채운 데이터프레임

data = pd.DataFrame({'A':['a', 'b', 'c', None],
                      'B':['d', None, 'f', 'g'],
                      'C':[None, 'h', 'i', 'i']})

data_fillna = data.fillna({'A':'a'})

### 3. 이상치 ###
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(8,3), columns=['C1','C2','C3'])

df.loc[1,'C1'] = 11
df.loc[3,'C3'] = 10

plt.boxplot([df['C1'],df['C3']])
plt.show()



### 4. 목적에 맞는 특징(변수) 추출 방법 ###
import seaborn as sns








































