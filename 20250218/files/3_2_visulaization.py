# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:02:15 2025

@author: Admin
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform
import seaborn as sns

df = pd.read_excel('./files/kto_total.xlsx')

# 운영체제에 맞는 기본 폰트 설정
if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    

### 중국인 관광객 시계열 ###

# 1. 중국 국적 데이터 필터링
df_filter = df[df['국적'] == '중국']

# 2. 시계열: plot()
plt.figure(figsize=(12,4))

plt.plot(df_filter['기준년월'], df_filter['관광'])

plt.suptitle('중국인 관광객 시계열', fontsize=15)
plt.title('중국인 관광객', fontsize=11)

plt.xlabel('기준년월',fontsize=14)
plt.ylabel('관광객 수', fontsize=14)

plt.xticks(['2010-01','2011-01','2012-01','2013-01','2014-01','2015-01',
           '2016-01','2017-01','2018-01','2019-01','2020-01'])

plt.show()


### 국내 외국인 관광객 중 상위 5개 국가를 각각 시계열 ###
### (중국, 일본, 대만, 미국, 홍콩)
cntry_list = ['중국', '일본', '대만', '미국', '홍콩']


for cntry in cntry_list:
    df_filter = df[(df['국적'] == cntry)]

    # 2. 시계열: plot()
    plt.figure(figsize=(12,4))

    plt.plot(df_filter['기준년월'], df_filter['관광'])

    plt.suptitle(f'상위 5개 국가 관광객 시계열', fontsize=15)
    plt.title(f'{cntry}인 관광객 시계열', fontsize=11)

    plt.xlabel('기준년월',fontsize=14)
    plt.ylabel('관광객 수', fontsize=14)

    plt.xticks(['2010-01','2011-01','2012-01','2013-01','2014-01','2015-01',
               '2016-01','2017-01','2018-01','2019-01','2020-01'])

    plt.show()


### 히트맵 ###
'''
매트릭스 형태에 값을 컬러로 표현하는 데이터 시각화 방법
전체 데이터를 한눈에 파악 가능.
x축, y축에 어떤 변수를 사용할지 고민해야 된다.
'''
# x축:월, y축:연
# 데이터: 관광객 수

# '기준년월'을 월과 년으로 나눠줘야됨
df['년도']=df['기준년월'].str.slice(0,4)
df['월']=df['기준년월'].str.slice(5,7)

# 원하는 국적 데이터만 추출
df_filter = df[df['국적'] == '중국']

# pivot_table을 이용해 데이터를 매트릭스 형태로 변환
df_pivot = df_filter.pivot_table(index = '년도',
                                 columns = '월',
                                 values = '관광')

plt.figure(figsize=(12,4))

sns.heatmap(df_pivot,
            annot = True,
            fmt = '.0f',
            cmap = 'rocket_r')

plt.suptitle('중국인 관광객 히트맵', fontsize=15)
plt.title('년 월에 따른 관광객 수', fontsize=11)

plt.xlabel('월',fontsize=14)
plt.ylabel('년', fontsize=14)

plt.show()






















