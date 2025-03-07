# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:21:33 2025

@author: Admin
"""

'''
다음의 주가가 89,000원이고
네이버의 주가가 751,000원이라고 가정하고,
어떤 사람이 다음 주식 100주와 네이버 주식 20주를 가지고 있을 때
그 사람이 가지고 있는 주식의 총액을 계산하는 프로그램을 적성
'''
daum = 89000
naver = 751000

total = daum*100 + naver*20

print(total)


'''
위에서 구한 주식 총액에서
다음과 네이버의 주가가 각각 5%, 10% 하락한 경우에
손실액을 구하는 츠로그램을 작성
'''
loss = total - (daum*0.95*100+ naver*0.9*20)

print(loss)


'''
월요일에 너이버의 주가가 100만원 으로 시작해
3일 연속으로 하한가(-30%)를 기록했을 때 수요일의 종가를 계산
'''
amount = 100
for i in range(3):
    amount *=0.7

print(amount*10000)


'''
s라는 변수에 Daum KaKao라는 문자열이 있다고 했을 때
문자열의 슬라이싱 기능과 연결하기를 이용해
s의 값을 KaKao Daum으로 변환
'''
s = 'Daum KaKao'

ss = s.split()
ss = ss[1] + ' ' + ss[0]
print(ss)

sss = s[5:] + ' ' + s[:4]
print(sss)


'''
a라는 변수에 'hello world'라는 문자열이 있다고 했을 때
a의 값을 'hi world'로 변경
'''
a = 'hello world'
a = a.replace('hello', 'hi')
print(a)


'''
x라는 변수에 'abcdef'라는 문자열이 있다고 했을 때
x의 값을 'bcdefa'로 변경
'''
x = 'abcdef'
x = x[1:]+x[0]
print(x)


'''
문제 3
'''
naver_closing_price = [474500, 461500, 501000, 500500, 488500]

print(max(naver_closing_price))

print(max(naver_closing_price)-min(naver_closing_price))


'''
신문배달
arrears리스트에 있는 새대에는 신문을 배달하지 않아야 한다
'''
apart = [[101,102,103,104],
        [201,202,203,204],
        [301,302,303,304],
        [401,402,403,404],
        ]

arrears = [101, 203, 301, 404]

for i in range(len(apart)):
    for j in range(len(apart[i])):
        if apart[i][j] in arrears:
            print(f'{apart[i][j]}호는 신문배달하지 않는다')
        else:
            print(f'{apart[i][j]}호 신문 배달 완료')

