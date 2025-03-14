# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 08:58:01 2025

@author: Admin
유사도

코사인 유사도 / 유클리드 거리 / 자카드 유사도
"""

## 코사인 유사도
import numpy as np
from numpy import dot
from numpy.linalg import norm

def cos_sin(A, B):
    return dot(A,B)/(norm(A)*norm(B)) # -> 코사인 유사도 공식
            # (A,B의 내적) / (A크기) * (B크기)
            # A·B/|A|*|B|

doc1 = np.array([0,1,1,1])
doc2 = np.array([1,0,1,1])
doc3 = np.array([2,0,2,2])

print(f'similarity of doc1 & doc2 : {cos_sin(doc1,doc2)}') # 0.6666666666666667
print(f'similarity of doc1 & doc3 : {cos_sin(doc1,doc3)}') # 0.6666666666666667
print(f'similarity of doc2 & doc3 : {cos_sin(doc2,doc3)}') # 1.0000000000000002
'''
두 문서 내의 모든 단어의 빈도수가 동일하게 증가하는 경우에는(doc2 & doc3의 경우) 유사도 값이 1

'''


'''
유사도를 이용한 추천 시스템 구현 : TF-IDF와 코사인 유사도

해당 데이터는 총 24 개의 열을 가진 45,466 개의 샘플로 구성된 영화 정보 데이터

코사인 유사도에 사용할 데이터: 영화 제목 title / 줄거리 overview
좋아하는 영화를 입력 -> 해당 영화의 줄거리와 유사한 줄거리의 영화 추천

'''
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('dataset/movies_metadata.csv', low_memory=False)

# 훈련 데이터: 20000
data = data.head(20000)

# null값 -> ''로 대체
data['overview'].isnull().sum() # 135
data['overview'] = data['overview'].fillna('')

# overview 열에 대해서 TF-IDF 행렬
# TfidfVectorizer로 문서를 숫자로 변환하는 TF-IDF 벡터화를 수행. overview를 벡터 수치로 변환한 것.
tfidf = TfidfVectorizer(stop_words = 'english') # 불용어 제거
tfidf_matrix = tfidf.fit_transform(data['overview'])
tfidf_matrix.shape # (20000, 47487)
# 20,000개의 영화를 표현하기 위해서 총 47,487개의 단어가 사용
# 47,487차원의 문서 벡터가 20,000개 존재


# 20,000개의 문서 벡터에 대해서 상호간의 코사인 유사도
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix) 
cosine_sim.shape # (20000, 20000) 
# 2만개의 문서 벡터와 자기 자신을 포함한 2만개의 문서 벡터 간의 유사도가 기록된 행렬
# 각 영화 줄거리가 47,487개의 단어를 기준으로 표현된 하나의 벡터
'''
유사도 행렬 활용하기
- 사용자가 특정 영화를 입력하면, 
- 그 영화의 줄거리 벡터를 가져와서,
- 다른 모든 영화와의 유사도를 확인한 뒤,
- 가장 유사한 영화들을 추천!
'''


# data로 부터 영화 타이틀을 key로, 영화 인덱스를 value로 하는 딕셔너리 생성
title_to_index = dict(zip(data['title'], data.index))

'''
선택한 영화의 제목을 입력하면: title_to_index
코사인 유사도를 통해: cosine_sim
가장 overview가 유사한 10개의 영화를 찾아내는 함수
'''

def get_recommendations(title, cosine_sim = cosine_sim):
    idx = title_to_index[title]
    
    # 해당 영화와 모든 영화와의 유사도
    sim_scores = list(enumerate(cosine_sim[idx]))
    # [(0, 0.12), (1, 0.87), (2, 0.34), (3, 0.78), (4, 1.0), ...] 이런 식으로 반환됨.
    # (영화 인덱스, 해당 영화와의 유사도 값)
    
    # 유사도 기준 내림차순 정렬
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
    
    # 자기 자신(첫 번째 요소)을 제외하고 상위 10개 추천
    sim_scores = sim_scores[1:11]
    
    # 10개 영화의 인덱스
    movies_indices = [idx[0] for idx in sim_scores]
    
    return data['title'].iloc[movies_indices]


get_recommendations('The Dark Knight Rises')
'''
12481                            The Dark Knight
150                               Batman Forever
1328                              Batman Returns
15511                 Batman: Under the Red Hood
585                                       Batman
9230          Batman Beyond: Return of the Joker
18035                           Batman: Year One
19792    Batman: The Dark Knight Returns, Part 1
3095                Batman: Mask of the Phantasm
10122                              Batman Begins
'''


'''
유클리드 거리
'''
import numpy as np

def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))

doc1 = np.array((2,3,0,1))
doc2 = np.array((1,2,3,1))
doc3 = np.array((2,1,2,2))

docQ = np.array((1,1,0,1))

print(f'distance  of doc1 & docQ : {dist(doc1,docQ)}') # 2.23606797749979
print(f'distance  of doc2 & docQ : {dist(doc2,docQ)}') # 3.1622776601683795
print(f'distance  of doc3 & docQ : {dist(doc3,docQ)}') # 2.449489742783178
'''
doc1이 docQ와 가장유사
값이 작을수록 문서 간 거리가 가깝다
'''


'''
자카드 유사도
A∩B / A∪B
'''
doc1 = "apple banana everyone like likey watch card holder"
doc2 = "apple banana coupon passport love you"

tokenized_doc1 = doc1.split()
tokenized_doc2 = doc2.split()

union = set(tokenized_doc1).union(set(tokenized_doc2))

intersection = set(tokenized_doc1).intersection(set(tokenized_doc2))
# {'apple', 'banana'}

print('자카드 유사도 :',len(intersection)/len(union))
# 0.16666666666666666










































