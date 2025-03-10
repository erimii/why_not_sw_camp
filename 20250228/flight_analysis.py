# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:14:32 2025

@author: Admin
"""
import pandas as pd
import numpy as np

cols_to_drop = [
    'DepTime',         # 실제 출발 시각 (예약 시각 사용)
    'ArrTime',         # 실제 도착 시각
    'CRSArrTime',      # 예약 도착 시각
    'FlightNum',       # 항공편 번호
    'CRSElapsedTime',  # 예약 운항 시간
    'AirTime',         # 실제 공중 비행 시간
    'TaxiIn',          # 착륙 후 택시 시간
    'TaxiOut',         # 이륙 전 택시 시간
    'CancellationCode',# 취소 사유 (분석 목적에 따라 생략)
    'Diverted',        # 우회 여부
    'NASDelay',        # 항공 관제 관련 지연
    'SecurityDelay'    # 보안 관련 지연
]

flights = []
for i in range(1987, 2009):
    df = pd.read_csv(f'data/{i}.csv', encoding="ISO-8859-1")  # 파일 읽기
    flights.append(df)

# 하나의 데이터프레임으로 합치기
flight_data = pd.concat(flights, ignore_index=True)

flight_data = flight_data.drop(columns=cols_to_drop)

airports_df = pd.read_csv("data/airports.csv")
carriers_df = pd.read_csv("data/carriers.csv")
plane_df = pd.read_csv("data/plane-data.csv")

# 'year' 컬럼을 'PlaneYear'로 변경
plane_df.rename(columns={'year': 'PlaneYear'}, inplace=True)

# df_reduced의 항공기 등록번호 컬럼은 'TailNum'임. plane_df의 'tailnum'과 병합
flight_data = pd.merge(flight_data, plane_df[['tailnum', 'PlaneYear']], how='left',
                      left_on='TailNum', right_on='tailnum')

# 항공편 발생 연도(Year)와 제조 연도(PlaneYear)로 항공기 연식(AircraftAge) 계산
flight_data['AircraftAge'] = flight_data['Year'] - flight_data['PlaneYear']

# 불필요한 병합 후의 'tailnum' 컬럼 제거
flight_data.drop(columns=['tailnum'], inplace=True)
print("plane-data 병합 후 flight_data 컬럼:", flight_data.columns)

# carriers 데이터와 병합하여 항공사명(Description) 추가 (carriers_df의 'Code' 기준)
flight_data = pd.merge(flight_data, carriers_df, how='left',
                      left_on='UniqueCarrier', right_on='Code')



# -----------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

flight_data = pd.read_csv("data/all_data.csv")

flight_data['Year'].value_counts()
flight_data['AircraftAge'].value_counts()
flight_data.describe()
# --------------------------------------------------------------------------------------
#출발지연을 최소화하려면 비행에 가장 적합한 시간대/요일/시간은 언제인가?

# 월 평균 출발 지연
monthly_avg_delay = flight_data.groupby("Month")["DepDelay"].mean().reset_index()

# 선 그래프 시각화
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_avg_delay, x="Month", y="DepDelay", marker="o", color="b")
plt.xlabel("Month")
plt.ylabel("Average Departure Delay (minutes)")
plt.title("Monthly Average Departure Delay (1995-2008)")
plt.xticks(range(1, 13))
plt.grid(True)
plt.show()

# 시간대 & 요일별 출발 지연 평균 계산
flight_data["Hour"] = flight_data["CRSDepTime"] // 100  # 시간(HH만 추출)
heatmap_data = flight_data.pivot_table(index="DayOfWeek", columns="Hour", values="DepDelay", aggfunc="mean")

# 9월 데이터 필터링
september_data = flight_data[flight_data["Month"] == 9]
september_data["Hour"] = september_data["CRSDepTime"] // 100  # 시간(HH만 추출)
heatmap_september = september_data.pivot_table(index="DayOfWeek", columns="Hour", values="DepDelay", aggfunc="mean")

# 9월 히트맵 시각화
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_september, cmap="coolwarm", annot=True, linewidths=0.5)
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week (1=Mon, 7=Sun)")
plt.title("Average Departure Delay in September by Time and Day of Week")
plt.show()

# 12월 데이터 필터링
december_data = flight_data[flight_data["Month"] == 12]
december_data["Hour"] = december_data["CRSDepTime"] // 100  # 시간(HH만 추출)
heatmap_december = december_data.pivot_table(index="DayOfWeek", columns="Hour", values="DepDelay", aggfunc="mean")

# 12월 히트맵 시각화
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_december, cmap="coolwarm", annot=True, linewidths=0.5)
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week (1=Mon, 7=Sun)")
plt.title("Average Departure Delay in December by Time and Day of Week")
plt.show()

# --------------------------------------------------------------------------------------
# 오래된 비행기일수록 지연이 더 잦나?
# 비행기 연식별 평균 도착 지연 시간 계산
age_arrival_delay = flight_data.groupby("AircraftAge")["ArrDelay"].mean().reset_index()

age_arrival_delay = age_arrival_delay[age_arrival_delay['AircraftAge'] >= 0]
age_arrival_delay = age_arrival_delay[age_arrival_delay['AircraftAge'] < 60]

# 그래프 설정
sns.lineplot(x="AircraftAge", y="ArrDelay", data=age_arrival_delay, marker='o', color='r')
plt.title("Average Arrival Delay by Aircraft Age")
plt.xlabel("Aircraft Age (Years)")
plt.ylabel("Average Arrival Delay (Minutes)")

plt.tight_layout()
plt.show()

flight_data[['AircraftAge', 'ArrDelay']].corr()

# --------------------------------------------------------------------------------------
# 시간이 지남에 따라 다양한 장소 간을 비행하는 사람의 수는 어떻게 변하나?
# 연도별 항공편 수 계산
yearly_flights = flight_data.groupby("Year").size().reset_index(name="FlightCount")

# 월별 항공편 수 계산
monthly_flights = flight_data.groupby(["Year", "Month"]).size().reset_index(name="FlightCount")

# 그래프 그리기
plt.figure(figsize=(12, 5))

# 연도별 항공편 수 트렌드
plt.subplot(1, 2, 1)
sns.lineplot(data=yearly_flights, x="Year", y="FlightCount", marker='o')
plt.title("Total Flights per Year")
plt.xlabel("Year")
plt.ylabel("Number of Flights")

# 월별 항공편 수 변화 트렌드
plt.subplot(1, 2, 2)
sns.lineplot(data=monthly_flights, x="Month", y="FlightCount", hue="Year", palette="coolwarm")
plt.title("Monthly Flight Trends Over the Years")
plt.xlabel("Month")
plt.ylabel("Number of Flights")

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------
#날씨는 비행기 지연을 얼마나 잘 예측할 수 있나?

flight_data["WeatherImpact_Dep"] = flight_data["WeatherDelay"] / flight_data["DepDelay"]
flight_data["WeatherImpact_Arr"] = flight_data["WeatherDelay"] / flight_data["ArrDelay"]

# 2. 상관관계 분석
correlation = flight_data[["WeatherDelay", "DepDelay", "ArrDelay"]].corr()
print("Correlation Matrix:\n", correlation)

# 3. 월별 날씨 지연 패턴 분석
monthly_weather_delay = flight_data.groupby("Month")["WeatherDelay"].mean()

# 그래프 그리기
plt.figure(figsize=(12, 5))

# 월별 날씨 지연 평균
plt.subplot(1, 2, 1)
sns.lineplot(x=monthly_weather_delay.index, y=monthly_weather_delay.values, marker='o')
plt.title("Average Weather Delay by Month")
plt.xlabel("Month")
plt.ylabel("Average Weather Delay (minutes)")

# 히트맵으로 상관관계 시각화
plt.subplot(1, 2, 2)
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation between Weather Delay & Flight Delays")

plt.tight_layout()
plt.show()




# --------------------------------------------------------------------------------------
# 한 공항의 지연으로 인해 다른 공항의 지연이 발생하는 연쇄적 실패를 감지할 수 있는지? 

import networkx as nx
# 기존 데이터에서 평균 출발 및 도착 지연 계산
delay_network = flight_data.groupby(["Origin", "Dest"])[["DepDelay", "ArrDelay"]].mean().reset_index()

# 1. 평균 지연이 30분 이상인 공항만 필터링
high_delay_routes = delay_network[(delay_network["DepDelay"] > 30) & (delay_network["ArrDelay"] > 30)]

# 2. 그래프 생성
G = nx.DiGraph()

# 3. 필터링된 데이터 기반으로 노드 및 엣지 추가
for _, row in high_delay_routes.iterrows():
    G.add_edge(row["Origin"], row["Dest"], weight=row["DepDelay"])

# 4. Degree 기준으로 필터링 (연결된 공항이 5개 이상인 경우만)
node_degree = dict(G.degree())
filtered_nodes = [node for node, degree in node_degree.items() if degree >= 5]
G_filtered = G.subgraph(filtered_nodes)

# 5. 네트워크 그래프 시각화
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_filtered, k=0.5)  # 노드 간격 조정

# 노드 크기를 연결된 개수(degree)에 따라 가변적으로 설정
node_sizes = [node_degree[node] * 200 for node in G_filtered.nodes()]

nx.draw(G_filtered, pos, with_labels=True, node_size=node_sizes, font_size=10, edge_color="red")
plt.title("Simplified Flight Delay Propagation Network")
plt.show()


# --------------------------------------------------------------------------------------

# 9/11 이전과 이후의 비행 패턴을 비교
# 연도별 비행 횟수 계산
flights_per_year = flight_data.groupby("Year").size()

# 연도별 평균 지연 시간 계산
average_delay_per_year = flight_data.groupby("Year")["ArrDelay"].mean()

# 시각화 설정
fig, ax1 = plt.subplots(figsize=(10,5))

# 첫 번째 그래프 (비행 횟수 변화)
color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Flights', color=color)
ax1.plot(flights_per_year.index, flights_per_year.values, marker='o', color=color, label='Number of Flights')
ax1.tick_params(axis='y', labelcolor=color)

# 두 번째 그래프 (평균 지연 시간 변화)
ax2 = ax1.twinx()  # Y축 공유
color = 'tab:red'
ax2.set_ylabel('Average Delay (minutes)', color=color)
ax2.plot(average_delay_per_year.index, average_delay_per_year.values, marker='s', linestyle='--', color=color, label='Avg Delay Time')
ax2.tick_params(axis='y', labelcolor=color)

# 제목 및 범례 추가
fig.suptitle('Yearly Flight Count and Average Delay Time')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 그래프 출력
plt.show()



# --------------------------------------------------------------------------------------
#가장 자주 비행하는 두 도시 간을 오가는 모든 항공편을 비교.

# 가장 자주 운항된 두 도시 찾기
# 2007년 데이터 필터링
flight_data_2007 = flight_data[flight_data["Year"] == 2007]

# 가장 자주 운항된 두 도시 찾기
route_counts = flight_data_2007.groupby(["Origin", "Dest"]).size().reset_index(name="count")
top_route = route_counts.nlargest(1, "count")

# 해당 구간의 데이터 필터링
top_origin, top_dest = top_route.iloc[0]["Origin"], top_route.iloc[0]["Dest"]
filtered_df = flight_data_2007[(flight_data_2007["Origin"] == top_origin) & (flight_data_2007["Dest"] == top_dest)]

# 이상치 제거 (지연 시간이 180분 이하인 데이터만 사용)
filtered_df = filtered_df[(filtered_df["DepDelay"].between(0, 120)) & (filtered_df["ArrDelay"].between(0, 120))]

# 시각화 - 출발 및 도착 지연 비교
plt.figure(figsize=(12, 6))
sns.histplot(filtered_df["DepDelay"], bins=30, color="blue", label="Departure Delay", kde=True)
sns.histplot(filtered_df["ArrDelay"], bins=30, color="orange", label="Arrival Delay", kde=True)
plt.legend()
plt.title(f"Flight Delay Distribution (2007): {top_origin} ↔ {top_dest}")
plt.xlabel("Delay (minutes)")
plt.ylabel("Count")
plt.show()


# --------------------------------------------------------------------------------------
# 시카고(ORD)와 같은 주요 공항을 오가는 모든 항공편을 비교
# ORD(시카고 오헤어 공항)와 가장 많이 연결된 상위 5개 경로


# ORD를 포함하는 항공편 필터링
ord_flights = flight_data[(flight_data["Origin"] == "ORD") | (flight_data["Dest"] == "ORD")]

# ORD와 가장 많이 연결된 공항 찾기
ord_routes = ord_flights.groupby(["Origin", "Dest"]).size().reset_index(name="count")
top_ord_route = ord_routes.nlargest(5, "count")  # 가장 많은 항공편이 운항된 경로 5개 선택

# 상위 5개 공항의 평균 출발 지연 & 도착 지연 비교
top_5_airports = top_ord_route[["Origin", "Dest"]].values.flatten()
filtered_top_5_df = ord_flights[(ord_flights["Origin"].isin(top_5_airports)) & 
                                (ord_flights["Dest"].isin(top_5_airports))]

delay_means = filtered_top_5_df.groupby(["Origin", "Dest"])[["DepDelay", "ArrDelay"]].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=delay_means.melt(id_vars=["Origin", "Dest"], var_name="DelayType", value_name="Minutes"),
            x="Origin", y="Minutes", hue="DelayType", palette={"DepDelay": "blue", "ArrDelay": "orange"})

plt.title("Average Departure & Arrival Delay for Top 5 Routes")
plt.xlabel("Airport")
plt.ylabel("Average Delay (minutes)")
plt.legend(title="Delay Type")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# 상위 5개 공항의 시간대별 평균 지연 비교
filtered_top_5_df["Hour"] = (filtered_top_5_df["CRSDepTime"] // 100).astype(int)  # 시간대 추출
hourly_delay_top_5 = filtered_top_5_df.groupby(["Hour", "Origin"])[["DepDelay", "ArrDelay"]].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_delay_top_5, x="Hour", y="DepDelay", hue="Origin", marker="o", palette="tab10")
plt.title("Average Departure Delay by Hour for Top 5 Airports")
plt.xlabel("Hour of the Day")
plt.ylabel("Average Departure Delay (minutes)")
plt.xticks(range(0, 24))
plt.legend(title="Airport")
plt.grid(True)
plt.show()


#----------------------------------------------------------------
# Q9. 항공사(UniqueCarrier)별 평균 출발 지연 시간(DepDelay)을 비교하여 어떤 항공사가 가장 정시 운항을 잘하는지 분석
#----------------------------------------------------------------


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 운영체제에 맞는 기본 폰트 설정
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

# 새로운 데이터프레임 생성 (원본 유지)
df_analysis = flight_data[['UniqueCarrier', 'DepDelay']].copy()

# 결측값 제거
df_analysis = df_analysis.dropna()

# 항공사별 평균 출발 지연 시간 계산
carrier_delay = df_analysis.groupby('UniqueCarrier')['DepDelay'].mean().reset_index()

# 평균 출발 지연 시간이 낮은 순으로 정렬
carrier_delay = carrier_delay.sort_values(by='DepDelay')

# 시각화 (막대 그래프)
plt.figure(figsize=(12, 6))
sns.barplot(x='UniqueCarrier', y='DepDelay', data=carrier_delay, palette='coolwarm')
plt.xlabel('항공사 코드')
plt.ylabel('평균 출발 지연 시간 (분)')
plt.title('항공사별 평균 출발 지연 시간 비교')
plt.xticks(rotation=45)
plt.show()

# 가장 정시 운항을 잘하는 항공사 출력
best_carrier = carrier_delay.iloc[0]
print(f'가장 정시 운항을 잘하는 항공사: {best_carrier["UniqueCarrier"]}, 평균 출발 지연 시간: {best_carrier["DepDelay"]:.2f}분')

# 가장 출발 지연이 심한 항공사 출력
worst_carrier = carrier_delay.iloc[-1]
print(f'가장 출발 지연이 심한 항공사: {worst_carrier["UniqueCarrier"]}, 평균 출발 지연 시간: {worst_carrier["DepDelay"]:.2f}분')
















