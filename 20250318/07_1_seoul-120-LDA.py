# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:59:38 2025

@author: Admin

120다산콜재단은 2007년 다산콜센터로 시작한, 
365일 24시간 상담 서비스를 제공.

다산콜재단의 질문과 답변 데이터를 사용

    ‘120다산콜재단’ 데이터를 토픽별로 분석
    RNN, LSTM을 통한 모델링
    
먼저 LDA(Latent Dirichlet Allocation) 을 통한 토픽 모델링으로 분석하고,

그리고 학습, 시험 데이터를 분리해 RNN 으로 모델을 만들어 학습.

데이터 분석에 기본이 되는 내용이므로
토픽 모델링을 시작하는 것이 좋다.

분석 과정
 
1. 머신러닝 방법인 LDA 를 통한 토픽 모델링으로 분석
        TF-IDF LDA 적용
        
2. 토픽 모델링으로 데이터를 토픽별로 분류한 뒤,
        딥러닝 방법 중 하나인 순환 신경망(RNN) 모델로 학습해서 분류.

"""

'''
LDA: 잠재 디리클래 할당

주어진 문서에 대해
각 문서에 어떤 주제들이 들어있는지
서술하는 확률적 토필 분류 기법 중 하나

-> 미리 알고있는 주제별 단어 수 분포를 바탕으로
    주어진 문서에서 발견된 단어 수 분포를 분석함
    해당 문서가 어떤 주제들을 함께 다루고 있을지 예측

1. 사용자 지정 파라미터
2. 문서당 주제 비율
3. 각 문서에 등장한 단어에 주제를 할당
4. 관찰 대상인 문서와 단어 추출
5. 주제 별 분포를 나타내는 파라미터로 분포 할당
6. 사용자 지정 하이퍼 파라미터

문서에 대한 범주의 연관성을 찾는 데 사용되는 확률론적 모델
'''

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# data load
# https://bit.ly/seoul-120-text-csv

df = pd.read_csv('https://bit.ly/seoul-120-text-csv')

df.shape # (2645, 5)
df.isnull().sum() # 결측치 없음

# 문서 만들기
df['문서'] = df['제목'] + ' ' + df['내용']

# CountVectorizer로 단어 벡터화
# 단어 출현 빈도로 여러 문서들을 벡터화 하기 위해 사용
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(stop_words=['돋움', '경우', '또는'])

# fit_transform()로 문장에서 노출되는 feature(특징이 될 만한 단어) 수를 
dtm_cv = cv.fit_transform(df['문서'])

# 단어집합 확인
cv.vocabulary_

cv_cols = cv.get_feature_names_out()

# 벡터를 표현하려면 단어 가방에 있는 모든 단어를 행렬값으로
pd.DataFrame(dtm_cv.toarray(), columns=cv_cols).sum().sort_values()

# LDA
# '분류'의 유일한 값으 ㄹ확인하여 주제 수 확인
df['분류'].value_counts()
'''
분류
행정        1098
경제         823
복지         217
환경         124
주택도시계획     110
문화관광        96
교통          90
안전          51
건강          23
여성가족        13
'''

'''
주어진 문서에 대하여
각 문서에 어떤 주제들이 존재하는지 확인하는 LDA 불러옴
-> LatentDirichletAllocation
'''

from sklearn.decomposition import LatentDirichletAllocation

NUM_TOPICS = 10
LDA_model = LatentDirichletAllocation(n_components= NUM_TOPICS,
                                      random_state=42)

# 학습
LDA_model.fit(dtm_cv)

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words=['돋움', '경우', '또는', '있습니다', '있는', '합니다'])
dtm_tfidf = tfidf.fit_transform(df['문서'])
cols_tfidf = tfidf.get_feature_names_out()

# dtn_tf를 axis=0(수직방향으로) 기준으로 합계를 낸 dist 변수 생성
dist = np.sum(dtm_tfidf, axis=0)

pd.DataFrame(dist, columns= cols_tfidf).T.sort_values(by=0).tail(10)
'''
               0
의한     15.021840
무엇입니까  15.270257
이상     15.577954
관한     16.593598
무엇인가요  16.650743
따라     16.652594
대한     18.866037
있나요    19.707343
서울시    22.586695
어떻게    37.924574
'''

# 희소 행렬을 배열로 변환해 값 확인
pd.DataFrame(dtm_tfidf.toarray(), columns=cols_tfidf)


from sklearn.metrics.pairwise import cosine_similarity

similarity_simple_pair = cosine_similarity(dtm_tfidf[0], dtm_tfidf)
result_list = similarity_simple_pair.tolist()[0]

df['유사도'] = result_list
df[['분류', '제목', '유사도']].sort_values(by='유사도', ascending=False).head(10)
'''
유사도 분석하기
벡터화된 텍스트의 거리를 측정하면
어떤 텍스트가 가까운 위치에 있는지를 계산

등장 빈도에 기반해 코사인 유사도 알고리즘 적용

'''



































