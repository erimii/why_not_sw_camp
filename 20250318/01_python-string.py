# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:38:40 2025

@author: Admin
"""
### 데이터의 타입

# 소수점이 없는 숫자는 int 형이다.
type(1)

# 따옴표로 감싸주면 문자형으로 바뀐다.
type("1")

type("하나 One")

type(["파이썬", "Python"])


### 문자열

# 문자열은 큰따옴표나 작은따옴표로 표현할 수 있다.
"문자열은 큰따옴표나 작은따옴표로 표현할 수 있다."

# 문자열은 큰따옴표나 작은따옴표로 표현할 수 있다.
'문자열은 큰따옴표나 작은따옴표로 표현할 수 있다.'

'작은따옴표 안에 '작은따옴표'를 쓰면 오류가 발생한다.'

"그래서 문자열을 구현할 때 '작은따옴표'가 문자열 안에 들어 있다면 문장을 큰따옴표로 감싸주고 사용한다."


### 오류 처리

'작은따옴표로만 구현할 때 \'역슬래시\'를 통해 예외 처리를 할 수도 있다.'

# 따옴표 3개를 앞뒤로 감싸주면 줄바꿈 문자를 표현한다.
"""
줄바꿈
문자를
표현한다.
"""

# 문자를 이어 작성하면 붙여서 반환이 된다.
'Py' 'thon'

# 따옴표가 없으면 숫자이다.
1 + 1

# 따옴표가 있으면 문자이다.
"1" + "1"

# 문자와 문자를 더하거나 곱해도 같은 결과를 보여준다.

"파이썬" + "좋아요"

"파이썬좋아요" * 3

# 더하기(+)를 이용해서 문자와 문자는 연결할 수 있지만 문자와 숫자는 연결할 수 없다
"문자는 숫자와 더할 수 없다." + 1 

# 더하기(+)를 이용해서 문자와 문자는 연결할 수 있지만 문자와 숫자는 연결할 수 없다. 이럴 때는 f-string을 사용하여 연결할 수 있다.
f"1+{1}"


num = 0
f"오늘의 코로나 확진자는 {num}명 입니다."


### 변수
# 변수(아래 코드에서 addess에 해당)에 문자열을 할당하면 코드 블록이 길게 이어지더라도 문자열을 손쉽게 다루고, 재사용할 수 있다.
address = "서울특별시 강서구 방화3동 827 국립국어원"
address

# 변수명을 정할 때 사용하지 말아야하는 예약어 목록
from keyword import kwlist

print(kwlist)


### 인덱싱
'''
인덱싱은 인덱스 순서대로 값을 가져오는데 
파이썬은 인덱스 순서가 0부터 시작해서 마지막 인덱스를 가져올 때는 -1로 가져온다. 

뒤에서부터 인덱싱을 할때는 마이너스 값을 사용할 수 있는데 
위에서 지정한 변수(adress)에 담긴 문자열에서 값을 가져온다.
'''
address[0]
address[1]
address[-1]
address[-2]


### 슬라이싱
# 슬라이싱(Slicing)으로는 특정 위치의 문자, 범위를 지정해 출력할 수 있다.
address[:]
address[:5]
address[6:9]
address[::2]
address[::-1]


### 문자열의 길이, 단어 수
# len(변수 이름)방식으로 띄어쓰기를 포함하여 몇 음절로 되어 있는지 셀 수 있다.
len('국립 국어원')


# 중복된 단어를 제외하고 단어의 빈도수 계산(유일값 계산)
len(set("서울 강서구 서울 국립국어원".split()))

# 중복된 단어를 포함하는 단어의 빈도수
len("서울 강서구 서울 국립국어원".split())


### 문자열 함수
use_python = " 인생은 짧아요. Python을 쓰세요! "

# 소문자로 변환
use_python.lower()

# 대문자로 변환
use_python.upper()

# 앞뒤 공백을 제거
use_python.strip()

'''
strip() 함수는 
문자열의 가장 앞쪽과 뒤쪽에 있는 공백을 제거해주기 때문에 
원래 문자열과 똑같아 보이지만 len()으로 확인해 보면 문자열의 길이는 2개가 줄어든다.
'''
len(use_python)
len(use_python.strip())


### 추가, 분리, 정렬
# 추가
address_words = ['서울특별시', '강서구', '방화동', '국립국어원'] 
address_words.append('1층')
address_words 


# 분리
address = "서울특별시 강서구 방화동 국립국어원"
words = address.split()
words


# 순방향 정렬
address_words = ['서울특별시', '강서구', '방화동', '국립국어원'] 
address_words.sort()
address_words


# 역방향 정렬
address_words = ['서울특별시', '강서구', '방화동', '국립국어원'] 
address_words.reverse()
address_words


# 슬라이싱 [::-1]을 사용한 역방향 정렬
address_words[::-1]

" ".join(address_words)

# join()을 사용해 문자열 형태로 변경
"-".join(address_words)


### 반복

# range()의 괄호 안에 반복할 횟수를 설정
for i in range(3):
    # print()의 괄호 안에 입력한 단어를 출력하도록 설정
    print("사랑해")


# 다음은 i가 1부터 시작해 10이 될 때까지 3씩 증가하는 것을 반복하는 for 반복문
for i in range(1,10, 3):
    print(i)


### 함수
# 반복되는 내용은 함수로 작성하면 편리

# 함수를 정의한다.
def text_preprocessing(txt):
    """
    문자열에 포함된 영문자를 소문자로 만들고
    문자열 양끝 공백을 제거하며
    구두점(.)을 제거하는 사용자 정의 함수
    """
    txt = txt.lower()
    txt = txt.strip()
    txt = txt.replace(".", "")
    return txt

# 함수를 호출한다.
txt = " Python 문자열 전처리 함수를 만들면 전처리 함수를 호출해서 여러 텍스트에 적용할 수 있습니다. "
text_preprocessing(txt)


### 문자열 내장 함수 목록
print(dir(address))

for func in dir(address):
    if not func.startswith("__"):
        print(func, end = ", ")




