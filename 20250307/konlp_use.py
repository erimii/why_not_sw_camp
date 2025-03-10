# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 17:37:37 2025

@author: Admin
"""


'''
텍스트 전처리(text preprocessing): 텍스트를 사전에 처리하는 작업

1. 토큰화(tokenization)
2. 정제(cleaning) and 정규화(normalization)
3. 어간 추출 and 표재어 추출
4. 불용어(stopword)
5. 정규 표현식(regular expression)
6. 정수 인코딩(integer encoding)
7. 패딩(padding)
8. 원 핫 인코딩(one-hot encoding)
9. 데이터의 분리(splitting data)
10. 한국어 전처리 패키지(texy preprocessing tools for korean text)
'''

'''
5. 정규 표현식(regular expression)
'''
import re
# .기호
r = re.compile('a.c')
r.search('kkk')

result = re.split("[ ,]+", "사과, 바나나 포도")
print(result)  # ['사과', '바나나', '포도']


result = re.sub("[^a-zA-Z]", " ", "Hello! 123, Welcome.")
print(result)  # 'Hello  Welcome '

text = "Regular expression : A regular expression, regex or regexp[1] (sometimes called a rational expression)[2][3] is, in theoretical computer science and formal language theory, a sequence of characters that define a search pattern."
result = re.sub

text = '''100 John PROF
101 James STUD
102 Moc STUD'''

# \s+ 
re.split('\s+', text)
# ['100', 'John', 'PROF', '101', 'James', 'STUD', '102', 'Moc', 'STUD']

# \d+
re.findall('\d+', text)
# ['100', '101', '102']

re.findall('[A-Z]{4}', text)
# ['PROF', 'STUD', 'STUD']

re.findall('[A-Z][a-z]+', text)
# ['John', 'James', 'Moc']


### 정규 표현식을 이용한 토큰화
from nltk.tokenize import RegexpTokenizer

text = "Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop"

# 문자 또는 숫자가 1개 이상인 경우: \w+
tokenizer1 = RegexpTokenizer('[\w]+')
print(tokenizer1.tokenize(text))
# ['Don', 't', 'be', 'fooled', 'by', 'the', 'dark', 'sounding', 'name', 'Mr', 'Jone', 's', 'Orphanage', 'is', 'as', 'cheery', 'as', 'cheery', 'goes', 'for', 'a', 'pastry', 'shop']

# 공백을 기준으로 토큰화
tokenizer2 = RegexpTokenizer('[\s]+', gaps=True)
print(tokenizer2.tokenize(text))
# ["Don't", 'be', 'fooled', 'by', 'the', 'dark', 'sounding', 'name,', 'Mr.', "Jone's", 'Orphanage', 'is', 'as', 'cheery', 'as', 'cheery', 'goes', 'for', 'a', 'pastry', 'shop']









'''
6. 정수 인코딩(integer encoding)
- 단어를 빈도수 순으로 정렬한 단어 집합을 만들고 ,빈도수가 높은 순서대로 차례로 낮은 숫자부터 정수 부여
'''
import nltk
nltk.download('punkt')
nltk.download('stopwords')

################################ dictionary 사용하기 ################################
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

raw_text = """A barber is a person. a barber is good person. 
            a barber is huge person. he Knew A Secret! 
            The Secret He Kept is huge secret. Huge secret. 
            His barber kept his word. a barber kept his word. 
            His barber kept his secret. 
            But keeping and keeping such a huge secret to himself was driving the barber crazy. 
            the barber went up a huge mountain."""

# 문장 토큰화
sentences = sent_tokenize(raw_text)
'''
['A barber is a person.',
 'a barber is good person.',
 'a barber is huge person.',
 'he Knew A Secret!',
 'The Secret He Kept is huge secret.',
 'Huge secret.',
 'His barber kept his word.',
 'a barber kept his word.',
 'His barber kept his secret.',
 'But keeping and keeping such a huge secret to himself was driving the barber crazy.',
 'the barber went up a huge mountain.']
'''

'''
정제 작업과 정규화 작업을 병행하며 단어 토큰화를 수행
1. 단어들을 소문자화
2. 단어의 개수를 통일
3. 불용어와 단어 길이가 2 이하인 경우 제외
4. 텍스트를 수치화
'''

vocab = {} # 각 단어에 대한 빈도수
preprocessed_sentences = [] # 문장별 단어 (불용어와 단어 길이가 2 이하인 경우 제외)

stop_words = set(stopwords.words('english'))

for sentence in sentences:
    tokenized_sentence = word_tokenize(sentence)
    result=[]
    # 단어들을 소문자화 & 불용어와 단어 길이가 2 이하인 경우 제외
    for word in tokenized_sentence:
        word = word.lower()
        if word not in stop_words:
            if len(word) > 2:
                result.append(word)
                if word not in vocab:
                    vocab[word] = 0
                vocab[word] += 1
    preprocessed_sentences.append(result)

'''
vocab
{'barber': 8,
 'person': 3,
 'good': 1,
 'huge': 5,
 'knew': 1,
 'secret': 6,
 'kept': 4,
 'word': 2,
 'keeping': 2,
 'driving': 1,
 'crazy': 1,
 'went': 1,
 'mountain': 1}

preprocessed_sentences
[['barber', 'person'],
 ['barber', 'good', 'person'],
 ['barber', 'huge', 'person'],
 ['knew', 'secret'],
 ['secret', 'kept', 'huge', 'secret'],
 ['huge', 'secret'],
 ['barber', 'kept', 'word'],
 ['barber', 'kept', 'word'],
 ['barber', 'kept', 'secret'],
 ['keeping', 'keeping', 'huge', 'secret', 'driving', 'barber', 'crazy'],
 ['barber', 'went', 'huge', 'mountain']]
'''

vocab_sorted = sorted(vocab.items(),
                      key = lambda x:x[1],
                      reverse=True)
'''
[('barber', 8),
 ('secret', 6),
 ('huge', 5),
 ('kept', 4),
 ('person', 3),
 ('word', 2),
 ('keeping', 2),
 ('good', 1),
 ('knew', 1),
 ('driving', 1),
 ('crazy', 1),
 ('went', 1),
 ('mountain', 1)]
'''

# 빈도수가 낮은 단어는 제외하고 높은 빈도수를 가진 단어일수록 낮은 정수 부여. 1부터
word_to_index = {}
i = 0

for (word, frequency) in vocab_sorted:
    if frequency >1:
        i += 1
        word_to_index[word] = i
'''
{'barber': 1,
 'secret': 2,
 'huge': 3,
 'kept': 4,
 'person': 5,
 'word': 6,
 'keeping': 7}
'''

# 상위 5개 단어만 사용한다고 가정
vocab_size = 5
word_frequency = [word for word, index in word_to_index.items()
                      if index >= vocab_size+1]

for w in word_frequency:
    del word_to_index[w]
'''
word_to_index
{'barber': 1, 'secret': 2, 'huge': 3, 'kept': 4, 'person': 5}
'''

# preprocessed_sentences에 있는 각 단어를 word_to_index를 사용해서 정수로 바꾸는 작업
encoded_sentences = []
word_to_index['OOV'] = len(word_to_index) + 1

for sentence in preprocessed_sentences:
    encoded_sentence = []
    
    for word in sentence:
        try:
            encoded_sentence.append(word_to_index[word])
        except KeyError: 
            encoded_sentence.append(word_to_index['OOV'])
            
    encoded_sentences.append(encoded_sentence)

'''
encoded_sentences
[[1, 5],
 [1, 6, 5],
 [1, 3, 5],
 [6, 2],
 [2, 4, 3, 2],
 [3, 2],
 [1, 4, 6],
 [1, 4, 6],
 [1, 4, 2],
 [6, 6, 3, 2, 6, 1, 6],
 [1, 6, 3, 6]]
'''

# ------------------------ 여기까지 단어를 정수화 하는 원리 ---------------------------------
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# python의 Counter() 사용 텍스트 수치화 방법 두 번째
from collections import Counter

all_words_list = sum(preprocessed_sentences, [])
vocab = Counter(all_words_list)
# selelct top5
vocab = vocab.most_common(5)
#  [('barber', 8), ('secret', 6), ('huge', 5), ('kept', 4), ('person', 3)]


word_to_index = {}
i = 0
for (word, freq) in vocab:
    i += 1
    word_to_index[word] = i
    
word_to_index['OOV'] = len(word_to_index) + 1


# preprocessed_sentences에 있는 각 단어를 word_to_index를 사용해서 정수로 바꾸는 작업
encoded_sentences = []

for sentence in preprocessed_sentences:
    encoded_sentence = []
    
    for word in sentence:
        try:
            encoded_sentence.append(word_to_index[word])
        except KeyError: 
            encoded_sentence.append(word_to_index['OOV'])
            
    encoded_sentences.append(encoded_sentence)



# NLTK의 FreDist 텍스트 수치화 방법 세 번째
from nltk import FreqDist
import numpy as np

vocab = FreqDist(np.hstack(preprocessed_sentences))
# FreqDist({'barber': 8, 'secret': 6, 'huge': 5, 'kept': 4, 'person': 3, 'word': 2, 'keeping': 2, 'good': 1, 'knew': 1, 'driving': 1, ...})

# selelct top5
vocab = vocab.most_common(5)

word_to_index = {word[0]: index + 1 for index, word in enumerate(vocab)}
# {'barber': 1, 'secret': 2, 'huge': 3, 'kept': 4, 'person': 5}


### 케라스Keras의 텍스트 전처리

from tensorflow.keras.preprocessing.text import Tokenizer
# select top 5
tokenizer = Tokenizer(num_words = 6)

tokenizer.fit_on_texts(preprocessed_sentences)

print(tokenizer.word_index)

print(tokenizer.word_counts)

print(tokenizer.texts_to_sequences(preprocessed_sentences))



'''
7. 패딩(padding)
여러 문장의 길 이를 임의로 동일하게 맞춰주는 작업

길이가 전부 동일한 문서들에 대해서는 하나의 행렬로 보고 한꺼번에 묶어서 처리하기 위함
'''
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer

preprocessed_sentences = [['barber', 'person'], ['barber', 'good', 'person'], ['barber', 'huge', 'person'], ['knew', 'secret'], ['secret', 'kept', 'huge', 'secret'], ['huge', 'secret'], ['barber', 'kept', 'word'], ['barber', 'kept', 'word'], ['barber', 'kept', 'secret'], ['keeping', 'keeping', 'huge', 'secret', 'driving', 'barber', 'crazy'], ['barber', 'went', 'huge', 'mountain']]

tokenizer = Tokenizer()

# 빈도수를 기준으로 단어 집합 생성
tokenizer.fit_on_texts(preprocessed_sentences)
encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
'''
encoded
[[1, 5],
 [1, 8, 5],
 [1, 3, 5],
 [9, 2],
 [2, 4, 3, 2],
 [3, 2],
 [1, 4, 6],
 [1, 4, 6],
 [1, 4, 2],
 [7, 7, 3, 2, 10, 1, 11],
 [1, 12, 3, 13]]
'''

# 모두 동일한 길이로 맞춰주기
max_len = max(len(item) for item in encoded)

for sentence in encoded:
    while len(sentence) < max_len:
        sentence.append(0)

padded_np = np.array(encoded)
'''
zero padding
array([[ 1,  5,  0,  0,  0,  0,  0],
       [ 1,  8,  5,  0,  0,  0,  0],
       [ 1,  3,  5,  0,  0,  0,  0],
       [ 9,  2,  0,  0,  0,  0,  0],
       [ 2,  4,  3,  2,  0,  0,  0],
       [ 3,  2,  0,  0,  0,  0,  0],
       [ 1,  4,  6,  0,  0,  0,  0],
       [ 1,  4,  6,  0,  0,  0,  0],
       [ 1,  4,  2,  0,  0,  0,  0],
       [ 7,  7,  3,  2, 10,  1, 11],
       [ 1, 12,  3, 13,  0,  0,  0]])

'''

from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer()

# 빈도수를 기준으로 단어 집합 생성
tokenizer.fit_on_texts(preprocessed_sentences)
encoded = tokenizer.texts_to_sequences(preprocessed_sentences)

padded = pad_sequences(encoded, padding='post', maxlen=5, truncating = 'post') 
# padding 미설정 시 0이 앞에 채워짐
# truncating 미설정 시 maxlen에 맞게 앞 데이터(여기서는 7,7)가 지워짐
'''
array([[ 1,  5,  0,  0,  0],
       [ 1,  8,  5,  0,  0],
       [ 1,  3,  5,  0,  0],
       [ 9,  2,  0,  0,  0],
       [ 2,  4,  3,  2,  0],
       [ 3,  2,  0,  0,  0],
       [ 1,  4,  6,  0,  0],
       [ 1,  4,  6,  0,  0],
       [ 1,  4,  2,  0,  0],
       [ 7,  7,  3,  2, 10],
       [ 1, 12,  3, 13,  0]])
'''


# 임의의 숫자로 패딩
last_value = len(tokenizer.word_index) + 1

padded = pad_sequences(encoded, padding='post', value = last_value) 
'''
array([[ 1,  5, 14, 14, 14, 14, 14],
       [ 1,  8,  5, 14, 14, 14, 14],
       [ 1,  3,  5, 14, 14, 14, 14],
       [ 9,  2, 14, 14, 14, 14, 14],
       [ 2,  4,  3,  2, 14, 14, 14],
       [ 3,  2, 14, 14, 14, 14, 14],
       [ 1,  4,  6, 14, 14, 14, 14],
       [ 1,  4,  6, 14, 14, 14, 14],
       [ 1,  4,  2, 14, 14, 14, 14],
       [ 7,  7,  3,  2, 10,  1, 11],
       [ 1, 12,  3, 13, 14, 14, 14]])
'''



'''
8. 원 핫 인코딩(one-hot encoding)
표현하고 싶은 단어의 인덱스에 1의 값을 부여
다른 인덱스에는 0을 부여

한계
1. 단어 개수가 늘어날수록 필요한 공간이 늘어남
2. 단어의 유사도 표현 불가

'''

from konlpy.tag import Okt
okt = Okt()

tokens = okt.morphs('나는 자연어 처리를 배운다')
# ['나', '는', '자연어', '처리', '를', '배운다']

word_to_index = {word: index for index, word in enumerate(tokens)}
# {'나': 0, '는': 1, '자연어': 2, '처리': 3, '를': 4, '배운다': 5}

# 특정 단어에 대한 원-핫 인코딩
def one_hot_encdoing(word, word_to_index):
    one_hot_vector = [0]*(len(word_to_index))
    index = word_to_index[word]
    one_hot_vector[index] = 1
    return one_hot_vector

one_hot_encdoing('처리', word_to_index)
# [0, 0, 0, 1, 0, 0]

# keras를 이용한 원-핫 인코딩
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

text = '나랑 점심 먹으러 갈래 점심 메뉴는 햄버거 갈래 갈래 햄버거 최고야'

tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
print(tokenizer.word_index)
# {'갈래': 1, '점심': 2, '햄버거': 3, '나랑': 4, '먹으러': 5, '메뉴는': 6, '최고야': 7}
sub_text = "점심 먹으러 갈래 메뉴는 햄버거 최고야"
encoded = tokenizer.texts_to_sequences([sub_text])[0]
# [2, 5, 1, 6, 3, 7]

one_hot = to_categorical(encoded)
'''
array([[0., 0., 1., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 1., 0., 0.],
       [0., 1., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 1., 0.],
       [0., 0., 0., 1., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 1.]])
'''


