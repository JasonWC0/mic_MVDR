import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import os

import matplotlib.pyplot as plt

# 配置 matplotlib 中文字體
plt.rcParams['font.family'] = 'STFangsong'  # 替換為你選擇的字體

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

# 濾波器參數
CUTOFF_FREQUENCY = 20000  # 20 kHz

for j in range(1, 5):  # Loop for j from 1 to 4
	print(f'處理第 {j} 組數據...')

	# 設置輸入文件夾
	INPUT_FOLDER = f'./PREPROCESSED_TDM{j}/'

	# 設置輸出文件夾
	OUTPUT_FOLDER = f'./MVDR_TDM{j}/'

	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	# 定義每個麥克風到聲源的距離 (單位：米)
	distance_mic1 = 1.00  # 假設麥克風1到聲源的距離為0.98米
	distance_mic2 = 1.00  # 假設麥克風2到聲源的距離為1.02米
	distance_mic3 = 1.00  # 假設麥克風3到聲源的距離為0.98米

	# 計算聲速
	sound_speed = 343  # 聲速 (單位：米/秒)

	for i in range(1, 21):  # 根據需要更改範圍
		print(f'處理第 {i} 組數據...')

		# 讀取三個麥克風的數據
		mic_files = {
			'mic1': f'./{INPUT_FOLDER}/mic1/wear{i}-1_timeDM.csv',
			'mic2': f'./{INPUT_FOLDER}/mic2/wear{i}-2_timeDM.csv',
			'mic3': f'./{INPUT_FOLDER}/mic3/wear{i}-3_timeDM.csv'
		}
        #time秒數，Amplitude為波的大小(這裡用電壓)
		data_mic1 = pd.read_csv(mic_files['mic1'], names=['time', 'Amplitude'],skiprows=1)
		data_mic2 = pd.read_csv(mic_files['mic2'], names=['time', 'Amplitude'],skiprows=1)
		data_mic3 = pd.read_csv(mic_files['mic3'], names=['time', 'Amplitude'],skiprows=1)

		# 計算採樣率
		sample_rate = 1 / (data_mic1['time'].iloc[1] - data_mic1['time'].iloc[0])

		# 應用濾波器
		data_mic1_filtered = lowpass_filter(data_mic1['Amplitude'].values, CUTOFF_FREQUENCY, sample_rate)
		data_mic2_filtered = lowpass_filter(data_mic2['Amplitude'].values, CUTOFF_FREQUENCY, sample_rate)
		data_mic3_filtered = lowpass_filter(data_mic3['Amplitude'].values, CUTOFF_FREQUENCY, sample_rate)

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

		# 創建數據矩陣
		X = np.vstack([data_mic1_delayed, data_mic2_delayed, data_mic3_delayed])

		# 計算協方差矩陣
		R = np.cov(X)

		# 定義目標方向向量（假設聲源在正前方）
		d = np.array([1, 1, 1])

		# 計算 MVDR 權重
		R_inv = np.linalg.inv(R)
		w_mvdr = R_inv @ d / (d.T @ R_inv @ d)

		# 進行 MVDR 波束形成
		mvdr_signal = w_mvdr @ X

		# 儲存 MVDR 結果
		mvdr_data = pd.DataFrame({'time': data_mic1['time'], 'Amplitude': mvdr_signal.real})
		output_file_path = os.path.join(OUTPUT_FOLDER, f'micAll_wear{i}_filtered.csv')
		mvdr_data.to_csv(output_file_path, index=False)

		print(f'MVDR 波束形成的結果已保存到: {output_file_path}')
