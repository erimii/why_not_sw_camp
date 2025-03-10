# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:02:40 2025

@author: Admin
"""

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'
csv_file = './data/allStoreModified.csv'


# brand를 index로
myframe = pd.read_csv(csv_file, index_col=0, encoding = 'utf-8')

myframe['brand'].unique() 
# array(['cheogajip', 'goobne', 'nene', 'pelicana'], dtype=object) -> 결측치 확인

brand_dict = {'cheogajip':'처가집', 
              'goobne':'굽네', 
              'kyochon':'교촌', 
              'pelicana':'페리카나' , 
              'nene':'네네'}

mygrouping=myframe.groupby(['brand'])['brand']
chartData = mygrouping.count()
'''
brand
cheogajip    1204
goobne       1066
nene         1125
pelicana     1098
Name: brand, dtype: int64
'''

newindex = [brand_dict[idx] for idx in chartData.index]
chartData.index=newindex
'''
처가집     1204
굽네      1066
네네      1125
페리카나    1098
Name: brand, dtype: int64
'''

mycolor = ['r', 'g', 'b', 'm']
plt.figure()
chartData.plot(kind='pie',
               legend=False,
               autopct='%1.2f%%',
               colors=mycolor)



filename = 'Chicken.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(f'{filename} 파일이 내 파일속에 저-장-')

plt.show()



















