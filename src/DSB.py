import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# 配置 matplotlib 中文字體
plt.rcParams['font.family'] = ['SimHei']  # 可以更換為你選擇的字體，如 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取三個麥克風的數據
mic_files = {
    'mic1': './PREPROCESSED_TDM/mic1/wear1-1_timeDM.csv',
    'mic2': './PREPROCESSED_TDM/mic2/wear1-2_timeDM.csv',
    'mic3': './PREPROCESSED_TDM/mic3/wear1-3_timeDM.csv'
}

data_mic1 = pd.read_csv(mic_files['mic1'], header=None, names=['秒數', '波的大小'])
data_mic2 = pd.read_csv(mic_files['mic2'], header=None, names=['秒數', '波的大小'])
data_mic3 = pd.read_csv(mic_files['mic3'], header=None, names=['秒數', '波的大小'])

# 不需要延遲處理，直接合併數據並求和
beamformed_signal = (data_mic1['波的大小'].values + data_mic2['波的大小'].values + data_mic3['波的大小'].values) / 3

# 採樣率
sample_rate = 1 / (data_mic1['秒數'].iloc[1] - data_mic1['秒數'].iloc[0])

# 計算傅里葉變換
def compute_fft(signal, sample_rate):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sample_rate)[:N // 2]
    return xf, 2.0 / N * np.abs(yf[0:N // 2])

# 計算每個信號的頻域表示
xf_mic1, yf_mic1 = compute_fft(data_mic1['波的大小'].values, sample_rate)
xf_mic2, yf_mic2 = compute_fft(data_mic2['波的大小'].values, sample_rate)
xf_mic3, yf_mic3 = compute_fft(data_mic3['波的大小'].values, sample_rate)
xf_beamformed, yf_beamformed = compute_fft(beamformed_signal, sample_rate)

# 計算能量
def compute_energy(signal):
    return np.sum(signal ** 2)

energy_mic1 = compute_energy(data_mic1['波的大小'].values)
energy_mic2 = compute_energy(data_mic2['波的大小'].values)
energy_mic3 = compute_energy(data_mic3['波的大小'].values)
energy_beamformed = compute_energy(beamformed_signal)

# 繪製三個麥克風的原始波形和 DSB 後的波形（時間域和頻域）
plt.figure(figsize=(15, 20))

plt.subplot(4, 2, 1)
plt.plot(data_mic1['秒數'], data_mic1['波的大小'], label='Mic1 原始波形')
plt.title(f'Mic1 原始波形 (時間域)\n能量: {energy_mic1:.2f}')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 3)
plt.plot(data_mic2['秒數'], data_mic2['波的大小'], label='Mic2 原始波形')
plt.title(f'Mic2 原始波形 (時間域)\n能量: {energy_mic2:.2f}')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 5)
plt.plot(data_mic3['秒數'], data_mic3['波的大小'], label='Mic3 原始波形')
plt.title(f'Mic3 原始波形 (時間域)\n能量: {energy_mic3:.2f}')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 7)
plt.plot(data_mic1['秒數'], beamformed_signal, label='DSB 波束形成信號')
plt.title(f'DSB 延遲和求和波束形成 (時間域)\n能量: {energy_beamformed:.2f}')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 2)
plt.plot(xf_mic1, yf_mic1, label='Mic1 原始波形')
plt.title('Mic1 原始波形 (頻域)')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 4)
plt.plot(xf_mic2, yf_mic2, label='Mic2 原始波形')
plt.title('Mic2 原始波形 (頻域)')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 6)
plt.plot(xf_mic3, yf_mic3, label='Mic3 原始波形')
plt.title('Mic3 原始波形 (頻域)')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 8)
plt.plot(xf_beamformed, yf_beamformed, label='DSB 波束形成信號')
plt.title('DSB 延遲和求和波束形成 (頻域)')
plt.xlabel('頻率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
