# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 09:08:21 2025

@author: Admin
"""

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 데이터 준비
filePath = 'https://raw.githubusercontent.com/blackdew/tensorflow1/master/csv/iris.csv'
iris = pd.read_csv(filePath)
iris.head()
iris.info()
'''
 0   꽃잎길이    150 non-null    float64
 1   꽃잎폭     150 non-null    float64
 2   꽃받침길이   150 non-null    float64
 3   꽃받침폭    150 non-null    float64
 4   품종      150 non-null    object 
 '''
iris['품종'].value_counts()
'''
품종
setosa        50
versicolor    50
virginica     50
'''
# 원-핫 인코딩
encode = pd.get_dummies(iris)

ind = encode.iloc[:,:4]
dep = encode.iloc[:,4:]

X = tf.keras.layers.Input(shape=[4])
Y = tf.keras.layers.Dense(3, activation = 'softmax')(X)
model = tf.keras.models.Model(X,Y)
model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(ind, dep, epochs=100)

model.predict(ind[:5])
'''
[[0.6886242 , 0.10155978, 0.20981596],
[0.6399689 , 0.13006285, 0.22996831],
[0.67086416, 0.11305016, 0.2160857 ],
[0.6457227 , 0.13792948, 0.21634784],
[0.6995269 , 0.0979647 , 0.20250835]],
'''
dep[:5]
'''
   품종_setosa  품종_versicolor  품종_virginica
0       True          False         False
1       True          False         False
2       True          False         False
3       True          False         False
4       True          False         False
'''

model.predict(ind[-5:])
'''
array([[0.04584517, 0.33005303, 0.6241018 ],
       [0.06676155, 0.36740923, 0.5658292 ],
       [0.07544409, 0.3479659 , 0.57659006],
       [0.06595609, 0.29930133, 0.63474256],
       [0.11453639, 0.3420426 , 0.543421  ]],
'''
dep[-5:]
'''
     품종_setosa  품종_versicolor  품종_virginica
145      False          False          True
146      False          False          True
147      False          False          True
148      False          False          True
149      False          False          True
'''

# 학습된 가중치(기울기)와 절편 확인
weights, bias = model.get_weights()
print(f'기울기(Weight): {weights[0][0]}')
print(f'절편(Bias): {bias[0]}')

# 모델 확인
model.summary()
























































