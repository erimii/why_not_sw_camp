# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:02:08 2025

@author: Admin
"""

import pandas as pd
import pymysql

from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb

host = 'localhost'
user = 'root'
password = 'rubi'
db='test'
charset='utf8'

df = pd.read_csv('data/2024년 1월 국내노선 여객 이용률.csv')

engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
conn = engine.connect()


df.to_sql(name='tmp2', con=engine, if_exists='replace', index=False)

conn.close()













































