# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:59:59 2025

@author: Admin

RNN
"""

'''
RNN은 모델 아키텍처가 그래프의 형태를 지니는데,
장단기 메모리(Long Short-Term Memory, LSTM)와
이를 더 단순화한 모델인 게이트 순환 유닛(Gated Recurrent Unit, GRU) 이 있다.

단순화했다는 이유는?
LSTM: 출력, 입력, 삭제 게이트가 있음
GRU: 업데이트 게이트와 리셋 게이트만으로 동작

RNN으로 텍스트 분류
    입출력 개수에 따른 구분
        문장 간 의존성과 연산 흐름 이해 필요
        
    입출력 개수에 따른 모델 유형
        일대일(one to one): 기본 모델
        일대다(one to many): 하나의 이미지 → 여러 문장 표현
        다대일(many to one): 영화 리뷰 긍정/부정 감성 분류
        다대다(many to many): 여러 단어 입력 → 여러 단어 구성 문장 번역
'''

'''
순환 신경망 RNN
'''

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# data load
df = pd.read_csv('https://bit.ly/seoul-120-text-csv')

# 문서 만들기
df['문서'] = df['제목'] + ' ' + df['내용']

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

행정의 빈도와 건강, 여성가족의 빈도수 차이가 심함
이와 같이 불균형이 심할 경우 성능 저하 문제 발생
-> 상위 3 개만 사용
'''

df = df[df['분류'].isin(['행정', '경제', '복지'])]

label_name = '분류'

X = df['문서']
y= df[label_name]

y_onehot = pd.get_dummies(y)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y_onehot,
                                                    test_size=0.2,
                                                    random_state=2025,
                                                    stratify=y_onehot)





'''
매개변수
num_words : 단어 빈도에 따라 유지될 최대 단어 수
filters:각 원소가 텍스트에서 필터링 될 문자인 문자열.
        기본값은 문자를 제외한 모든 구두점, 탭, 줄바꿈

lower : 부울. 텍스트를 소문자로 변환할지 여부
split : str. 단어 분할을 위한 구분 기호
char_level : True이면 모든 문자가 토큰으로 처리
oov_token : 주어진 경우, 그것은 word_index에 추가되고
text_to_sequence 호출 중에 어휘 밖의 단어를 대체하는 데 사용
벡터화 과정
Tokenizer 인스턴스를 생성
fit_on_texts와 word_index를 사용하여 key-value로 이루어진 딕셔너리 생성
texts_to_sequences를 이용하여 text 문장을 숫자로 이루어진 리스트로 변경
마지막으로 pad_sequences를 이용하여 리스트의 길이를 통일화

'''
from tensorflow.keras.preprocessing.text import Tokenizer
vocab_size = 1000
oov_tok = '<oov>'
tokenizer = Tokenizer(num_words =vocab_size, oov_token = oov_tok)

tokenizer.fit_on_texts(X_train)
word_to_index = tokenizer.word_index
sorted(word_to_index)[:10]

list(tokenizer.word_counts.items())[:5]

word_df = pd.DataFrame(tokenizer.word_counts.items(),
                       columns=['단어', '빈도수']).set_index('단어')

word_df.sort_values(by='빈도수',ascending=False).T

train_sequence = tokenizer.texts_to_sequences(X_train)
test_sequence = tokenizer.texts_to_sequences(X_test)


# padding
from tensorflow.keras.preprocessing.sequence import pad_sequences

max_length = 500
padding_type ='post'

X_train_sp = pad_sequences(train_sequence, maxlen = max_length, padding=padding_type)
X_test_sp = pad_sequences(test_sequence, maxlen = max_length, padding=padding_type)

# 모델 만들기

'''
SimpleRNN과 RNN, LSTM, GRU

LSTM : BiLSTM

BiLSTM의 장점
양방향 처리 : 입력 시퀀스를 앞뒤 방향으로 모두 처리
문맥의 이해 : 두 방향을 모두 고려함으로써 BiLSTM은 시퀀스 내의 맥락을 더욱 풍부하게 이해
특히 요소의 의미가 앞뒤 요소에 따라 달라지는 작업에서 매우 유용

BiLSTM의 작동 방식
BiLSTM은 두 개의 LSTM 계층으로 구성
첫 번째 계층은 입력 시퀀스를 순방향으로 처리
다른 계층은 입력 시퀀스를 역방향으로 처리

응용 분야
감정 분석 : 텍스트의 감정(예. 긍정적, 부정적)을 파악
기계 번역 : 한 언어에서 다른 언어로 텍스트를 번역하는 것
음성 인식 : 말한 언어를 텍스트로 변환

단점
표준 LSTM보다 더 많은 계산 리소스가 필요
반대 방향으로 작동하는 두 개의 LSTM 레이어가 있어 모델이 더 복잡
'''
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN, GRU, Bidirectional, LSTM, Dropout, BatchNormalization

n_class = y_train.shape[1]

# Bidirectional RNN
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=64, input_length = max_length),
    Bidirectional(LSTM(units=64, return_sequences = True)),
    BatchNormalization(),
    Bidirectional(LSTM(units=32)),
    Dropout(0.2),
    Dense(units =16, activation='relu'),
    Dense(units=n_class, activation='softmax')
    ])

model.compile(loss= 'categorical_crossentropy',
              optimizer='adam',
              metrics = ['accuracy'])
model.summary()


# 학습
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor = 'val_loss', patience=5)

history = model.fit(X_train_sp, y_train,
                    epochs=100,
                    batch_size = 64,
                    callbacks = early_stop,
                    validation_split=0.2)

df_hist = pd.DataFrame(history.history)

df_hist[['accuracy', 'val_accuracy']].plot()
plt.show()
'''
간격이 큰 것으로 보아 과적합 발생
과적합 피하기 위해
조기종료와 드롭아웃 사용햇지만..
'''

df_hist[['loss', 'val_loss']].plot()
plt.show()
'''
loss가 꾸준히 하강하다가 학습 종료했음
'''






































