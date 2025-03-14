# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:08:13 2025

@author: Admin

선형회귀
"""

import tensorflow as tf

## 자동 미분: tape_gradient()
w = tf.Variable(2.)

def f(w):
    y = w**2
    z = 2*y +5
    return z

with tf.GradientTape() as tape:
    z = f(w)

gradients = tape.gradient(z,[w])

## 자동 미분을 이용한 선형 회귀 구현
# 가중치 변수 w와 편향 변수 b를 선언
W = tf.Variable(4.0)
b = tf.Variable(1.0)

# 가설을 함수로서 정의 : w*x + b
@tf.function
def hypothesis(x):
    return W*x + b

x_test = [3.5, 5, 5.5, 6]
print(hypothesis(x_test).numpy())
# [15. 21. 23. 25.]

# 평균 제곱 오차를 손실 함수로서 정의
@tf.function
def mse_loss(y_pred, y):
    # 두 개의 차이값을 제곱해서 평균을 리턴
    return tf.reduce_mean(tf.square(y_pred-y))

# 공부하는 시간
x = [1,2,3,4,5,6,7,8,9]
# 공부하는 시간에 따른 성적
y = [11,22,33,44,53,66,77,87,95]

# 옵티마이저는 경사하강법 사용 /학습률(learnning rate)는 0.01
optimizer = tf.optimizers.SGD(0.01)

# 약 300번에 걸쳐 경사하강법을 수행: epoch 300
for i in range(301):
    with tf.GradientTape() as tape:
        # x에 대한 에측값
        y_pred = hypothesis(x)
        
        # MSE 구하기
        cost = mse_loss(y_pred, y)
        
    # loss function에 대한 파라미터의 미분값 계산
    gradients = tape.gradient(cost, [W,b])
    
    # 파라미터 업데이트
    optimizer.apply_gradients(zip(gradients, [W,b]))
    
    if i % 10 == 0:
        print('epoch:{:3} | w: {:5.4f} | b: {:5.4} | cost: {:5.6f}'.format(i, W.numpy(), b.numpy(), cost))





## 케라스로 구현하는 선형 회귀
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers
import numpy as np
'''
케라스로 모델을 만드는 기본적인 형식
1. sequential로 모델을 만들고,
2 add를 통해 입력과 출력 벡터의 차원과 같은 필요한 정보들을 추가
'''

x = np.array([1,2,3,4,5,6,7,8,9])
y = np.array([11,22,33,44,53,66,77,87,95])

model = Sequential()

# 입력 x의 차원은 1, 출력 y의 차원도 1 / 선형회귀이므로 linear
model.add(Dense(1, input_dim=1, activation='linear'))

# 경사하강법: SGD / 학습률: 0.01
sgd = optimizers.SGD(learning_rate = 0.01)

# complie()
model.compile(optimizer=sgd, loss='mse', metrics=['mse'])

# 오차 최소화하는 작업 수행 300번
model.fit(x,y,epochs=300)

import matplotlib.pyplot as plt

plt.plot(x, model.predict(x), 'b', x, y,'k.')
plt.show()

print(model.predict(np.array([9.5]))) # [[102.2059]]
print(model.predict(np.array([0.5]))) # [[6.3121185]]



































