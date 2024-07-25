# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# import os

# # 指定單一文件的路徑
# file_path = 'C:/Users/NTU138/Desktop/test/noise/wear4_DSB_fft.csv'

# # 定義平滑和下採樣的點數
# point = 1000

# def downsample_and_smooth(frequency, amplitude, point):
#     downsampled_frequency = []
#     downsampled_amplitude = []
#     for i in range(0, len(frequency), point):
#         if i + point <= len(frequency):
#             downsampled_frequency.append(np.mean(frequency[i:i+point]))
#             downsampled_amplitude.append(np.mean(amplitude[i:i+point]))
#     return np.array(downsampled_frequency), np.array(downsampled_amplitude)

# if os.path.exists(file_path):
#     freqdomain_data = pd.read_csv(file_path)

#     # 提取頻率和幅度數據
#     frequency = freqdomain_data['Frequency (Hz)']
#     amplitude = freqdomain_data['Amplitude']

#     # 下採樣並平滑數據
#     downsampled_frequency, downsampled_amplitude = downsample_and_smooth(frequency, amplitude, point)

#     # 將數據保存為CSV文件
#     downsampled_data = pd.DataFrame({
#         'Frequency (Hz)': downsampled_frequency,
#         'Amplitude': downsampled_amplitude
#     })
#     csv_path = file_path.replace('.csv', f'_{point}.csv')
#     downsampled_data.to_csv(csv_path, index=False)
    
#     # 可視化處理後的信號
#     plt.figure(figsize=(15,8), dpi=360)
#     plt.plot(downsampled_frequency, downsampled_amplitude, linestyle='-', color='b', linewidth=0.5)
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Amplitude')
#     plt.xlim(0, 20000)
#     plt.ylim(0, 1000)
#     y_major_locator = MultipleLocator(100)
#     ax = plt.gca()
#     ax.yaxis.set_major_locator(y_major_locator)
#     plt.grid(True)
#     image_path = file_path.replace('.csv', f'_{point}_downsampled1.png')
#     plt.savefig(image_path)  # 保存圖像
#     plt.close()
# else:
#     print(f"文件 {file_path} 不存在。")

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# import os

# # 定義要處理的CSV文件目錄和文件前綴
# base_dir = 'C:/Users/NTU138/Desktop/row_data_0613/S7500_mic_silence_1/cut/fft'
# file_prefix = 'wear'
# file_suffix = '_fft.csv'

# # 定義平滑和下採樣的點數
# point = 10

# def downsample_and_smooth(frequency, amplitude, point):
#     downsampled_frequency = []
#     downsampled_amplitude = []
#     for i in range(0, len(frequency), point):
#         if i + point <= len(frequency):
#             downsampled_frequency.append(np.mean(frequency[i:i+point]))
#             downsampled_amplitude.append(np.mean(amplitude[i:i+point]))
#     return np.array(downsampled_frequency), np.array(downsampled_amplitude)

# # 處理多個文件
# for i in range(1, 21):
#     for j in range(1, 4):
#         file_path = os.path.join(base_dir, f'{file_prefix}{i}-{j}{file_suffix}')
#         if not os.path.exists(file_path):
#             print(f"文件 {file_path} 不存在，跳過。")
#             continue

#         freqdomain_data = pd.read_csv(file_path)

#         # 提取頻率和幅度數據
#         frequency = freqdomain_data['Frequency (Hz)']
#         amplitude = freqdomain_data['Amplitude']

#         # 下採樣並平滑數據
#         downsampled_frequency, downsampled_amplitude = downsample_and_smooth(frequency, amplitude, point)

#         # 將數據保存為CSV文件
#         downsampled_data = pd.DataFrame({
#             'Frequency (Hz)': downsampled_frequency,
#             'Amplitude': downsampled_amplitude
#         })
#         csv_path = os.path.join(base_dir, f'10Hz/{file_prefix}{i}-{j}_{point}.csv')
#         downsampled_data.to_csv(csv_path, index=False)
        
#         # 可視化處理後的信號
#         plt.figure(figsize=(15,8), dpi=360)
#         plt.plot(downsampled_frequency, downsampled_amplitude, linestyle='-', color='b',label=f'wear{i}-{j}', linewidth=0.5)
#         plt.xlabel('Frequency (Hz)')
#         plt.ylabel('Amplitude')
#         plt.xlim(0, 20000)
#         plt.ylim(0,1000)
#         y_major_locator = MultipleLocator(100)
#         ax = plt.gca()
#         ax.yaxis.set_major_locator(y_major_locator)
#         plt.legend()
#         plt.grid(True)
#         plt.savefig(os.path.join(base_dir, f'{file_prefix}{i}-{j}_{point}.png'))  # 保存圖像
#         plt.close()



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os

