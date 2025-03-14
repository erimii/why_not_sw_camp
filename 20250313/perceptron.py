# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 09:08:40 2025

@author: Admin
"""

### 퍼셉트론
## Gate
# AND
def AND_gate(x1,x2):
    w1=0.5
    w2=0.5
    b=-0.7
    result = x1*w1 + x2*w2 +b
    
    if result <=0:
        return 0
    else:
        return 1

AND_gate(0, 0),AND_gate(0, 1),AND_gate(1, 0),AND_gate(1, 1)
# (0, 0, 0, 1)


# NAND
def NAND_gate(x1,x2):
    w1=-0.5
    w2=-0.5
    b=0.7
    result = x1*w1 + x2*w2 +b
    
    if result <=0:
        return 0
    else:
        return 1

NAND_gate(0, 0),NAND_gate(0, 1),NAND_gate(1, 0),NAND_gate(1, 1)
# (1, 1, 1, 0)


# OR
def OR_gate(x1,x2):
    w1=0.6
    w2=0.6
    b= -0.5
    result = x1*w1 + x2*w2 +b
    
    if result <=0:
        return 0
    else:
        return 1

OR_gate(0, 0),OR_gate(0, 1),OR_gate(1, 0),OR_gate(1, 1)
# (0, 1, 1, 1)



### 활성화 함수
import numpy as np
import matplotlib.pyplot as plt

## step function
def step(x):
    return np.array(x>0, dtype=np.int64)

x=np.arange(-5.0, 5.0, 0.1)
y=step(x)

plt.title('step function')
plt.plot(x,y)
plt.show()

## sigmoid function
def sigmoid(x):
    return 1/(1+np.exp(-x))

x=np.arange(-5.0, 5.0, 0.1)
y=sigmoid(x)

plt.title('sigmoid function')
plt.plot(x,y)
plt.plot([0,0], [1.0,0.0], ':')
plt.show()

# Hyperbolic tangent function
x=np.arange(-5.0, 5.0, 0.1)
y=np.tanh(x)

plt.title('Hyperbolic tangent function')
plt.plot(x,y)
plt.plot([0,0], [1.0,-1.0], ':')
plt.axhline(y=0, color='orange',linestyle='--')
plt.show()

# Relu Function
def relu(x):
    return np.maximum(0,x)
x=np.arange(-5.0, 5.0, 0.1)
y=relu(x)

plt.title('Relu function')
plt.plot(x,y)
plt.plot([0,0], [5.0,0.0], ':')
plt.show()


# Leaky ReLU function
a=0.1

def leaky_relu(x):
    return np.maximum(a*x, x)

x=np.arange(-5.0, 5.0, 0.1)
y=leaky_relu(x)

plt.title('Leaky ReLU function')
plt.plot(x,y)
plt.plot([0,0], [5.0,0.0], ':')
plt.show()

## 은닉층에서는 relu 함수를 사용하는 것이 일반적
## 출력층에서는 softmax(다중클래스 분류), sigmoid(이진분류)

# softmax function
x=np.arange(-5.0, 5.0, 0.1)
y=np.exp(x) /np.sum(np.exp(x))
plt.title('softmax function')
plt.plot(x,y)
plt.show()




### 행렬곱 신경망 ###
## 1. 순전파 (Foward Propagation)
'''
주어진 입력이 입력층으로 들어가서
은닉층을 지나
출력층에서 예측값을 얻는 과정.

활성화 함수, 은닉층의 수, 각 은닉층의 뉴런 수 등 딥 러닝 모델
1. 입력값은 은닉층
2. 은닉층을 지나면서 각 층에서의 가중치와 함계 연산
3. 출력층으로 향하게 된다
4. 출력층에서 모든 연산을 마친 예측값
'''

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(2, input_dim=3, activation='softmax'))
model.summary()


## 손실함수 loss function

# mse
model.compile(optimizer='adam', loss='mse', metrics=['mse'])

# binary cross-entropy
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

# categorical cross-entropy-다중클래스 분류일 경우
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['mse'])

# 정수값을 가진 레이블에 대해서 다중 클래스 분류를 수행
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['mse'])


### batch size에 따른 경사 하강법
# batch: 매개변수 값을 조정하기 위해 사용되는 데이터의 양

# 배치 경사 하강법




# 옵티마이저

# 모멘텀

# adagrad


### 5. 에포크와 배치 크기와 이터레이션(Epochs and Batch size and Iteration) ###
'''
머신 러닝의 학습 : 실제값과 예측값의 오차로부터 옵티마이저를 통해서 가중치를 업데이트

머신 러닝 학습과정을 현실의 학습에 비유하면
사람은 문제지의 문제를 풀고,
정답지의 정답을 보면서 채점을 하면서
부족했던 점을 깨달으며 머릿속의 지식이 업데이트되는 과정

사람마다 동일한 문제지와 정답지를 주더라도 공부 방법은 천차만별

어떤 사람은 문제지 하나를 다 풀고 나서 정답을 채점하는데

어떤 사람은 문제지의 문제를 10개 단위로 끊어서 공부
문제 10개를 풀고 채점하고
다시 다음 문제 10개를 풀고 채점하고 반복하는 방식

성실한 사람은 문제지의 문제를 달달 외울만큼 문제지를 100번 공부

같은 문제지와 정답지를 주더라도 공부 방법을 다르게 설정할 수 있다.

'''

"""
1) 에포크(Epoch)

    인공 신경망에서 전체 데이터에 대해서 순전파와 역전파가 끝난 상태
 => 문제지의 모든 문제를 끝까지 다 풀고,
    정답지로 채점을 하여 문제지에 대한 공부를 한 번 끝낸 상태
    
에포크가 50이라고 하면, 전체 데이터 단위로는 총 50번 학습

"""

"""
2) 배치 크기(Batch size)

배치 크기는 몇 개의 데이터 단위로 매개변수를 업데이트 하는지

중요한 포인트는 업데이트가 시작되는 시점이 정답지/실제값을 확인하는 시점

주의할 점 : 배치 크기와 배치의 수는 다른 개념
    전체 데이터가 2,000일 때 배치 크기를 200으로 준다면
    배치의 수는 10
    
"""

"""
3) 이터레이션(Iteration) 또는 스텝(Step)

이터레이션이란 한 번의 에포크를 끝내기 위해서 필요한 배치의 수
=> 한 번의 에포크 내에서 이루어지는 매개변수의 업데이트 횟수

전체 데이터가 2,000일 때
배치 크기를 200으로 한다면
이터레이션의 총 수는 10

배치 크기가 1인 확률적 경사 하강법
모든 이터레이션마다 하나의 데이터를 선택하여
경사 하강법을 수행
"""









































































