# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 08:59:03 2025

@author: Admin
"""

### 병원 노쇼 환자 데이터 분석 ###
'''
문제 정의  
A 병원에서는 예약한 환자들이 오지 않아  
진료가 원활히 이루어지지 않는 일이 종종 발생.  

문제를 해결하기 위해  
예약하고 오지 않는 환자들의 특징을 파악하고,  
'No Show' 발생률을 줄일 수 있는 아이디어를 제시!!!  

작업 내용  
1. 데이터 처리 과정이 필요한 이유 및 과정  
2. 결측치를 확인 후 삭제 혹은 처리 및 보완  
3. 통계치를 이용하여 이상치 제거 (이상치 처리)  
4. 데이터 타입을 맞춰서 변환 후 저장  
5. 데이터를 다양한 방식으로 분석 및 가공  
6. 각 변수들 간의 관계 파악  
7. 종속 변수와 독립 변수 추출  
8. 분석에 이용할 변수 선택  
9. 노쇼의 특성 파악  
10. No-show와 연결할 변수의 특성 파악  
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/medical.csv')
df.head(3)
'''
      PatientId  AppointmentID Gender  ...    Neighbourhood SMS_received  No-show
0  2.990000e+13        5642903      F  ...  JARDIM DA PENHA            0       No
1  5.590000e+14        5642503      M  ...  JARDIM DA PENHA            0       No
2  4.260000e+12        5642549      F  ...    MATA DA PRAIA            0       No
'''
df.isnull().sum()
df.info()
'''
 #   Column          Non-Null Count   Dtype  
---  ------          --------------   -----  
 0   PatientId       110527 non-null  float64
 1   AppointmentID   110527 non-null  int64  
 2   Gender          110527 non-null  object 
 3   ScheduledDay    110527 non-null  object 병원 예약을 한 날
 4   AppointmentDay  110527 non-null  object 실제 병원에 방문하는 날
 5   Age             110527 non-null  int64  나이
 6   Neighbourhood   110527 non-null  object 병원 위치
 7   SMS_received    110527 non-null  int64  메시지 수락 여부
 8   No-show         110527 non-null  object 노쇼 여부
 '''

df.describe()
# Age에 이상치 제거
df = df[df.Age>=0]
df = df[df.Age<=110]

# No-show 데이터 타입 변경
df['No-show'] = df['No-show'].map({'Yes': 1, 'No':0})

# datetime으로 타입 변경
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['ScheduledDay'] = pd.to_datetime((df['ScheduledDay']))

# 대기기간 변수 추가 후 이상치 제거
df['waiting_day'] = df['AppointmentDay'].dt.dayofyear - df['ScheduledDay'].dt.dayofyear
df = df[df.waiting_day >= 0]


# 목적(노쇼 줄이기)에 적합한 변수 추출
# 당일 예약(waiting_day==0) 노쇼 비율 구하기
a= df[df.waiting_day==0]['waiting_day'].value_counts()
b=df[(df['waiting_day']==0)&(df['No-show']==1)]['waiting_day'].value_counts()
b/a

# waiting_day <= 10
no_show = df[df['No-show']==1]
show = df[df['No-show']==0]

# waiting_day <= 10 중 노쇼 건수 비교
no_show[no_show['waiting_day']<=10]['waiting_day'].hist(alpha=0.7, label='no_show')
show[show['waiting_day']<=10]['waiting_day'].hist(alpha=0.3, label='show')
plt.legend()
plt.show()
'''
그래프 분석 결과 당일 예약에서는 노쇼가 거의 발생하지 않는다
'''


# 예약 잡은 날짜에 따른 노쇼 건수 비교
no_show['ScheduledDay'].hist(alpha=0.7, label='no_show')
show['ScheduledDay'].hist(alpha=0.3, label='show')
plt.legend()
plt.show()
''' 2016년 5월 초 ~ 5월 말에 예약 건수가 많고, 
2016년 4월 말 ~5월 초에 No-show가 많이 발생 '''

# 병원 방문(AppointmentDay)와 'No-show' :hist()
no_show['AppointmentDay'].hist(alpha=0.7, label='no_show')
show['AppointmentDay'].hist(alpha=0.3, label='show')
plt.legend()    
plt.show()
''' No-show 발생 건수와 방문일 간에는 특이점이 없다 '''

## 알림 메시지 허용 여부(x축)와 기다리는 기간(y축)에 따른 노쇼 발생 횟수
sns.barplot(x= 'SMS_received',
            y= 'waiting_day',
            hue= 'No-show',
            data=df
            )
plt.show()
''' 
메시지 허용하지 않은 경우 waiting_day가 5일 이상일 경우 노쇼
        허용 한 경우                 18일 이상일 경우 노쇼
'''

a = len(df[(df['SMS_received']==0)& (df['No-show']==1)])
b = len(df[(df['SMS_received']==0)& (df['No-show']==0)])
a/(a+b) # 0.1669243894635811

c = len(df[(df['SMS_received']==1)& (df['No-show']==1)])
d = len(df[(df['SMS_received']==1)& (df['No-show']==0)])
c/(c+d) # 0.2756927591850556

#상관 관계로 확인
temp = df[['SMS_received', 'No-show', 'waiting_day']].corr()
sns.heatmap(temp,annot = True)
plt.show()

# 노쇼의 특징 파악 정리
'''
1. 대기일수가 길수록 노쇼
2. 알람 미허용시 대기일수가 5일 이상이면 노쇼
'''

# 노쇼와 연결하여 변수의 특성 파악 시각화로
# 얼마나 많은 환자가 예정된 약속에 오지 않았는가?
sns.countplot(x='No-show', data = df)

# 성별에 따른 노쇼 여부 차이
sns.countplot(x='Gender', hue='No-show' ,data = df)

# 노쇼와 남여 비율
f = df[(df['Gender']=="F") & (df['No-show']==1)]['Gender'].value_counts()
m = df[(df['Gender']=="M") & (df['No-show']==1)]['Gender'].value_counts()

F = df[(df['Gender']=="F")]['Gender'].value_counts()
M = df[(df['Gender']=="M")]['Gender'].value_counts()

f/F
m/M
































