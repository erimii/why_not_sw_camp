'''

### 음주 빈도가 삶의 만족도와 건강 상태에 미치는 영향을 분석 ###
 
가족 만족도 → Family_sat
1년간 평균 음주량 → avg_drink
전반적 만족도 → life_sat

가족생활에 대한 만족도	
1. 매우불만족
2. 불만족
3. 약간 불만족                     
4. 보통
5.약간 만족
6. 만족                           
7. 매우 만족
0. 비해당

전반적 만족도	
1.매우불만족                            
2.대체로 만족                  
3.그저그렇다                                                         
4.대체로 만족                           
5.매우만족    

1년간 평균 음주량	
1. 월 1회 이하             
2. 월 2~4회                      
3. 주 2~3회
4. 주 4회이상              
5. 전혀 마시지 않는다
-> 주 1회 이하 / 주 2~3회 / 주 4회 이상

### 음주 빈도와 삶의 만족도의 관계

### 음주 빈도와 가족생활 만족도의 관계

### 가족생활 만족도와 삶의 만족도의 관계**

'''

# 1. import 하기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. data 불러오기
raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')

# 복사본
welfare = raw_welfare.copy()

welfare = welfare.rename(columns = {'p1403_12' : 'life_sat',
                                    'p1405_aq1' : 'family_sat',
                                    'p1405_2' : 'avg_drink'})



# 데이터 확인

welfare['avg_drink'].dtypes
welfare['avg_drink'].isna().sum() # 2546
welfare['avg_drink'].value_counts()

welfare['life_sat'].dtypes
welfare['life_sat'].isna().sum() # 3063
welfare['life_sat'].value_counts()

welfare['family_sat'].dtypes
welfare['family_sat'].isna().sum() # 2546
welfare['family_sat'].value_counts()






### 음주 빈도와 삶의 만족도의 관계
# 음주 빈도별 삶의 만족도 평균을 막대그래프로 표현



# 음주 빈도 변수
welfare['avg_drink'] = np.where(welfare['avg_drink'] == 3, '주 2~3회',
                                np.where(welfare['avg_drink'] == 4, '주 4회 이상', '주 1회 이하'))


avg_life_sat_by_drink = welfare.dropna(subset=['life_sat', 'avg_drink']) \
                        .groupby(['avg_drink', 'life_sat'], as_index = False).agg(life_sat_count = ('life_sat', 'count'))



avg_life_sat_by_drink

# 데이터 피벗: family_sat별 음주 빈도 그룹 내 비율 구하기
df_pivot = avg_life_sat_by_drink.pivot(index='avg_drink', columns='life_sat', values='life_sat_count')
df_pivot = df_pivot.div(df_pivot.sum(axis=1), axis=0)  # 각 행(음주 빈도)별 비율 변환

# 그래프 그리기
# 맑은 고딕 폰트 설정
plt.rcParams.update({'font.family' : 'Malgun Gothic'})
fig, ax = plt.subplots(figsize=(10,7))
df_pivot.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax)

plt.xticks(rotation=0)
plt.xlabel('음주 빈도')
plt.ylabel('삶 만족도 비율')
plt.title('음주 빈도별 삶 만족도 분포')
plt.legend(title="삶 만족도", loc='upper right')

# 막대 위에 퍼센트 표시
for i, bar_group in enumerate(ax.containers):  # 각 그룹(막대) 순회
    for bar in bar_group:
        height = bar.get_height()  # 각 섹션 높이 (비율)
        if height > 0:  # 높이가 0보다 클 때만 표시
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                    f'{height*100:.1f}%', ha='center', va='center', fontsize=10, color='black')

plt.show()







### 음주 빈도와 가족생활 만족도의 관계

family_sat_by_drink = welfare.dropna(subset=['family_sat', 'avg_drink']) \
                         .query("family_sat in [1,2,3,4,5,6,7]").groupby(['avg_drink', 'family_sat'], as_index=False) \
                         .agg(family_sat_count = ('family_sat', 'count'))

family_sat_by_drink


# 데이터 피벗: family_sat별 음주 빈도 그룹 내 비율 구하기
df_pivot = family_sat_by_drink.pivot(index='avg_drink', columns='family_sat', values='family_sat_count')
df_pivot = df_pivot.div(df_pivot.sum(axis=1), axis=0)  # 각 행(음주 빈도)별 비율 변환

# 그래프 그리기
# 맑은 고딕 폰트 설정
plt.rcParams.update({'font.family' : 'Malgun Gothic'})
fig, ax = plt.subplots(figsize=(10,7))
df_pivot.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax)

plt.xlabel('음주 빈도')
plt.xticks(rotation=0)
plt.ylabel('가족생활 만족도 비율')
plt.title('음주 빈도별 가족생활 만족도 분포')
plt.legend(title="가족생활 만족도", loc='upper right')

# 막대 위에 퍼센트 표시
for i, bar_group in enumerate(ax.containers):  # 각 그룹(막대) 순회
    for bar in bar_group:
        height = bar.get_height()  # 각 섹션 높이 (비율)
        if height > 0:  # 높이가 0보다 클 때만 표시
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                    f'{height*100:.1f}%', ha='center', va='center', fontsize=10, color='black')

plt.show()







### 가족생활 만족도와 삶의 만족도의 관계**
# 가족생활 만족도에 따른 삶의 만족도 평균 값 비교 

avg_life_sat_by_family_sat = welfare.dropna(subset=['family_sat', 'life_sat']) \
                                .query("family_sat in [1,2,3,4,5,6,7]").groupby('family_sat', as_index=False)['life_sat'].mean()

# 맑은 고딕 폰트 설정
plt.rcParams.update({'font.family' : 'Malgun Gothic'})
plt.figure(figsize=(8,5))
sns.barplot(data=avg_life_sat_by_family_sat, x='family_sat', y='life_sat', palette='coolwarm')

plt.xlabel('가족생활 만족도')
plt.ylabel('평균 삶의 만족도')
plt.title('가족생활 만족도별 평균 삶의 만족도')

plt.show()



