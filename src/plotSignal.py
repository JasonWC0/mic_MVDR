import pandas as pd
import matplotlib.pyplot as plt

# 讀取原始 CSV 檔案並指定標題
file_path = './TDM/mic1/wear1-1_timeDM.csv'
data = pd.read_csv(file_path, header=None, names=['seconds', 'magnitude'])

# 讀取準位均化後的 CSV 檔案
file_path2 = './PREPROCESSED_TDM/mic2/wear2-2_timeDM.csv'
data2 = pd.read_csv(file_path2, header=None, names=['seconds', 'magnitude'])

# 繪製對比波形
plt.figure(figsize=(10, 5))

# 原始波形
plt.plot(data['seconds'], data['magnitude'], label='original wave')

# 準位均化後的波形
#plt.plot(data2['seconds'], data2['magnitude'], label='after normalization')

# 設置圖表標題和標籤
plt.title('波形對比圖')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)
plt.show()
