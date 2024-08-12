import numpy as np

# 定義所有的函式
def EachClass_Mean(Signal):
    Class_Mean = []    
    for c in range(len(Signal)):
        feature = Signal[c]        
        M = feature[0].size        
        mean_class = 0
        for j in range(M):                
            memory = feature[0][j]
            mean_class += memory
        Class_Mean.append(mean_class / M)
    return Class_Mean
        
def System_ClassMean(Class_Mean, Pi):
    System_Mean = 0
    for c in range(len(Class_Mean)):
        memory = Pi[c] * Class_Mean[c]
        System_Mean += memory
    return System_Mean

def Scatter_WithinClass(Signal, Class_Mean):
    Ri = [0] * len(Signal)
    for c in range(len(Signal)):
        M = Signal[c][0].size
        feature = Signal[c]
        R_memory = 0
        for j in range(M):
            memory = (feature[0][j] - Class_Mean[c]) ** 2
            R_memory += memory
        Ri[c] = R_memory / M
    return Ri

def Scatter_betweenClass(Signal, System_Mean, Class_Mean, Pi):
    R_memory = 0
    for c in range(len(Signal)):
        memory = (Class_Mean[c] - System_Mean) ** 2
        R_memory += memory * Pi[c]
    return R_memory

def Index_CostFunction(Signal, Ri, Rc):
    R = sum(Ri)
    Cost_J = Rc / R if R != 0 else float('inf')
    return Cost_J

# 假設的信號數據
Signal = [
    np.array([[0.1, 0.2, 0.3]]),
    np.array([[0.4, 0.5, 0.6]]),
    np.array([[0.7, 0.8, 0.9]])
]

# 計算每個類別的平均值
Class_Mean = EachClass_Mean(Signal)

# 設定每個類別的先驗概率
Pi = [1/3, 1/3, 1/3]

# 計算系統類別平均
System_Mean = System_ClassMean(Class_Mean, Pi)

# 計算類內散射
Ri = Scatter_WithinClass(Signal, Class_Mean)

# 計算類間散射
Rc = Scatter_betweenClass(Signal, System_Mean, Class_Mean, Pi)

# 計算成本函數指數
Cost_J = Index_CostFunction(Signal, Ri, Rc)

# 打印結果
print("每個類別的平均值:", Class_Mean)
print("系統類別平均:", System_Mean)
print("類內散射:", Ri)
print("類間散射:", Rc)
print("成本函數指數:", Cost_J)
