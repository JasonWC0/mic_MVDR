import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.fft import fft, fftfreq


plt.rcParams['font.sans-serif'] = ['SimHei']  # 設定字體為黑體
plt.rcParams['axes.unicode_minus'] = False  # 確保負號可以正常顯示
# 讀取數據
file_path = '././TDM1/mic1/wear5-1_timeDM.csv'
data = pd.read_csv(file_path, header=None)
time = data[0].values  # 時間 (秒)
amplitude = data[1].values  # 震幅

# 設計帶通濾波器
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# 應用濾波器到數據上
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 設定參數
lowcut = 3.75  # 帶通濾波器的低頻臨界點
highcut = 20000.0  # 帶通濾波器的高頻臨界點
fs = 1 / (time[1] - time[0])  # 計算取樣頻率

# 應用濾波器
filtered_amplitude = butter_bandpass_filter(amplitude, lowcut, highcut, fs, order=6)

# 計算原始信號的頻譜
N = len(amplitude)
yf_original = fft(amplitude)
xf = fftfreq(N, 1 / fs)[:N//2]

# 計算濾波後信號的頻譜
yf_filtered = fft(filtered_amplitude)

# 繪製時間域的信號對比
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, amplitude)
plt.title('未濾波信號')
plt.xlabel('時間 [秒]')
plt.ylabel('震幅')

plt.subplot(3, 1, 2)
plt.plot(time, filtered_amplitude)
plt.title('濾波後的信號 (3.75 Hz - 20,000 Hz)')
plt.xlabel('時間 [秒]')
plt.ylabel('震幅')

# 繪製頻域的頻譜對比
plt.subplot(3, 1, 3)
plt.plot(xf, 2.0/N * np.abs(yf_original[:N//2]), label='原始頻譜')
plt.plot(xf, 2.0/N * np.abs(yf_filtered[:N//2]), label='濾波後頻譜')
plt.title('頻譜對比')
plt.xlabel('頻率 [Hz]')
plt.ylabel('幅度')
plt.legend()

plt.tight_layout()
plt.show()
