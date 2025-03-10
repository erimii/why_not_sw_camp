# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:02:41 2025

@author: Admin
"""

import matplotlib.pyplot as plt

### 직선 또는 꺾은선 형태의 그래프: plot()

plt.plot([10,20,30,40]) # 데이터 하나만 넣으면 y축 데이터로 인식
plt.show()

plt.plot([1,2,3,4], [12,43,25,15]) # x축데이터, y축 데이터로 인식
plt.show()
plt.title('plotting')

# 두 그래프, 색상, 범례: legned()-> 반드시 label값 필요, 
plt.title('legend & color')
plt.plot([10,20,30,40], color = 'skyblue', label = 'skyblue')
plt.plot([40,30,20,10], color = 'pink', label = 'pink')
plt.legend()
plt.show()

# 선 형태: ls = '' / linestyle = , lw= 선 두께
plt.title('linestyle')
plt.plot([10,20,30,40], color = 'r', linestyle= '--', label = 'dashed')
plt.plot([40,30,20,10], color = 'g', linestyle= ':', label = 'dotted')
plt.legend()
plt.show()

# 선 대신 모양으로
plt.plot([10,20,30,40], 'r.', label = 'circle')
plt.plot([40,30,20,10], 'g^', label = 'triangle up')
plt.legend()
plt.show()

# 그래프 기본 구조 생성 : matplotlib.pyplot.figure()
plt.figure()
# 그래프 기본 구조에 그래프 그려주기: matplotlib.pyplot.plot(시각화 데이터)
# 그래프 출력 : matplotlib.pyplot.show()
plt.show()



# Numpy 이용하여 Dummy 데이터 생성 후 sin()을 이용하여 시각화
import numpy as np

# Numpy의 범위: Numpy.arange(시작, 끝, 사이간격)
t = np.arange(0,10,0.01)
y = np.sin(t)

plt.figure(figsize = (10,6)) # 10:6 비율로 준비
plt.plot(t, y, label='sin')
plt.plot(t, np.cos(t), lw=3, label='cos')

plt.grid()
plt.legend()
plt.xlabel('time')
plt.ylabel('Amplitude')
plt.title('sample sin graph')
plt.xlim(0, np.pi) # x tick 값 변경, 보여지는 x축 변경되는 것
plt.ylim(-1.2, 1.2) # y tick 값 변경
plt.show()

# 다양한 모양
t = np.arange(0, 5, 0.5)
plt.figure(figsize=(10,6))
plt.plot(t, t, 'r--')
plt.plot(t, t**2, 'bs')
plt.plot(t, t**3, 'g^')
plt.show()

# 색상, 선스타일 변경 두 번째 방법
t = [0,1,2,3,4,5,6]
y = [1,4,5,8,9,5,3]

plt.figure(figsize=(10,6))
plt.plot(t,y,color='green', 
         linestyle= 'dashed',
         marker='o',
         markerfacecolor='blue',
         markersize=20)
plt.show()


### 산점도 그래프 plt.scatter()
t = np.array([0,1,2,3,4,5,6,7,8,9])
y = np.array([9,8,7,9,8,3,2,4,3,4])
colormap=t # 데이터에 따른 마커 색 변경
plt.figure(figsize=(10,6))
plt.scatter(t,y, marker='>', s = 50, c=colormap)
plt.colorbar() # 그래프 오른쪽에 칼라바 표시
plt.show()

