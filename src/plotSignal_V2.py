import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案並指定標題，只取前兩列
file_path = './RAW_TDM_DATA/mic1/1.csv'
data = pd.read_csv(file_path, usecols=[0, 1], header=None, names=['seconds', 'magnitude'])

# 繪製圖表
plt.figure(figsize=(10, 5))
plt.plot(data['seconds'], data['magnitude'], label='wave')

# 設置圖表標題和標籤
plt.title('Magnitude vs. Seconds')
plt.xlabel('Seconds')
plt.ylabel('Magnitude')
plt.legend()
plt.show()
