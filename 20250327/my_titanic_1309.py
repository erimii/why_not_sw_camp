# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 09:48:00 2025

@author: Admin
"""

import pandas as pd

uri = './data/titanic.csv'
df = pd.read_csv(uri, sep='\t')

# 컬럼명 소문자로
df.columns = [col.lower() for col in df.columns]

# 필요한 컬럼만 추출
df1 = df[['survived', 'pclass', 'name', 'sex', 'age', 'sibsp', 'parch', 'fare']]

# female 0, male 1
df1['sex'] = df1['sex'].map({'female': 0, 'male': 1})


# name에 호칭을 숫자로
condition = lambda x:x.split(',')[1].split('.')[0].strip()
df1['title'] = df1['name'].map(condition)

Special = ['Master', 'Don', 'Rev']
df1['title'] = df1['title'].apply(lambda x: 1 if x in Special else 0)


# 동반자 수 컬럼 추가
sibpar = df1['sibsp'] + df1['parch']
df1['num_family'] = sibpar + 1

# 1인당 평균 탑승 요금 넣기
df1['fare'] = df1['fare'] / df1['num_family']

df1.drop(['sibsp', 'parch', 'name'], axis=1, inplace=True)
df1.dropna(inplace=True)

df1.info()

# ------------------------------
raw = df1
np_raw = raw.values
# ------------------------------
train = np_raw[:100]
test=np_raw[100:]

y_train = [i[0] for i in train]
y_test = [i[0] for i in test]

X_train = [i[1:] for i in train]
X_test = [i[1:] for i in test]

print(len(y_train), len(y_test),len(X_train),len(X_test))
# 100 26 100 26
# ------------------------------
'''
[의사결정나무]
여러 개의 "예/아니오" 질문을 따라가면서 최종 결론을 내리는 방법!
'''
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(criterion='entropy',
                               max_depth=3,
                               min_samples_leaf=5)

model.fit(X_train, y_train)

# 생존률
model.score(X_train, y_train) # 0.84
model.score(X_test, y_test) # 0.8846153846153846

# 시각화
from sklearn.tree import export_graphviz

export_graphviz(
    model,
    out_file='titanic.dot',
    feature_names=['pclass', 'sex', 'age', 'title', 'fare', 'num_family'],
    class_names=['0','1'],
    rounded=True,
    filled=True)

import graphviz
import os

graphviz_path = "C:\\Program Files\\Graphviz\\bin"
os.environ["PATH"] += os.pathsep + graphviz_path

with open('titanic.dot') as f:
    dot_graph = f.read()

dot = graphviz.Source(dot_graph)
dot.format = 'png'
dot.render(filename='titanic_tree',
           directory = 'image/decision_trees',
           cleanup= True)

# 평가
from sklearn.metrics import confusion_matrix # 분류 모델 성능 평가
from sklearn.metrics import accuracy_score # 분류모델 정확도 계산

y_pred=model.predict(X_test)
print(accuracy_score(y_test, y_pred)*100)

confusion_matrix(y_test, y_pred)
'''
array([[18,  1],
       [ 2,  5]], dtype=int64)

18: TN '0'을 올바르게 예측
1: FP '0'인데 '1'로 예측
2: FN '1'인데 '0'으로 예측
5: TP '1'을 올바르게 예측
'''

feature_names=['pclass', 'sex', 'age', 'title', 'fare', 'num_family'],
Tom=[1,1,33,1,50,4]
Jane=[2,0,50,0,8,1]

model.predict_proba([Tom])
# array([[0.64705882, 0.35294118]])
model.predict_proba([Jane])
# array([[0.16666667, 0.83333333]])

# ------------------------------

'''
[로지스틱 회귀 분석]
어떤 일이 일어날지 안 일어날지 (예/아니오)를 예측하는 방법"
결과는 "예"가 될 확률을 0부터 1 사이의 값으로 출력
"S자 모양"의 특별한 곡선을 이용해서 확률을 예측.
'''
from sklearn.linear_model import LogisticRegression

# 정규화
X= df1

from sklearn.preprocessing import MinMaxScaler, StandardScaler
MMS = MinMaxScaler()
SS=StandardScaler()

X_ss = SS.transform(X)
X_mms = MMS.transform(X)

X_ss_pd = pd.DataFrame(X_ss, columns=X.columns)
X_mms_pd = pd.DataFrame(X_mms, columns=X.columns)

#------------------------------------------
y = raw['survived']
X=raw.drop(['survived'], axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,
                                                    test_size=0.2,
                                                    random_state=13)

import numpy as np
np.unique(y_train, return_counts = True)

X_out = X_mms_pd
X_train, X_test, y_train, y_test = train_test_split(X_out,y,
                                                    test_size=0.2,
                                                    random_state=13)

log_reg = LogisticRegression(C=10.,
                             solver='liblinear',
                             random_state=13)

log_reg.fit(X_train, y_train)

pred = log_reg.predict(X_test)
accuracy_score(y_test, pred) # 왜 1임?

X_out = X_ss_pd
X_train, X_test, y_train, y_test = train_test_split(X_out,y,
                                                    test_size=0.2,
                                                    random_state=13)


log_reg = LogisticRegression(C=10.,
                             solver='liblinear',
                             random_state=13)

log_reg.fit(X_train, y_train)

pred = log_reg.predict(X_test)
accuracy_score(y_test, pred)

log_reg.coef_
'''
array([[ 4.73666302e+00, -2.53303155e-01, -5.08052874e-01,
        -1.93453169e-01,  3.13171381e-02,  2.68954893e-03,
        -1.70331998e-01]])

회귀 계수: 독립변수가 종속변수에 얼마나 영향을 미치는지 알려주는 숫자.
+면 양의 관계, -면 음의 관계
|숫자|가 클수록 영향 크게 미침
'''













