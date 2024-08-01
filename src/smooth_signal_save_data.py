import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os

# 定義要處理的CSV文件目錄和文件前綴
TARGET_FILE_NAME = 'MVDR_TDM1_FFT'
INPUT_DIR = f'././{TARGET_FILE_NAME}'
PROCESS_CSV_FILE_NAME = 'micAll_wear{}_filtered.csv'
output_dir = f'././{TARGET_FILE_NAME}_SMOOTH'

# 定義平滑和下採樣的點數
point = 1000

def downsample_and_smooth(frequency, amplitude, point):
    downsampled_frequency = []
    downsampled_amplitude = []
    for i in range(0, len(frequency), point):
        if i + point <= len(frequency):
            downsampled_frequency.append(np.mean(frequency[i:i+point]))
            downsampled_amplitude.append(np.mean(amplitude[i:i+point]))
    return np.array(downsampled_frequency), np.array(downsampled_amplitude)

# 假設這裡是你的 MVDR_TDM1_FFT_SMOOTH 函數
def MVDR_TDM1_FFT_SMOOTH(frequency, amplitude):
    # 這裡放置你實現 MVDR_TDM1_FFT_SMOOTH 的邏輯
    return frequency, amplitude  # 返回處理後的頻率和幅度

# 確保輸出目錄存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 處理多個文件
for i in range(1, 21):
    file_path = os.path.join(INPUT_DIR, PROCESS_CSV_FILE_NAME.format(i))
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，跳過。")
        continue

    freqdomain_data = pd.read_csv(file_path)

    # 提取頻率和幅度數據
    #Frequency (Hz),Amplitude
    frequency = freqdomain_data['Frequency (Hz)']
    amplitude = freqdomain_data['Magnitude']

    # 使用 MVDR_TDM1_FFT_SMOOTH 進行處理
    processed_frequency, processed_amplitude = MVDR_TDM1_FFT_SMOOTH(frequency, amplitude)

    # 下採樣並平滑數據
    downsampled_frequency, downsampled_amplitude = downsample_and_smooth(processed_frequency, processed_amplitude, point)

    # 將數據保存為CSV文件
    downsampled_data = pd.DataFrame({
        'Frequency (Hz)': downsampled_frequency,
        'Magnitude': downsampled_amplitude
    })
    output_csv_path = os.path.join(output_dir, PROCESS_CSV_FILE_NAME.format(i))
    downsampled_data.to_csv(output_csv_path, index=False)

    print(f"文件已保存至 {output_csv_path}")
