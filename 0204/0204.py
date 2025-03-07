# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 09:05:26 2025

@author: Admin
함수에 대하여
def 함수명():
    처리할 내용
"""
# 함수 선언
def print_ntimes():
    print('rubi zzang')
    
# 함수 호출
print_ntimes()


'''
어떤 주식 종목의 전날 종가를 입력받아
상한가(30%)를 계산하고
그 값을 반환하는 함수를 작성
'''
def call_upper(price):
    upper_price = price*1.3
    return upper_price

upper = call_upper(1000)
print(upper)

'''
전일 종가, 상한, 하한을 입력받은 후
상한가와 하한가를 한 번에 계산하여 반환하는 함수
단, 상한가는 매일 변경될 수 있다
'''
def call_upper_lower(price, up, low):
    upper=price * (1+(up/100))
    lower=price * (1-(low/100))
    return upper, lower

upper, lower = call_upper_lower(2000, 20, 30)
print(upper)
print(lower)


































