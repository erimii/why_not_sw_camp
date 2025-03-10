# -*- coding: utf-8 -*-

'''
데이터 정제: 이상치 / 결측치
'''

'''
결측치 찾기 및 처리
'''

import pandas as pd
import numpy as np

df = pd.DataFrame({'sex' :['M','F',np.nan,'M','F'],
                    'score': [5,4,3,4,np.nan]})

df['score'] +1
'''
0    6.0
1    5.0
2    4.0
3    5.0
4    NaN
'''

pd.isna(df)
'''
     sex  score
0  False  False
1  False  False
2   True  False
3  False  False
4  False   True
'''

# 컬럼 별 결측치 확인
pd.isna(df).sum()
'''
sex      1
score    1
'''

'''
결측리 제거 / 대체(평균, 최소, 최대, 임의의 숫자)
'''
# 결측치 있는 행 제거: 데이터프레임.dropna(subset='컬럼지정')
# 원본데이터에 영향 미치지 않음.
df.dropna(subset = 'score')
'''
0    M    5.0
1    F    4.0
2  NaN    3.0
3    M    4.0
'''

# 결측치가 없는 데이터 추출
df_nomiss = df.dropna(subset = ['score', 'sex']) # = df.dropna()
'''
  sex  score
0   M    5.0
1   F    4.0
3   M    4.0.
'''

# 연산 시, 결측치 자동 배제하는 함수: mean()/sum()
df['score'].mean() # 4.0
df['score'].sum() # 16.0

# groupby(), agg() : 잡단(그룹)별 통계량
df.groupby('sex').agg(mean_score = ('score', 'mean'),
                       sum_socre = ('score', 'sum'))

'''
     mean_score  sum_socre
sex                       
F           4.0        4.0
M           4.5        9.0
'''

# 평균값으로 결측치 대체

exam = pd.read_csv('./data/exam.csv')
exam.loc[[2,7,14], ['math']] = np.nan

exam.isnull().sum()
'''
id         0
nclass     0
math       3
english    0
science    0
'''

exam['math']=exam['math'].fillna(int(exam['math'].mean()))
exam.isna().sum()

'''
이상치 정제
'''
df = pd.DataFrame({'sex' :[1,2,1,3,2,1],
                    'score': [5,4,3,4,2,6]})

'''
   sex  score
0    1      5
1    2      4
2    1      3
3    3      4
4    2      2
5    1      6
'''

# 이상치 확인: 데이터프레임.value_counts()
df['sex'].value_counts(sort=False).sort_index()
'''
1    3
2    2
3    1  <- 이상치
'''

df['score'].value_counts(sort=False).sort_index()
'''
score
2    1
3    1
4    2
5    1
6    1  <- 이상치
'''

# 이상치 -> 결측치로 변경: np.where()
# np.wher()는 문자와 nan을 함께 반환할 수 없다
df['sex'] = np.where(df['sex']==3, np.nan, df['sex'])
df['score'] = np.where(df['score']>5, np.nan, df['score'])
'''
   sex  score
0  1.0    5.0
1  2.0    4.0
2  1.0    3.0
3  NaN    4.0
4  2.0    2.0
5  1.0    NaN
'''

# sex, score 결측치 제거.sex로 그룹화.score평균 구하기
df.dropna(subset=['sex', 'score']).groupby('sex').agg(mean_score = ('score','mean'))
'''
     mean_score
sex            
1.0         4.0
2.0         3.0
'''

'''
boxplot을 이용한 이상치 확인 및 제거
'''
import matplotlib.pyplot as plt
import seaborn as sns

mpg = pd.read_csv('./data/mpg.csv')

mpg.shape
mpg.info()
mpg.describe()

sns.boxplot(data=mpg, y='hwy')
plt.show()

# 극단치 기준값 구하기
# 1. 1사분위수, 3사분위수
pct25 = mpg['hwy'].quantile(.25)
# 18.0

pct75 = mpg['hwy'].quantile(.75)
# 27.0


# 2. IQR 구하기: 1사분위수, 3사분위수의 거리
iqr = pct75 - pct25

# 3. 극단 경계 : 하한(1사분위-1.5*IQR), 상한 구하기(3사분위+1.5*IQR)
min_b = pct25 - 1.5*iqr # 4.5
max_b = pct75 + 1.5*iqr # 40.5

# 극단치를 결측 처리
mpg['hwy'] = np.where((mpg['hwy']<min_b)|(mpg['hwy']>max_b), np.nan,mpg['hwy'])

# 결측치 확인
mpg['hwy'].isna().sum()
# 3

# mpg['hwy']결측치 제거.'drv'로 그룹화. 평균구하기
mpg.dropna(subset = 'hwy').groupby('drv').agg(mean_hwy = ('hwy', 'mean'))
'''
      mean_hwy
drv           
4    19.174757
f    27.728155
r    21.000000
'''

#----------정리----------
## 1. 결측치 정제하기
# 결측치 확인
# 결측치 제거 / 대체
# 여러 변수 동시에 결측치 제거

## 2. 이상치 정제하기
# 이상치 확인
# 이상치 결측 처리
# 결측치 정제하기

# 상자 그림으로 극단치 기준값 찾기
# 1사분위수
# 3사분위수
# IQR
# 하한
# 상한
# 극단치 결측 처리















