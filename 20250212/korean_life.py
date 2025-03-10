# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:05:39 2025

@author: Admin
"""

'''
한국인의 삶을 파악하라!
한국복지패널데이터로 데이터 분석하기
'''
# 1. import 하기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. data 불러오기
raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')
# 컬럼명에 대한 쿡북을 봐야됨.

# 복사본
welfare = raw_welfare.copy()

# 3. 데이터 검토
# head, tail
welfare.head()
welfare.tail()

# row, cols 개수 확인
welfare.shape # (14418, 830)

# 변수 속성 확인
welfare.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 14418 entries, 0 to 14417
Columns: 830 entries, h14_id to h14_pers_income5
dtypes: float64(826), object(4)
memory usage: 91.3+ MB
'''

# 요약 통게량
welfare.describe()
'''
             h14_id       h14_ind  ...  h14_pers_income4  h14_pers_income5
count  14418.000000  14418.000000  ...      14418.000000        715.000000
mean    4672.108406      3.121723  ...          2.038702       1183.292308
std     2792.998128      3.297963  ...         32.965477       2147.418274
min        2.000000      1.000000  ...          0.000000     -10600.000000
25%     2356.000000      1.000000  ...          0.000000        206.000000
50%     4535.000000      1.000000  ...          0.000000        530.000000
75%     6616.000000      7.000000  ...          0.000000       1295.000000
max     9800.000000     14.000000  ...       3000.000000      22644.000000
'''

# 성별, 태어난 연도, 혼인 상태, 종교, 월급, 직업코드, 지역 코드
# 4. 변수명 변경
welfare = welfare.rename(columns = {'h14_g3' : 'sex',
                                    'h14_g4' : 'birth',
                                    'h14_g10' : 'marriage_type',
                                    'h14_g11' : 'religion',
                                    'p1402_8aq1' : 'income',
                                    'h14_eco9' : 'code_job',
                                    'h14_reg7' : 'code_region'})

'''
데이터 분석 절차
1. 변수(컬럼) 검토 및 전처리
    변수의 특징 파악 -> 이상치, 결측치 정제 => 분석의 용이성
    전처리: 북석할 변수를 각각 진행
2. 변수간의 관계 분석
    2-1. 요약 테이블
    2-2. 시각화
'''

'''
주제: 한국인의 삶의 질
하위목표 1. 성별에 따른 월급 차이
'''
### 성별 변수 검토 및 전처리
# 1. 변수 검토: 타입 파악, 범주마다 몇 명?
welfare['sex'].dtypes # dtype('float64')

# 항목별 개수 -> 이상치 확인 가능
welfare['sex'].value_counts()
'''
sex
2.0    7913
1.0    6505
Name: count, dtype: int64
'''
## 만약 이상치가 발견되었을 경우
# np.where() 로 결측 처리
# isna().sum() 로 결측 확인
# dropna() 로 결측치 제거

# 성별 항목에 이름 부여
welfare['sex'] = np.where(welfare['sex'] ==1, 'male', 'female')
welfare['sex'].value_counts()
'''
sex
female    7913
male      6505
Name: count, dtype: int64
'''

# 빈도 막대 그래프
sns.countplot(data = welfare, x = 'sex')
plt.show()


### 월급 변수 검토 및 전처리
welfare['income'].dtypes # dtype('float64')

# 히스토그램
sns.histplot(data = welfare, x = 'income')
plt.show()

# 이상치 확인 
welfare['income'].describe()
'''
count    4534.000000
mean      268.455007
std       198.021206
min         0.000000
25%       150.000000
50%       220.000000
75%       345.750000
max      1892.000000
Name: income, dtype: float64
'''

# 결측치 확인
welfare['income'].isna().sum() # 9884

### 성별에 따른 월급 차이 분석
# 성별 월급 평균표
# income 결측치 제거
# sex별 그룹
# income 평균 구하기

sex_income = welfare.dropna(subset = 'income').groupby('sex', as_index = False).agg(mean_income = ('income', 'mean'))
'''
      sex  mean_income
0  female   186.293096
1    male   349.037571
'''

sns.barplot(data = sex_income, x = 'sex', y='mean_income')
plt.show()


'''
나이와 월급의 관계 
'''
welfare['birth'].dtypes # dtype('float64')
welfare['birth'].describe()
'''
count    14418.000000
mean      1969.280205
std         24.402250
min       1907.000000
25%       1948.000000
50%       1968.000000
75%       1990.000000
max       2018.000000
Name: birth, dtype: float64
'''

sns.histplot(data = welfare, x = 'birth')
plt.show()

welfare['birth'].isna().sum() # 0

# 파생변수 만들기 -나이
#welfare['age'] = 2019 - welfare['birth'] + 1
welfare = welfare.assign(age = 2019-welfare['birth'] + 1)
welfare['age'].describe()
'''
count    14418.000000
mean        50.719795
std         24.402250
min          2.000000
25%         30.000000
50%         52.000000
75%         72.000000
max        113.000000
Name: age, dtype: float64
'''

sns.histplot(data = welfare, x = 'age')
plt.show()

## 나이별 월급 평균표
# income 결측치 제거
# age별 그룹화
# income 평균 구하기
age_income = welfare.dropna(subset='income').groupby('age').agg(mean_income = ('income', 'mean'))
'''
      mean_income
age              
19.0   162.000000
20.0   121.333333
21.0   136.400000
22.0   123.666667
23.0   179.676471
          ...
88.0    27.000000
89.0    27.000000
90.0    27.000000
91.0    20.000000
92.0    27.000000
'''

# 선그래프
sns.lineplot(data = age_income, x = 'age', y='mean_income')
plt.show()


'''
연령대에 따른 월급 차이
초년(30세 미만) / 중년 / 노년(59세 이상)
'''

# 연령대 변수 만들기
welfare = welfare.assign(ageg = np.where(welfare['age']<30, 'young', 
                                         np.where(welfare['age']<=59, 'middle', 'old')))

welfare['ageg'].value_counts()
'''
ageg
old       5955
middle    4963
young     3500
Name: count, dtype: int64
'''

sns.countplot(data = welfare, x = 'ageg')
plt.show()


# 연령대별 월급 평균표
# income 결측치 제거
# ageg별 분리
# income 평균 구하기
ageg_income = welfare.dropna(subset='income').groupby('ageg', as_index = False).agg(mean_income = ('income', 'mean'))

sns.barplot(data=ageg_income, x = 'ageg', y = 'mean_income',
            order = ['young', 'middle', 'old'])
plt.show()


'''
연령대 및 성별 월급 차이
'''
# 연령대 및 성별 평균표
# income 결측치 제거
# ageg별 분리, sex별 분리
# income 평균 구하기
ageg_sex =  welfare.dropna(subset='income').groupby(['ageg','sex'], as_index = False).agg(mean_income =('income', 'mean'))
'''
     ageg     sex  mean_income
0  middle  female   230.481735
1  middle    male   409.541228
2     old  female    90.228896
3     old    male   204.570231
4   young  female   189.822222
5   young    male   204.909548
'''

sns.barplot(data=ageg_sex, x = 'ageg', y='mean_income',
            hue = 'sex',
            order = ['young', 'middle', 'old'])

plt.show()

'''
나이 및 성별 월급 차이
'''
# 나이 및 성별 월급 평균표
# income 결측치 제거
# ageg 및 sex별 분리
# income 평균 구하기
age_sex =  welfare.dropna(subset='income').groupby(['age','sex'], as_index = False).agg(mean_income =('income', 'mean'))

sns.lineplot(data = age_sex, x = 'age', y='mean_income',
             hue = 'sex')
plt.show()


'''
직업별 월급 차이
'''
welfare['code_job'].dtypes # dtype('float64')
welfare['code_job'].describe()
welfare['code_job'].value_counts()
'''
code_job
611.0    962
941.0    391
521.0    354
312.0    275
873.0    236

112.0      2
784.0      2
423.0      1
861.0      1
872.0      1
Name: count, Length: 150, dtype: int64
'''

# 전처리하기
list_job = pd.read_excel('./data/Koweps_Codebook_2019.xlsx',
                         sheet_name = '직종코드')

list_job.head()
'''
   code_job                     job
0       111  의회 의원∙고위 공무원 및 공공단체 임원
1       112                기업 고위 임원
2       121          행정 및 경영 지원 관리자
3       122         마케팅 및 광고∙홍보 관리자
4       131       연구∙교육 및 법률 관련 관리자
'''

list_job.shape # (156, 2)

# welfare list_job 결합
welfare = welfare.merge(list_job, how = 'left', on = 'code_job')

welfare.dropna(subset = 'code_job')[['code_job', 'job']].head()
'''
    code_job               job
2      762.0               전기공
3      855.0       금속기계 부품 조립원
7      941.0       청소원 및 환경미화원
8      999.0  기타 서비스 관련 단순 종사자
14     312.0         경영 관련 사무원
'''

# 직업별 월급에 평균표
# job, income 결측치 제거
# job별 그룹
# income 평균 구하기
job_income = welfare.dropna(subset=['job', 'income']).groupby('job', as_index = False).agg(mean_income = ('income', 'mean'))
job_income.head()
'''
                job  mean_income
0       가사 및 육아 도우미    92.455882
1               간호사   265.219178
2  감정∙기술영업및중개관련종사자    391.000000
3      건물 관리원 및 검표원   168.375000
4    건설 및 광업 단순 종사자   261.975000
'''

# 월급이 많은 직업 상위 10개
top10 = job_income.sort_values('mean_income', ascending=False)
plt.rcParams.update({'font.family': 'Malgun Gothic'})
sns.barplot(data = top10[:10], x ='mean_income', y='job' )
plt.show()


'''
성별 직업 빈도
'''
## 남성 직업 빈도 상위 10개 추출
# job 결측치 제거
# male 추출 .query()
# job별 그룹
# job 빈도 구하기
# 내림차순 후 상위 10행 추출


job_male = welfare.dropna(subset = 'job').query('sex == "male"').groupby('job', as_index = False).agg(n = ('job', 'count')).sort_values('n', ascending = False).head(10)
job_male
'''
                job    n
107       작물 재배 종사자  486
104         자동차 운전원  230
11        경영 관련 사무원  216
46        매장 판매 종사자  142
89           영업 종사자  113
127     청소원 및 환경미화원  109
4    건설 및 광업 단순 종사자   96
120    제조 관련 단순 종사자   80
3      건물 관리원 및 검표원   79
141          행정 사무원   74
'''
job_female = welfare.dropna(subset = 'job').query('sex == "female"').groupby('job', as_index = False).agg(n = ('job', 'count')).sort_values('n', ascending = False).head(10)
job_female
'''
                  job    n
83          작물 재배 종사자  476
91        청소원 및 환경미화원  282
33          매장 판매 종사자  212
106       회계 및 경리 사무원  163
31    돌봄 및 보건 서비스 종사자  155
87       제조 관련 단순 종사자  148
73       음식 관련 단순 종사자  126
58        식음료 서비스 종사자  117
88                조리사  114
24   기타 서비스 관련 단순 종사자   97
'''



'''
종교 유무에 따른 이혼율 구하기
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. data 불러오기
raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')
# 컬럼명에 대한 쿡북을 봐야됨.

# 복사본
welfare = raw_welfare.copy()

welfare = welfare.rename(columns = {'h14_g3' : 'sex',
                                    'h14_g4' : 'birth',
                                    'h14_g10' : 'marriage_type',
                                    'h14_g11' : 'religion',
                                    'p1402_8aq1' : 'income',
                                    'h14_eco9' : 'code_job',
                                    'h14_reg7' : 'code_region'})



# religion
welfare['religion'].dtypes #  dtype('float64')
welfare['religion'].value_counts()
'''
religion
2.0    7815
1.0    6603
1.있음                2.없음
'''
welfare['religion'].isna().sum()
# 0 -> 결측치 없음

welfare['religion'] = np.where(welfare['religion'] ==1, 'Y', 'N')
welfare['religion'].value_counts()


# marriage_type
welfare['marriage_type'].dtypes #  dtype('float64')
welfare['marriage_type'].value_counts()
'''
marriage_type
1.0    7190
5.0    2357
0.0    2121
2.0    1954
3.0     689
4.0      78
6.0      29
Name: count, dtype: int64

"0.비해당(18세 미만)
1.유배우         2.사별         3.이혼          4.별거          
5.미혼(18세이상, 미혼모 포함)   6.기타(사망 등)"

'''
welfare['marriage_type'].isna().sum()
# 0 -> 결측치 없음

dm={0:'비해당(18세 미만)',
   1:'유배우',
   2:'사별',
   3:'이혼',
   4:'별거',
   5:'미혼(18세이상, 미혼모 포함)',
   6:'기타(사망 등)'}

welfare['marriage_type'] = welfare['marriage_type'].replace(dm)
welfare['marriage_type'].value_counts()

### 종교 유무에 따른 이혼율 분석
#  종교 유무에 따른 이혼율표
# religion별 그룹
# 이혼율 구하기
religion_marriage = welfare.query("marriage_type in ['유배우', '이혼']").groupby(['religion', 'marriage_type'], as_index=False).agg(n = ('marriage_type','count'))

'''
  religion marriage_type     n
0        N           유배우  3660
1        N            이혼   384
2        Y           유배우  3530
3        Y            이혼   305
'''
religion_marriage['total'] = religion_marriage.groupby('religion')['n'].transform('sum')
religion_marriage['ratio'] = religion_marriage['n'] / religion_marriage['total']
religion_marriage

# 그래프 그리기
plt.figure(figsize=(8, 5))
ax=sns.barplot(data = religion_marriage, x = 'religion', y='ratio',
             hue = 'marriage_type')

plt.ylabel("이혼율 (%)")
plt.xlabel("종교 유무")
plt.title("종교 유무에 따른 이혼율 비교")
plt.ylim(0, 1)

for container in ax.containers:
    ax.bar_label(container, fmt="%.3f%%", fontsize=10)

plt.show()





'''
지역별 연령대 비율
code_region
'''
welfare['code_region'].dtypes # dtype('float64')
welfare['code_region'].value_counts()
welfare['code_region'].isna().sum()

dr={1:'서울',
   2:'수도권(인천/경기)',
   3:'부산/경남/울산',
   4:'대구/경북',
   5:'대전/충남',
   6:'강원/충북',
   7:'광주/전남/전북/제주도'}

welfare['code_region'] = welfare['code_region'].replace(dr)
welfare['code_region'].value_counts()
'''
code_region
수도권(인천/경기)      3246
광주/전남/전북/제주도    2466
부산/경남/울산        2448
서울              2002
대구/경북           1728
대전/충남           1391
강원/충북           1137
Name: count, dtype: int64
'''

# 연령대 변수 만들기
welfare = welfare.assign(age = 2019-welfare['birth'] + 1)
welfare['age'].describe()
welfare = welfare.assign(ageg = np.where(welfare['age']<30, 'young', 
                                         np.where(welfare['age']<=59, 'middle', 'old')))

welfare['ageg'].value_counts()

### 지역별 연령대 비율 분석
#  지역별 연령대 비율표
# region 별, ageg 별 그룹
# 카운트?

region_ageg = welfare.groupby(['code_region', 'ageg'], as_index = False).agg(n = ('ageg', 'count'))
region_ageg.head()
'''
    code_region    ageg     n  total     ratio
0         강원/충북  middle   351   1137  0.308707
1         강원/충북     old   522   1137  0.459103
2         강원/충북   young   264   1137  0.232190
3  광주/전남/전북/제주도  middle   784   2466  0.317924
4  광주/전남/전북/제주도     old  1108   2466  0.449311
'''

# 비율 계산
region_ageg['total'] = region_ageg.groupby('code_region')['n'].transform('sum')
region_ageg['ratio'] = region_ageg['n'] / region_ageg['total']

# 그래프 그리기
plt.figure(figsize=(8, 5))
ax=sns.barplot(data = region_ageg, x = 'code_region', y='ratio',
             hue = 'ageg')
plt.xticks(rotation=25)
plt.ylabel("연령대 비율 (%)")
plt.xlabel("지역")
plt.title("지역에 따른 연령대 비율 비교")
plt.ylim(0, 0.6)

for container in ax.containers:
    ax.bar_label(container, fmt="%.3f%%", fontsize=7)

plt.show()




'''
지역별 연령대 비율
'''
# 지역 변수 검토 및 전처리
welfare['code_region'].dtypes

# 지역 변수 추가


## 지역 연령대 비율
# 지역별 연령대 비율표
# region별 분리
# ageg 추출
# 비율 구하기
region_ageg2 = welfare.groupby('code_region', as_index = False)['ageg'].value_counts(normalize=True)
region_ageg2 = region_ageg2.assign(proportion = region_ageg2['proportion']*100).round(1)
'''
     code_region    ageg  proportion
0          강원/충북     old        45.9
1          강원/충북  middle        30.9
2          강원/충북   young        23.2
3   광주/전남/전북/제주도     old        44.9
4   광주/전남/전북/제주도  middle        31.8
'''

sns.barplot(data=region_ageg2,
            y='code_region', x='proportion',
            hue='ageg')

plt.show()



# 시각화(막대, 누적)

'''
     code_region    ageg  proportion
0          강원/충북     old        45.9
1          강원/충북  middle        30.9
2          강원/충북   young        23.2
3   광주/전남/전북/제주도     old        44.9
4   광주/전남/전북/제주도  middle        31.8

피벗을 이용해 이 구조를 바꿀거임.
피벗: 행과 열을 회전하여 표의 구성을 변경하는 작업.
      누적 그래프 형태로 시각화 할 때 사용
1. 지역, 연령대, 비율 추출
    region_ageg2에 [['code_region', 'ageg','proportion']] 추출
2. DataFrame.pivot()
2-1. 지역을 기준으로 : index = 지역
2-2. 연령대별로 컬럼을 구성: columns = 연령대
2-3. 각 항목의 값을 비율로 채우기: values = 비율

'''

pivot_df = region_ageg2[['code_region', 'ageg', 'proportion']].pivot(index='code_region', columns='ageg', values = 'proportion')

# 초년 중년 노년 으로 순서 바꾸기
reorder_df = pivot_df.sort_values('old')[['young', 'middle', 'old']]

'''
ageg          young  middle   old
code_region                      
수도권(인천/경기)     28.7    38.8  32.5
서울             23.9    38.5  37.6
대전/충남          25.0    33.6  41.3
부산/경남/울산       22.9    33.4  43.8
광주/전남/전북/제주도   23.3    31.8  44.9
강원/충북          23.2    30.9  45.9
대구/경북          20.0    29.6  50.4
'''

reorder_df.plot.barh(stacked = True)
plt.show()


# 초년 중년 노년 으로 순서 바꾸기
reorder_df = pivot_df.sort_values('old')[['young', 'middle', 'old']]






















