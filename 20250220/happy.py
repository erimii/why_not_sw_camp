# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:41:12 2025

@author: Admin
"""
'''
```
시도별 행복 지수 요소별 시각화 : 선 그래프

행복 지수 요소별 각각 시각화 : 막대 그래프 (서브플롯 반드시 사용)

행복 지수 요소간의 상관관계 시각화 : 히트맵

행복지수가 '시도'별 지역에 따라 얼마나 차이가 나는지 시각화 : 선 그래프
    시도별 행복 지수 요소별 시각화 
8개의 요소들을 구분하여 시각화 : 세로 막대 그래프의 서브플롯 반드시 사용
8개의 요소들의 데이터 범위를 다양한 색상으로 출력 : 시본(Seaborn) 히트맵
    행복 지수 요소간의 상관관계 시각화
```
'''

import pandas as pd

health = pd.read_excel('data/대한민국행복지도_건강.xlsx')
economy = pd.read_excel('data/대한민국행복지도_경제.xlsx')
society = pd.read_excel('data/대한민국행복지도_관계및사회참여.xlsx')
education = pd.read_excel('data/대한민국행복지도_교육.xlsx')
satisfaction = pd.read_excel('data/대한민국행복지도_삶의만족도.xlsx')
safety = pd.read_excel('data/대한민국행복지도_안전.xlsx')
leisure = pd.read_excel('data/대한민국행복지도_여가.xlsx')
environment = pd.read_excel('data/대한민국행복지도_환경.xlsx')


health.isnull().sum()
economy.isnull().sum()
society.isnull().sum()
education.isnull().sum()
satisfaction.isnull().sum()
safety.isnull().sum()
leisure.isnull().sum()
environment.isnull().sum()


health.info()
economy.info()
society.info()
education.info()
satisfaction.info()
safety.info()
leisure.info()
environment.info()


health= health.iloc[:,0:4].rename(columns={'평균': '건강_평균'})
economy=  economy[['No', '평균']].rename(columns={'평균': '경제_평균'})
society= society[['No', '평균']].rename(columns={'평균': '사회_평균'})
education= education[['No', '평균']].rename(columns={'평균': '교육_평균'})
satisfaction= satisfaction[['No', '삶의 만족도']].rename(columns={'삶의 만족도': '만족도_평균'})
safety= safety[['No', '평균']].rename(columns={'평균': '안전_평균'})
leisure= leisure[['No', '평균']].rename(columns={'평균': '여가_평균'})
environment= environment[['No', '평균']].rename(columns={'평균': '환경_평균'})

mg = pd.merge(health, economy, on='No', how='left')
mg = pd.merge(mg, society, on='No', how='left')
mg = pd.merge(mg, education, on='No', how='left')
mg = pd.merge(mg, satisfaction, on='No', how='left')
mg = pd.merge(mg, safety, on='No', how='left')
mg = pd.merge(mg, leisure, on='No', how='left')
mg = pd.merge(mg, environment, on='No', how='left')

mg.info()
# mg['모든행복지수평균'] = mg[['건강_평균', '경제_평균','사회_평균', '교육_평균', '만족도_평균', '안전_평균', '여가_평균', '환경_평균']].mean(axis=1)


# 시도별 행복 지수 요소별 시각화 : 선 그래프
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    
    
sido_avg  = mg.groupby('시도')[['건강_평균', '경제_평균', '사회_평균', '교육_평균', 
                               '만족도_평균', '안전_평균', '여가_평균', '환경_평균']].mean().reset_index()

# 그래프 스타일 설정
plt.figure(figsize=(10, 5))
sns.lineplot(x='시도', y='건강_평균', data=sido_avg, marker='o', color='b')
sns.lineplot(x='시도', y='경제_평균', data=sido_avg, marker='o', color='r')
sns.lineplot(x='시도', y='사회_평균', data=sido_avg, marker='o', color='pink')
sns.lineplot(x='시도', y='교육_평균', data=sido_avg, marker='o', color='yellow')
sns.lineplot(x='시도', y='만족도_평균', data=sido_avg, marker='o', color='green')
sns.lineplot(x='시도', y='안전_평균', data=sido_avg, marker='o', color='black')
sns.lineplot(x='시도', y='여가_평균', data=sido_avg, marker='o', color='skyblue')
sns.lineplot(x='시도', y='환경_평균', data=sido_avg, marker='o', color='darkblue')

# 그래프 제목 및 라벨 추가
plt.title('시도별 평균 행복지수 변화', fontsize=14)
plt.xlabel('시도', fontsize=12)
plt.ylabel('행복지수', fontsize=12)
plt.xticks(rotation=45)  # 시도 이름이 길 경우 회전
plt.grid(True)

# 그래프 출력
plt.show()







# 행복 지수 요소별 각각 시각화 : 막대 그래프 (서브플롯 반드시 사용)
plt.style.use("ggplot")


factors = ['건강_평균', '경제_평균', '사회_평균', '교육_평균', '만족도_평균', '안전_평균', '여가_평균', '환경_평균']

# 서브플롯 크기 설정
fig, axes = plt.subplots(2, 4, figsize=(20, 10))  # 2행 4열 서브플롯
axes = axes.flatten()  # 2D 배열을 1D 리스트로 변환

# 각 행복지수 요소별 막대 그래프 그리기
for i, factor in enumerate(factors):
    sns.barplot(x=mg["시도"], y=mg[factor], ax=axes[i], palette="Blues")
    axes[i].set_title(factor)  # 그래프 제목
    axes[i].set_xticklabels(mg["시도"], rotation=45)  # X축 라벨 회전

plt.tight_layout()  # 그래프 간격 조정
plt.show()

# 행복 지수 요소간의 상관관계 시각화 : 히트맵
import matplotlib.pyplot as plt
import seaborn as sns

# 상관관계 계산 (행복지수 요소만 선택)
correlation_matrix = mg[['건강_평균', '경제_평균', '사회_평균', '교육_평균', 
                         '만족도_평균', '안전_평균', '여가_평균', '환경_평균']].corr()

# 히트맵 시각화
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

# 그래프 제목 설정
plt.title("행복 지수 요소 간 상관관계", fontsize=15)

# 그래프 출력
plt.show()































