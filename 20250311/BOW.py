# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:28:51 2025

@author: Admin
"""

import nltk
nltk.download('stopwords')

from konlpy.tag import Okt

okt = Okt()

### Bag of Words 함수 ###
# 입력된 문서에 대해서 단어 집합을 만들어 각 단어에 정수 인덱스를 할당하고,
# BoW

def build_bag_of_words(doc):
    doc = doc.replace('.', '')
    tokenized_doc = okt.morphs(doc)
    
    word_to_index ={}
    bow = []
    
    for word in tokenized_doc:
        if word not in word_to_index.keys():
            word_to_index[word] = len(word_to_index)
            bow.insert(len(word_to_index)-1, 1)
            
        else:
            index = word_to_index.get(word)
            bow[index] = bow[index] + 1
            
    return word_to_index, bow

doc1 = '정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다'

vocab, bow = build_bag_of_words(doc1)
'''
vocab
{'정부': 0,
 '가': 1,
 '발표': 2,
 '하는': 3,
 '물가상승률': 4,
 '과': 5,
 '소비자': 6,
 '느끼는': 7,
 '은': 8,
 '다르다': 9}

bow
[1, 2, 1, 1, 2, 1, 1, 1, 1, 1]
'''

doc2 = '소비자는 주로 소비하는 상품을 기준으로 물가상승률을 느낀다'
vocab, bow = build_bag_of_words(doc2)
'''
vocab
{'소비자': 0,
 '는': 1,
 '주로': 2,
 '소비': 3,
 '하는': 4,
 '상품': 5,
 '을': 6,
 '기준': 7,
 '으로': 8,
 '물가상승률': 9,
 '느낀다': 10}

bow
[1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1]
'''



# CountVectorizer 클래스로 BoW 만들기
# 사이킷런에서는 단어의 빈도를 Count 하여 Vector 로 만드는 CountVectorizer 클래스를 지원 .

from sklearn.feature_extraction.text import CountVectorizer
corpus1 = ['you know I want your love. because I love you.']
vector = CountVectorizer()

# 각 단어의 빈도수를 기록
print('bag of words vector :', vector.fit_transform(corpus1).toarray())
# [[1, 1, 2, 1, 2, 1]]

# 각 단어의 인덱스가 어떻게 부여되었는지 출력 : vocabulary_
print('vocabulary :',vector.vocabulary_)
# {'you': 4, 'know': 1, 'want': 3, 'your': 5, 'love': 2, 'because': 0}
'''
I는 BoW 만드는 과정에서 사라짐. 
CountVectorizer가 길이가 2 이상인 문자에 대해서만 토큰으로 사용하기 때문
'''
corpus2 = ['정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다']
vector.fit_transform(corpus2).toarray()
# [[1, 1, 1, 1, 1, 1, 1]]
vector.vocabulary_
# {'정부가': 6, '발표하는': 4, '물가상승률과': 2, '소비자가': 5, '느끼는': 0, '물가상승률은': 3, '다르다': 1}
'''
CountVectorizer는 띄어쓰기를 기준으로 분리하기 때문에 '물가상승률과'와 '물가상승률은'를 다른 단어로 인식
'''



### 불용어를 제거한 BoW
# 불용어를 지정하면 불용어는 제외하고 bow를 만들 수 있도록 기능 지원
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

# 사용자가 직접 정의한 불용어 사용
text = ["Family is not an important thing. It's everything."]
vect = CountVectorizer(stop_words=["the", "a", "an", "is", "not"]) # 불용어 지정
print('bag of words vector :',vect.fit_transform(text).toarray())
# [[1 1 1 1 1]]
print('vocabulary :',vect.vocabulary_)
# {'family': 1, 'important': 2, 'thing': 4, 'it': 3, 'everything': 0}

# CountVectorizer에서 제공하는 자체 불용어 사용
vect = CountVectorizer(stop_words="english")
print('bag of words vector :',vect.fit_transform(text).toarray())
# [[1 1 1]]
print('vocabulary :',vect.vocabulary_)
# {'family': 0, 'important': 1, 'thing': 2}

# NLTK에서 지원하는 불용어 사용
stop_words = stopwords.words("english")
vect = CountVectorizer(stop_words=stop_words)
print('bag of words vector :',vect.fit_transform(text).toarray())
# [[1 1 1 1]]
print('vocabulary:',vect.vocabulary_)
# {'family': 1, 'important': 2, 'thing': 3, 'everything': 0}



'''
TF-IDF
DTM  내에 있는 각 단어에 대한 중요도를 게산할 수 있는 TF-IDF 가중치
DTM을 사용하는 것보다 많은 정보를 고려하여 문서들을 비교

주로 문서의 유사도를 구하는 작업
검색시스템에서 검새 ㄱ결과의 주우요도를 정하는 작업
문서 내에서 특정 단어에 대한 중요도를 구하는 작업

TF-IDF: TF * IDF
'''

corpus = [
    "정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다",
    "소비자는 주로 소비하는 상품을 기준으로 물가상승률을 느낀다"
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
print(X)


# 파이썬으로  TF-IDF 직접구현
from math import log
import pandas as pd

docs = [
        '먹고 싶은 사과',
        '먹고 싶은 바나나',
        '길고 노란 바나나 바나나',
        '저는 과일이 좋아요',
        ]
vocab = list(set(w for doc in docs for w in doc.split()))
vocab.sort()
# ['과일이', '길고', '노란', '먹고', '바나나', '사과', '싶은', '저는', '좋아요']

# TF, IDF, TF-IDF 값 구하는 함수
# 총 문서의 수
N = len(docs)

def tf(t,d):
    return d.count(t)

def idf(t):
    df = 0
    for doc in docs:
        df += t in doc
    return log(N/(df+1))

def tfidf(t,d):
    return tf(t,d) * idf(t)

# DTM을 데이터프레임에 저장하여 출력
result = []

for i in range(N):
    result.append([])
    
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]
        result[-1].append(tf(t,d))

tf_ = pd.DataFrame(result, columns=vocab)
'''
   과일이  길고  노란  먹고  바나나  사과  싶은  저는  좋아요
0    0      0    0      1    0      1     1     0    0
1    0      0    0      1    1      0     1     0    0
2    0      1    1      0    2      0     0     0    0
3    1      0    0      0    0      0     0     1    1
'''

# 각 단어에 대한 IDF값
result = []

for j in range(len(vocab)):
    t = vocab[j]
    result.append(idf(t))
    
idf_ = pd.DataFrame(result, index = vocab, columns=["IDF"])
'''
          IDF
과일이  0.693147
길고   0.693147
노란   0.693147
먹고   0.287682
바나나  0.287682
사과   0.693147
싶은   0.287682
저는   0.693147
좋아요  0.693147
'''

# TF-IDF 행렬
result = []

for i in range(N):
    result.append([])
    
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]
        result[-1].append(tfidf(t,d))


tfidf_ = pd.DataFrame(result, columns=vocab)
'''
        과일이      길고        노란  ...   싶은        저는       좋아요
0       0.000000  0.000000  0.000000  ...  0.287682  0.000000  0.000000
1       0.000000  0.000000  0.000000  ...  0.287682  0.000000  0.000000
2       0.000000  0.693147  0.693147  ...  0.000000  0.000000  0.000000
3       0.693147  0.000000  0.000000  ...  0.000000  0.693147  0.693147
'''

'''
사이킷런을 이용한 DTM과 TF-IDF
'''

from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    'you konw I want your Love',
    'I like you',
    'What should I do'
    ]

vector = CountVectorizer()

vector.fit_transform(corpus).toarray()
'''
array([[0, 1, 0, 1, 0, 1, 0, 1, 1],
       [0, 0, 1, 0, 0, 0, 0, 1, 0],
       [1, 0, 0, 0, 1, 0, 1, 0, 0]]
'''

vector.vocabulary_
'''
{'you': 7,
 'konw': 1,
 'want': 5,
 'your': 8,
 'love': 3,
 'like': 2,
 'what': 6,
 'should': 4,
 'do': 0}
'''

# TFF-IDF를 자동 계산해주는 TfidfVectorizer를 제공
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    'you konw I want your Love',
    'I like you',
    'What should I do'
    ]

# 1. fit()로 학습
tfidfv = TfidfVectorizer().fit(corpus)

# transform()
tfidfv.transform(corpus).toarray()
'''
[[0., 0.46735098, 0., 0.46735098, 0. ,0.46735098, 0. , 0.35543247, 0.46735098],
[0.   , 0.     , 0.79596054, 0.    , 0.     ,0.        , 0.        , 0.60534851, 0.   ],
[0.57735027, 0.    , 0.    , 0.     , 0.57735027, 0.    , 0.57735027, 0.     , 0.     ]]
'''
tfidfv.vocabulary_
'''
{'you': 7,
 'konw': 1,
 'want': 5,
 'your': 8,
 'love': 3,
 'like': 2,
 'what': 6,
 'should': 4,
 'do': 0}
'''











