# 定義要處理的CSV文件目錄和文件前綴
base_dir = 'C:/Users/NTU138/Desktop/row_data_0613/S7500_mic_silence_1/cut/TDM/adjust/mic1/fft'
file_prefix = 'wear'
file_suffix = '-1_fftt.csv'

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

# 處理多個文件
for i in range(1, 21):
    file_path = os.path.join(base_dir, f'{file_prefix}{i}{file_suffix}')
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，跳過。")
        continue

    freqdomain_data = pd.read_csv(file_path)

    # 提取頻率和幅度數據
    frequency = freqdomain_data['Frequency (Hz)']
    amplitude = freqdomain_data['Amplitude']

    # 下採樣並平滑數據
    downsampled_frequency, downsampled_amplitude = downsample_and_smooth(frequency, amplitude, point)

    # 將數據保存為CSV文件
    downsampled_data = pd.DataFrame({
        'Frequency (Hz)': downsampled_frequency,
        'Amplitude': downsampled_amplitude
    })
    csv_path = os.path.join(base_dir, f'{file_prefix}{i}_OG_{point}.csv')
    downsampled_data.to_csv(csv_path, index=False)
    
#     # 可視化處理後的信號
#     plt.figure(figsize=(15,8), dpi=360)
#     plt.plot(downsampled_frequency, downsampled_amplitude, linestyle='-', color='b',label=f'wear{i}', linewidth=0.5)
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Amplitude')
#     plt.xlim(0, 20000)
#     plt.ylim(0,1000)
#     y_major_locator = MultipleLocator(100)
#     ax = plt.gca()
#     ax.yaxis.set_major_locator(y_major_locator)
#     plt.legend()
#     plt.grid(True)
#     plt.savefig(os.path.join(base_dir, f'{file_prefix}{i}_DSB_{point}.png'))  # 保存圖像
#     plt.close()



# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# import os

# # 定義要處理的CSV文件目錄和文件後綴
# base_dir = 'C:/Users/NTU138/Desktop/row_data_0613/S7500_mic_noise_1/cut/fft'
# file_suffix = '_fft.csv'

# # 定義平滑和下採樣的點數
# point = 10

# def downsample_and_smooth(frequency, amplitude, point):
#     downsampled_frequency = []
#     downsampled_amplitude = []
#     for i in range(0, len(frequency), point):
#         if i + point <= len(frequency):
#             downsampled_frequency.append(np.mean(frequency[i:i+point]))
#             downsampled_amplitude.append(np.mean(amplitude[i:i+point]))
#     return np.array(downsampled_frequency), np.array(downsampled_amplitude)

# # 處理多個文件
# for i in range(1, 21):
#     for j in range(1, 4):
#         file_name = f'{i}-{j}{file_suffix}'
#         file_path = os.path.join(base_dir, file_name)
#         if not os.path.exists(file_path):
#             print(f"文件 {file_path} 不存在，跳過。")
#             continue

#         freqdomain_data = pd.read_csv(file_path)

#         # 提取頻率和幅度數據
#         frequency = freqdomain_data['Frequency (Hz)']
#         amplitude = freqdomain_data['Amplitude']

#         # 下採樣並平滑數據
#         downsampled_frequency, downsampled_amplitude = downsample_and_smooth(frequency, amplitude, point)

#         # 將數據保存為CSV文件
#         downsampled_data = pd.DataFrame({
#             'Frequency (Hz)': downsampled_frequency,
#             'Amplitude': downsampled_amplitude
#         })
#         new_file_name = file_name.replace(file_suffix, f'_{point}.csv')
#         csv_path = os.path.join(base_dir, new_file_name)
#         downsampled_data.to_csv(csv_path, index=False)
        
#         # 可視化處理後的信號
#         plt.figure(figsize=(15,8), dpi=360)
#         plt.plot(downsampled_frequency, downsampled_amplitude, linestyle='-', color='b', label=f'{i}-{j}', linewidth=0.5)
#         plt.xlabel('Frequency (Hz)')
#         plt.ylabel('Amplitude')
#         plt.xlim(0, 20000)
#         plt.ylim(0, 1000)
#         y_major_locator = MultipleLocator(100)
#         ax = plt.gca()
#         ax.yaxis.set_major_locator(y_major_locator)
#         plt.legend()
#         plt.grid(True)
#         new_image_name = file_name.replace(file_suffix, f'_{point}.png')
#         plt.savefig(os.path.join(base_dir, new_image_name))  # 保存圖像
#         plt.close()
