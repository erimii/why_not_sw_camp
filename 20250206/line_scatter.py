# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:21:18 2025

@author: Admin
"""


# 산점도 : scatter()
'''
산점도는 여기저기 점이 흩어진 모양의 그래프
x축과 y축에 해당하는 데이터의 상관관계를 표현할 때 사용
두 개의 축을 기준으로 데이터가 얼마나 퍼져있는지 

scatter()
x축에 해당하는 데이터 / y축에 해당하는 데이터
각각 넣으면 그에 해당하는 산점도가 나옴
'''

import csv
import matplotlib.pyplot as plt

plt.style.use('ggplot')
x = [1,2,3,4]
y = [10,20,30,40]
size = [100,25,200,180]

plt.scatter(x, y, s=size, c = range(4), cmap='jet')
plt.colorbar()
plt.show()







import csv
import matplotlib.pyplot as plt
import math

f = open('./data/gender.csv')
data = csv.reader(f)

m=[]
f=[]

size = []

name = input('궁금한 지역을 입력해주세요: ')

for row in data:
    if name in row[0]:
        for i in range(3,104):
            m.append(int(row[i]))
            f.append(int(row[i+103]))
            size.append(math.sqrt(int(row[i]) + int(row[i+103]))) # 점 사이즈
        break

plt.rc('font', family = 'Malgun Gothic')
plt.scatter(m, f, s = size,  c=range(101), cmap='jet', alpha=0.5)
plt.colorbar()

# 추세선 추가  plot()
'''
남성 인구수 중 가장 큰 값을 기준으로 
y=x형태의 직선
'''
plt.plot(range(max(m)), range(max(m)), 'g')
plt.xlabel('male')
plt.ylabel('female')
plt.title(name + ' 지역의 성별 인구 그래프')
plt.show()
            



































