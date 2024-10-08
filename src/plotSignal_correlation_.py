import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 設置 matplotlib 使用支持中文的字體
plt.rcParams['font.family'] = ['Microsoft JhengHei']  # 或者 'SimHei', 'STFangsong'
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取原始 CSV 檔案並指定標題
file_path1 = './PREPROCESSED_TDM_STEP01_1_FFT_SMOOTH/mic1/wear4-1_timeDM.csv'
data1 = pd.read_csv(file_path1, header=None, names=['seconds', 'magnitude'], skiprows=1)
file_path3 = './PREPROCESSED_TDM_ANGLE_30_STEP01_1_FFT_SMOOTH/mic1/wear4-1_timeDM.csv'
data3 = pd.read_csv(file_path3, header=None, names=['seconds', 'magnitude'], skiprows=1)
# 讀取準位均化後的 CSV 檔案
file_path2 = './DSB_TDM1_FFT_SMOOTH/micAll_wear4_filtered.csv'
data2 = pd.read_csv(file_path2, header=None, names=['seconds', 'magnitude'], skiprows=1)
file_path4 = './DSB_ANDLE_30_TDM1_FFT_SMOOTH/micAll_wear4_filtered.csv'
data4 = pd.read_csv(file_path4, header=None, names=['seconds', 'magnitude'], skiprows=1)
# 繪製對比波形
plt.figure(figsize=(10, 5))

# 原始波形
plt.plot(data1['seconds'], data1['magnitude'], label='未濾波對準訊號', linewidth=0.8)
plt.plot(data3['seconds'], data3['magnitude'], label='未濾波30度訊號', linewidth=0.8)

# 準位均化後的波形
plt.plot(data2['seconds'], data2['magnitude'], label='DSB濾波對準訊號', linewidth=0.8)
plt.plot(data4['seconds'], data4['magnitude'], label='DSB濾波30度訊號', linewidth=0.8)

# 設置圖表標題和標籤
# plt.title('波形對比圖')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0,20000)
plt.ylim() 
plt.legend()
plt.grid(True)
plt.show()

# 計算相似度：皮爾遜相關係數
correlation = np.corrcoef(data1['magnitude'], data3['magnitude'])[0, 1]
print(f"兩個波形之間的皮爾森相關係數是: {correlation:.4f}")
correlation = np.corrcoef(data2['magnitude'], data4['magnitude'])[0, 1]
print(f"兩個波形之間的皮爾森相關係數是: {correlation:.4f}")
