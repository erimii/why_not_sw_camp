# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:08:58 2025

@author: Admin

seoul.csv를 이용한 시각화
"""

'''
파이썬의 csv 모듈

csv.reader() :csv 파일에서 데이터를 읽어오는 함수
csg.writer() : csv 파일에서 데이터를 저장하는 함수
'''

### csv.reader()
'''
1. csv모듈 불러오기
2. csv 파일을 open()으로 열고 f변수에 저장
3. f변수를 reader()에 전달 -> csv reader 객체
'''

import csv
f = open('./data/seoul.csv', 'r', encoding='cp949')
# 'r' : 읽기 전용
data = csv.reader(f, delimiter=',')
# csv파일 유형 2가지: ,로 구분 / tab으로 구분
# delimiter=',' : seoul.csv를 읽어낼 때 ,로 분리해서 저장해라
# reader()는 한줄 읽어서 list 형태로 저장

print(data)
# -> <_csv.reader object at 0x0000025B3CD7B220>

seoul_list = []
for row in data :
    seoul_list.append(row) # 2차원 리스트가 됨
 #   print(row) -> for문으로 읽으면 데이터 출력됨
f.close()




f = open('./data/seoul.csv')
data = csv.reader(f)
header = next(data)
# next(): 실행할때마다 한 행씩 반환하면서 데이터를 패스

# 결측치 발생했을 경우 처리
'''
1. 해당 데이터를 삭제
2. 결측치를 최고값/최소값/평균값/임의의수 로 대체
'''
max_temp=-999
max_date=''

seoul_list_noheader =[]
for row in data:
    if row[-1] == '':
        row[-1] = max_temp
    row[-1] = float(row[-1]) # 최고 기온을 실수로 변경
    
    if max_temp < row[-1]:
        max_date = row[0]
        max_temp = row[-1]
    seoul_list_noheader.append(row)
f.close()

print(f'기온이 가장 높았던 날은 {max_date}로, {max_temp}도 였습니다.')



# 최고 기온 시각화
import matplotlib.pyplot as plt

f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

# 최고 기온 데이터를 저장할 리스트
result=[]
for row in data:
    if row[-1] != '':
        result.append(row[-1])

plt.figure(figsize=(10,6), dpi = 300)
plt.plot(result, 'r')
plt.show()


### 1983년 이후 매년 내 생일에 해당하는 최고/최저 기온을 추출하여 시각화
# split('-') 사용 -> ['1908', '02', '03']
f = open('./data/seoul.csv')
data = csv.reader(f)
next(data)

high = []
low = []
for row in data:
    if row[-1] != '' and row[-2] != '' :
        date_split = row[0].split('-')
        if 1983 <= int(date_split[0]):
            if date_split[1] == '03' and date_split[2] == '03' :
                    high.append(float(row[-1]))
                    low.append(float(row[-2]))

# 맑은 고딕으로 기본 글꼴 설정
plt.rc('font', family = 'Malgun Gothic')

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10,6), dpi = 300)
plt.title('my birthday high & low')

# 선 형태: ls = '' / linestyle = , lw= 선 두께
plt.plot(high, 'red', label = 'high', linestyle= '--')
plt.plot(low, 'blue', label = 'low', linestyle= ':')
plt.legend()
plt.show()










































