# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 14:53:56 2025

@author: Admin
"""
'''
-- 52주간의 주식 최저가와 최고가 조회
-- 1일간의 시작가와 종가를 비교한 정보 조회
-- 10% 이상 가격이 오른 종목 조회
-- 전일 대비 증감과 즘감률 조회


주가가 연속적으로 상승한 종목 분석
-- 1. 특정 기간동안 종목별 등락을 저장하는 테이블
-- 2. 10% 상승한 종목들의 정보를 저장하는 테이블 생성
-- 3. symbol 열을 기준으로 전일 데이터 전일 대비 상승한 종목 데이터를 저장하는 테이블
-- 4. 주가가 한 번도 하락하지 않은 데이터를 저장하는 테이블 생성
-- 5. nasdaq_company 테이블과 임시 테이블을 조인해 최종 정보 출력
'''

import pandas as pd
import pymysql
from datetime import datetime, timedelta

# mysql에 연결
host = 'localhost'
user = 'root'
password = 'rubi'
db_name = 'us_stock'

conn = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db_name,
                             charset='utf8')

# cursor 생성
cursor = conn.cursor(pymysql.cursors.DictCursor)
# 쿼리 작성해서 원하는 데이터 선택
query1 = """ select * from stock; """
query2 = """ select * from nasdaq_company; """

# execute()로 query 실행
cursor.execute(query1)
execute_result1 = cursor.fetchall()
stock = pd.DataFrame(execute_result1)

cursor.execute(query2)
execute_result2 = cursor.fetchall()
nasdaq = pd.DataFrame(execute_result2)

conn.close()


# 주어진 날짜를 기준으로 지난 52주 동안의 최고가와 최저가를 반환하는 함수
stock.head()
stock.info()

cols_to_convert = ['open', 'high', 'low', 'close', 'adj_close']
stock[cols_to_convert] = stock[cols_to_convert].astype(float)

stock['diff_price'] = stock['close']-stock['open']
stock['diff_ratio'] = round((stock['close']-stock['open']) / stock['open'] * 100, 2)

def get_52_week_high_low(stock, date):
    target_date = pd.to_datetime(date)
    
    start_date = target_date - pd.DateOffset(weeks=52)
    
    # 52주 기간 내 데이터 필터링
    filtered_df = stock[(stock['date'] >= start_date) & (stock['date'] <= target_date)]
    
    # 종목(symbol)별 52주 최고가 및 최저가 계산
    result = filtered_df.groupby('symbol').agg(
        high_52_week=('high', 'max'),
        low_52_week=('low', 'min')
    ).reset_index()
    
    return result


result = get_52_week_high_low(stock, '2025-03-04')
print(result)


# 하루동안 10% 이상 가격이 오른 종목 시작가와 종가를 비교한 정보 조회
def get_day_open_close_diff(stock, date):
    target_date = pd.to_datetime(date)
    
    filtered_df = stock[(stock['date'] == target_date) & (stock['diff_ratio'] >= 10)]
    
    # 종목별 시작가(open), 종가(close), 가격 차이(diff) 계산
    result = filtered_df[['symbol', 'open', 'close', 'diff_price', 'diff_ratio']]
    
    return result

result = get_day_open_close_diff(stock, '2022-02-24')
print(result)

# 전일 대비 종목의 변화 분석하기
def get_previous_day_stock_change(stoc, date):
    target_date = pd.to_datetime(date)
    previous_date = target_date + pd.DateOffset(days=1)
    
    df1 = stock[['date', 'symbol', 'close']][stock['date'] == date]
    df2 = stock[['date','symbol', 'close']][stock['date'] == previous_date]
    merged_df = pd.merge(df1, df2, on='symbol', suffixes=('_a', '_b'))

    merged_df['diff_price'] = merged_df['close_b'] - merged_df['close_a']
    merged_df['diff_ratio'] = (merged_df['diff_price'] / merged_df['close_b']) * 100
    
    return merged_df
    
result = get_previous_day_stock_change(stock, '2023-10-04')
print(result)

# 주가가 1주일 동안 연속적으로 상승한 종목 분석
def get_continuous_price_increase_stocks(stock, date):
    target_date = pd.to_datetime(date)
    start_date = target_date - pd.DateOffset(weeks=1)
    
    filtered_df = stock[(stock['date'] >= start_date) & (stock['date'] <= target_date)]
    
    continuous_rise_stocks = []

    for symbol, group in filtered_df.groupby('symbol'): 
        group['price_increase'] = group['close'].diff() > 0
        
        if group['price_increase'].sum() == 5:
            continuous_rise_stocks.append(symbol)
    
    filtered_df.isin(continuous_rise_stocks)
    result = filtered_df[filtered_df['symbol'].isin(continuous_rise_stocks)].groupby('symbol').agg(start_close=('close', 'min'), close = ('close', 'max'))

    return result

result = get_continuous_price_increase_stocks(stock, '2021-02-24')
print(result)










