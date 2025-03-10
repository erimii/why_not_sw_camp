# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 09:04:38 2025

@author: Admin
"""

'''
넷플릭스 데이터 분석 프로젝트

사용 라이브러리
- 넘파이: 수치해석
- 판다스: 데이터 분석, 전처리하기 위해 사용
- 맷프롯립 / 시본: 데이터 시각화
- 워드클라우드: 텍스트 강조

데이터 분석 목표
- 데이터를 빠르게 파악하고
- 전처리를 수행 한 후
- 여러 인사이트 도출

데이터 전처리
- 데이터 결측치 처리
- 피처 엔지니어링 -> 파생 변수 생성

데이터 시각화: 요청 기업의 브랜드 색상을 사용
- 브랜드 색상: 데이터 시각화 하기 전에 색상을 미리 정해주는 것이 중요
               색상을 데이터의 성격에 맞게 선택
               중요도에 따라 강조 방법 계획-> 시각화 효과 극대화
               
- 파이차트: 데이터의 카테고리별 비율 시각화에 효과적
            비율을 쉽게 비교할 수 있고,
            각 카테고리의 상대적 중요성 파악 가능
            ->넷플릭스에서 영화와 TV쇼의 비율을 시각화
            
- 막대 그래프: 데이터의 항목 간의 비교를 명확하게 시각화 하는데 유용
                각 장르의 빈도를 막대그래프로 시각화
                -> 넷플릭스에서 어떤 장르가 가장 많이 등장하는지
                
- 히트맵: 데이터의 밀도나 강도를 색상으로 시각화하여
          복잡한 데이터셋에서 패턴, 트랜드 파악 용이
          나이 그룹별로 국가별 콘텐츠 비율 시각화
          -> 각 국가가 어떤 나이 그룹을 타겟으로 하는 콘텐츠가 많은지 분석
          -> 각 콘텐츠를 통해 국가별 시청층을 이해
          -> 각 국가에 대한 시텅 트랜드, 콘텐츠 기획에 대한 인사이트 도출
         
- 워드크라우드: 텍스트 데이터에서 빈도가 높은 단어를 시각적으로 강조
                데이터의 주요 주제, 키워드를 한눈에 파악
                -> 넷플릭스 콘텐츠 설명에서 자주 등장하는 단어들을 시각화
                -> 어떤 주제나 키워드가 자주나오는지 파악
                -> 콘텐츠의 주요 테마 파악
                -> 이를 통해 마케팅, 콘텐츠 기획, 전략, 사용자 분석 등 유용한 인사이트 파악

'''

'''
1. 넷플릭스 데이터 파악
'''

''' 1-1 데이터 분석 라이브러리 '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

''' 1-2. csv 로드 '''
netflix = pd.read_csv('./data/netflix_titles.csv')
netflix.head(3)


''' 1-3. 데이터 내용 확인 : 컬럼 확인 '''
netflix.columns
'''
Index(['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
       'release_year', 'rating', 'duration', 'listed_in', 'description'],
      dtype='object')
'''

''' 1-4 열에 대한 요약 정보 확인 '''
netflix.info()
'''
RangeIndex: 8807 entries, 0 to 8806 -> 총 8807개
Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   show_id       8807 non-null   object
 1   type          8807 non-null   object
 2   title         8807 non-null   object
 3   director      6173 non-null   object -> 결측치가 있음
 4   cast          7982 non-null   object -> 결측치가 있음
 5   country       7976 non-null   object -> 결측치가 있음
 6   date_added    8797 non-null   object -> 결측치가 있음
 7   release_year  8807 non-null   int64 
 8   rating        8803 non-null   object -> 결측치가 있음
 9   duration      8804 non-null   object -> 결측치가 있음
 10  listed_in     8807 non-null   object
 11  description   8807 non-null   object
dtypes: int64(1), object(11)
'''

'''
2. 넷플릭스 데이터셋 결측치 처리
'''

'''
넷플릭스 결칙치 비율 확인하고 처리
일반적으로 결측치 비율이 
- 5% 미만일 경우: 삭제
    -> 데이터 손실 최소화, 분석의 신뢰성에는 영향 x
- 5%~20%: 대체 방향 모색. 평균 / 중간값 / 최빈값
- 20% 이상: 열전체 삭제
    -> 변수에 대한 중요성, 분석 목적, 데이터의 양을 종합적으로 고려
    -> 데이터 손실 커지기 때문에 신중한 판단 필요
    -> 특히, 데이터셋이 작거나, 해당 변수가 중요한 역할을 할 경우
    -> 모델 기반 대체나, 예측 모델을 통해 결측치를 보완
    
결측치 개수 : isna().sum()
결측치 비율: isna().sum() / len() * 100
'''
for i in netflix.columns:
    missingValueRate = netflix[i].isna().sum() / len(netflix) * 100
    
    if missingValueRate > 0 :
        print(f'{i} null rate: {round(missingValueRate,2)}')

'''
director null rate: 29.91   <- 제거(컬럼) : 대체
cast null rate: 9.37        <- 대체
country null rate: 9.44     <- 대체
date_added null rate: 0.11  <- 제거(해당 행)
rating null rate: 0.05      <- 제거(해당 행)
duration null rate: 0.03    <- 제거(해당 행)

'''
''' 2-1 country 결측치(9.44%) 대체 '''
netflix['country'] = netflix['country'].fillna('No Data')

''' 2-2. director/cast 대체 '''
netflix['director'] = netflix['director'].replace(np.nan, 'No Data')
netflix['cast'] = netflix['cast'].replace(np.nan, 'No Data')

''' 2-3. 결측지를 가진 행 제거 '''
netflix = netflix.dropna(subset = ['date_added', 'rating', 'duration'])
netflix.info()

''' 2-4. 결측치 갯수로 재확인 '''
netflix.isna().sum()

'''
3. 넷플릭스 피처 엔지니어링

피처 엔지니어링: 데이터프레임의 기존 변수를 조합하거나, 새로운 변수를 만드는 것을 의미

데이터분석/머신러닝 모델을 학습시킬 때 매우 중요
현업: 예측 모델이 데이터의 패턴을 잘 이해하고 학습할 수 있는 기준

피처 엔지니어링을 명확하고 의미있는 피러를 만들어 사용하면,
모델의 결과를 쉽게 해석할 수 있다
'''

''' 3-2. 넷플릭스 시청 등급 변수 '''
'''
넷플릭스 데이터 프레임에서 rating 변수를 이용하여 age_grop(시청등급)
ALL(모든) / Older Kids(어린이) / Teens(청소년초반) / Young Adults(청소년후반) / Aaults(성인)
'''
netflix['age_group'] = netflix['rating']

age_group_dic = {'G': 'ALL',                # 전체
                 'TV-G': 'ALL',
                 'TV-Y': 'ALL',
                 'PG': 'Older Kids',        # 7세 이상
                 'TV-Y7': 'Older Kids',
                 'TV-Y7-FV': 'Older Kids',
                 'TV-PG': 'Older Kids',
                 'PG-13': 'Teens',          # 13세 이상
                 'TV-14': 'Young Adults',   # 16세 이상
                 'NC-17': 'Adults',         # 18세 이상
                 'NR': 'Adults',            # 등급 보류
                 'UR': 'Adults',            # 무삭제 등급
                 'R': 'Adults',
                 'TV-MA': 'Adults'
                 }

# map()을 이용하여 age_group에 저장
netflix['age_group'] = netflix['age_group'].map(age_group_dic)

''' 3-2. 전처리가 완료된 데이터를 csv 파일로 저장 '''
netflix.to_csv('./result/netflix_prepro.csv', index =False)

'''
4. 넷플릭스 시각화하기
전처리된 넷플릭스 파일 읽기
시각화 라이브러리 
'''

'''4-1. 시각화 라이브러리 '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''4-2. 전처리된 데이터 읽기 '''
netflix = pd.read_csv('./result/netflix_prepro.csv')

'''4-3. 넷플릭스 브랜드 색상 시각화 '''
sns.palplot(['#221f1f','#b20710','#e50914','#f5f5f1'])
plt.title('Netflic brand palette',
          loc='left', # 정렬 기준
          fontfamily='serif',
          fontsize=15,
          y=1.2 # 제목의 y축 위치값
          )
plt.show()

''' 4-4. 넷플릭스 파이 차트: Movies & TV shows'''
type_counts = netflix['type'].value_counts()
'''
type
Movie      6126
TV Show    2664
'''

plt.figure(figsize=(5,5))
plt.pie(type_counts,
        labels= type_counts.index,
        autopct='%0.f%%',
        startangle=100,
        explode=[0.05, 0.05],
        shadow=True,
        colors=['#b20710','#221f1f'])

plt.suptitle('netflix', fontfamily='serif', fontsize=15)
plt.title('Movies & TV shows', fontfamily='serif', fontsize=11)
plt.show()

'''4-5. 넷플릭스 막대 그래프 - 어떤 장르가 인기가 많은지 '''
netflix['listed_in']
'''
0                                           Documentaries
1         International TV Shows, TV Dramas, TV Mysteries
2       Crime TV Shows, International TV Shows, TV Act...
3                                  Docuseries, Reality TV
4       International TV Shows, Romantic TV Shows, TV ...
                       
8785                       Cult Movies, Dramas, Thrillers
8786               Kids' TV, Korean TV Shows, TV Comedies
8787                              Comedies, Horror Movies
8788                   Children & Family Movies, Comedies
8789       Dramas, International Movies, Music & Musicals
Name: listed_in, Length: 8790, dtype: object
'''
genres = netflix['listed_in'].str.split(', ', expand=True) \
                            .stack().value_counts()
# expand =True: split에 대해서 분할된 결과를 확장하여 여러 열로 변환
# 분할된 문자가 개별적인 열로 배치되어 데이터프레임을 생성
genres.head()
'''
International Movies      2752
Dramas                    2426
Comedies                  1674
International TV Shows    1349
Documentaries              869
'''


plt.figure(figsize=(10,7))
sns.barplot(x= genres.values,
            y= genres.index,
            hue=genres.index,
            palette='RdGy'
            )

plt.suptitle('netflix', fontfamily='serif', fontsize=15)
plt.title('popular genres', fontfamily='serif', fontsize=11)
plt.xlabel('count',fontsize=14)
plt.ylabel('genre', fontsize=14)
plt.grid(axis='x')
plt.show()

''' 4-3. 넷플릭스 히트맵 '''
'''
넷플릭스 데이터넷을 이용하여 각 나라의 콘텐츠 수를 집계.
각 나라에서 어느 나이 그룹이 어떤 콘텐츠를 소비하는지 분석.
특정 나이층의 시청 선호도를 파악하여 마케팅 전력을 세우고자..
특정 나라에서 특정 나이 그룹을 위한 콘텐츠가 부족하다면
해당 연령층을 겨냥한 새로운 콘텐츠를 개발
country / age_group / 
genres
'''

# 1. 넷플릭스 데이터의 title => 'Sankofa'인 행의 데이터 확인
netflix[netflix['title'].str.contains('Sankofa', na=False, case=False)]

# 2. 'country' 열의 값을 , 기준으로 구분
# 출력할 최대 행 수를 None으로 출력해서 모두 출력
pd.set_option('display.max_rows', None)
# pd.set_option: 출력 옵션을 설정하는 함수. 
# 'display.max_rows', None: 전체 행을 생략없이 출력 가능

# 쉼표로 country 열의 값을 파이썬 리스트로
netflix['country'] = netflix['country'].str.split(', ')

# 파이썬 리스트로바꾼 것을 explode함수를 적용하여 개별 행으로 분리
netflix_age_country = netflix.explode('country')

# 확인
netflix_age_country[netflix_age_country['title'].str.contains('Sankofa', na=False, case=False)]

# 5. 각 나이 그룹에 따른 국가별 넷플릭스 콘텐츠 수?
netflix_age_country_unstack = netflix_age_country.groupby('age_group')['country'] \
                        .value_counts().unstack()
# unstack(): 그룹화된 데이터를 풀어서 다시 데이터프레임으로 변환

# 6. 특정 나이 그룹에 따른 특정 나라별 콘텐츠로 필터링
# 6-1. 연령
age_order = ['ALL', 'Older Kids', 'Teens', 'Adults']
# 6-2
country_order = ['United States', 'India', 'United Kingdom', 'Canada',
                 'Japan', 'France', 'South Korea', 'Spain', 'Mexico', 'Turkey']

# 6-3 필터링
# 행: age_order / 열: country_order
netflix_age_country_unstack = netflix_age_country_unstack.loc[age_order, country_order]


# 6-4 결측치 처리 0
netflix_age_country_unstack=netflix_age_country_unstack.fillna(0)
'''
country     United States  India  United Kingdom  ...  Spain  Mexico  Turkey
age_group                                         ...                       
ALL                 255.0   16.0            63.0  ...    9.0     3.0     1.0
Older Kids          694.0  169.0           145.0  ...   15.0    20.0     9.0
Teens               433.0   11.0            84.0  ...    5.0     4.0     0.0
Adults             1803.0  278.0           408.0  ...  185.0   120.0    71.0
'''

# 6-5 나이 그룹에 따른 국가별 콘텐츠 비율
# 각 열의 값을 각 열의 합으로 나누기: div(어떤 값을, 무엇으로) 나눔
# axis = 1
netflix_age_country_unstack = netflix_age_country_unstack.div(netflix_age_country_unstack.sum(axis=0), axis =1)


plt.figure(figsize =(15,5))

cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('', ['#221f1f','#b20710','#f5f5f1'])

sns.heatmap(netflix_age_country_unstack,
            cmap = cmap,
            linewidths=2.5,
            annot=True, # 각 셀에 데이터 값 표시
            fmt = '.0%'
            )
plt.suptitle('netflix', fontfamily='serif', fontsize=15)
plt.title('Percentage of content by country by age group', fontfamily='serif', fontsize=11)
plt.show()


'''
7. 넷플릭스 워드 클라우드
pip install wordcloud
'''

from wordcloud import WordCloud
from PIL import Image

plt.figure(figsize=(15,5))

# netflix['description']을 list로 변환시킨 후 str로 변환
text = str(list(netflix['description']))

# logo image 갖고오고 Image.open()
# image를 넘파이 배열로 변환해줘야됨 np.array()
mask = np.array(Image.open('C:/work_python0203~/20250214/data/netflix_logo.jpg'))
# mask = : 단어를 그릴 위치 설정, 흰색 항목은 마스킹 된 것으로 간주

# 색상맵
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('', ['#221f1f','#b20710'])

# 워드클라우드 생성
wordcloud = WordCloud(background_color='white',
                      width = 1400, height = 1400,
                      max_words = 170,
                      mask = mask,
                      colormap=cmap).generate(text)

plt.suptitle('Movies and TV shows',
             fontweight='bold', fontfamily='serif', fontsize=15)

# 워드클라우드 결과를 plots 창에 나타내기
plt.imshow(wordcloud)
plt.axis('off') # 축 감추기
plt.show()





















