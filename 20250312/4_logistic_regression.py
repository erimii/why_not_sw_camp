# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:33:02 2025

@author: Admin
"""
# 로지스틱 회귀

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers

import tensorflow as tf
from tensorflow import keras
'''
독립 번수 데이터 : x -50~50
종속 변수 데이터 : y 숫자 10 이상인 경우에는1/미만인 경우에는 0

활성화 함수: 시그모이드 함수
옵티마이저: sqd
손실 함수: 크로스 엔트로피(binary_crossentropy)
'''

x = np.array([-50, -40, -30, -20, -10, -5, 0,5,10,20,30,40,50])
y = np.array([0,0,0,0,0,0,0,0,1,1,1,1,1])

model = Sequential()
model.add(Dense(1,input_dim=1, activation='sigmoid'))

sgd = optimizers.SGD(learning_rate=0.01)
model.compile(optimizer = sgd, loss='binary_crossentropy', metrics=['binary_accuracy'])

model.fit(x,y, epochs=200)


plt.plot(x, model.predict(x), 'b',x,y,'k.')
plt.show()

print(model.predict(np.array([1,2,3,4,4.5])))
'''
[[0.5015859 ]
 [0.5570842 ]
 [0.61119306]
 [0.6626941 ]
 [0.6871481 ]]
'''

print(model.predict(np.array([11,21,31,41,500])))
'''
[[0.9034601 ]
 [0.9886397 ]
 [0.9987658 ]
 [0.99986714]
 [1.        ]]
'''

'''
독립 변수 데이터가 5보다 작을 경우 0에 가깝게
10 보다 클 경우 1에 가깝게
'''































