# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:59:48 2025

@author: Admin
"""
'''
의로(심부전) 데이터 분석 프로젝트

1. 의료 데이터 프로젝트 소개:
2. 의료 데이터셋 파악:
3. 심부전 데이터셋 필터링:
4. 심부전 데이터셋 결측치 처리:
5. 심부전 데이터셋 통계 처리:
6. 심부전 데이터 셋 시각화:
'''

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

heart = pd.read_csv('./data/heart.csv')

list(heart.columns)
'''
['Age',
 'Sex',
 'ChestPainType',
 'RestingBP',
 'Cholesterol',
 'FastingBS',
 'RestingECG',
 'MaxHR',
 'ExerciseAngina',
 'HeartDisease']
'''

heart.info()
'''
RangeIndex: 918 entries, 0 to 917
Data columns (total 10 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   Age             918 non-null    int64  
 1   Sex             918 non-null    object 
 2   ChestPainType   918 non-null    object 
 3   RestingBP       891 non-null    float64   -> 결측치 존재
 4   Cholesterol     918 non-null    int64  
 5   FastingBS       827 non-null    float64   -> 결측치 존재
 6   RestingECG      918 non-null    object 
 7   MaxHR           918 non-null    int64  
 8   ExerciseAngina  918 non-null    object 
 9   HeartDisease    916 non-null    float64   -> 결측치 존재
dtypes: float64(3), int64(3), object(4)
'''

# 논리형 인덱싱으로 데이터 필터링
# 제일 중요한 변수 : HeartDisease
# HeartDisease : 심장병 여부 (1/0) 1만 뽑기
H = heart[ heart['HeartDisease'] == 1]
H.shape


# 결측치가 차지하는 비율에 따라 결측치 처리
for i in heart.columns:
    missingValueRate = heart[i].isna().sum() / len(H) * 100
    
    if missingValueRate > 0 :
        print(f'{i} null rate: {round(missingValueRate,2)}')
'''
RestingBP null rate: 5.33
FastingBS null rate: 17.95
HeartDisease null rate: 0.39

RestingBP: 혈압
FastingBS: 공복상태 혈당 / 120 이상이면 1
심장병 여부 (1/0)
'''

# 'HeartDisease' 결측치 제거
heart = heart.dropna(subset='HeartDisease')

# 'FastingBS' 최빈값인 0으로 대체
heart['FastingBS'].value_counts()
'''
0.0    303
1.0    167
'''
heart['FastingBS'] = heart['FastingBS'].fillna(0)

# 'RestingBP'중앙값으로 대체
heart['RestingBP'] = heart['RestingBP'].replace(np.nan, heart['RestingBP'].median())


"""--------------------------------
심부전 데이터셋 통계처리
-----------------------------------
1. MaxHR 평균값과 중앙값
2. ChestPainType 열의 빈도수
3. 심부전 데이터 셋 Age, MaxHR, Cholesterol열의 주요 통계량 요약
4. 그룹 별 집계
4-1. 심부전 데이터셋의 HeartDisease, ChestPainType 열로 그룹화 후,
    MaxHR, Cholesterol 열의 평균
