# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:16:27 2025

@author: Admin
"""

'''
iterator class
'''

class MyIterator:
    def __init__(self, data):
        self.data=data
        self.positon = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.positon >=len(self.data):
            raise StopIteration
        result = self.data[self.ppsition]
        self.positon +=1
        return result
    
if __name__ == '__main__':
    i = MyIterator(([1,2,3]))
    for item in i:
        print(item)
        
        
         


'''
generator : Iterator를 생성해주는 함수
next() 데이터 추출 가능
단, yield result 
'''

def mygen():
    yield 'a'
    yield 'b'
    yield 'c'

g = mygen()

next(g)

import time

def longtime_job():
    print('dfd')
    
    time.sleep(1)
    return 'done'

list_job = [longtime_job() for i in range(5)]

print(next(list_job))



# lasy
list_job = (longtime_job() for i in range(5))

print(next(list_job))


















































        