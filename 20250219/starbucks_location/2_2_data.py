# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:22:02 2025

@author: tuesv
"""

import pandas as pd

# 시군구 목록 데이터 불러오기
seoul_sgg = pd.read_excel('starbucks_location/files/seoul_sgg_list.xlsx')

# 시군구별 인구 통계 데이터 불러오기
seoul_pop = pd.read_excel('starbucks_location/files/sgg_pop.xlsx')

# 군구별 사업체 수 통계 데이터
seoul_biz = pd.read_excel('starbucks_location/files/sgg_biz.xlsx')

# 스타벅스 매장 목록 데이터 불러오기
seoul_starbucks = pd.read_excel('starbucks_location/files/seoul_starbucks_list.xlsx')

# 시군구별 스타벅스 매장 수 세기: '시군구명', '매장명' count로
starbucks_sgg_count = seoul_starbucks.pivot_table(index = '시군구명',
                                                   values='매장명',
                                                   aggfunc='count').rename(columns={'매장명':'스타벅스_매장수'})

# 서울시 시군구 목록 데이터(seoul_sgg)에 스벅 매장수 데이터를 병합
seoul_sgg = seoul_sgg.merge(starbucks_sgg_count, how = 'left', on = '시군구명')

# 서울시 시군구 목록 데이터에 서울시 시군구별 인구 통계 데이터(seoul_pop) 병합
seoul_sgg = seoul_sgg.merge(seoul_pop, how = 'left', on = '시군구명')
# 서울시 시군구 목록 데이터에 서울시 시군구별 사업체 수 통계 데이터(seoul_biz) 변합
seoul_sgg = seoul_sgg.merge(seoul_biz, how = 'left', on = '시군구명')
# 병합 결과를 엑셀 파일로 저장
seoul_sgg.to_excel('starbucks_location/files/seoul_sgg_stat2.xlsx', index = False)










































