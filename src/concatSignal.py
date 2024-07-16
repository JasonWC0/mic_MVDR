import pandas as pd
import matplotlib.pyplot as plt
import glob

# 定義檔案路徑模式
file_pattern = './TDM/mic1/wear*-1_timeDM.csv'

# 讀取所有符合模式的檔案
all_files = sorted(glob.glob(file_pattern))  # 使用 sorted 保持檔案順序

# 初始化一個空的 DataFrame
combined_data = pd.DataFrame()

# 初始化一個變數來記錄時間偏移量
time_offset = 0

# 讀取並合併所有檔案
for file in all_files:
    data = pd.read_csv(file, header=None, names=['秒數', '波的大小'])
    
    # 調整時間數據
    data['秒數'] += time_offset
    
    # 更新時間偏移量，假設每個檔案的時間間隔是相同的
    time_offset = data['秒數'].iloc[-1] + (data['秒數'].iloc[1] - data['秒數'].iloc[0])
    
    # 合併數據
    combined_data = pd.concat([combined_data, data], ignore_index=True)

# 繪製合併後的波形圖
plt.figure(figsize=(10, 5))
plt.plot(combined_data['秒數'], combined_data['波的大小'])
plt.title('合併波形圖')
plt.xlabel('秒數')
plt.ylabel('波的大小')
plt.grid(True)
plt.show()
print(combined_data)
