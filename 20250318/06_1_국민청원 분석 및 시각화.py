# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:40:22 2025

@author: Admin

국민청원 데이터 분석하기

"""
### 데이터 분석을 위한 판다스, 수치 계산을 위한 넘파이 불러오기
import pandas as pd
import numpy as np

# 출력 데이터를 깔끔하게 표시하기 위해
import warnings
warnings.filterwarnings('ignore')


### 시각화 도구로 plotnine(A grammar of graphics for Python)을 사용
# pip install plotnine
from plotnine import *


### 판다스로 데이터 불러오기
'''
petition.csv : 전체 데이터

petition_corrupted.csv
전체 행 중에서 5%는 임의 필드 1개에 결측치 삽입
범주(category)가 '육아/교육'이고 투표수(votes)가 50건 초과이면 20% 확률로 투표수에 결측치 넣기
나머지는 전체 데이터와 동일

petition_sampled.csv
전체 데이터 중 5%만 임의추출한 데이터

petition_corrupted_sampled.csv
결측치가 삽입된 샘플 데이터

petition_corrupted.csv : 파일에서 5%만 임의추출하여 생성
'''
import os
import platform

base_path = "data"
file_name = "petition.csv"

### 다운로드 받은 데이터 살펴보기
petitions = pd.read_csv(f"{base_path}/petition.csv", 
                        index_col="article_id",
                        parse_dates=['start', 'end'])

# 데이터의 행과 열의 수 확인
petitions.shape

# 데이터셋의 정보를 볼 수 있다.
# 어떤 컬럼이 있고 몇 개의 데이터가 있으며 어떤 타입인지 볼 수 있다.
petitions.info()


# head를 통해 상위 몇 개의 데이터만을 본다.
# 기본은 5개를 불러오며, 괄호안에 숫자를 적어주면 숫자만큼 불러온다.
petitions.head()
petitions.tail()

# 데이터프레임의 컬럼만을 불러올 수 있다.
petitions.columns

# 숫자로 된 데이터에 대해 count, mean, std, min, max값 등을 볼 수 있다.
petitions.describe()


### 결측치가 있는지 확인v
petitions.isnull().sum()
# content에만 1이 있고 나머지는 모두 0이므로 결측치가 없다.



### 판다스로 데이터 분석과 시각화

'''
답변대상 청원 행 다시 만들기

기존의 answerd 항목은 
청와대에서 답변을 했는지 여부를 알 수 있는 행이다. 

그런데 데이터 중에는 
답변 대기 중인 청원도 있으므로 이를 확인해야 한다. 

비교연산자(==)를 이용해 
20만개 이상의 동의를 받아 답변 대상인 청원에 대해 
answer라는 새로운 행을 추가해 주었다.
'''
(petitions['votes'] > 200000) == 1

petitions['answer'] = (petitions['votes'] > 200000) == 1
petitions.shape


petitions.head(3)


### 청원기간 컬럼 생성
petitions['duration'] = petitions['end'] - petitions['start']
petitions.sort_values('duration', ascending=True).head(3)


### 청원기간별 건
petitions['duration'].value_counts()

# 청원기간이 90일이고 답변 대상 건
petitions[(petitions['duration'] == '90 days') & (petitions['answer'] == 1)]


# 청원기간이 60일이고 답변 대상 건
petitions_60_answer = petitions[(petitions['duration'] == '60 days') & (petitions['answer'] == 1)]
print(petitions_60_answer.shape)
petitions_60_answer.head()

# 청원기간이 30일이고 답변 대상 건
petitions_30_answer = petitions[(petitions['duration'] == '30 days') \
                                    & (petitions['answer'] == 1)]
print(petitions_30_answer.shape)
petitions_30_answer.head(3)


# 청원기간이 7일이고 답변 대상 건
petitions_7_answer = petitions[(petitions['duration'] == '7 days') \
                                   & (petitions['answer'] == 1)]
print(petitions_7_answer.shape)

petitions_7 = petitions[(petitions['duration'] == '7 days')]
print(petitions_7.shape)

petitions_7_count = petitions_7['start'].value_counts().reset_index()
petitions_7_count.columns = ['start', 'count']
petitions_7_count.sort_values('start', ascending=True)



### 청원 기간과 분야별 분석
# 어느 분야의 청원이 가장 많이 들어왔는지 확인

category = pd.DataFrame(petitions['category'].value_counts()).reset_index()
category.columns = ['category', 'counts']
category



### 청원이 얼마 동안 집계되었는지
start_df = pd.DataFrame(petitions['start'].value_counts()).reset_index()
start_df.columns = ['start', 'counts']
start_df = start_df.sort_values('counts', ascending=False)
print('청원 집계: {}일'.format(start_df.shape[0]))

start_df.head()



### 피봇 테이블로 투표를 가장 많이 받은 분야 보기
petitions_unique = pd.pivot_table(petitions, index=['category'], values=['votes'], aggfunc=np.sum)
#petitions_unique = pd.pivot_table(petitions, index=['category'], aggfunc=np.sum)
petitions_best = petitions_unique.sort_values(by='votes', ascending=False).reset_index()
petitions_best



### 투표를 가장 많이 받은 날
petitions_start = pd.pivot_table(petitions, index=['start'], values=['votes'], aggfunc=np.sum)
votes_df = petitions_start.sort_values(by='votes', ascending=False)
votes_df.loc[petitions_start['votes'] > 350000]



### 청원을 많이 받은 날 VS 투표를 많이 받은 날
# 인덱스로 되어있는 start를 키로 사용하기 위해 
# index로 설정된 start를 컬럼으로 변경해주고 인덱스를 생성한다.
votes_df = votes_df.reset_index()
votes_df.head()


hottest_day_df = start_df.merge(votes_df, on='start', how='left')

hottest_day_df.nlargest(5, "votes")
hottest_day_df.nlargest(5, "counts")


### 답변 대상 청원
# 20만건 이상의 투표를 받으면 답변을 받을 수 있는 청원이 된다.
answered_df = petitions.loc[petitions['votes'] > 200000]
print('답변 대상 청원: {}건'.format(answered_df.shape[0]))

answered_df.head()



### 답변 대상 청원 중 투표를 가장 많이 받은 것
answered_df.sort_values('votes', ascending=False).head(10)



### 시각화
# A Grammar of Graphics for Python — plotnine
# 카테고리별로 집계된 데이터를 barplot으로 그려본다.
# 그런데 한글이 깨져보이는 것을 볼 수 있다.
(ggplot(petitions)
 + aes('category')
 + geom_bar(fill='green')
)


# 시각화를 위해 한글폰트 설치
import koreanize_matplotlib

 
font_family = 'NanumGothic'
font_family

# 글씨가 겹쳐보이지 않도록 rotation도 추가.
(ggplot(petitions)
 + aes('category')
 + geom_bar(fill='green')
 + theme(text=element_text(family=font_family),
        axis_text_x=element_text(rotation=60))
)



### 카테고리별 투표수
# coord_flip을 사용해서 x축과 y축을 플립.
(ggplot(petitions)
 + aes(x='category', y='votes')
 + geom_col(fill='skyblue')
 + ggtitle('카테고리별 투표수')
 + coord_flip()
 + theme(text=element_text(family=font_family))
)


# 투표를 가장 많이 받은 카테고리인 인권/성평등에서 투표수가 많은 순으로 보기
human = petitions.loc[(petitions['category']=='인권/성평등')]
human.sort_values('votes', ascending=False)[:2]


# 일별 투표수
petition_votes = petitions.groupby(['start'])['votes'].sum().reset_index()
petition_votes.columns = ['start', 'votes']
petition_votes.head()

(ggplot(petition_votes)
 + aes(x='start', y='votes')
 + geom_point()
 + geom_line(color='blue')
 + labs(x='날짜', y='투표 수', title='일별 투표 수')
 + theme(text=element_text(family=font_family),
        figure_size=(12,6),
        axis_text_x=element_text(rotation=60))
)
# 2018년 10월 17일이 투표가 가장 많았기 때문에 일별 투표 수에서도 가장 높게 나타남

petition_votes[petition_votes['votes'] > 1000000]

petitions[(petitions['start'] == '2018-10-17') &
          (petitions['votes'] > 1000000)]









