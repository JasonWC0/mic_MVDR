import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy import signal
from scipy.fft import fft, fftfreq

# 設置 matplotlib 使用支持中文的字體
plt.rcParams['font.family'] = ['Microsoft JhengHei']  # 或者 'SimHei', 'STFangsong'
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取數據
file_path = '././TDM1/mic1/wear1-1_timeDM.csv'
data = pd.read_csv(file_path, header=None)
time = data[0].values  # 時間 (秒)
amplitude = data[1].values  # 震幅

## 設計低通濾波器
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


# 應用低通濾波器到數據上
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 設定參數
lowcut = 20000.0  # 低通濾波器的截止頻率
highcut = 20 # 高通濾波器的截止頻率
fs = 1 / (time[1] - time[0])  # 計算取樣頻率

# 應用濾波器
filtered_amplitude_lowpass = butter_lowpass_filter(amplitude, lowcut, fs, order=5)
filtered_amplitude_highpass = butter_highpass_filter(filtered_amplitude_lowpass, highcut, fs,order=5)

# 計算原始信號的頻譜
N = len(amplitude)
yf_original = fft(amplitude)
xf = fftfreq(N, 1 / fs)[:N//2]

# 計算低通和高通濾波後信號的頻譜
yf_filtered_lowpass = fft(filtered_amplitude_lowpass)
yf_filtered_highpass = fft(filtered_amplitude_highpass)

# 繪製時間域的信號對比
plt.figure(figsize=(12, 12))

plt.subplot(4, 1, 1)
plt.plot(time, filtered_amplitude_highpass)
plt.title('未濾波信號')
plt.xlabel('時間 [秒]')
plt.ylabel('震幅')

plt.subplot(4, 1, 2)
plt.plot(time, filtered_amplitude_highpass)
plt.title('低通濾波後的信號 (截止頻率 20,000 Hz)')
plt.xlabel('時間 [秒]')
plt.ylabel('震幅')

plt.subplot(4, 1, 3)
plt.plot(time, filtered_amplitude_highpass)
plt.title('高通濾波後的信號 (截止頻率 3.75 Hz)')
plt.xlabel('時間 [秒]')
plt.ylabel('震幅')

# 繪製頻域的頻譜對比
plt.subplot(4, 1, 4)
plt.plot(xf, 2.0/N * np.abs(yf_original[:N//2]), label='原始頻譜')
plt.plot(xf, 2.0/N * np.abs(yf_filtered_lowpass[:N//2]), label='低通濾波後頻譜')
plt.plot(xf, 2.0/N * np.abs(yf_filtered_highpass[:N//2]), label='高通濾波後頻譜')
plt.title('頻譜對比')
plt.xlabel('頻率 [Hz]')
plt.ylabel('幅度')
plt.legend()

# 顯示圖形，並等待用戶關閉窗口
plt.show()
