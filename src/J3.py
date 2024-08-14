import glob
import math
import os
import matplotlib.pyplot as plt
import scipy.io as scio
import numpy as np
import J_2種特徵 as dj
from pathlib import Path
import scipy.io as sio
import openpyxl
from numpy.core.function_base import linspace



import itertools

GP1=list(itertools.chain(FA1, FA2, FA3))
          
GP2=list(itertools.chain(FA4, FA5, FA6)) 


case1 = np.empty((0,len(FA1[0])))
case2 = case1


case1 = np.vstack((case1,GP1))
case2 = np.vstack((case2,GP2))


feature = [[case1],[case2]] 


GD = dj.Scatter_Criterion(feature,2,0.5)
data = np.ravel(GD)