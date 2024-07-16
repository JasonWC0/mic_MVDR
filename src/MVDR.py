import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# 配置 matplotlib 中文字体
plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体

# 读取三个麦克风的数据
mic_files = {
    'mic1': './PREPROCESSED_TDM/mic1/wear1-1_timeDM.csv',
    'mic2': './PREPROCESSED_TDM/mic2/wear1-2_timeDM.csv',
    'mic3': './PREPROCESSED_TDM/mic3/wear1-3_timeDM.csv'
}

data_mic1 = pd.read_csv(mic_files['mic1'], header=None, names=['秒数', '波的大小'])
data_mic2 = pd.read_csv(mic_files['mic2'], header=None, names=['秒数', '波的大小'])
data_mic3 = pd.read_csv(mic_files['mic3'], header=None, names=['秒数', '波的大小'])

# 创建数据矩阵
X = np.vstack([data_mic1['波的大小'].values, data_mic2['波的大小'].values, data_mic3['波的大小'].values])

# 计算协方差矩阵
R = np.cov(X)

# 定义目标方向矢量（假设声源在正前方）
d = np.array([1, 1, 1])

# 计算 MVDR 权重
R_inv = np.linalg.inv(R)
w_mvdr = R_inv @ d / (d.T @ R_inv @ d)

# 进行 MVDR 波束形成
mvdr_signal = w_mvdr @ X

# 采样率
sample_rate = 1 / (data_mic1['秒数'].iloc[1] - data_mic1['秒数'].iloc[0])

# 计算傅里叶变换
def compute_fft(signal, sample_rate):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sample_rate)[:N // 2]
    return xf, 2.0 / N * np.abs(yf[0:N // 2])

# 计算每个信号的频域表示
xf_mic1, yf_mic1 = compute_fft(data_mic1['波的大小'].values, sample_rate)
xf_mic2, yf_mic2 = compute_fft(data_mic2['波的大小'].values, sample_rate)
xf_mic3, yf_mic3 = compute_fft(data_mic3['波的大小'].values, sample_rate)
xf_mvdr, yf_mvdr = compute_fft(mvdr_signal, sample_rate)

# 计算能量
def compute_energy(signal):
    return np.sum(signal ** 2)

energy_mic1 = compute_energy(data_mic1['波的大小'].values)
energy_mic2 = compute_energy(data_mic2['波的大小'].values)
energy_mic3 = compute_energy(data_mic3['波的大小'].values)
energy_mvdr = compute_energy(mvdr_signal)

# 绘制三个麦克风的原始波形和 MVDR 后的波形（时间域和频域）
plt.figure(figsize=(15, 20))

plt.subplot(4, 2, 1)
plt.plot(data_mic1['秒数'], data_mic1['波的大小'], label='Mic1 原始波形')
plt.title(f'Mic1 原始波形 (时间域)\n能量: {energy_mic1:.2f}')
plt.xlabel('秒数')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 3)
plt.plot(data_mic2['秒数'], data_mic2['波的大小'], label='Mic2 原始波形')
plt.title(f'Mic2 原始波形 (时间域)\n能量: {energy_mic2:.2f}')
plt.xlabel('秒数')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 5)
plt.plot(data_mic3['秒数'], data_mic3['波的大小'], label='Mic3 原始波形')
plt.title(f'Mic3 原始波形 (时间域)\n能量: {energy_mic3:.2f}')
plt.xlabel('秒数')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 7)
plt.plot(data_mic1['秒数'], mvdr_signal, label='MVDR Beamformed Signal')
plt.title(f'MVDR Beamforming (时间域)\n能量: {energy_mvdr:.2f}')
plt.xlabel('秒数')
plt.ylabel('波的大小')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 2)
plt.plot(xf_mic1, yf_mic1, label='Mic1 原始波形')
plt.title('Mic1 原始波形 (频域)')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 4)
plt.plot(xf_mic2, yf_mic2, label='Mic2 原始波形')
plt.title('Mic2 原始波形 (频域)')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 6)
plt.plot(xf_mic3, yf_mic3, label='Mic3 原始波形')
plt.title('Mic3 原始波形 (频域)')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 8)
plt.plot(xf_mvdr, yf_mvdr, label='MVDR Beamformed Signal')
plt.title('MVDR Beamforming (频域)')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
