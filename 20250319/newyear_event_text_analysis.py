# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 08:56:04 2025

@author: Admin
"""

'''
댓글을 군집화 분석
댓글 분석은 왜 필요할까? 분석해서 어디에 활용할 수 있을까?

수백, 수천 개의 댓글을 다 읽어야 한다면?
- 댓글 속에 제품에 대한 관심을 반드시 추출해야 한다면?
- 쇼핑몰에서 제품 관련 이벤트를 진행할 때 고객이 어떤 제품을 선호하는지 알고 싶다면?
- 1020대와 3040대에 대한 마케팅 세그먼트를 활용하고 싶다면?
- 홍보 마케팅이나 전략을 세울 때 활용한다면?


정답 레이블이 없는 데이터를 분류하고 시각화
정답 레이블이 없는 학습 방법을 '비지도 학습'으로 분류.

분석 과정
- 라이브러리와 데이터 불러오기
- head()와 tail()로 데이터 확인
- 문자열 분리로 관심 강의 분리
- 정규표현식으로 원하는 키워드가 들어 있는 텍스트 찾기
- 학습 데이터 세트와 시험 데이터 세트 분리
- TF-IDF로 텍스트 데이터를 벡터화하고 학습 데이터 세트 정규화
- 학습 및 예측
- 평가
'''

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/event_text.csv')
df.head

## 데이터 전처리
# 중복된 글 제거
df = df.drop_duplicates(['text'], keep='last')

df['origin_text'] = df['text']

# 소문자 변환
df['text'] = df['text'].str.lower()

# 같은 의미의 단어를 하나로 통일
df['text'] = df['text'].str.replace('python', '파이썬').str.replace('pandas', '판다스').str.replace('javascript', ' 자바스크립트').str.replace('java', '자바').str.replace('react', '리액트')


# 관심 강의(관심 강좌) 분리
df['course'] = df['text'].apply(lambda x: x.split('관심강의')[-1])
df['course'] = df['course'].apply(lambda x: x.split('관심 강의')[-1])
df['course'] = df['course'].apply(lambda x: x.split('관심 강좌')[-1])
df['course'] = df['course'].str.replace(':', '')


# 텍스트에서 특정 키워드 추출
search_keyword = ['머신러닝', '딥러닝', '파이썬', '판다스', '공공데이터',
                  'django', '크롤링', '시각화', '데이터분석',
                  '웹개발', '엑셀', 'c' ,'자바', '자바스크립트',
                  'node', 'vue', '리액트']

# 키워드가 있는지 여부 T/F 값
for keyword in search_keyword:
    df[keyword] = df['course'].str.contains(keyword)


# 빈도수 계산을 위한 텍스트 데이터 백터화
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(analyzer='word',
                             tokenizer = None,
                             preprocessor=None,
                             stop_words=None,
                             min_df=2,
                             ngram_range=(3,6),
                             max_features= 2000)

feature_vector = vectorizer.fit_transform(df['course'])
feature_vector.shape # (2410, 2000)

vocab = vectorizer.get_feature_names_out()

pd.DataFrame(feature_vector[:10].toarray(), columns=vocab).head()

# 단어가 전체에서 등장하는 횟수
dist = np.sum(feature_vector, axis=0) 

df_freq = pd.DataFrame(dist, columns=vocab) 
df_freq.T.sort_values(by=0, ascending=False).head(30) 



### 중복을 처리 ###
df_freq_T = df_freq.T.reset_index() 
df_freq_T.columns = ["course", "freq"] 

'''
중복을 제거하기 위해 강의명에서 지식공유자의 이름(***)을 빈 문자열로 변경

lambda 식을 사용해서 강의명을 x.split()으로 나눈 다움
[:4],  즉 앞에서 4개까지만 텍스트를 가져오고 다시 join으로 합친다
=> 중복된 텍스트를 구분해서 보기 위함

빈도수를 기준으로 내림차순으로 10개를 미리 보기로 확인

'''
df_freq_T["course_find"] = df_freq_T["course"].str.replace("박조은", "") 
df_freq_T["course_find"] = df_freq_T["course_find"].apply(lambda x: " ". join(x.split()[:4])) 

df_freq_T.sort_values(["course_find", "freq"], ascending=False).head() 


'''
3개의 ngram과 빈도수로 역순 정렬을 하게 되면 빈도수가 높고
=> ngram수가 많은 순으로 정렬이 됨

drop_duplicates로 첫 번째 강좌를 남기고 나머지 중복을 삭제

'''
print(df_freq_T.shape)  # (2000, 3)

df_course = df_freq_T.drop_duplicates(["course_find", "freq"], keep="first") 
print(df_course.shape)  # (2000, 3)

# 빈도수로 정렬을 하고, 어떤 강좌가 댓글에서 가장 많이 언급되었는지 확인
df_course = df_course.sort_values(by="freq", ascending=False) 
df_course.head(20) 

df_course.to_csv('./data/event-course-name-freq.csv')


# TF-IDF로 가중치를 주어 벡터화
from sklearn.feature_extraction.text import TfidfTransformer

tfidftrans = TfidfTransformer(smooth_idf=False)
feature_tfidf = tfidftrans.fit_transform(feature_vector)
feature_tfidf.shape # (2410, 2000)

tfidf_freq = pd.DataFrame(feature_tfidf.toarray(), columns=vocab)
tfidf_freq.head()

##-------------------------------------------------------------##
'''
KMeans: 머신러닝의 비지도학습 기법 중 하나
주어진 데이터를 K개로 묶는 알고리즘
군집 간 거리 차이의 분산을 최소화하는 방식으로 군집

데이터 집합에서 K개의 데이터 개체를 임의로 추출하고
각 클러스터의 중심점을 초깃값으로 설정

K개의 군집과 데이터 집합의 개체의 거리를 구해
각 개체가 어느 중심점과 가장 유사도가 높은지를 계산
찾은 중심점으로 다시 데이터 군집의 중심점을 계산하는 방법을 반복
유클리드 거리 측정 방법

K-평균 알고리즘의 특징
- 알고리즘이 단순하고 구현이 쉽다
- 대용량 데이터에도 비교적 빠르게 처리 할 수 있다.

- 클러스터의 개수 K를 미리 지정해야 된다.
    -> 초기 설정에 따라 결과가 달라질 수 있다
- 클러스터의 모양이 원형에 가까울 때 효과적
- 이상치에 민감

활용 분야
- 이미지 분할: 이미지를 여러개의 영역으로 분할 하는 데 사용
- 고객 분류: 고객을 여러 그룹으로 나누어 마케팅 전략을 수립하는 데 사용
- 문서 클러스터링: 문서를 주제별로 분류하는 데 사용
- 이상 감지: 정상 데이터와 거리가 먼 이상 데이터를 탐지하는 데 사용

사용 시 고려사항
- 적절한 k 값 선택: 엘보우 방법, 실루엣 분석 등 다양한 방법을 사용하여 죄적의 k 값을 선택
- 중심 설정: k-means++ 알고리즘과 같은 초기 중심 설정 방법을 사용하여 초기 중심 설정의 영향을 줄일 수 있다
- 데이터 전처리: 데이터의 스케일링, 이상치 제거 등 전처리 과정을 통해 알고리즘의 성능을 향상시킬 수 있다

작동 방식
1. 초기 중심 설정: k개의 클러스터 중심을 임의로 설정
2. 클러스터 할당: 각 데이터 포인트를 가장 가까운 클러스터 중심에 할당
3. 중심 재계산: 각 클러스터의 중심을 해당 클러스터에 속한 데이터 포인트들의 평균으로 다시 계산
4. 반복: 2번과 3번 과정을 클러스터 중심이 더 이상 변하지 않거나 최대 반복 횟수에 도달할 때 까지 반복
'''
from sklearn.cluster import KMeans
from tqdm import trange
# 엘보우 방법
inertia = []

start=10
end=70

for i in trange(start, end):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(feature_tfidf)
    inertia.append(kmeans.inertia_)

'''
엘보우 방법

이너셔 값이 급격하게 꺾이는 지점을 찾아 군집으로 정하는 것
'''
# x축 클러스터의 수 / y축 inertia 값
plt.plot(range(start, end), inertia)
plt.title('클러스터 수 비교')
plt.show()

n_clusters = 50
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(feature_tfidf)

prediction = kmeans.predict(feature_tfidf)
df['cluster'] = prediction

df['cluster'].value_counts().head()



from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score

b_inertia = []
silhouettes=[]

for i in trange(start, end):
    mkmeans = MiniBatchKMeans(n_clusters=i, random_state=42)
    mkmeans.fit(feature_tfidf)
    b_inertia.append(mkmeans.inertia_)
    silhouettes.append(silhouette_score(feature_tfidf, mkmeans.labels_))

plt.plot(range(start, end), b_inertia)
plt.title('클러스터 수 비교')
plt.show()


# yellowbrick은 머신러닝 시각화 도구
from yellowbrick.cluster import KElbowVisualizer

KElowM = KElbowVisualizer(kmeans, k=(start, end))
KElowM.fit(feature_tfidf.toarray())
KElowM.show()

# 군집 결과 시각화
mkmeans= MiniBatchKMeans(n_clusters= n_clusters, random_state=43)
mkmeans.fit(feature_tfidf)

prediction = mkmeans.predict(feature_tfidf)
df['bcluster'] = prediction




##클러스터 예측 평가

feature_array = feature_vector.toarray()

labels = np.unique(prediction) 

df_cluster_score = [] 
df_cluster = [] 

for label in labels:
    id_temp = np.where(prediction==label)
    x_means = np.mean(feature_array[id_temp], axis=0)
    sorted_means = np.argsort(x_means)[::-1][:n_clusters]
    
    features = vectorizer.get_feature_names_out()
    best_features = [(features[i], x_means[i]) for i in sorted_means]
                      
    df_score = pd.DataFrame(best_features, columns= ['features', 'score'])
    df_cluster_score.append(df_score)
    
    df_cluster.append(best_features[0])

# 점수가 클수록 예측 정도가 높음
pd.DataFrame(df_cluster, columns=['features', 'score']).sort_values(by=['features','score'], ascending=False)






































