import pandas as pd
import numpy as np
import glob
import os

# 定義三個麥克風的檔案路徑模式
mic_patterns = {
    'mic1': './TDM/mic1/wear*-1_timeDM.csv',
    'mic2': './TDM/mic2/wear*-2_timeDM.csv',
    'mic3': './TDM/mic3/wear*-3_timeDM.csv'
}
output_base_folder = './PREPROCESSED_TDM/'

# 確保輸出資料夾存在
for mic in mic_patterns:
    output_folder = os.path.join(output_base_folder, mic)
    os.makedirs(output_folder, exist_ok=True)

# 讀取並處理每個麥克風的檔案
for mic, file_pattern in mic_patterns.items():
    output_folder = os.path.join(output_base_folder, mic)
    all_files = sorted(glob.glob(file_pattern))  # 使用 sorted 保持檔案順序

    for file in all_files:
        data = pd.read_csv(file, header=None, names=['秒數', '波的大小'])
        
        # 計算 RMS 值
        rms_value = np.sqrt(np.mean(data['波的大小']**2))
        
        # 準位均化（對每個值進行標準化）
        data['波的大小'] = data['波的大小'] / rms_value
        
        # 生成輸出檔案名稱
        output_file = os.path.join(output_folder, os.path.basename(file))
        
        # 儲存準位均化後的數據
        data.to_csv(output_file, index=False, header=False)

        print(f'Processed and saved: {output_file}')
