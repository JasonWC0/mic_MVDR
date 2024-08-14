import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt
import os

# 計算濾波器的參數
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# 計算傅里葉變換
def compute_fft(signal, sample_rate):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sample_rate)[:N // 2]
    return xf, 2.0 / N * np.abs(yf[0:N // 2])

# 計算能量
def compute_energy(signal):
    return np.sum(signal ** 2)

# 設定濾波器參數
cutoff_frequency = 20000  # 20 kHz

# 定義每個麥克風到聲源的距離 (單位：米)
distance_mic1 = 1.00  # 假設麥克風1到聲源的距離為0.98米
distance_mic2 = 1.00  # 假設麥克風2到聲源的距離為1.02米
distance_mic3 = 1.00  # 假設麥克風3到聲源的距離為0.98米

# 計算聲速
sound_speed = 343  # 聲速 (單位：米/秒)

# 自動化處理多組數據
for j in range(2,5):  # 外層迴圈處理不同數據組
    print(f'處理第 {j} 組數據...')
    
    INPUT_FOLDER = f'./PREPROCESSED_TDM_STEP01_{j}/'
    OUTPUT_FOLDER = f'./DSB_TDM{j}/'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for i in range(1, 21):  # 根據需要更改範圍
        print(f'處理第 {i} 組數據...')
        
        # 讀取三個麥克風的數據
        mic_files = {
            'mic1': f'{INPUT_FOLDER}/mic1/wear{i}-1_timeDM.csv',
            'mic2': f'{INPUT_FOLDER}/mic2/wear{i}-2_timeDM.csv',
            'mic3': f'{INPUT_FOLDER}/mic3/wear{i}-3_timeDM.csv'
        }

        data_mic1 = pd.read_csv(mic_files['mic1'], header=None, names=['Time', 'Amplitude'], skiprows=1)
        data_mic2 = pd.read_csv(mic_files['mic2'], header=None, names=['Time', 'Amplitude'], skiprows=1)
        data_mic3 = pd.read_csv(mic_files['mic3'], header=None, names=['Time', 'Amplitude'], skiprows=1)

        # 計算採樣率
        sample_rate = 1 / (data_mic1['Time'].iloc[1] - data_mic1['Time'].iloc[0])

        # 應用濾波器
        data_mic1_filtered = lowpass_filter(data_mic1['Amplitude'].values, cutoff_frequency, sample_rate)
        data_mic2_filtered = lowpass_filter(data_mic2['Amplitude'].values, cutoff_frequency, sample_rate)
        data_mic3_filtered = lowpass_filter(data_mic3['Amplitude'].values, cutoff_frequency, sample_rate)

        # 計算每個麥克風的延遲時間
        delay_mic1 = distance_mic1 / sound_speed
        delay_mic2 = distance_mic2 / sound_speed
        delay_mic3 = distance_mic3 / sound_speed

        # 將延遲轉換為樣本數
        sample_delay_mic1 = int(delay_mic1 * sample_rate)
        sample_delay_mic2 = int(delay_mic2 * sample_rate)
        sample_delay_mic3 = int(delay_mic3 * sample_rate)

        # 調整麥克風數據以考慮延遲
        data_mic1_delayed = np.roll(data_mic1_filtered, sample_delay_mic1)
        data_mic2_delayed = np.roll(data_mic2_filtered, sample_delay_mic2)
        data_mic3_delayed = np.roll(data_mic3_filtered, sample_delay_mic3)

        # 進行 DSB 波束形成
        beamformed_signal = (data_mic1_delayed + data_mic2_delayed + data_mic3_delayed) / 3

        # 儲存 DSB 波束形成後的信號到 CSV 文件
        dsb_result = pd.DataFrame({'Time': data_mic1['Time'], 'Amplitude': beamformed_signal})
        output_csv_path = os.path.join(OUTPUT_FOLDER, f'micAll_wear{i}_filtered.csv')
        dsb_result.to_csv(output_csv_path, index=False)

        print(f'DSB 波束形成的結果已保存到: {output_csv_path}')
