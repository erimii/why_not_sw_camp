# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:56:25 2025

@author: Admin
"""

'''
우리동네 인구 구조 시각화
인구 구조를 다양한 형태로 시각화
인구 구조를 파이 차트로
인구 구조를 산점도로
'''

'''
인구 구조를 시각화

1. 인구 데이터 파일 읽어오기
2. 전체 데이터에서 한 줄씩 반복해서 읽어오기
3. 우리 동네에 대한 데이터인지 확인
4. 우리 동네일 경우 0세부터 100세 이상까지의 인구수를 순서대로 저장
5. 저장된 연령별 인구수 데이터를 시각화
'''

import csv
import matplotlib.pyplot as plt

f = open('./data/age.csv')
data = csv.reader(f)

result = []

name = input('인구 구조가 알고 싶은 지역 이름을 입력해주세요: ')

for row in data:
    if name in row[0]:
        for i in row[3:]:
            result.append(int(i))

plt.style.use('ggplot')
plt.title(name + '지역의 인구 구조')
plt.plot(result)
plt.show()

plt.bar(range(101), result)
plt.show()

plt.barh(range(101), result)
plt.show()



# 남녀 성별 인구 분포
import csv
import matplotlib.pyplot as plt

f = open('./data/gender.csv')
data = csv.reader(f)

m =[] # 3:104
f =[] # 106:

name = input('남녀 분포가 알고 싶은 지역 이름을 입력해주세요: ')

for row in data:
    if name in row[0]:
        for i in row[3:104]:
            m.append(-int(i)) # 0을 기준으로 남자는 왼쪽에 표현하기 위해 - 붙임
        for i in row[106:]:
            f.append(int(i))

plt.style.use('ggplot')
plt.figure(figsize=(10,5), dpi=300)
plt.rc('font', family = 'Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
plt.title(name + '지역의 인구 구조')
plt.barh(range(101), m, label = 'male') # len(m)와 갯수가 맞아야됨
plt.barh(range(101), f, label = 'female')
plt.show()


import csv
import matplotlib.pyplot as plt


f = open('./data/gender.csv')
data = csv.reader(f)

m=[]
f=[]

name = input('궁금한 지역을 입력해주세요: ')

for row in data:
    if name in row[0]:
        for i in range(3,104):
            m.append(int(row[i]))
            f.append(int(row[i+103]))
        break

plt.plot(m, label = 'Male')
plt.plot(f, label = 'Female')
plt.legend()
plt.show()
            

### 파이차트 : pie()
'''
전체 데이터 중 특정 데이터의 비율
'''

import matplotlib.pyplot as plt

plt.rc('font', family = 'Malgun Gothic')
size = [2441,2312,1031,1233]
label = ['A형', 'B형', 'AB형', 'O형']
color = ['darkmagenta', 'pink', 'deeppink', 'hotpink', 'pink']

plt.pie(size, 
        labels=label, 
        colors=color, 
        autopct = '%.1f%%',
        explode=(0,0,0.1,0)) # 소수점 이하 한자리 까지
plt.axis('equal')
plt.legend()
plt.show()


##### 지역명(경기도/서울특별시 등..) 입력했을 때 남녀 성비 파이차트로 표현

import csv
import matplotlib.pyplot as plt


f = open('./data/gender.csv')
data = csv.reader(f)

name = input('찾고 싶은 지역 이름을 입력해주세요: ')

size = [] # 남/여

for row in data :
    if name in row[0]:
        m=0
        f=0
        for i in range(101):
            m += int(row[i+3])
            f += int(row[i+106])
        break

size.append(m)
size.append(f)

plt.rc('font', family = 'Malgun Gothic')
label = ['Male', 'female']
color = ['crimson', 'darkcyan']

plt.pie(size, 
        labels=label, 
        colors=color, 
        autopct = '%.1f%%',
        startangle=90) # 소수점 이하 한자리 까지
plt.title(name + ' 지역의 남녀 성별 비율')
plt.legend()
plt.show()
























