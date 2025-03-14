# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 09:06:13 2025

@author: Admin

보스턴 집값 예측
"""

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 데이터 준비
filePath = 'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/boston.csv'
boston = pd.read_csv(filePath)
boston.head()
boston.info()
'''
 0   crim     506 non-null    float64 범죄율
 1   zn       506 non-null    float64 대형 주택 비율
 2   indus    506 non-null    float64 비상업 지역 비율
 3   chas     506 non-null    int64   찰스강 근처 여부 (0 or 1)
 4   nox      506 non-null    float64 공기 오염도 (NO2 농도)
 5   rm       506 non-null    float64 평균 방 개수
 6   age      506 non-null    float64 오래된 주택 비율
 7   dis      506 non-null    float64 고속도로 접근성
 8   rad      506 non-null    int64   방사형 고속도로 근접도
 9   tax      506 non-null    int64   재산세율
 10  ptratio  506 non-null    float64 학생-교사 비율
 11  b        506 non-null    float64 인구 중 흑인 비율
 12  lstat    506 non-null    float64 저소득층 비율
 13  medv     506 non-null    float64 주택 가격 (목표 변수)
'''

# 독립 변수(X)와 종속 변수(y) 설정
independence = boston.drop(columns=['medv']) # 특성(feature)
dependence = boston['c'] # 집값

X = tf.keras.layers.Input(shape=[13])
Y = tf.keras.layers.Dense(1)(X)
model = tf.keras.models.Model(X,Y)
model.compile(loss='mse')

model.fit(independence, dependence, epochs=1000, verbose=0)
model.fit(independence, dependence, epochs=500)

history = model.fit(independence, dependence, epochs=200)


model.predict(independence[5:10])
'''
array([[25.392542],
       [21.081745],
       [18.006487],
       [ 9.646249],
       [17.49296 ]],
'''
dependence[5:10]
'''
5    28.7
6    22.9
7    27.1
8    16.5
9    18.9
'''

# 모델 확인
model.summary()






































