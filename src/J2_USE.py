import glob
import math
import os
import matplotlib.pyplot as plt
import scipy.io as scio
import numpy as np
import J2 as dj
from pathlib import Path
import scipy.io as sio
#import openpyxl
from numpy.core.function_base import linspace



import itertools

# 模擬的資料範例
FA1 = np.random.rand(10, 5)  # 10個樣本，每個樣本有5個特徵
FA2 = np.random.rand(8, 5)   # 8個樣本，每個樣本有5個特徵
FA3 = np.random.rand(12, 5)  # 12個樣本，每個樣本有5個特徵

FA4 = np.random.rand(7, 5)   # 7個樣本，每個樣本有5個特徵
FA5 = np.random.rand(9, 5)   # 9個樣本，每個樣本有5個特徵
FA6 = np.random.rand(11, 5)  # 11個樣本，每個樣本有5個特徵

# 合併資料並進行後續處理
GP1 = list(itertools.chain(FA1, FA2, FA3))
GP2 = list(itertools.chain(FA4, FA5, FA6))

case1 = np.empty((0, len(FA1[0])))
case2 = case1

case1 = np.vstack((case1, GP1))
case2 = np.vstack((case2, GP2))

feature = [[case1], [case2]]

# 假設的 Scatter_Criterion 函數，這裡簡單返回特徵數組的形狀
#def Scatter_Criterion(feature, param1, param2):
#    return np.array([f.shape for f in feature[0]])

GD = dj.Scatter_Criterion(feature, 2, 0.5)
data = np.ravel(GD)

print("GD:", GD)
print("Flattened Data:", data)
