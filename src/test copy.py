import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def sine_generator(fs, sinefreq, duration):
    T = duration
    nsamples = fs * T
    w = 2. * np.pi * sinefreq
    t_sine = np.linspace(0, T, nsamples, endpoint=False)
    y_sine = np.sin(w * t_sine)
    result = pd.DataFrame({ 
        'data' : y_sine} ,index=t_sine)
    return result

# 帶阻濾波器
def butter_bandstop(cutoff_low, cutoff_high, fs, order=5):
    nyq = 0.5 * fs
    low = cutoff_low / nyq
    high = cutoff_high / nyq
    b, a = butter(order, [low, high], btype='bandstop', analog=False)
    return b, a

def butter_bandstop_filter(data, cutoff_low, cutoff_high, fs, order=5):
    b, a = butter_bandstop(cutoff_low, cutoff_high, fs, order=order)
    y = lfilter(b, a, data)
    return y

fps = 51200
sine_fq = 10  # Hz
duration = 10  # seconds
sine_5Hz = sine_generator(fps, sine_fq, duration)
sine_fq = 1  # Hz
sine_1Hz = sine_generator(fps, sine_fq, duration)

# 載入數據
file_path = '././TDM_CUT_1/mic1/wear1-1_timeDM_1s.csv'
data = pd.read_csv(file_path, header=None, skiprows=1)
time = data[0].values  # 時間 (秒)
amplitude = data[1].values  # 震幅

# 將訊號進行帶阻濾波
filtered_signal = butter_bandstop_filter(amplitude, 7000, 12000, fps)

# 計算帶阻濾波後與原始訊號的FFT
fft_filtered_sine = np.fft.fft(filtered_signal)
fft_amplitude = np.fft.fft(amplitude)

# 計算頻率軸
freq = np.fft.fftfreq(len(filtered_signal), 1 / fps)

# 繪製 FFT 結果
plt.figure(figsize=(20, 10))
plt.subplot(211)
plt.plot(freq, np.abs(fft_filtered_sine))
plt.title('FFT of bandstop filtered signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(freq, np.abs(fft_amplitude))
plt.title('FFT of original signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.show()