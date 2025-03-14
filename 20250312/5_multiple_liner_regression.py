# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:33:24 2025

@author: Admin
"""
'''
다중 로지스틱 회귀
독립 변수 2개 이상: 꽃받침의 길이와 꽃잎의 길이
종속 변수: 1개. 해당 꽃이 A인지 B인지

입력 차원=2

'''

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers

import tensorflow as tf
from tensorflow import keras

X = np.array([[0,0],[0,1],[1,0],[0,2],[1,1],[2,0]])

y = np.array([0,0,0,1,1,1])

model = Sequential()
model.add(Dense(1, input_dim=2, activation='sigmoid'))

model.compile(optimizer = 'sgd', loss='binary_crossentropy', metrics=['binary_accuracy'])

model.fit(X,y, epochs=2000)

model.predict(X)
'''
array([[0.17302638],
       [0.44414967],
       [0.46202478],
       [0.7531817 ],
       [0.76634693],
       [0.77901596]],
'''








































