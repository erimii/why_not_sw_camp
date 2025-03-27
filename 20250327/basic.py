# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 09:26:02 2025

@author: Admin
"""

###기본데이터###
train = [[25,100,],[52,256],[38,152],[32,140],[25,150]]

x = [i[0] for i in train]
y = [j[1] for j in train]

### 기초 통계 함수 구현 ###
## 평균 : mean(x) ##
'''
독립변수와 종속 변수 값의 평균을 구하는 함수

평균을 구하는 함수를 따로 구현
=> 분산, 표준편차, 공분산 등을 구할 때 편리.
'''
def mean(x): # 평균
    return sum(x) / len(x)

mean(x), mean(y) # (34.4, 159.6)

## 개별 값과 평군의 차 : d_mean(x)  ## 
def d_mean(x): # 편차
    x_mean = mean(x)
    return [i - x_mean for i in x]

d_mean(x), d_mean(y)

## 내적 : dot(x,y) ##
'''
변수로 전달받은 x,y값을 쌍으로 곱한 후,
총합계를 구하는 함수
'''
def dot(x,y):
    return sum([x*y for x,y in zip(x,y)])

dot(x,y) # 29818

## 제곱의 합 : sum_of_square(v) ##
def sum_of_square(v):
    return dot(v,v)

sum_of_square(x), sum_of_square(y) # (6422, 140740)

## 분산 : variance(x) ##
def variance(x): # 편차 제곱의 평균
    n = len(x)
    d = d_mean(x)
    return sum_of_square(d) / (n-1)

variance(x) # 126.3

## 표준편차 : standard_deviation(x) ##
def standard_deviation(x): # 루트 분산
    return variance(x) ** 0.5

standard_deviation(x) # 11.23

## 공분산 ##
'''
하나의 데이터가 증가할 때 다른 데이터도 함께 증가하는 경향이 있다면,
공분산은 양수 값
두 데이터 사이에 뚜렷한 관계가 없다면, 공분산은 0에 가까운 값
'''
def covariance(x,y):
    n = len(x)
    return dot(d_mean(x), d_mean(y)) / (n-1)

covariance(x,y) # 591.7

## 상관계수 ###
'''
공분산을 조금 더 보기 좋고 이해하기 쉽게 다듬은 개념.
-1부터 +1 사이의 숫자
'''
def corrlation(x,y):
    stdev_x =standard_deviation(x)
    stdev_y =standard_deviation(y)
    if stdev_x > 0 and stdev_y >0:
        return covariance(x, y) / (stdev_x * stdev_y)
    else:
        return 0
    
corrlation(x, y)


## nupmy 로 기초 통계 구하기
import numpy as np
x1 = np.array(x)
x1.mean()
x1.var()
x1.std()
np.cov(x1, y)
np.corrcoef(x1,y)


'''
회귀분석 : 두 변수간의 인과관게를 파악하기 위한 방법론
'''
#### 최소자승법을 이용한 회귀분석 ###
# 흩어져 있는 점들을 가장 잘 나타내는 선을 찾는 방법
# OLS : Ordinary Least Squares

# RMSE: 평균 제곱근 오차
# -> 회귀 모델의 성능 평가하는데 사용되는 대표적인 지표 중 하나
# -> 모델이 예측한 값과 실제 값 사이의 차이를 나타내는 값

## 회귀계수 구하기 ##
def OLS(x,y):
    beta = covariance(x, y) / variance(x)
    alpha = mean(y) - beta * mean(x)
    return [alpha, beta]

OLS(x, y)

# 다른 방법
def OLS_fit(x,y):
    beta = (corrlation(x, y)* standard_deviation(y))/standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return [alpha, beta]

OLS_fit(x, y)


## 예측값 구하기 : predict(alpha, beta, train, test) ##
'''
추정한 회귀게수를 학습 데이터에 적용하여
추정값을 계산하는 함수

alpha와 beta는 단순 선형 회귀 모델의 회귀게수
    alpha: 예측된 선형 회귀선의 y 절편
    beta: 예측된 선형 회귀선의 기울기

1. 예측값 선언

2. 변수 x에 train data : 아파트 평수 저장
   변수 y에 train data: 전력량 저장

3. OLS_fit() : alpha, beta에 OLS_fit 함수의 반환값 저장

4. predictions 리스트에 변수 yhat에 입력된 값 추가 <- 예측값

5. predictions 리스트 값 반환
'''
def predict(alpha, beta, train, test):
    predictions = list()
    x = [i[0] for i in train]
    y = [i[1] for i in train]
    
    alpha, beta = OLS_fit(x, y)
    
    for i in test:
        yhat = alpha + beta * i[0]
        predictions.append(yhat)
        
    return predictions

train = [[25,100,],[52,256],[38,152],[32,140],[25,150]]
alpha, beta = OLS_fit(x, y) # (-1.5597783056215349, 4.684877276326207)

pr = predict(alpha, beta, train, train)

import matplotlib.pyplot as plt

plt.rc('font', family='NanumGothic')
plt.title('아파트 평수에 따른 전기 사용량')
plt.scatter(x, y, c='red')
plt.plot(x,pr)
plt.xlabel('아파트 평형')
plt.ylabel('전기사용량')
plt.show()

## SSE(Error Sum of Squares) ##
def SSE(alpha, beta, train, test):
    sse = 0
    for i in test:
        error=(i[1]-(alpha + beta *i[0]))**2
        sse = error+sse
    return sse

SSE(alpha, beta, train, train) # 2291.0324623911324

## SST(Total Sum of Squares) ##
def SST(alpha, beta, train, test):
    sst = 0
    x = [i[0] for i in train]
    y = [j[1] for j in train]
    
    for i in test:
        sum_ds = (i[1] -mean(y)) **2
        sst = sum_ds + sst
    return sst

SST(alpha, beta, train, train) # 13379.2


## 결정계수 (R squared)
def R_squared(alpha, beta, train, test):
    return 1.0-(SSE(alpha, beta, train, test)) / SST(alpha, beta, train, test)

R_squared(alpha, beta, train, train) # 0.8287616253295315









# 예측력 구하기
def OLS_fit(x,y):
    beta = (corrlation(x, y)* standard_deviation(y))/standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return [alpha, beta]

train = [[25,100,],[52,256],[38,152],[32,140],[25,150]]
test = [[45,183],[40,175],[55,203],[28,152],[42,198]]

def predict(alpha, beta, train, test):
    predictions = list()
    
    x=[i[0] for i in train]
    y=[i[1] for i in train]
    
    alpha, beta = OLS_fit(x, y)
    
    for i in test:
        yhat = alpha + beta*i[0]
        predictions.append(yhat)
        
    return predictions

alpha, beta = OLS_fit(x, y)
predict(alpha, beta, train, test)
'''
[209.2596991290578,
 185.83531274742677,
 256.10847189231987,
 129.61678543151228,
 195.20506730007918]
'''

# 예측 결과 평가
actual=[j[1] for j in test]

predicted=predict(alpha, beta, train, test)
actual, predicted 
'''
([183, 175, 203, 152, 198],
 [209.2596991290578,
  185.83531274742674,
  256.1084718923198,
  129.61678543151228,
  195.20506730007918])
'''

from math import sqrt

def RMSE(actual, predicted):
    # 변수 sum_error 값을 0.0으로 초기화
    sum_error = 0.0

    # for 문은 변수 actual에 저장된 값만큼 반복
    for i in range(len(actual)):
        # 예측값[i] - 실제값[i] 반환
        prediction_error = predicted[i] - actual[i]
        # prediction_error 제곱 누적
        sum_error += (prediction_error ** 2)
    
        # sum_error / len(actual) 값 저장
        mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)
    
    
RMSE(actual, predicted) # 28.76214710565456

# --------------여기까지 최소자승법을 이용한 회귀-------------------







import numpy as np
from math import sqrt

# 학습 함수 (OLS)
def OLS_fit(x, y):
    beta = (np.corrcoef(x, y)[0, 1] * np.std(y)) / np.std(x)
    alpha = np.mean(y) - beta * np.mean(x)
    return [alpha, beta]

# 예측 함수
def predict(alpha, beta, test):
    return [alpha + beta * i[0] for i in test]

# RMSE 계산 함수
def RMSE(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

# 학습 데이터 및 테스트 데이터
train = [[25,100], [52,256], [38,152], [32,140], [25,150]]
test = [[45,183], [40,175], [55,203], [28,152], [42,198]]

# 학습 데이터로 OLS 모델 학습
x = [i[0] for i in train]
y = [i[1] for i in train]
alpha, beta = OLS_fit(x, y)

# 예측 수행
predicted = predict(alpha, beta, test)
actual = [j[1] for j in test]

# 결과 확인
print("예측값:", predicted)
print("실제값:", actual)

# RMSE 계산
rmse_value = RMSE(actual, predicted)
print("RMSE:", rmse_value)













