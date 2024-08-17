import pandas as pd
import numpy as np
import glob
import os
from scipy.signal import butter, lfilter


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    應用帶通濾波器

    :param data: 輸入信號
    :param lowcut: 低通截止頻率
    :param highcut: 高通截止頻率
    :param fs: 取樣頻率
    :param order: 濾波器的階數
    :return: 濾波後的信號
    """
    filtered_highpass = butter_highpass_filter(data, highcut, fs, order)
    filtered_bandpass = butter_lowpass_filter(filtered_highpass, lowcut, fs, order)
    return filtered_bandpass

# Iterate over i from 1 to 4
for i in range(1, 2):
    DATA_FOLDER = f'./TDM{i}_ANGLE_30/'
    OUTPUT_BASE_FOLDER = f'./PREPROCESSED_TDM_ANGLE_30_STEP03_{i}/'
    HIGH_PASS_CUTOFF = 20
    LOW_PASS_CUTOFF = 20000
    FS = 51200
    
    # Define the mic_patterns for each i
    mic_patterns = {
        'mic1': f'{DATA_FOLDER}mic1/wear*-1_timeDM.csv',
        'mic2': f'{DATA_FOLDER}mic2/wear*-2_timeDM.csv',
        'mic3': f'{DATA_FOLDER}mic3/wear*-3_timeDM.csv'
    }

    # Ensure the output folders exist
    for mic in mic_patterns:
        output_folder = os.path.join(OUTPUT_BASE_FOLDER, mic)
        os.makedirs(output_folder, exist_ok=True)

    # Process all files simultaneously considering mic1 as reference for each batch
    mic1_files = sorted(glob.glob(mic_patterns['mic1']))
    mic2_files = sorted(glob.glob(mic_patterns['mic2']))
    mic3_files = sorted(glob.glob(mic_patterns['mic3']))
    
    counter = 1
    rms1 = 0
    rms2 = 0
    rms3 = 0
    for f1, f2, f3 in zip(mic1_files, mic2_files, mic3_files):
        # Read and calculate RMS for mic1 current file
        data1 = pd.read_csv(f1, header=None, names=['Time', 'Amplitude'])
        data2 = pd.read_csv(f2, header=None, names=['Time', 'Amplitude'])
        data3 = pd.read_csv(f3, header=None, names=['Time', 'Amplitude'])
        
        # 取得第一道波形的RMS
        if counter == 1:
            rms1 = np.sqrt(np.mean(data1['Amplitude']**2))
            rms2 = np.sqrt(np.mean(data2['Amplitude']**2))
            rms3 = np.sqrt(np.mean(data3['Amplitude']**2))
            
            
        data1['Amplitude'] = data1['Amplitude'] / rms1
        # Normalize mic2 using mic1's current RMS
        data2['Amplitude'] = data2['Amplitude'] /rms2
        
        # Normalize mic3 using mic1's current RMS
        data3['Amplitude'] = data3['Amplitude'] * rms3

        print('rms1',rms1)
        print('rms2',rms2)
        print('rms3',rms3)
        
        #data1['Amplitude'] = bandpass_filter(data1['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)
        #data2['Amplitude'] = bandpass_filter(data2['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)
        #data3['Amplitude'] = bandpass_filter(data3['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)


        # Save the normalized data
        data1.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic1', os.path.basename(f1)), index=False, header=True)
        data2.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic2', os.path.basename(f2)), index=False, header=True)
        data3.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic3', os.path.basename(f3)), index=False, header=True)
        counter += 1
        print('rms1',rms1,'rms2',rms2,'rms3',rms3)
        print(f'Processed and saved: {os.path.basename(f1)}, {os.path.basename(f2)}, {os.path.basename(f3)}')
