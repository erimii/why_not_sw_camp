# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 08:56:03 2025

@author: Admin
"""
import pandas as pd

needed_columns = [
    "REG_YYMM", "MEGA_CTY_NM", "CTY_RGN_NM", 
    "MAIN_BUZ_DESC", "TP_BUZ_NM", "CSTMR_GUBUN", 
    "CSTMR_MEGA_CTY_NM", "CSTMR_CTY_RGN_NM", 
    "SEX_CTGO_CD", "AGE_VAL", "AMT", "CNT"
]

df = pd.read_csv('bc_card_data/201906.csv', encoding="utf-8", usecols=needed_columns, low_memory=False)

df.info()
df.isnull().sum()
df.head()

'''
1) 서울시 거주/비거주 고객의 소비 분석
- 서울시 거주/비거주 고객 수 구하기
- 총 소비액 구하기
- 성별 소비액 구하기
- 카드 이용 건수 구하기
'''

# 서울시 거주 / 비거주 고객 필터링
seoul_residents = df[df['CSTMR_MEGA_CTY_NM'] == '서울특별시']
non_seoul_residents = df[df['CSTMR_MEGA_CTY_NM'] != '서울특별시']

# 서울시 거주/비거주 고객 수 출력
print(f"서울 거주 고객 수: {seoul_residents.shape[0]}명")
# 서울 거주 고객 수: 54150명

print(f"비거주 고객 수: {non_seoul_residents.shape[0]}명")
# 비거주 고객 수: 45851명

# 총 소비액 구하기
total_amount = df['AMT'].sum() # 266250278498원

# 성별 소비액 구하기
# 거주 고객 남/녀
seoul_residents[df['SEX_CTGO_CD'] == 1]['AMT'].sum() # 58128378947
seoul_residents[df['SEX_CTGO_CD'] == 2]['AMT'].sum() # 61534763729

# 비거주 고객 남/녀
non_seoul_residents[df['SEX_CTGO_CD'] == 1]['AMT'].sum() # 73579570815
non_seoul_residents[df['SEX_CTGO_CD'] == 2]['AMT'].sum() # 73007565007

# 카드 이용 건수 구하기
seoul_residents['CNT'].sum() # 5542462
non_seoul_residents['CNT'].sum() # 4950200


'''
2) 편의점 소비 정보 분석
- 편의점 소비액 구하기
- 강남구 편의점 소비액 분석
'''

# 편의점 소비액 구하기
df['TP_BUZ_NM'].value_counts()
df[df['TP_BUZ_NM'] == '편 의 점']['AMT'].sum() # 7299184098

# 강남구 편의점 소비액 분석
df[(df['CTY_RGN_NM'] == '강남구') & (df['TP_BUZ_NM'] == '편 의 점')]['AMT'].sum() # 707275140

'''
3) 서울시 거주/비거주 고객의 소비액 구하기
'''
seoul_customers = seoul_residents['AMT'].sum() # 119663142676
non_seoul_customers = non_seoul_residents['AMT'].sum() # 146587135822

'''
4) 거주지 소재 편의점 소비액 구하기
'''
seoul_residents[(seoul_residents['CTY_RGN_NM'] == seoul_residents['CSTMR_CTY_RGN_NM']) & 
                (seoul_residents['TP_BUZ_NM'] == '편 의 점')]['AMT'].sum()
# 4206380676











































