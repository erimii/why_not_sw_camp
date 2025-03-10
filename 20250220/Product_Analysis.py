### 무선 청소기 모델별 비교 분석 ###

import pandas as pd

danawa_data = pd.read_excel('files/danawa_data_final.xlsx')

# 흡입력 기준 정렬: 평균
price_mean_value = danawa_data['가격'].mean()
sucton_mean_value = danawa_data['흡입력'].mean()
use_time_mean_value = danawa_data['사용시간'].mean()

# 가성비 좋은 제품 탐색
condition_data = danawa_data[
                            (danawa_data['가격'] <= price_mean_value) &
                            (danawa_data['흡입력'] >= sucton_mean_value) &
                            (danawa_data['사용시간'] >= use_time_mean_value)
                            ]

# 데이터 시각화
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
    

# 결측치 없애기
chart_data = danawa_data.dropna()

# 흡입력, 사용시간 최대 최소
suction_max_value = danawa_data['흡입력'].max()
sucton_mean_value = danawa_data['흡입력'].mean()
use_time_max_value = danawa_data['사용시간'].max()
use_time_mean_value = danawa_data['사용시간'].mean()

# 성능 시각화
plt.figure(figsize=(20,10))

plt.suptitle('가성비 무선 청소기 찾기', fontsize=15)
plt.title('', fontsize=11)


sns.scatterplot(x='흡입력', y = '사용시간',
                size = '가격',
                hue = chart_data['회사명'],
                data = chart_data,
                sizes = (10, 1000),
                )
# 사용 시간 평균을 선으로
plt.plot([0, suction_max_value],
         [use_time_mean_value, use_time_mean_value],
         lw = 1)

# 흡입력 평균을 선으로
plt.plot([sucton_mean_value, sucton_mean_value],
         [0, use_time_max_value],
         'r--',
         lw = 1)

plt.xlabel('흡입력',fontsize=14)
plt.ylabel('사용시간', fontsize=14)

plt.legend()

plt.show()

# 인기 제품의 데이터 시각화
chart_data_selected = chart_data[:20]

plt.figure(figsize=(20,10))

plt.title('무선 청소기 TOP 20', fontsize=11)


sns.scatterplot(x='흡입력', y = '사용시간',
                size = '가격',
                hue = chart_data_selected['회사명'],
                data = chart_data_selected,
                sizes = (100, 2000),
                )

# 사용 시간 평균을 선으로
plt.plot([60, suction_max_value],
         [use_time_mean_value, use_time_mean_value],
         lw = 1)

# 흡입력 평균을 선으로
plt.plot([sucton_mean_value, sucton_mean_value],
         [20, use_time_max_value],
         'r--',
         lw = 1)

for index, row in chart_data_selected.iterrows():
    x = row['흡입력']
    y = row['사용시간']
    s = row['제품']. split()[0]
    plt.text(x, y, s, size=20)

plt.xlabel('흡입력',fontsize=14)
plt.ylabel('사용시간', fontsize=14)

plt.legend()

plt.show()





































