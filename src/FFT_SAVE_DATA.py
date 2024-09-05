import os
import numpy as np
import pandas as pd
from scipy.fft import fft

# 資料夾路徑
input_folder = './RMS_TDM_5/mic3'
output_folder = './TDM5_FFT/mic3'

# 確保輸出資料夾存在
os.makedirs(output_folder, exist_ok=True)

# 處理每個 CSV 檔案
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # 讀取 CSV 檔案，假設第一行是標題行
        filepath = os.path.join(input_folder, filename)
        data = pd.read_csv(filepath, header=0)  # 使用 header=0 來自動將第一行作為標題
        
        # 假設數據是時間在第一列，振幅在第二列
        time = pd.to_numeric(data.iloc[:, 0], errors='coerce').dropna()
        amplitude = pd.to_numeric(data.iloc[:, 1], errors='coerce').dropna()

        # 確保數據長度一致
        min_length = min(len(amplitude), len(time))
        amplitude = amplitude[:min_length]
        time = time[:min_length]

        # 將 Pandas Series 轉換為 NumPy array
        amplitude = amplitude.values
        time = time.values

        # 計算 FFT
        if len(amplitude) > 1 and len(time) > 1:  # 確保數據足夠進行 FFT
            fft_result = fft(amplitude)
            freq = np.fft.fftfreq(len(amplitude), d=(time[1] - time[0]))  # 計算對應的頻率
            
            # 只保留正頻率部分
            positive_freq_idx = freq >= 0
            freq = freq[positive_freq_idx]
            fft_result = np.abs(fft_result[positive_freq_idx])
            
            # 將結果保存為新的 CSV 檔案
            result_df = pd.DataFrame({'Frequency (Hz)': freq, 'Magnitude': fft_result})
            output_filepath = os.path.join(output_folder, filename)
            result_df.to_csv(output_filepath, index=False)
