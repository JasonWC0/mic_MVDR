import pandas as pd
import numpy as np
import os
from scipy.fft import fft
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import matplotlib.pyplot as plt
import J2 as dj


# 讀取檔案
def load_data(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    data_list = [pd.read_csv(os.path.join(folder_path, file)) for file in files]
    return data_list

# 提取 FFT 特徵
def extract_features(data_list, signal_column='Amplitude'):
    features = []
    for data in data_list:
        signal = data[signal_column].values  # 使用 Amplitude 作為訊號
        fft_values = np.abs(fft(signal))
        features.append(fft_values[:len(fft_values)//2])  # 取前半段的頻譜數據
    return np.array(features)

# 計算群組分離準則 (J 值)
def calculate_j_values(negative_features, positive_features):
    num_features = negative_features.shape[1]
    j_values = []
    for i in range(num_features):
        neg_mean = np.mean(negative_features[:, i])
        pos_mean = np.mean(positive_features[:, i])
        overall_mean = (neg_mean + pos_mean) / 2
        
        # 群組間散佈
        sb = len(negative_features) * (neg_mean - overall_mean)**2 + len(positive_features) * (pos_mean - overall_mean)**2
        
        # 群組內散佈
        sw = np.sum((negative_features[:, i] - neg_mean)**2) + np.sum((positive_features[:, i] - pos_mean)**2)
        
        # 計算 J 值
        j_value = sb / sw
        j_values.append(j_value)
    
    return np.array(j_values)

# 主程序
def main():
    # 替換為實際的路徑
    negative_folder_path = './WEAR_OUT_NEGATIVE'  # 替換成你的路徑
    positive_folder_path = './WEAR_OUT_POSITIVE'  # 替換成你的路徑

    # 讀取資料
    negative_data = load_data(negative_folder_path)
    positive_data = load_data(positive_folder_path)

    # 提取特徵
    negative_features = extract_features(negative_data)
    positive_features = extract_features(positive_data)

    # 計算 J 值
    j_values=dj.Scatter_Criterion([[negative_features],[positive_features]],2,0.5)
    j_values_df = pd.DataFrame({'J Value': j_values})
    j_values_df.to_csv('j_values.csv', index=False)
    #j_values = calculate_j_values(negative_features, positive_features)

    # 繪製 J 值圖表
    plt.figure(figsize=(10, 6))
    plt.plot(j_values)
    plt.xlabel('Feature Index (Frequency)')
    plt.ylabel('J Value')
    plt.title('J Value for Each Frequency Feature')
    plt.grid(True)
    plt.show()

    # 選取 J 值最大的特徵
    top_n = 2  # 根據需求選擇最大的 n 個特徵
    top_features_indices = np.argsort(j_values)[-top_n:]

    # 準備訓練數據
    X = np.vstack((negative_features[:, top_features_indices], positive_features[:, top_features_indices]))
    y = np.hstack((np.zeros(len(negative_features)), np.ones(len(positive_features))))

    # 訓練 LDA 模型
    lda = LDA()
    lda.fit(X, y)

    # 測試模型
    predictions = lda.predict(X)

    # 計算準確度
    accuracy = np.mean(predictions == y)
    print(f'Classification accuracy: {accuracy:.2f}')

if __name__ == "__main__":
    main()
