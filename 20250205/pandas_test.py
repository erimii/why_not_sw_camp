# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:02:14 2025

@author: Admin
"""

'''
pandas의 특징
1. 빠르고 효율적으로 표현, 실세계 데이터를 분석하는데 가장 최적화돼있음
2. 다양한 형태의 데이터 표현 가능, 서로 다른 형태의 데이터를 표현
    시계열, 레이블을 가진 데이터, 다양한 관측 데이터
3. Series: 1차원 / DataFrame : 행령(2차원)
4. 결측(null) 데이터 처리
    데이터 추가/삭제
    데이터 정렬, 조작 용이
'''

'''
Pandas로 할 수 있는 일
1. 리스트, 딕셔너리, Numpy 배열 등을 DaataFrame으로 변환 가능
2. CSV/XLS 파일등을 열어 작업 가능
3. URL을 통해 웹 사이트의 csv, json과 같은 원격 데이터
    데이터베이스 등의 데이터를 다룰 수 있음
4. 데이터 보기 / 검사 기능을 제공
    mean(): 특정 열의 평균
    corr(): 상관관계
    count(): 열 데이터 갯수 파악 가능
5. 필터 / 정렬 / 그룹화
    sort_values(): 정렬
    groupby(): 기준에 따라 몇 개의 그룹화도 가능
6. 데이터 정제 - 데이터 누락, 특정 값을 다른 값으로 일괄 변경 가능
'''

# Pandas 모듈 import
from pandas import Series, DataFrame

# Series 사용 방법
kakao = Series([92600, 92400, 92100, 94300, 92300])

'''
Series 객체 생성시, 별도의 idx를 부여하지 않으면 기본적으로 0부터 시작함
'''

# Series의 인덱스로 사용할 Series 객체 생성
idx=['2025-02-19','2025-02-18','2025-02-17','2025-02-16','2025-02-15']


# Series의 데이터로 사용할 리스트 생성
data = [92600, 92400, 92100, 94300, 92300]

sample = Series(data, index=idx)

print(sample)
print(sample['2025-02-19'])


# Series 끼리의 연산
mine = Series([10,20,30], index =['naver', 'kt', 'sk'])
friend = Series([10,30,20], index=['kt', 'naver', 'sk'])
merge = mine + friend
print(merge)


'''
DataFrame 생성 방법 : 주로 딕셔너리 사용
딕셔너리를 통해 각 컬럼에 대한 데이터르 저장한 후
DataFrame의 생성자에게 전달
'''

# DataFrame 객체 생성을 위한 딕셔너리 생성
raw_data = {'col0':[1,2,3,4],
            'col1':[10,20,30,40],
            'col2':[100,200,300,400]}
dataframe_data = DataFrame(raw_data)
print(dataframe_data)

'''
딕셔너리를 이용하여 데이터프레임 객체를 생성하면
딕셔너리의 key가
데이터프레임의 컬럼명으로 자동 인덱싱 되고,
딕셔너리의 value에 해당하는 row에는
리스트처럼 0부터 시작하는 정수로 index가 인덱싱된다
'''

print(dataframe_data['col1'])
print(dataframe_data[['col1']])

# DataFrame의 데이터 추출 방법1: 컬럼명을 이용
print(dataframe_data['col1'])


# DataFrame의 컬럼명을 별로도 설정: columns=리스트
daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

daeshin_day = DataFrame(daeshin)

# 컬럼명 순서 변경
daeshin1_day = DataFrame(daeshin, 
                        columns=['open', 'low', 'close', 'high'])

# index로 사용될 리스트 생성
date = ['25.11.11', '25.11.12', '25.11.13', 
        '25.11.14', '25.11.15']

# 컬럼명 순서 변경
daeshin_day3 = DataFrame(daeshin, 
                        columns=['open', 'low', 'close', 'high'], 
                        index=date)


# DataFrame의 데이터 추출: 컬럼명 또는 index 이용
print(daeshin_day3['open'])

print(daeshin_day3['25.11.11': '25.11.13'])



'''
숫자 관련 Numpy 모듈의 기능 사용하는 방법
'''
import pandas as pd
import numpy as np

# 숫자가 아닌 데이터(NaN : Not a Numnber) 삽입
# Numpy의 nan을 이용
lst = [1,3,5,np.nan, 6,8]
s = pd.Series(lst)

# pandas의 date_range('시작날짜', periods=갯수)
dates = pd.date_range('20211208', periods=6)

# Numpy를 이용하여 행열형태의 난수 생성 방법
np.random.randn(6,4)

df = pd.DataFrame(np.random.randn(6,4),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])

                  
#샘플링 확인
df.head()
df.tail

df.index
df.columns
df.values

df.info()

df.describe()

# 정렬
df.sort_values(by='B', ascending = True)

# 컬럼명과 index명으로 데이터 추출
df.loc['2021-12-12':'2021-12-14', ['A','B']]

# 컬럼의 값을 비교하여 추출
df[df.A>0]

# DataFrame을 복사
df2 = df.copy()

# 기존 DataFrame에 새로운 컬럼과 데이터 추가
df2['E'] = ['one', 'two', 'three', 'four', 'one', 'two']


# 특정 컬럼에 지정한 데이터가 포함되어있는지 확인
df2['E'].isin(['two', 'three']) # True / False

# 특정 컬럼에 지정한 데이터가 포함되어있는 데이터만 추출
df2[df2['E'].isin(['two', 'three'])]




df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                   index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                    'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'],
                    'D': ['D4', 'D5', 'D6', 'D7']},
                   index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                    'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'],
                    'D': ['D8', 'D9', 'D10', 'D11']},
                   index=[8, 9, 10, 11])


# dataframe들을 순서대로 연결하여 새로운 dataframe으로 생성
result = pd.concat([df1, df2, df3])


# dataframe 연결 시 레벨에 해당하는 키를 부여할 경우
result = pd.concat([df1, df2, df3],
                   keys=['x', 'y', 'z'])


df4 = pd.DataFrame({'B': ['B2', 'B3', 'B6', 'B7'],
                    'D': ['D2', 'D3', 'D6', 'D7'],
                    'F': ['F2', 'F3', 'F6', 'F7']},
                   index=[2,3,6,7])


result = pd.concat([df1,df4]) # 행기준

result = pd.concat([df1, df4], axis =1) # 열기준

# 공통 부분만 연결
result = pd.concat([df1, df4], join = 'inner') # 열기준


# dataframe연결 시 기존 인덱스 무시하고 다시 0으로 재설정할 경우
result = pd.concat([df1,df4], ignore_index=True)





# DataFrame 병합
left = pd.DataFrame({'key': ['K0', 'K4', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})

pd.merge(left, right, on = 'key')
'''
  key   A   B   C   D
0  K0  A0  B0  C0  D0
1  K2  A2  B2  C2  D2
2  K3  A3  B3  C3  D3
'''
pd.merge(left, right, on = 'key', how='left')

pd.merge(left, right, on = 'key', how='right')

pd.merge(left, right, on = 'key', how='outer')

pd.merge(left, right, on = 'key', how='inner')





# 외부 파일을 DataFrame 형태로 불러오기

df = pd.read_csv('./data/csv/weather.csv', encoding='euc-kr')

'''
pandas의 read_csv() 함수는 인덱스 지정없이 파일을 읽는 경우
파일의 첫번째 행을 각 시리즈의 열이름으로 자동 설정하고
각 레코드에 대한 인덱스를 0부터 자동 생성함
'''

# 특정 열을 인덱스로 설정하여 읽기

df = pd.read_csv('./data/csv/weather.csv', 
                 encoding='euc-kr',
                 index_col=0)

df.head()

df_my_index = pd.read_csv('./data/csv/countries.csv',
                          index_col=0)

# 열기준 데이터 선택
print(df_my_index['population'])
print(df_my_index[['population', 'area']])



# 슬라이싱 이용하여 행 선택 가능
df_my_index[:3]


# 특정요소 하나만 선택할 경우
df_my_index.loc['US', 'capital']


# 특정 열에 대한 행을 선택할 경우
df_my_index['population'][:3]

# 데이터프레임의 기존 열들에 대한 연산 결과를 새로운 열로 추가할 경우
df_my_index['density'] = df_my_index['population'] / df_my_index['area']


# 특정 컬럼에 대한 통계 가능
pandas_std = df['평균기온(°C)'].std()

numpy_std = np.std(df['평균기온(°C)'])






