4-2. Sex 열로 그룹화 한 후, RestingBP 열의 평균
"""

# MaxHR 평균값과 중앙값
heart['MaxHR'].mean() # 136.83078602620088
heart['MaxHR'].median() # 138.0
'''
평균값과 중앙값이 비슷하다는 것은 데이터에 대한 극단적인 이상치가 없음을 뜻함
큰 왜곡 없이 고르게 분포돼있음
'''
# ChestPainType 열의 빈도수
heart['ChestPainType'].value_counts()
'''
ChestPainType
ASY    496 <- 무증상
NAP    202 <- 비협심증 흉통
ATA    172 <- 비전형적인 협심증
TA      46 <- 전형적인 협심증
-> 무증상이 다른 유형에 비해 훨씬 빈번하게 발생
'''

# Age, MaxHR, Cholesterol열의 주요 통계량 요약
heart[['Age', 'MaxHR', 'Cholesterol']].describe()
'''
              Age       MaxHR  Cholesterol
count  916.000000  916.000000   916.000000
mean    53.533843  136.830786   198.728166
std      9.425923   25.447917   109.466452
min     28.000000   60.000000     0.000000
25%     47.000000  120.000000   173.000000
50%     54.000000  138.000000   223.000000
75%     60.000000  156.000000   267.000000
max     77.000000  202.000000   603.000000

Age mean : 53.533843 <- 대부분 50대 초반
'''

# 그룹별 집계
# 1. HeartDisease
#   1-2. ChestPainType
#-> Age, MaxHR, Cholesterol 의 mean() 구하기
HD_CPT = heart.groupby(['HeartDisease', 'ChestPainType']) \
                [['Age', 'MaxHR', 'Cholesterol']].mean()

'''
                                  Age       MaxHR  Cholesterol
HeartDisease ChestPainType                                    
0.0          ASY            52.317308  138.548077   226.865385
             ATA            48.236486  152.621622   232.668919
             NAP            51.045802  150.641221   221.503817
             TA             54.692308  150.500000   222.730769
1.0          ASY            55.660714  125.806122   175.974490
             ATA            55.958333  137.500000   233.291667
             NAP            57.549296  129.394366   153.281690
             TA             55.000000  144.500000   186.700000
-> 심장병 없는 사람의 나이, 심박수, 콜레스테롤 수치가 
각각 어떠한 흉통 유형에 따라 달라지는 지를 확인 할 수 있다
'''

# 성별에 따른 혈압
SG = heart.groupby('Sex')['RestingBP'].mean()
'''
Sex
F    132.192708
M    132.473757
-> 별 차이 없음. 유의미 하지 않음

참고:
    연령대 그룹
    콜레스테롤 구간 분류
    복합 위험도: 고혈압 / 콜레스테롤 / 고혈당 -> 동시에 가진 환자의 위험도
    운동 관련 변수 : 운동시 심장 스트레스의 영향 : 이진 변수
    심전도 결과 : 이진변환-> 심전도 결과와 심전도 발생 위험
    최대 심박수의 비율 계산 -> 심장 운동능력 측정(나이)
'''



"""--------------------------------
시각화
-----------------------------------
"""
# 심전부 색깔 시각화
sns.palplot(['#003399', '#0099FF', '#00FFFF', '#CCFFFF'])
plt.show()

# 심전부 파이 차트: 'ChestPainType' 변수: 흉통 유형
# ratio: 'ChestPainType' 추출 후 1차원으로 변경

ratio = heart['ChestPainType'].value_counts()

plt.figure(figsize=(5,5))
plt.pie(x = ratio,
        labels= ratio.index,
        autopct='%0.f%%',
        startangle=90,
        explode=[0.05, 0.05, 0.05, 0.05],
        shadow=True,
        colors=['#003399', '#0099FF', '#00FFFF', '#CCFFFF'])

plt.suptitle('Chest Pain Type', fontfamily='serif', fontsize=15)
plt.title('ASY, NAP, ATA, TA', fontfamily='serif', fontsize=11)
plt.show()
'''
ASY(무증상): 무증상 흉통을 고려해야한다.
NAP, ATA(비전형적): 심장병 판단 시, 흉통 유형을 세밀하게 분석해야 한다
TA: 전형적인 흉통 증상이 드물다
'''

# 심부전증이 있을 때와 없을 때,
# 항상 ASY인 무증상이 압도적인지 궁금
# 'HeartDisease' 여부에 따른 'ChestpainType' 막대 시각화

# countplot(): 각 범주(심장병 여부)에 속하는
#               데이터(흉통 유형)의 개수를 막대 시각화
#data: cuntplot에서 사용할 데이터 셋
# x : HeartDisease
# hue: 특정 열 데이터로 색상을 구분
# hue_order: 색상 순서 수동 :'ASY, 'NAP', 'ATA', 'TA'

# x축 눈금 설정
#plt.xticks([0,1], ['',''])

# plt.tight_layout(): 겹치지 않도록 최소한의 여백을 만듬


plt.figure(figsize=(12,5))
sns.countplot(data=heart,
              x = 'HeartDisease',
              hue = 'ChestPainType',
              hue_order=['ASY', 'NAP', 'ATA', 'TA'],
              palette = ['#003399', '#0099FF', '#00FFFF', '#CCFFFF'])

plt.suptitle('Chest Pain Types / Heart Disease')
plt.title('ASY, NAP, ATA, TA')
plt.xticks([0,1], ['without heart disease', 'heart disease'])
plt.tight_layout()
plt.show()
'''
심장병 없는 사람: 비 전형적인 흉통
    -> 비환자들에게도 심장 건강에 대한 경각심 일꺠워주기
    -> 비환자들에게도 심장 검진이 필요하다고 알려줘야됨
심장병 있는 사람: 무증상
    -> 심장 실환과 흉통 유형간의 강한 관련성이 있음
    -> 심장병이 심각한 단계에 이를 때 까지 증상이 나타나지 않을 수 있다
    -> 무증상 환자에 대한 모니터링 강화 및 조기 검진 필요
'''

# 심부전 데이터영역 그래프
# 나이에 따른 심부전 여부 수치화
Heart_Age = heart.groupby('Age')['HeartDisease'] \
            .value_counts().unstack(level='HeartDisease')

Heart_Age.head(6)
'''
HeartDisease  0.0  1.0
Age                   
28            1.0  NaN
29            3.0  NaN
30            1.0  NaN
31            1.0  1.0
32            3.0  2.0
33            1.0  1.0
'''
plt.figure(figsize=(15,5))

# plt.fill_between(): x 축을 기준으로 그래프 영역 채움
# x : 곡선을 정의하는 노드의 x좌표
# y1: 첫 번째 곡선을 정의하는 노드의 y좌표
# y2: 두 번째 곡선을 정의하는 노드의 y좌표
# alpha: 투명도
# label: 범례에 표시할 문자열

# 심장병이 없는 환자들의 나이별 숫자 시각화
plt.fill_between(x=Heart_Age[0].index, 
                 y1=0, # y좌표의 0부터 그래프 영역을 채워라
                 y2 = Heart_Age[0], # 0컬럼에 대응하는 값
                 color = '#003399',
                 alpha = 0.8,
                 label='Normal')

# 심장병이 있는 환자들의 나이별 숫자 시각화
plt.fill_between(x=Heart_Age[1].index, 
                 y1=0, # y좌표의 0부터 그래프 영역을 채워라
                 y2 = Heart_Age[1],
                 color = '#003399',
                 alpha = 0.4,
                 label='heart disease')

plt.legend()
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Heart_Age')
plt.show()


# 심부전 범주형 산점도 그래프: sns.swarmplot()
# H_0: 심장병이 없는 환자의 데이터 추출 HeartDisease == 0
# H_1: 심장병이 있는 환자의 데이터 추출 HeartDisease == 1
H_0 = heart[heart['HeartDisease'] == 0]
H_1 = heart[heart['HeartDisease'] == 1]

# 그래프 객체 생성(2개의 subplot 생성)
fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(1,2,1) # 1행 2열의 1
ax2 = fig.add_subplot(1,2,2) # 1행 2열의 2

# RestingECG / ExerciseAngina
# H_0에서 Age별 RestingBP 수치에 따른 ExerciseAngina 여부
sns.swarmplot(x = 'RestingECG',
              y = 'Age',
              data= H_0,
              ax = ax1,
              hue = 'ExerciseAngina',
              palette=['#003399', '#0099FF'],
              hue_order = ['Y', 'N']
              )

# H_1에서 Age별 RestingBP 수치에 따른 ExerciseAngina 여부
sns.swarmplot(x = 'RestingECG',
              y = 'Age',
              data= H_1,
              ax = ax2,
              hue = 'ExerciseAngina',
              palette=['#003399', '#0099FF'],
              hue_order = ['Y', 'N']
              )

ax1.set_title('Without heart disease')
ax2.set_title('With heart disease')
plt.show()


# 심부전 워드 클라우드
# 심부전관련 논문의 제목 데이터
pubmed_title = pd.read_csv('./data/pubmed_title.csv')

from wordcloud import WordCloud
from PIL import Image

plt.figure(figsize=(15,5))

# pubmed_title['title']을 list로 변환시킨 후 str로 변환
text = str(list(pubmed_title['Title']))

# logo image 갖고오고 Image.open()
# image를 넘파이 배열로 변환해줘야됨 np.array()
mask = np.array(Image.open('./data/image.jpg'))
# mask = : 단어를 그릴 위치 설정, 흰색 항목은 마스킹 된 것으로 간주

# 색상맵
cmap = plt.matplotlib.colors.LinearSegmentedColormap \
        .from_list('', ['#000066','#003399', '#00FFFF'])

# 워드클라우드 생성
wordcloud = WordCloud(background_color='white',
                      width = 2500, height = 1400,
                      max_words = 170,
                      mask = mask,
                      colormap=cmap).generate(text)

plt.suptitle('Heart Disease WordCloud',
             fontweight='bold', fontfamily='serif', fontsize=15)
plt.title('Pubmed site: Heart Failure')
# 워드클라우드 결과를 plots 창에 나타내기
plt.imshow(wordcloud)
plt.axis('off') # 축 감추기
plt.show()
























