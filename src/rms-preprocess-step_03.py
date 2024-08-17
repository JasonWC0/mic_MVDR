import pandas as pd
import numpy as np
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
    filtered_highpass = butter_highpass_filter(data, highcut, fs, order)
    filtered_bandpass = butter_lowpass_filter(filtered_highpass, lowcut, fs, order)
    return filtered_bandpass

# Define the pattern for your input files
INPUT_FILE_PATTERN = 'wear{}-{}_timeDM.csv'
HIGH_PASS_CUTOFF = 20
LOW_PASS_CUTOFF = 20000
FS = 51200

# Iterate over i from 1 to 2 (adjust the range as needed)
for i in range(1, 2):
    DATA_FOLDER = f'./TDM{i}_ANGLE_30/'
    OUTPUT_BASE_FOLDER = f'./PREPROCESSED_TDM_ANGLE_30_STEP03_{i}/'
    
    # Ensure the output folders exist
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic1'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic2'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic3'), exist_ok=True)
    
    counter = 1
    rms1 = rms2 = rms3 = 0
    dataLength = 20

    for j in range(1, dataLength + 1):
        print(f"Processing i={i}, j={j}")
        
        # Manually create the file paths for each mic
        file_path_mic1 = os.path.join(DATA_FOLDER, 'mic1', INPUT_FILE_PATTERN.format(j, 1))
        file_path_mic2 = os.path.join(DATA_FOLDER, 'mic2', INPUT_FILE_PATTERN.format(j, 2))
        file_path_mic3 = os.path.join(DATA_FOLDER, 'mic3', INPUT_FILE_PATTERN.format(j, 3))
        
        # Read the data for each mic
        data1 = pd.read_csv(file_path_mic1, header=None, names=['Time', 'Amplitude'])
        data2 = pd.read_csv(file_path_mic2, header=None, names=['Time', 'Amplitude'])
        data3 = pd.read_csv(file_path_mic3, header=None, names=['Time', 'Amplitude'])
        
        # Apply bandpass filter
        #data1['Amplitude'] = bandpass_filter(data1['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)
        #data2['Amplitude'] = bandpass_filter(data2['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)
        #data3['Amplitude'] = bandpass_filter(data3['Amplitude'], LOW_PASS_CUTOFF, HIGH_PASS_CUTOFF, FS)
        
        # Calculate RMS for the first waveform
        if counter == 1:
            rms1 = np.sqrt(np.mean(data1['Amplitude']**2))
            rms2 = np.sqrt(np.mean(data2['Amplitude']**2))
            rms3 = np.sqrt(np.mean(data3['Amplitude']**2))
            
        # Normalize the amplitude using the respective RMS values
        data1['Amplitude'] = data1['Amplitude'] / rms1
        data2['Amplitude'] = data2['Amplitude'] / rms2
        data3['Amplitude'] = data3['Amplitude'] / rms3

        # Save the normalized data
        output_file_path_mic1 = os.path.join(OUTPUT_BASE_FOLDER, 'mic1', os.path.basename(file_path_mic1))
        output_file_path_mic2 = os.path.join(OUTPUT_BASE_FOLDER, 'mic2', os.path.basename(file_path_mic2))
        output_file_path_mic3 = os.path.join(OUTPUT_BASE_FOLDER, 'mic3', os.path.basename(file_path_mic3))
        
        data1.to_csv(output_file_path_mic1, index=False, header=True)
        data2.to_csv(output_file_path_mic2, index=False, header=True)
        data3.to_csv(output_file_path_mic3, index=False, header=True)
        
        counter += 1
        print(f'rms1: {rms1}, rms2: {rms2}, rms3: {rms3}')
