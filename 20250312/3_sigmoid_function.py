# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:08:31 2025

@author: Admin

이진분류: 둘 중 하나를 결정하는 문제. 대표적인 알고리즘: 로지스틱회귀
시그모이드함수: 0~1 사이의 값을 가지면서 S자 형태로 그려지는 함수
"""

# 시그모이드 함수 시각화
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1/(1+np.exp(-x))
    
x = np.arange(-5.0, 5.0, 0.1)

# w 가중치 추가
y1 = sigmoid(0.5*x)
y2 = sigmoid(x)
y3 = sigmoid(2*x)

plt.plot(x, y1, 'r', linestyle='--')
plt.plot(x, y2, 'g')
plt.plot(x, y3, 'b', linestyle='--')
plt.plot([0,0], [1.0,0.0], ':')
plt.title('sigmoid function')
plt.show()
# 그래프의 경사도가 w에 따라 변함


# b 편향 추가
y1 = sigmoid(x+0.5)
y2 = sigmoid(x+1)
y3 = sigmoid(x+1.5)

plt.plot(x, y1, 'r', linestyle='--')
plt.plot(x, y2, 'g')
plt.plot(x, y3, 'b', linestyle='--')
plt.plot([0,0], [1.0,0.0], ':')
plt.title('sigmoid function')
plt.show()

# b값에 따라서 그래프가 이동





































