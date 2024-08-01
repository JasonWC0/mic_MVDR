import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取原始 CSV 檔案並指定標題
file_path = './MVDR_TDM1_FFT/micAll_wear1_filtered.csv'
data = pd.read_csv(file_path, header=None, names=['seconds', 'magnitude'])

# 讀取準位均化後的 CSV 檔案
file_path2 = './MVDR_TDM1_FFT_SMOOTH/micAll_wear1_filtered.csv'
data2 = pd.read_csv(file_path2, header=None, names=['seconds', 'magnitude'])

# 繪製對比波形
plt.figure(figsize=(10, 5))

# 原始波形
#plt.plot(data['seconds'], data['magnitude'], label='original wave')

# 準位均化後的波形
plt.plot(data2['seconds'], data2['magnitude'], label='after normalization')

# 設置圖表標題和標籤
plt.title('波形對比圖')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)
plt.show()

# 計算相似度：皮爾遜相關係數
correlation = np.corrcoef(data['magnitude'], data2['magnitude'])[0, 1]
print(f"兩個波形之間的皮爾遜相關係數是: {correlation:.4f}")
