import glob
import math
import os
import matplotlib.pyplot as plt
import scipy.io as scio
import numpy as np



def EachClass_Mean(Signal):
    # [K,M] = [1,Signal[0][0].size]
    # A = [1,Signal[0][0].size]
    # B = [1,Signal[1][0].size]
    # C = [1,Signal[2][0].size]
    # D = [1,Signal[3][0].size]
    # print(A)
    # print(B)
    # print(C)
    # print(D)
    # print(len(Signal))  4
    # M1=[]
    
    # for i in range(len(Signal)):
    #     M1=Signal[i][0].size
        # print(M1)    
        
        
    # Class_Mean=[]
    # for c in range(len(Signal)):
    #     feature = Signal[c]
    #     # print(feature[0])
    #     mean_class=0
    #     for j in range(M):
            # print(M)
    #         memory = feature[0][j]
    #         # print(memory)
    #         mean_class = mean_class+memory
    #     Class_Mean.append(mean_class/M)
        
   
        
    Class_Mean=[]    
    for c in range(len(Signal)):
        feature = Signal[c]
        
        M=Signal[c][0].size
        
        mean_class=0
        for j in range(M):        
            print(M)        
            memory = feature[0][j]
            # print(memory)
    
            mean_class = mean_class+memory
            # print(mean_class)
        Class_Mean.append(mean_class/M)
        
        # print(Class_Mean)#群內特徵平均
        
        
    return Class_Mean
        
def System_ClassMean(Class_Mean,Pi):
    [K,M] = [Class_Mean[0].size,Class_Mean[0].size]
    # print([K,M])
    System_Mean = 0
    for c in range(len(Class_Mean)):
        memory = Pi[c]*Class_Mean[c]
        # print(memory)
        System_Mean = System_Mean+memory
        # print(System_Mean)#群間特徵平均
    return System_Mean

def Scatter_WithinClass(Signal,Class_Mean):
    Ri=[[],[]]
    for c in range(len(Signal)):
        
        # [K,M] = [1,Signal[0][0].size]
        # print([K,M])
        M=Signal[c][0].size
        feature = Signal[c]
        R_memory = 0
        for j in range(M):
            memory = (feature[0][j]-Class_Mean[c])*(feature[0][j]-Class_Mean[c]).T
            # print(memory)
            R_memory = R_memory+memory
            # print(R_memory)
        Ri[c] = R_memory/M
        # print(Ri)
    return Ri

def Scatter_betweenClass(Signal,System_Mean,Class_Mean,Pi):
    
    R_memory = 0
    for c in range(len(Signal)):
        # print(len(Signal))
        [K,M] = [1,Signal[0][0].size]
        
        memory = (Class_Mean[c]-System_Mean)*(Class_Mean[c]-System_Mean).T
        # print(memory)
        R_memory = R_memory+memory*Pi[c]
        # print(R_memory)
        Rc = R_memory
        # print(Rc)
       
    return Rc

def Index_CostFunction(Signal,Ri,Rc):
    [K,M] = [1,Signal[0][0].size]
    R=np.zeros([1])
    for c in range(len(Signal)):
        memory = Ri[c]
        R = R+memory
        # print(Rc)
    Cost_J = Rc/R
    # print(R)
    return Cost_J

def CostIndex_Block(Memory_First,Memory_Final1,Pi):
    J_index = np.zeros([1,Memory_First[0].shape[1]])
    for k in range(Memory_First[0].shape[1]):
        Class = [[Memory_First[0][:,k]],[Memory_Final1[0][:,k]]
                 ]
        # Mean for each class
        Class_Mean = EachClass_Mean(Class)
        # print(Class_Mean)
        # Mean for System
        System_Mean = System_ClassMean(Class_Mean,Pi)
        # R within Class
        Ri = Scatter_WithinClass(Class,Class_Mean)
       
        #R between Class
        Rc = Scatter_betweenClass(Class,System_Mean,Class_Mean,Pi)
        
        #Index for cost function
        Cost_J = Index_CostFunction(Class,Ri,Rc)
        #Index to J(k)
        J_index[:,k]=Cost_J
    return J_index

# def RankCounter(Input,Counter):        
#     Order = np.zeros([Input.shape[1],Input.shape[0]+1])
#     Memory = Input.tolist()
#     calculation = Input
#     if Input.shape[0] > 1:
#         print('欲比較之data其輸入格式應為行向量')
#     if Input.shape[0] == 1:
#         for i in range(Input.shape[1]):
#             (Max_value , Max_index) = [max(Memory[0]),Memory[0].index(max(Memory[0]))]
#             Order[i]=[Max_index , Max_value]
#             L=np.zeros([1,Max_index])
#             H=np.zeros([1,Input.size-Max_index-1])
#             b=np.append(L,[math.inf])
#             b=np.append(b,H)
#             b=b.reshape(1,Input.shape[1])
#             calculation=calculation-b
#             Memory=calculation
#             Memory = Memory.tolist()
#     AllRank = Order
    
#     if AllRank[Counter][1] > AllRank[Counter+1][1]:
#         SectionRank = AllRank[:Counter][:]
#     elif AllRank[Counter][1] == AllRank[Counter+1][1]:
#         tit = '實際上所找到的前幾項，比所設定的前'+str(Counter)+'項還要多!! \n'
#         print(tit)
#         print('請自行判斷設定值需改變或予以衡量!! \n')
#         SectionRank = AllRank[:Counter][:]
#     elif AllRank[Counter][1] < AllRank[Counter+1][1]:
#         print('分析錯誤，請檢查程式!! \n')
    
#     AllRank = Order.T    
#     return SectionRank,AllRank

#def Repeat(Input,Counter)
#        
def Scatter_Criterion(Feature,Counter,ratio):  #Counter
    Scatter_Reference = Feature[0]  #NonWorn
    Scatter_Compare1 = Feature[1]    #Worn
   
    Pi = [ratio,ratio]
    J_index = CostIndex_Block(Scatter_Reference,Scatter_Compare1
                              ,Pi)
    # SectionRank,AllRank = RankCounter(J_index,Counter),AllRank
    return J_index