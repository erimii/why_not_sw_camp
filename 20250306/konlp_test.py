# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 10:02:14 2025

@author: Admin
"""

# pandas
import pandas as pd

sr = pd.Series([17000, 18000, 1000, 5000],
               index=['피자', '치킨', '콜라', '맥주'])
sr.values
sr.index

values=[[1,2,3],[4,5,6],[7,8,9]]
index=['one','two','three']
columns=['A','B','C']

df=pd.DataFrame(values, index=index, columns=columns)
df.index

# Create as a list
data = [
        ['1000', 'steve', 90.72],
        ['1001', 'james', 78.09],
        ['1002', 'doyeon', 98.43],
        ]
df = pd.DataFrame(data, columns=['std_num','name','score'])


# Create as a dictionary
data = {
        'std_num': ['1000','1001','1002'],
        'name': ['steve','james','doyeon'],
        'score': [90.72, 78.99, 98.43]
        }
df = pd.DataFrame(data)


# numpy
import numpy as np

# 1dim array
vec = np.array([1,2,3,4,5])

# 2dim array
mat = np.array([[10,20,30], [60,70,80]])

vec.ndim
mat.shape

zero_mat = np.zeros((2,3))
one_mat = np.ones((2,3))
same_value_mat = np.full((2,3),7)

eye_mat = np.eye(3)
random_mat= np.random.random((2,2))
range_vec = np.arange(10)

step=2
range_n_step_vec = np.arange(1,10,step)

# change the structure of the array
reshape_mat = np.array(np.arange(30)).reshape((5,6))

# numpy slicing
mat = np.array([[10,20,30],
                [60,70,80]])
slicing_first_row = mat[0,:]
slicing_second_col= mat[:,1]

# integer indexing
mat = np.array([[1,2],
                [4,5],
                [7,8]])
mat[1,0] # 4
mat[[2,1],[0,1]] # array([7, 5])

# matplotlib
import matplotlib.pyplot as plt











































