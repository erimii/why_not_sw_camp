# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 16:45:34 2025

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
db='wordcloud_stopwords'
charset='utf8'

stopword_path = "data/불용어 사전의 예/성형gsub.txt"
with open(stopword_path, "r", encoding="cp949") as file:
    stopwords = file.read().split("\n")  # 불용어를 리스트로 변환

df = pd.DataFrame(stopwords)

engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
conn = engine.connect()

df.to_sql(name='plastic_surgery_consultation', con=engine, if_exists='replace', index=False)

conn.close()