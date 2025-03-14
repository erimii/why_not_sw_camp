# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 09:08:27 2025

@author: Admin

레모네이드 판매 예측

'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/lemonade.csv'
"""

import tensorflow as tf
import pandas as pd
import numpy as np

# 데이터 준비
filePath = 'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/lemonade.csv'
lemonade = pd.read_csv(filePath)
lemonade.head()
'''
   온도  판매량
0  20   40
1  21   42
2  22   44
3  23   46
4  24   48
'''

independence = lemonade[['온도']]
dependence = lemonade[['판매량']]
independence.shape # (6, 1)
dependence.shape # (6, 1)

# 모델 구축
X = tf.keras.layers.Input(shape=[1])  # 입력층 (온도)
Y = tf.keras.layers.Dense(1)(X)  # 출력층 (판매량)

# 모델 생성
model = tf.keras.models.Model(X,Y)
model.compile(loss='mse')

# 모델 학습
model.fit(independence, dependence, epochs=1000, verbose=1)
model.fit(independence, dependence, epochs=100, verbose=1)
# verbose=0: 학습 과정 출력 생략 (필요하면 1로 변경).

# 예측 수행
model.predict(np.array([[26]]))

# 학습된 가중치(기울기)와 절편 확인
weights, bias = model.get_weights()
print(f'기울기(Weight): {weights[0][0]}')
print(f'절편(Bias): {bias[0]}')

# 모델 확인
model.summary()
















































