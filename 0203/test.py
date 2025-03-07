# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:10:36 2025

@author: rubi

0203 python 실습
"""
8
import random
random.random()
for i in range(5):
    num1=random.randint(2,9)
    num2=random.randint(1,9)
    
    quesiton = str(num1)+' x '+str(num2)+' = '
    answer = int(input(quesiton))
    
    if answer != num1*num2 :
        print(f'You are wrong! The correct answer is {num1*num2}!')


# 50이상 쓴 금액 출력
spending = [25,36,8,53,24,56]
ls =[]
for i in spending:
    if i >= 50:
        ls.append(i)

print(ls)


data =[
       [1,'미국',46,37,38,121],
       [2,'영국',27,23,17,67],
       [3,'중국',26,18,26,70],
       [4,'러시아',19,18,19,56],
       [5,'독일',17,10,15,42],
       [6,'일본',12,8,21,41],
       [7,'프랑스',10,18,14,42],
       [8,'대한민국',9,3,9,21] 
       ]

for row in data :
    if row[2] < row[3] :
        print(f'{row[1]} 금메달:{row[2]}, 은메달:{row[3]}')
        
        
        

# 부동산 매물 알림
street = '서울시 종로구'
types = '아파트'
number_of_rooms = 3
price = 10000000000

print('###################')
print('# 부동산 매물 광고 #')        
print('###################')     
print('')
print(f'{street}에 위치한 아주 좋은 {types}가 매물로 나왔습니다. {types}는 {number_of_rooms}개의 방을 가지고 있으며 가격은 {price}원 입니다.')
        






drink_name = ['아메리카노', '카페라떼', '카푸치노']
drink_price = [2000, 3000, 3500]

sales =[]
for i in drink_name:
    sales.append(int(input(f'{i}의 판매개수:')))

total=0
for i in range(3):
    total += drink_price[i]*sales[i]
    
print(f'총 판매 금액은 {total}원 입니다.')





'''
자동판매기는 사용자로부터 투입한 돈과 물건값을 입력받는다
물건값은 100원 단위라고 가정
프로그램은 잔돈을 계산하여 출력
자판기는 동전 500원, 100원 짜리만 가지고있다고 가정

투입한돈 : 5000
물건 값: 2600

거스름돈 :2400
500원 동전의 개수:4
100원 동전의 개수:4
'''

money = int(input('투입한 돈: '))
price = int(input('물건 값: '))

print(f'거스름돈: {money-price}')
print(f'500원 동전의 개수: {(money-price)//500}')
print(f'100원 동전의 개수: {((money-price)%500)//100}')








midterm = {'도윤': 43, '하윤': 82, '시우': 76,
           '지유': 61, '주원': 94}

student = input('어떤 학생의 점수가 궁금한가요?')

if student in midterm.keys() :
    print(midterm[student], '점 입니다.')
else:
    print('해당 학생이 없습니다.')


for k, v in midterm.items():
    print(f'{k}의 점수는{v}')








