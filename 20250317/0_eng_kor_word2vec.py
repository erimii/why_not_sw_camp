# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:01:00 2025

@author: Admin
"""

### 케라스
## 1. 전처리
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer()
train_text = 'The earth is on awesome place live'

# 단어집합생성
tokenizer.fit_on_texts([train_text])

# 정수인코딩
sub_text = 'The earth is on awesome place live'
sequences = tokenizer.texts_to_sequences([sub_text])[0]

print(f'정수인코딩: {sequences}')
print(f'단어집합: {tokenizer.word_index}')
'''
정수인코딩: [1, 2, 3, 4, 5, 6, 7]
단어집합: {'the': 1, 'earth': 2, 'is': 3, 'on': 4, 'awesome': 5, 'place': 6, 'live': 7}

pad_sequences 사용 이유?
전체 훈련 데이터에서 각 샘플의 길이는 서로 다를 수 있음
모델의 입력으로 사용하려면 모든 샘플의 길이를 동일하게 해야됨
자연어 처리에서는 이를 패딩 작업 이라고 부름
보통 숫자 0을 넣어서 길이가 다른 샘플들의 길이를 맞춤

pad_sequences는
정해준 길이보다 길이가 긴 샘플은 값을 일부 자르고
정해주 길이보다 길이가 짧은 샘플은 값을 0으로 채움

첫번째: 패딩을 진행할 데이터
maxlen = 모든 데이터에 대해서 정규화 할 길이
padding =  'pre'를 선택하면 앞에 0 채우고, 'post' 선택하면 뒤에 0 채움
'''

pad_sequences([[1,2,3], [3,4,5,6], [7,8]],
              maxlen=3,
              padding='pre')
'''
array([[1, 2, 3],
       [4, 5, 6],
       [0, 7, 8]])
'''

'''
워드 임베딩 -> 단어를 밀집벡터(임베딩 벡터)로 만드는 작업

임베딩 벡터: 초기에는 랜덤값, 학습되며 변경

'''
from tensorflow.keras.layers import Embedding

tokenized_text = [['Hope', 'to', 'see', 'you', 'soon'],
                  ['Nice', 'to', 'see', 'you', 'again']]


encoded_text = [[0,1,2,3,4],
                 [5,1,2,3,6]]

vocab_size = 7
embedding_dim = 2
Embedding(vocab_size, embedding_dim, input_length=5)


'''
word2vec
단어 벡터 간의 유의마한 유사도를 반영할 수 있도록
단어의 의미를 수치화 할 수 있는 방법
'''
import nltk
nltk.download('punkt')

import urllib.request
import zipfile
from lxml import etree
import re
from nltk.tokenize import word_tokenize, sent_tokenize

# data download
urllib.request.urlretrieve("https://raw.githubusercontent.com/ukairia777/tensorflow-nlp-tutorial/main/09.%20Word%20Embedding/dataset/ted_en-20160408.xml", filename="ted_en-20160408.xml")

# xml 문법으로 작성되어있어서 전처리 필요
targetXML = open('ted_en-20160408.xml', 'r', encoding='UTF8')

target_text = etree.parse(targetXML)

parse_text = '\n'.join(target_text.xpath('//content/text()'))

content_text = re.sub(r'\([^)]*\)', '', parse_text)

sent_text = sent_tokenize(content_text)

normalized_text=[]

for string in sent_text:
    tokens = re.sub(r'[^a-z0-9]+', ' ', string.lower())
    normalized_text.append(tokens)

result = [word_tokenize(sentence) for sentence in normalized_text]

for line in result[:3]:
    print(line)

## word2vec 모델에 텍스트 데이터를 훈련
import gensim




#-------------------------------------------------------
# 한국어 word2vec
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request

from tqdm import tqdm
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")

train_data = pd.read_table('ratings.txt')


train_data[:5]

train_data = train_data.dropna(how='any')

train_data['document'] = train_data['document'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣]', '')

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()

tokenized_data = []

for sentence in tqdm(train_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True)
    
    stopwords_removed_sentence= [word for word in tokenized_sentence if not word in stopwords]
    
    tokenized_data.append(stopwords_removed_sentence)


plt.hist([len(s) for s in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()


# 토큰화된 네이버 영화 리뷰 데이터를 학습
from gensim.models import Word2Vec

model = Word2Vec(sentences = tokenized_data,
                 vector_size= 100,
                 window=5,
                 min_count=5,
                 workers=4,
                 sg=0)

print(model.wv.most_similar('발연기'))
'''
[('연기', 0.7702683210372925), ('연기력', 0.7515908479690552), ('어색', 0.7181136608123779), ('발음', 0.7179075479507446), ('조연', 0.7139722108840942), ('미스캐스팅', 0.6840712428092957), ('사투리', 0.6780403852462769), ('캐스팅', 0.670058012008667), ('권상우', 0.6619139909744263), ('명연기', 0.654475212097168)]
'''











