# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:19:33 2025

@author: Admin
"""
'''
항공사 운항 실태 조사
24년 1월~8월 국내 노선 여객 이용률 데이터 활용

주제
문제 인식
아이디어 도출
데이터 분석
기대 효과 및 활용 방안
'''

import pandas as pd
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    
# 데이터 불러오기
flights = []
for i in range(1, 9):
    df = pd.read_csv(f'data/2024년 {i}월 국내노선 여객 이용률.csv')  # 파일 읽기
    df['월'] = i
    flights.append(df)

# 하나의 데이터프레임으로 합치기
flight_data = pd.concat(flights, ignore_index=True)

flight_data['항공사'].value_counts()

airline_dict = {
    "KAL": "대한항공",
    "AAR": "아시아나",
    "JJA": "제주항공",
    "JNA": "진에어",
    "ABL": "에어부산",
    "ASV": "에어서울",
    "TWB": "티웨이항공",
    "EOK": "에어로케이",
    "ESR": "이스타항공"
}

# 항공사 코드 변환
flight_data['항공사'] = flight_data['항공사'].replace(airline_dict)
flight_data['항공사'].value_counts()

flight_data=flight_data.dropna()
flight_data['노선'] = flight_data['노선'].str.strip()
flight_data.loc[(flight_data["노선"] == "김포-제주") & (flight_data["항공사"] == "이스타항공"), "좌석수"] = 89091

# --------------------------------------------------------------------------------------------
# 전처리된 데이터 mysql에 저장
host = 'localhost'
user = 'root'
password = 'rubi'
db='test'
charset='utf8'

engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
conn = engine.connect()

flight_data.to_sql(name='flight', con=engine, if_exists='replace', index=False)

conn.close()

# --------------------------------------------------------------------------------------------
# 노선별 이용률 평균 분석: 전체 노선의 평균 이용률을 계산하여 수요가 높은 노선과 낮은 노선 구분
overall_avg = flight_data['이용률'].mean()
print("전체 노선 평균 이용률:", overall_avg)

route_mean = flight_data.groupby('노선')['이용률'].mean().reset_index()
route_mean.columns = ['노선', '평균이용률']

top10 = route_mean.sort_values(by='평균이용률', ascending=False).head(10)
bottom10 = route_mean.sort_values(by='평균이용률', ascending=True).head(10)

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  # Y축 공유

# 수요가 높은 노선 (TOP 10)
sns.barplot(x='노선', y='평균이용률', data=top10, palette='Blues_r', ax=ax1)
ax1.set_title('수요가 높은 노선 TOP 10', fontsize=14)
ax1.set_xlabel('노선', fontsize=12)
ax1.set_ylabel('평균 이용률 (%)', fontsize=12)
ax1.tick_params(axis='x', rotation=45)  # X축 라벨 회전
ax1.axhline(y=overall_avg, color='red', linestyle='--', label=f'전체 평균 ({overall_avg:.2f}%)')
ax1.legend()

# 수요가 낮은 노선 (BOTTOM 10)
sns.barplot(x='노선', y='평균이용률', data=bottom10, palette='Reds_r', ax=ax2)
ax2.set_title('수요가 낮은 노선 BOTTOM 10', fontsize=14)
ax2.set_xlabel('노선', fontsize=12)
ax2.tick_params(axis='x', rotation=45)
ax2.axhline(y=overall_avg, color='red', linestyle='--', label=f'전체 평균 ({overall_avg:.2f}%)')
ax2.legend()

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------
# 수요가 높은 상위 10개 노선에서의 항공사별 이용률 비교를 통해 경쟁력 평가
# (노선, 항공사) 별 평균 이용률
airline_mean = flight_data.groupby(['노선', '항공사'])['이용률'].mean().reset_index()

# 수요가 높은 상위 10개 노선 추출
filtered_data1 = airline_mean[airline_mean['노선'].isin(top10['노선'])]

# 시각화
plt.figure(figsize=(16, 5))
ax=sns.barplot(x='노선', y='이용률', hue='항공사', data=filtered_data1, palette='Paired', order=top10['노선'])

plt.title('항공사별 노선 이용률 비교 (수요 상위 10개 노선)', fontsize=16)
plt.xlabel('노선', fontsize=12)
plt.ylabel('평균 이용률 (%)', fontsize=12)
plt.legend(title='항공사')
plt.ylim(70, 100)  # y축 범위를 60~100%로 제한
legend = plt.legend(title='항공사' , prop={'size': 8}, ncol=5)
legend.get_frame().set_alpha(0.3)

# x축 눈금 위치 가져오기
xticks_positions = [tick.get_position()[0] for tick in ax.get_xticklabels()]

# 막대 사이 위치에 세로선 추가
for x in range(len(xticks_positions) - 1):
    mid_point = (xticks_positions[x] + xticks_positions[x + 1]) / 2
    plt.axvline(mid_point, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)

plt.show()

# --------------------------------------------------------------------------------------------
# 항공사별 월별 평균 이용률과 그에 따른 좌석수 시각화
# 항공사별 월별 평균 이용률
airline_monthly_usage = flight_data.groupby(['항공사', '월'])['이용률'].mean().reset_index()

# 항공사별 월별 총 좌석 수
airline_monthly_seats = flight_data.groupby(['항공사', '월'])['좌석수'].sum().reset_index()

# 그래프 그리기
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# 월별 이용률 (항공사별)
sns.lineplot(data=airline_monthly_usage, x='월', y='이용률', hue='항공사', marker='o', ax=axes[0])
axes[0].set_title('항공사별 월별 평균 이용률')
axes[0].set_ylabel('평균 이용률 (%)')
axes[0].legend(title='항공사', bbox_to_anchor=(1.005, 1), loc='upper left')
axes[0].grid(True, linestyle='--', alpha=0.5)

# 월별 좌석 수 (항공사별)
sns.lineplot(data=airline_monthly_seats, x='월', y='좌석수', hue='항공사', marker='o', ax=axes[1])
axes[1].set_title('항공사별 월별 좌석 수')
axes[1].set_ylabel('좌석 수')
axes[1].set_xlabel('월')
axes[1].ticklabel_format(style='plain', axis='y')
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].legend().remove()

plt.tight_layout()
plt.show()
