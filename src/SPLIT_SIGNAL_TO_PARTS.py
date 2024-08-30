import pandas as pd
import numpy as np
import os

# Define the pattern for your input files
INPUT_FILE_PATTERN = 'wear{}-{}_timeDM.csv'
HIGH_PASS_CUTOFF = 1
LOW_PASS_CUTOFF = 20000
FS = 51200
SPLIT_DURATION = 1

# Iterate over i from 1 to 2 (adjust the range as needed)
for i in range(1, 2):
    DATA_FOLDER = f'./LONG_TDM{i}/'
    OUTPUT_BASE_FOLDER = f'./TDM_V2_{i}/'
    
    # Ensure the output folders exist
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic1'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic2'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE_FOLDER, 'mic3'), exist_ok=True)
    
    counter = 1
    rms1 = rms2 = rms3 = 0
    dataLength = 1

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
        
		# Split the data into parts based on split duration
        split_data1 = np.array_split(data1, int(data1.shape[0] / (FS * SPLIT_DURATION)))
        split_data2 = np.array_split(data2, int(data2.shape[0] / (FS * SPLIT_DURATION)))
        split_data3 = np.array_split(data3, int(data3.shape[0] / (FS * SPLIT_DURATION)))

		# Iterate over the split data and save each part
        for k in range(len(split_data1)):
            output_file_path_mic1_part = os.path.join(OUTPUT_BASE_FOLDER, 'mic1', f'part{k+1}_{os.path.basename(file_path_mic1)}')
            output_file_path_mic2_part = os.path.join(OUTPUT_BASE_FOLDER, 'mic2', f'part{k+1}_{os.path.basename(file_path_mic2)}')
            output_file_path_mic3_part = os.path.join(OUTPUT_BASE_FOLDER, 'mic3', f'part{k+1}_{os.path.basename(file_path_mic3)}')
			
            split_data1[k].to_csv(output_file_path_mic1_part, index=False, header=True)
            split_data2[k].to_csv(output_file_path_mic2_part, index=False, header=True)
            split_data3[k].to_csv(output_file_path_mic3_part, index=False, header=True)
        ## Save the normalized data
        #output_file_path_mic1 = os.path.join(OUTPUT_BASE_FOLDER, 'mic1', os.path.basename(file_path_mic1))
        #output_file_path_mic2 = os.path.join(OUTPUT_BASE_FOLDER, 'mic2', os.path.basename(file_path_mic2))
        #output_file_path_mic3 = os.path.join(OUTPUT_BASE_FOLDER, 'mic3', os.path.basename(file_path_mic3))
        
        #data1.to_csv(output_file_path_mic1, index=False, header=True)
        #data2.to_csv(output_file_path_mic2, index=False, header=True)
        #data3.to_csv(output_file_path_mic3, index=False, header=True)
        
        counter += 1
        print(f'rms1: {rms1}, rms2: {rms2}, rms3: {rms3}')
