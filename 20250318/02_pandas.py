# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:38:57 2025

@author: Admin
"""
### 판다스 기초
# pandas를 pd라는 별칭(alias)으로 불러 온다
import pandas as pd


# 데이터를 pd 데이터 프레임 안에 ()로 감싸서 변수 df에 할당한다.
df = pd.DataFrame(
        {"a" : [4 ,5, 6],
        "b" : [7, 8, 9],
        "c" : [10, 11, 12]},
        index = [1, 2, 3])    
df
# 위의 결과처럼 판다스는 행과 열로 구성된 표 형태의 데이터를 처리할 수 있다는 장점이 있다.

df["a"]


#대소문자 구분에 주의해야 한다.아래와 같이 입력하면 KeyError 가 발생한다.
#df[["A"]]


# a행과 b행의 데이터 보기 
df[["a", "b"]]


#특정 인덱스의 열만 보기
df.loc[3]


import numpy as np
df = pd.DataFrame(
    {"a" : [4 ,5, 6],
     "b" : [7, 8, 9],
     "c" : [10, 11, 12]},
    index = [1, 2, 3])  
index = pd.MultiIndex.from_tuples(
    [('d',1),('d',2),('e',2)],
    names=['n','v'])
df


#판다스 데이터 프레임 : 비교연산자로 색인하기
import numpy as np
df = pd.DataFrame(
        {"a" : [4 ,5, 6, 6, np.nan],
        "b" : [7, 8, np.nan, 9, 9],
        "c" : [10, 11, 12, np.nan, 12]},
        index = pd.MultiIndex.from_tuples(
        [('d',1),('d',2),('e',2),('e',3),('e',4)],
        names=['n','v']))
df

df[df.a < 6]

#특정값 5가 들어있는 행과 열 찾기
df.a.isin([5])
# a열 2행에 찾고자 하는 값‘5’가 있음을 확인할 수 있다.


### 중복 데이터 제거
# keep = 'first', 'last', False 등과 같은 매개변수를 사용해서 중복을 제거할 수 있다.
df = df.drop_duplicates(subset="a", keep='last')
df
# 중복이 있었던 6,9,12는 keep='last'를 사용했으므로 앞에 값이 남고 뒤에 중복되는 값은 삭제된 것을 알 수 있다.


### head()와 tail()로 데이터 미리보기
# df.head(n): 처음의 일부 데이터를 확인
# df.tail(n): 끝의 일부 데이터를 확인
# n에는 보고자 하는 행만큼의 숫자를 넣어주면 된다. 아무 숫자도 입력하지 않으면 기본값인 5행이 출력된다.

df.head(2)
df.tail(2)


### str 접근자로 문자열 다루기
'''
판다스의 시리즈 형태의 데이터를 문자열로 다루게 되면 
파이썬 문자열 함수와 비슷하게 문자열을 처리할 수 있다. 

다음과 같은 문서가 판다스의 시리즈 형태로 있다고 할 때 
대소문자 변경, 공백제거, 어절 나누기, 특정문자 찾기, 바꾸기 등의 
문자열 전처리에 필요한 몇 가지 기능을 알아본다.
'''

# 실습을 위한 예시 문장  
document = ["코로나 상생지원금 문의입니다.",
            " 지하철 운행시간 문의입니다.",
            "버스 운행시간 문의입니다. ",
            "사회적 거리두기로 인한 영업시간 안내입니다.",
            "Bus 운행시간 문의입니다.",
            " Taxi 승강장 문의입니다."]

df_doc = pd.DataFrame(document, columns=["문서"])
df_doc


# astype()을 사용해서 df_doc의 각 행에 들어있는 데이터의 타입을 바꿀 수 있다.
df_doc["문서"].astype("string")


### 대소문자 변경
# 대문자로 변경하기
df_doc["문서"].str.upper()

# 소문자로 변경하기
df_doc["문서"].str.lower()


### 양끝 공백 제거
# 양끝 공백 제거
df_doc["문서"].str.strip()


### 어절 나누기
# 띄어쓰기를 기준으로 어절 나누기
df_doc["문서"].str.split()

# 어절을 나누고 데이터프레임으로 반환받기
df_doc["문서"].str.split(expand=True)


### 특정 문자 찾기
# str.contains("찾고자 하는 문자")를 입력하면 문자가 있는 열은 True, 없는 열은 False를 반환한다.

# 특정 문자가 들어가는 텍스트 찾기
df_doc["문서"].str.contains("버스")


# 특정 문자가 들어가는 텍스트를 찾아 다시 데이터프레임으로 감싸주면 해당 데이터만 가져오게 된다.
df_doc[df_doc["문서"].str.contains("버스")]


### 문자열 바꾸기

# replace 를 통해 특정 문자열을 변경할 수 있다.
df_doc["문서"].str.replace("운행", "영업")

# replace 를 사용해서 문자열을 변경할 때 정규표현식을 함께 사용할 수 있다.
df_doc["문서"].str.replace("버스|지하철", "대중교통", regex=True)


'''
str 을 제외하고 replace()를 사용해서 문자열의 일부만 변경하고자 할때는 
regex=True 를 함께 사용해야 한다.

replace() 는 전체 일치하는 값이 있을 때 값이 변경되며 

데이터프레임에서 사용할 때는 
딕셔너리 형태로 변경하고자 하는 컬럼과 값을 지정해서 사용할 수 있다.
'''
df_doc.replace("지하철", "교통", regex=True)
df_doc.replace({"문의":"질문"}, regex=True)
df_doc["문서"].str.split("문의")





























