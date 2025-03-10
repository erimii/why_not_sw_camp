# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 14:13:53 2025

@author: Admin
"""

'''
9. 데이터의 분리(splitting data)

지도학습의 훈련 데이터

훈련 데이터
X_train
t-train

테스트 데이터
X_test
y_test
'''

# x와 y 분리- zip함수 이용
X, y = zip(['a', 1],['b', 2],['c', 3])

# x와 y 분리- 데이터프레임을 이용
values = [['dfdfdff', 1],
          ['qwqwqwqwq', 0],
          ['rtrttrtr', 0],
          ['hjhjhjhj', 1]]

columns = ['qqq', 'ddd']

import pandas as pd
df = pd.DataFrame(values, columns=columns)
X = df['qqq']
y = df['ddd']

# x와 y 분리- numpy 이용
import numpy as np
np_array = np.arange(0,16).reshape((4,4))

X = np_array[:, :-1]
y = np_array[:, -1]



### test data 분리 ###
'''
x : 독립 변수 데이터
y : 종속 변수 데이터
test_size : 테스트용 데이터 개수를 지정. 1보다 작은 실수
random_state:난수 시드

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=2025)

'''
X,y = np.arange(10).reshape((5,2)), range(5)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.3, 
                                                    random_state=1234)
'''
random_state 값이 달라지면 분리된 데이터도 달라짐

X_train
array([[2, 3],
       [4, 5],
       [6, 7]])

X_test
array([[8, 9],
       [0, 1]])

y_train
[1, 2, 3]

y_test
[4, 0]
'''








'''
10. 한국어 전처리 패키지(texy preprocessing tools for korean text)
'''




































