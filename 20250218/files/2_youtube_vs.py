# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:00:37 2025

@author: Admin

youtube_rank.xlsx 파일 이용한 시각화
"""

import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
import platform

# 운영체제에 맞게 폰트 설정
if platform.system() == 'Darwin':  # Mac
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    
df = pd.read_excel('./files/youtube_rank.xlsx')
df.head()
'''
         title     category subscriber       view   video
0    BLACKPINK   [음악/댄스/가수]      9590만  378억7825만    604개
1    김프로KIMPRO  [BJ/인물/연예인]      8690만  547억3689만  2,979개
2    BANGTANTV   [음악/댄스/가수]      7980만  244억0527만  2,699개
3  HYBE LABELS   [음악/댄스/가수]      7650만  380억8129만  2,294개
4   Mark Rober        [미분류]      6430만  102억4266만    196개
'''

# 카테고리 별 구독자 수를 이용해 파이차트 만들기
df['replaced_subscriber'] = df['subscriber'].str.replace('만', '0000').astype('int')
df.info()

# 구독자 수, 채널 수 피봇 테이블 생성
pivot_df = df.pivot_table(index = 'category',
                          values = 'replaced_subscriber',
                          aggfunc = ['sum', 'count'])
pivot_df.head()
'''
                            sum               count
                  replaced_subscriber      replaced_subscriber
category                                           
[BJ/인물/연예인]           238590000                  57
[IT/기술/컴퓨터]            11070000                   6
[TV/방송]               285970000                 108
[게임]                   76830000                  45
[교육/강의]                31090000                  18
'''

pivot_df.columns = ['subscriber_sum', 'category_count']
pivot_df = pivot_df.reset_index()
pivot_df = pivot_df.sort_values(by = 'subscriber_sum', ascending=False )
pivot_df.head()
'''
    index     category  subscriber_sum  category_count
12     12   [음악/댄스/가수]       888860000             139
7       7        [미분류]       782960000             240
16     16     [키즈/어린이]       464780000             131
2       2      [TV/방송]       285970000             108
0       0  [BJ/인물/연예인]       238590000              57
'''

# 카테고리별 구독자 수 파이차트
plt.figure(figsize=(30,10))

plt.pie(pivot_df['subscriber_sum'],
        labels=pivot_df['category'],
        autopct='%1.1f%%')
plt.title('카테고리별 구독자 수', fontsize=11)
plt.show()



# 카테고리별 채널 수 파이차트
pivot_df = pivot_df.sort_values(by = 'category_count', ascending=False )
plt.figure(figsize=(30,10))

plt.pie(pivot_df['category_count'],
        labels=pivot_df['category'],
        autopct='%1.1f%%')
plt.title('카테고리별 채널 수', fontsize=11)
plt.show()





























