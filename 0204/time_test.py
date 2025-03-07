# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:54:12 2025

@author: Admin
"""

# 시계열 데이터 분석을 위한 시간 다루기

import time

# time()
# 1970.1.1.0:0:0 부터 현재까지의 시간을 숫자로 표현
time.time()
# -> 1738638400.8208778

time.ctime()
# -> 'Tue Feb  4 12:07:08 2025'

currnet_time = time.ctime()

print(currnet_time.split()[-1])
# -> 2025

# sleep() 잠시멈춤 / 초단위

for i in range(10):
    print(i)
    
for i in range(10):
    print(i)
    time.sleep(1)
    


# 모듈 import 방법
import os
os.listdir()

from os import listir
listdir

from os import *

import os as winos
winos.listdir()







'''파이썬 내장함수'''
#abs(): 절댓값
x=-3
abs(x) 
# -> 3

# chr(): 유니코드 값을 문자로 변환
x=97
chr(x)
# -> 'a'

# enumerate()
for i , stock in enumerate(['naver', 'kakao', 'lg']):
    print(i, stock)
'''
0 naver
1 kakao
2 lg
'''

# id():고유값(객채의 메모리 주소) 반환
a=1
id(a)
# -> 140720567495096


# 길이(데이터 갯수)
len()

# list()
list('python')
# -> ['p', 'y', 't', 'h', 'o', 'n']

# 최댓값/최솟값
lst = [2,8,5]
max(lst)
min(lst)

# 정렬
sorted(lst)
sorted(lst, reverse=True)



'''
입력 : ['Seoul', 'Daegu', 'Kwangju', 'Jeju'] 
출력 : ['SEO', 'DAE', 'KWA', 'JEJ']
'''
loc = ['Seoul', 'Daegu', 'Kwangju', 'Jeju'] 

def get_abbr(data_list):
    lst =[]
    for i in data_list:
        lst.append(i[:3].upper())
    return lst

get_abbr(loc)






































