# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:40:04 2025

@author: Admin

기초 분류 모델 만들기
"""

### 라이브러리 설치
'''
koreanize-matplotlib : 한글폰트 사용을 위해
tqdm : 오래 걸리는 작업의 진행상태를 보기 위해
konlpy : 한국어 형태소 분석을 위해
'''

# 데이터 분석을 위한 pandas, 수치계산을 위한 numpy, 시각화를 위한 seaborn, matplotlib 을 불러온다.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# !pip install -qU koreanize-matplotlib konlpy tqdm
### 시각화를 위한 폰트 설정
import koreanize_matplotlib
pd.Series([1, 3, 5, -7, 9]).plot(title="한글")
plt.show()



### 데이터 로드
import os, platform

base_path = "data/klue/"
file_name = "dacon-klue-open-zip"

# 학습, 예측 데이터셋을 불러온다.
train = pd.read_csv(os.path.join(base_path, "train_data.csv"))
test = pd.read_csv(os.path.join(base_path, "test_data.csv"))
train.shape, test.shape


# 토픽을 불러온다.
topic = pd.read_csv(os.path.join(base_path, "topic_dict.csv"))
topic

# head()와 tail()로 데이터 확인
train.head()
test.head()

topic["topic"].values


### 전처리를 위한 데이터 병합
# 전처리를 위해 데이터 병합
raw = pd.concat([train, test])
raw.shape

raw.head()
raw.tail()

df = raw.merge(topic, how="left")
df.shape

df.head()



### 정답값 빈도수

# test는 결측치로 되어 있기 때문에 빈도수에 포함되지 않습니다.
df["topic_idx"].value_counts()


# df 로 빈도수를 구했지만 test 데이터는 topic이 결측치라 포함되지 않습니다. 
sns.countplot(data=df, y="topic")
plt.show()



### 문자 길이
# 문자 길이, 단어 빈도, 유일 어절의 빈도수를 알기 위한 파생 변수 만들기
df["len"] = df["title"].apply(lambda x : len(x))
df["word_count"] = df["title"].apply(lambda x : len(x.split()))
df["unique_word_count"] = df["title"].apply(lambda x : len(set(x.split())))


# 파생변수가 잘 만들어졌는지 확인한다.
df.head()



### 맷플롯립(matplotlib)과 시본(seaborn)을 이용을 이용해 히스토그램으로 시각화
fig, axes = plt.subplots(1, 3, figsize=(15, 2))
sns.histplot(df["len"], ax=axes[0])
sns.histplot(df["word_count"], ax=axes[1])
sns.histplot(df["unique_word_count"], ax=axes[2])
plt.show()


df[["len", "word_count", "unique_word_count"]].describe()


### 주제별 글자와 단어 수 확인
# 낱글자의 길이(len) 빈도
sns.displot(data=df, x="len",
            hue="topic", col="topic", col_wrap=2, aspect=5, height=2)
plt.show()


# 단어 빈도
sns.displot(data=df, x="word_count",
            hue="topic", col="topic", col_wrap=2, aspect=5, height=2)
plt.show()


# 유일 어절의 빈도
sns.displot(data=df, x="unique_word_count",
            hue="topic", col="topic", col_wrap=2, aspect=5, height=2)
plt.show()



### 문자 전처리
# 숫자 제거
import re

# df["title"] = df["title"].map(lambda x : re.sub("[0-9]", "", x))
df["title"] = df["title"].str.replace("[0-9]", "", regex=True)



# 영문자는 모두 소문자로 변경
# 대소문자가 섞여 있으면 다른 다른 단어로 다루기 때문에
# 영문자는 모두 대문자 혹은 소문자로 변경합니다
df["title"] = df["title"].str.lower()



### 불용어 제거
def remove_stopwords(text):
    tokens = text.split(' ')
    stops = [ '합니다', '하는', '할', '하고', '한다', 
             '그리고', '입니다', '그 ', ' 등', '이런', ' 것 ', ' 및 ',' 제 ', ' 더 ']
    meaningful_words = [w for w in tokens if not w in stops]
    return ' '.join(meaningful_words)

df["title"] = df["title"].map(remove_stopwords)


### 조사, 어미, 구두점 제거
'''
조사나 어미를 제거하기 위해 
문장에 품사 정보를 부착해서 분리할 수 있도록 
형태소 분석기를 부착. 형태소 분석기는 Konlpy의 OKT 분석기를 사용.
'''
label_name = "topic_idx"

'''
test의 topic_idx는 NaN이었다. 

따라서 notnull()과 isnull()을 사용하여 
topic 이 있으면 학습 데이터, 없으면 시험 데이터 세트로 재분할한다.
'''
train = df[df[label_name].notnull()].copy()
test = df[df[label_name].isnull()].copy()
train.shape, test.shape


# 형태소 분석기에서 Okt 태거 불러오기 
from konlpy.tag import Okt

okt = Okt() 

# 어간 추출(stemming) : 조사, 어미, 구두점 제거
def okt_clean(text):
    clean_text = []
    for word in okt.pos(text, stem=True):
        if word[1] not in ['Josa', 'Eomi', 'Punctuation']:
            clean_text.append(word[0])
    
    return " ".join(clean_text) 

from tqdm import tqdm
tqdm.pandas() 

train['title'] = train['title'].progress_map(okt_clean)
test['title'] = test['title'].progress_map(okt_clean)



### 학습, 시험 데이터 세트 분리
X_train = train["title"]
X_test = test["title"]

X_train.shape, X_test.shape

y_train = train[label_name]
y_train.value_counts()

y_test = test[label_name]
y_test.value_counts()



### 벡터화
## TF-IDF(Term Frequency - Inverse Document Frequency)
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vect = TfidfVectorizer(tokenizer=None, 
                             ngram_range=(1,2),
                             min_df=3, 
                             max_df=0.95)
tfidf_vect.fit(X_train)


train_feature_tfidf = tfidf_vect.transform(X_train)
test_feature_tfidf = tfidf_vect.transform(X_test)

train_feature_tfidf.shape, test_feature_tfidf.shape


# 단어 사전
vocab = tfidf_vect.get_feature_names_out()
print(len(vocab))
vocab[:10]


# np.sum 으로 위에서 구한 train_feature_vector 의 값을 모두 더한다. axis=0 으로 한다. 
dist = np.sum(train_feature_tfidf, axis=0)

vocab_count = pd.DataFrame(dist, columns=vocab)
vocab_count


# 위에서 구한 빈도수를 그래프로 그린다.
vocab_count.T[0].sort_values(ascending=False).head(50).plot.bar(figsize=(15, 4))
plt.show()



### 학습과 예측
# RandomForestClassifier 를 불러온다.
from sklearn.ensemble import RandomForestClassifier

### 랜덤포레스트 분류기를 사용
model = RandomForestClassifier(n_estimators = 100, n_jobs = -1, random_state=42)
model


### 교차 검증
from sklearn.model_selection import cross_val_predict

y_pred = cross_val_predict(model, train_feature_tfidf, y_train, cv=3, n_jobs=-1, verbose=1)


### 교차 검증 정확도
valid_accuracy = (y_pred == y_train).mean()
valid_accuracy

df_accuracy = pd.DataFrame({"pred": y_pred, "train": y_train})
df_accuracy["accuracy"] = (y_pred == y_train)


### 추가 작업(그룹별 정확도)
topic


df_accuracy.groupby(["train"])["accuracy"].mean()

df_accuracy.rename(columns={"pred":"predict"})

# 학습
# fit 으로 학습
model.fit(train_feature_tfidf, y_train)

# 예측
# predict로 예측
y_predict = model.predict(test_feature_tfidf)
y_predict[:5]


# 답안지 로드
# sample_submission.csv 파일은 마치 답안지와 같다.
submit = pd.read_csv(os.path.join(base_path, "sample_submission.csv"))
submit.head()


# 정답값 측정을 위해 y_test 변수에 할당
submit["topic_idx"] = y_predict
'''
index,topic_idx
45654,2.0
45655,3.0
45656,0.0
45657,2.0
45658,3.0
'''

file_name = os.path.join(base_path, f"submit_{valid_accuracy}.csv")
file_name

submit.to_csv(file_name, index=False)








