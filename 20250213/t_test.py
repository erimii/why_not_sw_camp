# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:36:33 2025

@author: Admin
"""

'''
통계 분석 기법을 이용한 가설 검정

가설 검정이란?
통계분석 : 기술통계, 추론통계

기술통계 : 데이터를 요약해서 설명하는 통계분석기법
    예) 월급을 집계해서 월급의 평균 구하기
추론통계: 어떤 값이 발생할 확률을 계산하는 통계분석기법
    예) 성별에 따라 월급차이가 있는 것으로 나타냈을때,
        이 차이가 우연히 발생할 확률을 계산
        만약, 이 차이가 우연히 발생할 확률이 적다면,
        성별에 따른 월급 차이가 통계적으로 유의하다 라고 결론.
    
    * 데이터를 이용해서 신뢰할 수 있는 결론을 내리려면 
    유의확률을 계산하는 통계적 가설 검정 절차를 거쳐야 한다
    
    통계적 가설 검정: 유의확률을 이용하여 가설을 검정하는 방법
    
    유의확률: 실제로는 집단간의 차이가 없는데,
            우연히 차이가 있는 데이터가 추출될 확률
        통계분석 결과,
        유의 확률이 크게 나타났다면
        -> 집단 간의 차이가 통게적으로 유의하지 않다
        
        통계적 가설 검정 방법:
            두 집단간의 평균의 차이가 있는지 검정하는 t 검정
            두 집단간의 관련이 있는지 검정하는 상관분석
'''




### compact 자동차와 suv 자동차의 도시 연비(cty)에 대한 t검정

import pandas as pd

mpg = pd.read_csv('./data/mpg.csv')

## 기술 통계 분석
# compact, suv 추출
# category별 분리
# 빈도 구하기
# cty평균 구하기

mpg.query('category in ["compact", "suv"]') \
    .groupby('category', as_index=False) \
    .agg(n=('category', 'count'), mean=('cty', 'mean'))

'''
  category   n      mean
0  compact  47  20.12766
1      suv  62  13.50000
'''

## t검정
# mpg에서 category가 'compact' -> cty
# mpg에서 category가 'suv' -> cty

compact = mpg.query('category == "compact"')['cty']
suv = mpg.query('category == "suv"')['cty']

# t-test
# equal_var = True : 집단(변수)간의 분산 같다
from scipy import stats

stats.ttest_ind(compact, suv, equal_var = True)
'''
TtestResult(statistic=11.917282584324107, 
            pvalue=2.3909550904711282e-21, -> e-21은 앞에 0이 21개 있다는 뜻
            df=107.0)

pvalue: 유의확률

일반적으로 유의확률 5% 판단 기준
pvalue 0.05 미만이면 집단각 차이가 통계적으로 유의하다

compact와 suv간 평균 도시연비 차이가 통계적으로 유의하다
'''


### 일반 휘발유(r)와 고급 휘발유(p)의 도시 연비(cty)에 대한 t검정
## 기술 통계 분석
# r, q 추출하기
# f1별 분리
# 빈도 구하기
# cty 평균 구하기

mpg.query('fl in ["r", "p"]') \
    .groupby('fl', as_index = False) \
    .agg(n = ('category', 'count'),
         mean = ('cty', 'mean'))
'''
  fl    n       mean
0  p   52  17.365385
1  r  168  16.738095
'''

regular = mpg.query('fl == "r"')['cty']
premium = mpg.query('fl == "p"')['cty']

stats.ttest_ind(regular, premium, equal_var=True)
'''
TtestResult(statistic=-1.066182514588919, 
            pvalue=0.28752051088667036, 
            df=218.0)
pvalue->28%
=> 실제로는 차이가 없는데 우연에 의해 차이가 관찰될 학률이 28.75% 라는 의미

일반 휘발유와 고급 휘발유를 사용하는 도시연비차이가
통계적으로 유의하지 않다

고급 휘발유 도시 연비 평균이 0.6정도 높지만
이런 정도의 차이는 우연히 발생했을 가능성이 크다
'''


# ------------------------------------------------------------


'''
상관분석 - 두 변수의 관계 분석하기

상관분석을 통해 도출한 상관계수 값으로 판단 가능(관련성 여부)

상관계수: 0~1 사이의 값
         1에 가까울수록 관련성이 크다
         양수면 정비례 / 음수면 반비례
'''
## 실업자 수(unemploy)와 개인 소비 지출(pce)의 상관관계

economics = pd.read_csv('./data/economics.csv')

# 상관계수: corr()
economics[['unemploy', 'pce']].corr()
'''
상관행렬
          unemploy       pce
unemploy  1.000000  0.614518
pce       0.614518  1.000000
'''

# 유의확률 구하기 : stats.pearsonr()
stats.pearsonr(economics['unemploy'], economics['pce'])
'''
PearsonRResult(statistic=0.6145176141932082, <- 상관계수
               pvalue=6.773527303289964e-61) <- 유의확률


'''


### 상관행렬 히트맵 : mtcars.csv 사용
mtcars = pd.read_csv('./data/mtcars.csv')
mtcars.head(3)
'''
    mpg  cyl   disp   hp  drat     wt   qsec  vs  am  gear  carb
0  21.0    6  160.0  110  3.90  2.620  16.46   0   1     4     4
1  21.0    6  160.0  110  3.90  2.875  17.02   0   1     4     4
2  22.8    4  108.0   93  3.85  2.320  18.61   1   1     4     1
'''

# 상관행렬 만들기
car_cor = mtcars.corr()

# 소수점 둘째 자리까지 반올림
car_cor = round(car_cor, 2)

import matplotlib.pyplot as plt
import seaborn as sns

# 해상도 설정
plt.rcParams.update({'figure.dpi': '120',
                     'figure.figsize': [7.5, 5.5]})

# 히트맵: sns.heatmap(상관행렬, 상관계수 표시, 컬러맵)
# 상관계수 표시: annot: True
# 컬러맵: cmap='RdBu'
sns.heatmap(car_cor, annot=True, cmap='RdBu')
plt.show()

## 대각행렬 제거
# mask 만들기
import numpy as np
mask = np.zeros_like(car_cor)

# 오른쪽 위 대각 행렬을 1로 바꾸기
mask[np.triu_indices_from(mask)] = 1

# 히트맵 mask 적용: 
sns.heatmap(data=car_cor, 
            annot=True, 
            cmap='RdBu',
            mask = mask)

plt.show()

## 빈 행과 열 제거하기
# mask 첫번째 행, 마지막 열 제거
# 상관행렬 첫번째 행, 마지막 열 제거
mask_new = mask[1:, :-1]
cor_new = car_cor.iloc[1:, :-1]

sns.heatmap(data=cor_new, 
            annot=True, 
            cmap='RdBu',
            mask = mask_new)

plt.show()











































