import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

# 定義統計分析的函式
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

# 讀取 CSV 文件並處理數據
def read_and_process_files(pattern):
    file_paths = glob.glob(pattern)
    data_list = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        data_list.append(df['Amplitude'].values)
    return [np.array(data).reshape(1, -1) for data in data_list]

# 使用 glob 模式匹配文件路徑
signals = read_and_process_files('./DSB_TDM1/micAll_wear*_filtered.csv')

# 應用統計函式
Class_Mean = EachClass_Mean(signals)
Pi = [1/len(signals)] * len(signals)  # 假設每個類別的概率相等
System_Mean = System_ClassMean(Class_Mean, Pi)
Ri = Scatter_WithinClass(signals, Class_Mean)
Rc = Scatter_betweenClass(signals, System_Mean, Class_Mean, Pi)
Cost_J = Index_CostFunction(signals, Ri, Rc)

# 輸出結果
print("每個類別的平均值:", Class_Mean)
print("系統類別平均:", System_Mean)
print("類內散射:", Ri)
print("類間散射:", Rc)
print("成本函數指數:", Cost_J)

# 可視化一個信號的數據
plt.figure(figsize=(10, 6))
plt.plot(signals[0][0], label='Amplitude of Signal 1')
plt.title('Signal Amplitude Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
