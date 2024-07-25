import pandas as pd
import numpy as np
import os
import librosa
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# 讀取所有 CSV 文件
FOLDER_PATH = '././MVDR_TDM'  # 修改為你的資料夾路徑
file_list = [os.path.join(FOLDER_PATH, file) for file in os.listdir(FOLDER_PATH) if file.endswith('.csv')]

data = []
labels = [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  # 假設前 10 個文件代表未磨耗狀態，後 10 個文件代表已磨耗狀態

for i, file in enumerate(file_list):
    df = pd.read_csv(file)
    signal = df.iloc[:, 1].values  # 提取波的大小列
    data.append(signal)
    #labels.append(i)  # 假設每個文件代表不同的磨耗狀態，可以根據實際情況調整

data = np.array(data)
labels = np.array(labels)

# 假設採樣率為 51.2 kHz
sr = 51200

def extract_features(signal, sr, wear_time):
    rms = librosa.feature.rms(y=signal).mean()
    zcr = librosa.feature.zero_crossing_rate(y=signal).mean()
    spectral_centroid = librosa.feature.spectral_centroid(y=signal, sr=sr).mean()
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr).mean()
    spectral_contrast = librosa.feature.spectral_contrast(y=signal, sr=sr).mean()
    spectral_flatness = librosa.feature.spectral_flatness(y=signal).mean()
    spectral_rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sr).mean()
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13).mean(axis=1)
    
    # 將已磨耗時間加入特徵向量
    features = np.hstack((rms, zcr, spectral_centroid, spectral_bandwidth, spectral_contrast, spectral_flatness, spectral_rolloff, mfccs, 
                          wear_time
                          ))
    return features

# 提取每個文件的特徵
feature_data = []
for i, signal in enumerate(data):
    wear_time = i  # 已磨耗時間
    features = extract_features(signal, sr, wear_time)
    feature_data.append(features)

feature_data = np.array(feature_data)

# 拆分數據集
X_train, X_test, y_train, y_test = train_test_split(feature_data, labels, test_size=0.2, random_state=42)

# 創建 SVM 模型並訓練
svm_model = make_pipeline(StandardScaler(), SVC(kernel='linear'))
svm_model.fit(X_train, y_train)

# 測試模型
accuracy = svm_model.score(X_test, y_test)
print(f'模型準確度: {accuracy * 100:.2f}%')
