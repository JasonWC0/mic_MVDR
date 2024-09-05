import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert
import os

# 讀取 CSV 文件

file_path = './S6500_30deg_3/6.csv'
START_INDEX= 25         #第2個FILE要加5，第3個要加10，以此類推(取決於整段訊號有幾個包絡)
output_folder_mic1_template = './LONG_TDM_30deg_3/mic1/'
output_folder_mic2_template = './LONG_TDM_30deg_3/mic2/'
output_folder_mic3_template = './LONG_TDM_30deg_3/mic3/'

mic1_data = pd.read_csv(file_path, usecols=[0, 1], header=None, names=['Time', 'Amplitude'])
mic2_data = pd.read_csv(file_path, usecols=[0, 2], header=None, names=['Time', 'Amplitude'])
mic3_data = pd.read_csv(file_path, usecols=[0, 3], header=None, names=['Time', 'Amplitude'])

# 假設 CSV 包含 "Time" 和 "Amplitude" 兩個列
time = mic1_data['Time']
amplitude = mic1_data['Amplitude']

# 計算包絡
analytic_signal = hilbert(amplitude)
envelope = np.abs(analytic_signal)

# 計算包絡的99.9%百分位數作為峰值的閾值
threshold = np.percentile(envelope, 99)

# 找到大於閾值的所有峰值位置
peak_indices = np.where(envelope > threshold)[0]

# 選取最靠前的峰值點，並避免重複選取相鄰的點
peak_times = []
last_peak_time = -np.inf
for index in peak_indices:
    current_time = time.iloc[index]
    if current_time >= last_peak_time + 20:  # 每段長度为 20 秒
        peak_times.append(current_time)
        last_peak_time = current_time

# 初始化存儲切割數據的列表
segments1 = []
segments2 = []
segments3 = []

for peak_time in peak_times:
    start_time = peak_time
    end_time = start_time + 17  # 每段長度為17秒(16.6s)取17秒

    segment1 = mic1_data[(time >= start_time) & (time < end_time)].copy()
    segment2 = mic2_data[(time >= start_time) & (time < end_time)].copy()
    segment3 = mic3_data[(time >= start_time) & (time < end_time)].copy()
    
    if not segment1.empty:
        segment1['Envelope'] = envelope[(time >= start_time) & (time < end_time)]
        segment1['Time'] = segment1['Time'] - start_time
        segments1.append(segment1)
        
        segment2['Time'] = segment2['Time'] - start_time
        segments2.append(segment2)
        
        segment3['Time'] = segment3['Time'] - start_time
        segments3.append(segment3)
    

# 畫出整個包絡線和原始數據
plt.figure(figsize=(15, 6))
plt.plot(time, amplitude, color='lightblue', label='Original Signal')
plt.plot(time, envelope, color='blue', label='Envelope')

# 在每個峰值點處繪製垂直線
for peak_time in peak_times:
    plt.axvline(x=peak_time, color='red', linestyle='--', linewidth=2)

plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Original Signal and Envelope with Peak-Based Segments')
plt.legend()
plt.grid(True)
plt.show()

# 保存每個片段為單獨的 CSV 文件，並畫出每個片段的波形和包絡線
for i, segment in enumerate(segments1):
    output_folder = os.path.join(output_folder_mic1_template.format(i))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    segment[['Time', 'Amplitude']].to_csv(output_folder + f'wear{i+1+START_INDEX}-1_timeDM.csv', index=False)

for i, segment in enumerate(segments2):
    output_folder = os.path.join(output_folder_mic2_template.format(i))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    segment[['Time', 'Amplitude']].to_csv(output_folder + f'wear{i+1+START_INDEX}-2_timeDM.csv', index=False)

for i, segment in enumerate(segments3):
    output_folder = os.path.join(output_folder_mic3_template.format(i))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    segment[['Time', 'Amplitude']].to_csv(output_folder + f'wear{i+1+START_INDEX}-3_timeDM.csv', index=False)

print("包絡計算、切割和繪圖完成，並保存到不同的 CSV 文件中。")
