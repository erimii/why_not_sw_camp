# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:01:13 2025

@author: Admin
"""

# 크롤링 결과가 담긴 엑셀 파일 통합

import pandas as pd

excel_names=['./files/melon.xlsx',
             './files/bugs.xlsx',
             './files/genie.xlsx']

appended_data = pd.DataFrame()

for name in excel_names:
    pd_data = pd.read_excel(name)
    appended_data = pd.concat([appended_data, pd_data], ignore_index=True)

appended_data.sample(5)
'''
       서비스  순위          타이틀          가수
3    Melon   4     Whiplash       aespa
274  Genie  75  미안해 미워해 사랑해       Crush
66   Melon  67     미치게 그리워서         황가람
272  Genie  73   earthquake  지수 (JISOO)
101   Bugs   2     ATTITUDE   IVE (아이브)
'''

appended_data.to_excel('./files/total.xlsx', index = False )


































