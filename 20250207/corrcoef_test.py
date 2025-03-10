# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:44:29 2025

@author: Admin
"""

'''
상관관계(correlation)
변수 : 독립변수 / 종속 변수
->키, 몸무게, 연간 소득과 같이 변하는 양을 표현한 것

상관관계 (correlation coefficient)
-> 두 개의 변수들이 함께 변화하는 관계

상관 게수
-> 변수들 사이의 상관관계의 정도를 나타내는 수치

상관관계가 있는 두 변수가 있을 때
한 값이 증가 할 때 다른 값도 증가할 경우 양의 상관관계
반대의 경우 음의 상관관계

!! 상관 관계와 인과관계는 다른것임 !!
corrcoef(x, y)
'''

import numpy as np

np.random.seed(85)
# 동일한 결과를 얻기 위해 85라는 초기값 사용

x= np.arange(0, 10)
y1 = x*2

np.corrcoef(x,y1)
'''
array([[1., 1.],
       [1., 1.]]) 
'''

x= np.arange(0, 10)

y2= x**3

y3 = np.random.randint(0,100, size=10)

np.corrcoef(x,y3)
'''
array([[1.       , 0.5002124],
       [0.5002124, 1.       ]])
'''


np.corrcoef(x,y2)
'''
array([[1.        , 0.90843373],
       [0.90843373, 1.        ]])
'''

np.corrcoef((x,y2, y3))
'''
array([[1.(x x)관계, 0.90843373, 0.5002124 ],
       [0.90843373, 1.(y2y2)관계, 0.43149426],
       [0.5002124 , 0.43149426, 1.(y3y3)관계]])
'''
result = np.corrcoef((x,y2,y3))

import matplotlib.pyplot as plt

plt.imshow(result)
plt.colorbar()
plt.show()


'''
seaborn 라이브러리
1. 팻플롯립을 기반
2. 맷플롯립에 비하여 높은 수준의 인터페이스 제공
3. import seaborn
'''

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# set_theme() : setyle = 테마명
sns.set_theme(style = 'darkgrid')

# load_dataset(): 기본 제공 데이터 로드
tips = sns.load_dataset('tips')

# relplot(): 산점도
# 점심시간, 저녁시간대의 식사비와 팁의 관계
sns.relplot(data=tips, 
           x='total_bill', y='tip',
           col='time',
           hue='smoker',
           style='smoker',
           size='size')

plt.savefig('test.png') # 이미지 저장하려면 show()전에 코드 쳐야됨
plt.show() 


# distplot(컬럼명): 히스토그램?
# kde = True : 가우시안 커널 밀도 추정을 선으로
# bins=숫자 : 구간 개수
sns.distplot(tips['tip'],
             kde=True,
             bins=20)
plt.show()


# 실제 식사 요금 대비 팁
tips['tip_pct'] = tips['tip'] / tips['total_bill']

sns.distplot(tips['tip_pct'],
             kde=True,
             bins=20)
plt.show()

# 산점도에 선형회귀선 시각화: regplot()
# data = 데이터프레임
# x = 컬럼, y = 컬럼
# 단, 변수에 저장해야됨
ax = sns.regplot(data=tips, x='total_bill', y='tip')
ax.set_xlabel('Total Bill')
ax.set_ylabel('Tip')
ax.set_title('Total Bill and Tip')
plt.show()



'''
pairplot()
여러 변수들 사이의 관계를 시각화
수치형 데이터를 가지고있는 컬럼 간의 관계

두 변수 a, b 
상관도가 높을경우 a 증가시 b 증가
상관도가 낮을 경우  b는 랜덤한 분포 또는 특정값에 몰림

전체 데이터프레임을 사용 할 수 있음
'''

sns.pairplot(tips, kind='hist')
plt.show()

'''
Anscombe's quartet 데이터 셋
'''
anscombe = sns.load_dataset('anscombe')
anscombe.head()

'''
lamplot(): 선형 회귀 직선을 구하는 기능
x =
y =
data = anscombe.query('dataset == I')
  dataset     x     y
0       I  10.0  8.04
1       I   8.0  6.95
2       I  13.0  7.58
3       I   9.0  8.81
4       I  11.0  8.33

'''
sns.lmplot(x='x', y='y',
           data=anscombe.query("dataset == 'I'"),
           ci=None,
           scatter_kws={'s':80})
plt.show()


sns.lmplot(x='x', y='y',
           data=anscombe.query("dataset == 'III'"),
           ci=None,
           order=2,
           scatter_kws={'s':80})
plt.show()

'''
flights 데이터셋
'''
flights = sns.load_dataset('flights')
sns.relplot(data=flights, x='year', y='passengers')
plt.show()
'''
x축은 년도->이산적으로 표시
y축은 승객 수
매년 전 세계의 비행기 이용자는 꾸준히 증가하는 추세
'''

sns.relplot(data=flights, x='year', y='passengers',
            kind='line')
plt.show()





























