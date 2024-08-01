import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取原始 CSV 檔案並指定標題
file_path = './TDM1/mic1/wear2-1_timeDM.csv'
data = pd.read_csv(file_path, header=None, names=['seconds', 'magnitude'])

# 讀取準位均化後的 CSV 檔案
file_path2 = './PREPROCESSED_TDM1/mic1/wear2-1_timeDM.csv'
data2 = pd.read_csv(file_path2, header=None, names=['seconds', 'magnitude'])

# 定義移動平均函數，將每 1000 個點取平均
def moving_average(data, window_size):
    return data.rolling(window=window_size, min_periods=1).mean()

window_size = 10000
# 使用移動平均對數據進行平滑處理
smoothed_data = moving_average(data['magnitude'], window_size)
smoothed_data2 = moving_average(data2['magnitude'], window_size)

# 計算傅里葉變換
fft_data = np.fft.fft(smoothed_data)
fft_data2 = np.fft.fft(smoothed_data2)

# 計算頻率
n = len(smoothed_data)
sampling_rate = n / (data['seconds'].iloc[-1] - data['seconds'].iloc[0])  # 估計採樣率
freqs = np.fft.fftfreq(n, d=1/sampling_rate)

# 過濾出 -5000 Hz 到 5000 Hz 的範圍
filtered_indices = np.where((freqs >= 0) & (freqs <= 5000))
filtered_freqs = freqs[filtered_indices]
filtered_fft_data = np.abs(fft_data)[filtered_indices]
filtered_fft_data2 = np.abs(fft_data2)[filtered_indices]

# 將頻域中的每 100 Hz 範圍內的頻率分量壓縮成一個點
freq_resolution = 100
compressed_freqs = np.arange(0, 5000, freq_resolution)
compressed_fft_data = [
    np.mean(filtered_fft_data[(filtered_freqs >= f) & (filtered_freqs < f + freq_resolution)])
    for f in compressed_freqs
]
compressed_fft_data2 = [
    np.mean(filtered_fft_data2[(filtered_freqs >= f) & (filtered_freqs < f + freq_resolution)])
    for f in compressed_freqs
]

# 繪製頻域對比圖
plt.figure(figsize=(10, 5))

# 原始波形的頻域（經平滑處理後）
plt.plot(compressed_freqs, compressed_fft_data, label='Smoothed Original Wave Frequency')

# 準位均化後的波形頻域（經平滑處理後）
plt.plot(compressed_freqs, compressed_fft_data2, label='Smoothed After Normalization Frequency')

# 設置圖表標題和標籤
plt.title('頻域對比圖（經平滑處理後，100 Hz 壓縮）')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)
plt.xlim(0, 5000)  # 設置 X 軸顯示範圍
plt.show()
