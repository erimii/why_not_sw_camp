# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 17:07:35 2021
@author: Playdata


분석을 위해 사용되는 문법 및 사용 모듈
Python 기본 문법을 확인
Pandas와 Matplotlib의 기본적 사용법을 확인

분석 내용

국감브리핑 강남3구의 주민들이 
자신들이 거주하는 구의 체감 안전도를 높게 생각한다는 기사를 확인
http://news1.kr/articles/?1911504    

1. 서울시 각 구별 CCTV수를 파악하고, 
2. 인구대비 CCTV 비율을 파악해서 순위 비교
3. 인구대비 CCTV의 평균치를 확인하고 그로부터 CCTV가 과하게 부족한 구를 확인
4. 단순한 그래프 표현에서 한 단계 더 나아가 경향을 확인하고 시각화하는 기초 확인

"""
####################################################
### ------ 서울시 구별 CCTV 현황 분석하기  ----- ###
####################################################

#데이터 프레임 밑 csv, excel을 읽기 위한 모듈
import pandas as pd

# 숫자 관련 모듈
import numpy as np

# 시각화 작업 모듈
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 파이썬이 실행되고 있는 운영체제 관련 모듈
import platform

# --------------------------------------------------#
# =========  분석작업을 위한 1차 전처리 =========== #
# --------------------------------------------------#

### 1. 엑셀파일 읽기 - 서울시 CCTV 현황
CCTV_seoul = pd.read_csv("cctv_data/data1/01. CCTV_in_Seoul.csv", encoding='utf-8')

CCTV_seoul.columns
# Index(['기관명', '소계', '2013년도 이전', '2014년', '2015년', '2016년'], dtype='object')

# 컬럼명 변경
CCTV_seoul.rename(columns={CCTV_seoul.columns[0]:'구별'},
                 inplace=True)
CCTV_seoul.columns
# Index(['구별', '소계', '2013년도 이전', '2014년', '2015년', '2016년'], dtype='object')

### 2. 엑셀파일 읽기 - 서울시 인구현황
# 분석에 필요한 부분만 추출해서 읽기:
# header= 액셀 행(index)번호
# usecols = '엑셀컬럼명, 엑셀컬럼명,...'
# -> B:구이름, D:인구수, G:한국인, J:외국인, N:고령자

pop_seoul = pd.read_excel('cctv_data/data1/01. population_in_Seoul.xls', 
                          header=2,
                          usecols="B,D,G,J,N")

# 컬럼명 변경
pop_seoul.rename(columns={pop_seoul.columns[0]:'구별',
                          pop_seoul.columns[1]: '인구수',
                          pop_seoul.columns[2]: '한국인',
                          pop_seoul.columns[3]: '외국인',
                          pop_seoul.columns[4]: '고령자'},
                 inplace=True)
pop_seoul.head()

# --------------------------------------------------#
# ==== 분석작업을 위한 2차 전처리 : 데이터파악 ==== #
# --------------------------------------------------#

### 3. CCTV 데이터 파악하기
CCTV_seoul.head()

# '최근증가율' 컬럼 추가 : 2013년도 이전과 그 이후에 대한 증가률
# 증가율 = (2014년+2015년+2016년)/ 2013년도 이전 *100

CCTV_seoul['최근증가율'] =  (CCTV_seoul['2014년'] + CCTV_seoul['2015년'] + CCTV_seoul['2016년']) / CCTV_seoul['2013년도 이전']* 100

CCTV_seoul.sort_values(by='최근증가율', ascending=False).head()

### 4. 서울시 인구 데이터 파악하기
# 불필요한 행 삭제(합계에 해당하는 행)
pop_seoul.drop([0], inplace=True)

# 유일한 값인지 확인
pop_seoul['구별'].unique()

# 결측치 확인 및 삭제
pop_seoul[pop_seoul['구별'].isnull()]
pop_seoul.drop([26], inplace=True)

pop_seoul.tail()

# 외국인비율, 고령자비율 컬럼 추가
pop_seoul['외국인비율']=pop_seoul['외국인']/pop_seoul['인구수']*100
pop_seoul['고령자비율']=pop_seoul['고령자']/pop_seoul['인구수']*100

# --------------------------------------------------#
# =================== 분석작업 ==================== #
# --------------------------------------------------#

### 5. CCTV 데이터와 인구 데이터 합치고 분석하기
data_result = pd.merge(CCTV_seoul, pop_seoul, on='구별')

'''
만약, 두 개의 데이터프레임에 공통 컬럼명이 없을 경우
left_on=컬럼명, right_on=컬럼명 으로 merge가능
'''
# 불필요한 컬럼 제거
del data_result['2013년도 이전']
del data_result['2014년']
del data_result['2015년']
del data_result['2016년']

# 분석 작업 및 향후 시작화를 위해
# '구별' 컬럼의 데이터를 index값으로 설정
data_result.set_index('구별', inplace =True)

# 각 데이터간의 연관성을 위한 상관관계 확인
np.corrcoef(data_result['고령자비율'], data_result['소계'])
np.corrcoef(data_result['인구수'], data_result['소계'])

### 6. matplotlib를 이용하여 CCTV와 인구현황 그래프로 분석
# 한글 깨짐 방지를 위한 설정
plt.rcParams['axes.unicode_minus'] = False

# 운영체제에 맞는 기본 폰트 설정
if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")


# 구별 / 소계 데이터 시각화


# 소계를 기준으로 정렬시킨 후 시각화
plt.figure(figsize=(10, 10))
data_result['소계'].sort_values().plot(kind='barh', grid=True)
plt.xlabel('CCTV 개수')
plt.ylabel('서울시 구별')
plt.title('서울시 구별 CCTV 설치 현황')
plt.show()

# 인구대비 CCTV 비율 시각화
data_result['CCTV비율']= data_result['소계']/data_result['인구수'] *100

data_result['CCTV비율'].sort_values().plot(kind='barh',
                                           grid=True,
                                           figsize=(10,10))
plt.show() 



# 인구수와 CCTV 수 에 대한 산점도 시각화
plt.figure(figsize=(6,6))
plt.scatter(data_result['인구수'], data_result['소계'], s=50) #  s는 점 사이즈
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show()

# 인구수와 CCTV 수에 대한 산점도에 선형회귀선 시각화
# 선형회귀: 두가지 변수(컬럼)에 대한 관계
fp1 = np.polyfit(data_result['인구수'], data_result['소계'], 1)
f1 = np.poly1d(fp1)
fx = np.linspace(100000, 700000, 100)

plt.figure(figsize=(10,10))
plt.scatter(data_result['인구수'], data_result['소계'], s=50)
plt.plot(fx, f1(fx), ls='dashed', lw=3, color='r')
# ls -> line style
# lw -> line width
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show()

'''
결론: 서울시에서 다른 구에 비해 강남구, 양천구, 용산구, 서초구는 인구대비 cctv가 많고,
      그에 비해 강서구, 송파구 등은 이구대비 cctv 갯수가 부족하다
      따라서 강남 3구 전체가 안전하다고 볼수는 없다.
'''

### 7. 보다 설득력 있는 자료 작업
fp1 = np.polyfit(data_result['인구수'], data_result['소계'], 1)
f1 = np.poly1d(fp1)
fx = np.linspace(100000, 700000, 100)

# 오차구하기
data_result['오차'] = np.abs(data_result['소계'] - f1(data_result['인구수']))


df_sort = data_result.sort_values(by='오차', ascending = False)

# 시각화
plt.figure(figsize=(14,10))
plt.scatter(df_sort['인구수'], df_sort['소계'], c=data_result['오차'], s=50)
plt.plot(fx, f1(fx), ls='dashed', lw=3, color='r')

for n in range(10):
    plt.text(df_sort['인구수'][n]*1.02, # x 좌표
             df_sort['소계'][n]*0.98, # y 좌표
             df_sort.index[n], # 구이름
             fontsize=15)



plt.xlabel('인구수')
plt.ylabel('인구당비율')
plt.colorbar()
plt.grid()
plt.show()


















