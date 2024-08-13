import pandas as pd
import matplotlib.pyplot as plt

# 設定 CSV 檔案的路徑
csv_path_mic1 = './PREPROCESSED_TDM_STEP01_1/mic1/wear4-1_timeDM.csv'
csv_path_mic2 = './PREPROCESSED_TDM_STEP01_1/mic2/wear4-2_timeDM.csv'
csv_path_mic3 = './PREPROCESSED_TDM_STEP01_1/mic3/wear4-3_timeDM.csv'

# 直接讀取 CSV 檔案
data_mic1 = pd.read_csv(csv_path_mic1,header=None, names=['Time', 'Amplitude'], skiprows=1)
data_mic2 = pd.read_csv(csv_path_mic2,header=None, names=['Time', 'Amplitude'], skiprows=1)
data_mic3 = pd.read_csv(csv_path_mic3,header=None, names=['Time', 'Amplitude'], skiprows=1)

plt.figure(figsize=(8, 8))

# 繪製 Mic1 原始波形
plt.subplot(3, 1, 1)  # 3行1列佈局的第一張圖
plt.plot(data_mic1['Time'], data_mic1['Amplitude'])
plt.title('Mic1 Adjust')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.ylim(-2,2)
plt.legend()
plt.grid(True)

# 繪製 Mic2 原始波形
plt.subplot(3, 1, 2)  # 3行1列佈局的第二張圖
plt.plot(data_mic2['Time'], data_mic2['Amplitude'])
plt.title('Mic2 Adjust')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.ylim(-2,2)
plt.legend()
plt.grid(True)

# 繪製 Mic3 原始波形
plt.subplot(3, 1, 3)  # 3行1列佈局的第三張圖
plt.plot(data_mic3['Time'], data_mic3['Amplitude'])
plt.title('Mic3 Adjust')
plt.xlabel('Time(s)')
plt.ylabel('Amplitude')
plt.ylim(-2,2)
plt.legend()
plt.grid(True)

# 調整圖表佈局以避免重疊
plt.tight_layout()

# 顯示圖表
plt.show()
