# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:45:08 2025

@author: Admin
클래스에 대하여

클래스 구조
1. 클래스 선언부: class 클래스명 :
    2. 함수 선언
    3.변수 선언
    4.생성자 선언

클래스명: 첫글자는 대문자로 표현

클래스 내에 함수 선언:
def 함수명(self, 매개변수1, 매개변수2, ...):
    self.변수명1 = 매개변수1
    self.변수명2 = 매개변수2
    
"""

class BusinessCard:
    def __init__(self, name, email, addr):
        self.name = name
        self.email = email
        self.addr = addr
        
    def print_info(self):
        print('---------------')
        print(f'이름: {self.name}')
        print(f'이메일: {self.email}')
        print(f'주소: {self.addr}')
        print('---------------')
    

member1 = BusinessCard('rubi', 'rubi@n.com', 'seoul')

member1.print_info()



class Account:
    num_account=0 # 클래스 변수
    
    def __init__(self, name):   # 객체가 생성될 때 자동 호출
        self.name = name # 인스턴스 변수
        Account.num_account += 1
    
    
kang = Account('kang')
kim = Account('kim')

# 클래스 변수는 객체 없이 클래스명으로 바로 사용  가능
print(Account.num_account)

print(kang.num_account) # 2

print(kim.num_account) # 2



# 클래스 상속
# 부모 클래스의 내용을 자식 클래스가 물려받을 경우

class ParentClass:
    def can(self):
        print('pc의 can')

class ChildClass(ParentClass):
    pass

p = ParentClass()
p.can() # pc의 can

c = ChildClass()
c.can() # pc의 can





































































