# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:33:59 2025

@author: Admin

다중 클래스 분류
-> 세개 이상의 선택지 중 하나를 고르는 문제

분꽃 분류

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import urllib.request

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

urllib.request.urlretrieve('https://raw.githubusercontent.com/ukairia777/tensorflow-nlp-tutorial/main/06.%20Machine%20Learning/dataset/Iris.csv', filename='Iris.csv')

data = pd.read_csv('Iris.csv', encoding='Latin1')
len(data) # 150
data[:5]
'''
        꽃받침 길이,    꽃받침 넓이,   꽃잎 길이,      꽃잎 넓이,         품종
   Id  SepalLengthCm  SepalWidthCm  PetalLengthCm  PetalWidthCm      Species
0   1            5.1           3.5            1.4           0.2  Iris-setosa
1   2            4.9           3.0            1.4           0.2  Iris-setosa
2   3            4.7           3.2            1.3           0.2  Iris-setosa
3   4            4.6           3.1            1.5           0.2  Iris-setosa
4   5            5.0           3.6            1.4           0.2  Iris-setosa
'''
data['Species'].value_counts()
'''
Species
Iris-setosa        50
Iris-versicolor    50
Iris-virginica     50
'''

sns.set(style='ticks', color_codes=True)

sns.pairplot(data, hue = 'Species', palette='husl')
plt.show()

'''
4개의 특성에 대해서
모든 쌍의 조합인 16개의 경우에 대해서 산점도
동일한 특성의 쌍일 경우에는 히스토그램
'''

# 각 종과 특성에 대한 연관 관계
sns.barplot(x=data['Species'], y = data['SepalWidthCm'], errorbar=('ci',95))
plt.show()

# 레이블에 해당하는 Species열에 수치화
data['Species'] = data['Species'].replace(['Iris-virginica', 'Iris-setosa', 'Iris-versicolor'], [0,1,2])

data_X = data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].values
data_y = data['Species'].values

data_X[:5]
'''
array([[5.1, 3.5, 1.4, 0.2],
       [4.9, 3. , 1.4, 0.2],
       [4.7, 3.2, 1.3, 0.2],
       [4.6, 3.1, 1.5, 0.2],
       [5. , 3.6, 1.4, 0.2]])
'''
data_y[:5]
# array([1, 1, 1, 1, 1]

# ------------------------모델에 학습 시키기 위한 전처리 끝----------------------

# 훈련 데이터와 테스트 데이터 분리 -> 8:2
(X_train, X_test, y_train, y_test)=train_test_split(data_X, 
                                                    data_y, 
                                                    train_size=0.8, 
                                                    random_state=1)

# 원 핫 인코딩
y_train = to_categorical(y_train)
y_test= to_categorical(y_test)


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers

model = Sequential()
model.add(Dense(3, input_dim=4, activation='softmax'))

# 옵티마이저는 경사하강법의 일종인 adam을 사용
# 손실 함수는 크로스 엔트로피 함수
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=200, batch_size=1,validation_data=(X_test, y_test))

epochs = range(1, len(history.history['accuracy'])+1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


epochs = range(1, len(history.history['accuracy'])+1)
plt.plot(epochs, history.history['accuracy'])
plt.plot(epochs, history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

print('\n 테스트 정확도: %.4f' % (model.evaluate(X_test, y_test)[1]))
#  테스트 정확도: 1.0000








































