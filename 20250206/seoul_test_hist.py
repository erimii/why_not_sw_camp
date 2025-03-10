# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:02:03 2025

@author: Admin

히스토그램:hist()
자료의 분포 상태(데이터의 빈도)를 직사각형 모양의 막대 그래프로 나타냄
"""

import matplotlib.pyplot as plt

hist_data = [1,1,2,3,4,5,6,6,7,8,10]

plt.hist(hist_data)
plt.show()


# 8월 데이터만 뽑아서 히스토그램으로
import matplotlib.pyplot as plt
import csv

f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

result=[]
for row in data:
    month = row[0].split('-')[1]
    if row[-1] != '':
        if month == '08':
            result.append(float(row[-1]))
        
plt.hist(result, bins = 100, color = 'r')
# bins= : 구간은 100개
plt.show()

'''
역대 8월에는 최고 기온이 30도인 날이 가장 많았고
최고 기온이 20도 이하이거나 40도 에 가까웠던 적은 거의 없었다
'''




# 1월, 8월 데이터만 뽑아서 히스토그램으로
import matplotlib.pyplot as plt
import csv

f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

aug=[]
jan=[]
for row in data:
    month = row[0].split('-')[1]
    if row[-1] != '':
        if month == '08':
            aug.append(float(row[-1]))
        elif month == '01':
            jan.append(float(row[-1]))
        
plt.hist(aug, bins = 100, color = 'r', label = 'Aug')
plt.hist(jan, bins = 100, color = 'b', label = 'Jan')
# bins= : 구간은 100개
plt.legend()
plt.show()

'''
역대 8월에는 최고 기온이 30도인 날이 가장 많았고
최고 기온이 20도 이하이거나 40도 에 가까웠던 적은 거의 없었다

8월의 히스토그램은 20~40범위
1월의 히스토그램은 -10~10 범위
'''

# 기온 데이터를 상자 그림: (boxplot)
'''
최댓값, 최솟값, 상위 1/4, 2/4(중앙값), 3/4에 위치한 값을 보여주는 그래프
'''

import matplotlib.pyplot as plt
import random

result = []
for i in range(13):
    result.append(random.randint(1, 1000))


plt.boxplot(result)
plt.show()



# 1월, 8월 데이터만 뽑아서 히스토그램으로
import matplotlib.pyplot as plt
import csv

f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

aug=[]
jan=[]
for row in data:
    month = row[0].split('-')[1]
    if row[-1] != '':
        if month == '08':
            aug.append(float(row[-1]))
        elif month == '01':
            jan.append(float(row[-1]))
        
plt.boxplot([aug, jan])
plt.show()

'''
이상치(outlier)
다른 수치에 비해 너무 크거나 작은 값을 자동으로 나타낸 것
'''


### 최고 기온 데이터를 월별로 구분 ###
'''
1. 데이터를 월별로 분류해 저장
2. 원별 데이터를 상자그림으로 표현
'''
import matplotlib.pyplot as plt
import csv

f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

months = [[] for _ in range(12)]

for row in data:
    if row[-1] != '':
        months[int(row[0].split('-')[1])-1].append(float(row[-1]))
        
plt.boxplot(months)
plt.show()




























