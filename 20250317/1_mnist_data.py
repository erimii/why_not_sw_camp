# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:04:47 2025

@author: Admin

이미지
1. 패션 MNIST 데이터셋 임포트
2. 데이터 탐색
3. 데이터 전처리
4. 모델 구성 층 / 모델 컴파일
5. 모델 훈련
6. 정화도 평가
7. 예측

tf. keras 사용

"""
# import
import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top','Trouser','Pullover','Dress',
               'Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']

### 데이터 탐색
train_images.shape # (60000, 28, 28)

# 데이터 전처리
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

# 신경망 모델에 주입 전 값의 범위를 0-1사이로 조정
train_images = train_images / 255.0
test_images = test_images / 255.0

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])

plt.show()


# 모델 구성
'''
신경망으 기본 구성 요소는 layer
layer는 주입된 데이터에서 표현을 추출
'''
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)), # 2차원 배열의 이미지 포맷을 1차원 배열로 변환
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation = 'softmax') # 10개 클래스 중 하나에 속할 확률 출력
    ])

model.compile(loss = 'sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


model.fit(train_images, train_labels, epochs=5)

# 정확도 평가
pred = model.predict(train_images[0:5])
print(np.round(pred, 2))





















































