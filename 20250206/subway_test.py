# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:54:58 2025

@author: Admin
"""

# 지하철 시간대별 승하차 인원 추이

'''
1. 데이터 읽어오기
2. 모든 역에 대한 시간대별 승하차 인원 각각 누적
3. 시간대별 승하차 인원 시각화
'''

import csv
import matplotlib.pyplot as plt

f = open('./data/subwaytime.csv')
data = csv.reader(f)

# 지하철 시간대별 이용 현황 데이터 정제 
'''
header 데이터가 2개 next() 함수로 제외

'''

next(data)
next(data)

# 24시간 데이터를 순서대로 저장하기 위해 리스트 사용
'''
밤 11시: 23:00:00 ~ 23:59:59

승차 시간이 1시간씩 늦어질 때 마다 인덱스는 2씩 늘어남
승차를 시작하는 인덱스 값은 4
승차 시각(t)과 승차 인원이 적힌 인덱스(i) 값의 관게를 분석
-> i = 4+(t-4)*2
'''
# 시간별 승하차 데이터를 저장할 리스트 생성
s_in = [0]*24
s_out = [0]*24

# 각 행의 4번 인덱스부터 마지막까지의 데이터는 정수로 변환
'''
map(변환 함수,변환 데이터) 사용
'''

for row in data:
    row[4:] = map(int, row[4:])
    
    # 모든 역에 대한 시간대별 승하차 인원 누적
    for i in range(24):
        s_in[i] += row[4+i*2]
        s_out[i] += row[5+i*2]

plt.figure(dpi=300)
plt.rc('font', family = 'Malgun Gothic')
plt.title('지하철 시간대별 승하차 인원 추이')

plt.plot(s_in, label = '승차')
plt.plot(s_out, label = '하차')
plt.grid()
plt.legend()

plt.xticks(range(24), range(4,28))

plt.show()



# 사람들이 가장 많이 타는 역은 어딜까?
# 각 역의 데이터를 막대그래프로 시각화
# 단, x축은 plt.xticks(range(24), mx_station, rotatoin=90)을 사용
import csv
import matplotlib.pyplot as plt

f = open('./data/subwaytime.csv')
data = csv.reader(f)

next(data)
next(data)

mx = [0]*24
mx_station = ['']*24

for row in data:
    row[4:] = map(int, row[4:])
    for i in range(4):
        n = row[4+i*2]
        if n > mx[i]:
            mx[i] = n
            mx_station[i] = row[3]

plt.figure(dpi=300)
plt.rc('font', family = 'Malgun Gothic')
plt.title('지하철 시간대별 max인 승차 역')
plt.bar(range(24), mx)
plt.xticks(range(24), mx_station, rotation=90)
plt.show()






















