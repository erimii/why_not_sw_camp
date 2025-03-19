# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:39:14 2025

@author: Admin
"""
### 넘파이 배열NumPy Arrays
'''
넘파이(numpy)는 Numerical Python의 줄임말로 
고성능 수치 계산을 쉽게 할 수 있도록 도와주는 라이브러리다. 

자연어를 기계가 이해할 수 있는 벡터 형태로 바꾸려면 
다차원 계산이 필수적이기 때문에 넘파이는 텍스트 분석에서 광범위하게 사용되고 있다.
'''
import numpy as np

a = np.array([1, 2, 3], dtype = float)
a

#차원 반환
a.ndim

#데이터 타입 반환
a.dtype
a.shape


# object dimension의 구성을 튜플 형태로 반환
b = np.array([(1.5,2,3), (4,5,6)], dtype = float)
b.shape


### 브로드캐스팅broadcasting
'''
브로드캐스팅은 
산술 연산에서 다른 모양의 배열을 처리하는 방법으로 
배열 연산을 빠른 속도로 벡터화한다. 

다음 코드는 배열과 스칼라값의 연산이다. 
스칼라 값은 배열과 모양이 다르더라도 연산할 수 있다
'''
data = np.array([1.0, 2.0])
data * 1.6


'''
다음 코드의 변수 c는 (4, 3)의 배열 형태이고, 
d는 (3,)으로 1차원 벡터 형태이지만 연산할 수 있다. 

이때 1차원 벡터의 크기는 배열의 열의 수인 3과 같아야 한다.
'''
c = np.array([[ 0,  0,  0],
           [10, 10, 10],
           [20, 20, 20],
           [30, 30, 30]])
d = np.array([1, 2, 3])

print(c.shape, d.shape)
c + d


'''
다음과 같이 (4, 3) 형태의 배열과 (4,) 형태의 1차원 벡터를 연산하면 
열의 크기와 1차원 벡터의 크기가 달라 
브로드캐스팅 되지 않고 오류가 발생할 수 있으므로 주의해야 한다.
'''
e = np.array([1, 2, 3, 4])
print(c.shape, e.shape)
c + e
# 배열의 열 크기와 다른 크기의 1차원 벡터는 더할 수 없다


### 집계 함수Aggregate Functions
# 집계 함수를 통해 기술통계량을 계산핤 수 있다.
# max() 또는 np.max() : 최댓값을 반환하는 함수
max(a)
a.max()

# min() 또는 np.min() : 최솟값을 반환하는 함수
min(a)


# sum() 또는 np.sum() : 합계를 반환하는 함수
a.sum()


# np.mean(s, axis = 0) : 열을 따라 산술 평균을 반환하는 함수:
# np.mean(s, axis = 1) : 행을 따라 산술 평균을 반환하는 함수
s = [[10, 20, 30],
       [30, 40, 50],
       [50, 60, 70],
       [70, 80, 90]]

print("2차원 배열 :", s)
print("열에 따른 산술 평균 :", np.mean(s, axis=0))
print("행에 따른 산술 평균 :", np.mean(s, axis=1))


# np.where() : 괄호 안의 조건에 맞는 값을 찾아서 그 원소의 인덱스를 배열로 반환하는 함수:
np.where(a < 3)


### 배열 생성
# np.zeros((2, 3)): 원소가 모두 0으로 이루어진 2열 3행의 배열 생성
# np.ones((2, 3)): 원소가 모두 1로 이루어진 2열 3행의 배열 생성
# np.linspace(start, stop,step): 시작과 끝 사이에 균일하게 숫자를 생성

# 0에서 2까지 균일하게 9개의 숫자 생성
np.linspace(0, 2, 9)



### 난수 생성
# random.random()은 균등 분포로 표본을 추출
# random.rand()는 균등 비율로 표본을 추출
# random.randn()은 정규 분포로 표본을 추출
d = np.random.random((2, 2))
d

e = np.random.normal(0, 2, (2, 3))
print(e)



### 맷플롯립을 통한 넘파이 배열의 시각화
import matplotlib.pyplot as plt

plt.hist(np.random.normal(loc=0.0, scale=1.0, size=100000), bins=100)
plt.show()
































