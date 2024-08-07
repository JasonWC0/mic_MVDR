import pandas as pd
import numpy as np
import glob
import os

# Iterate over i from 1 to 4
for i in range(1, 5):
    DATA_FOLDER = f'./TDM{i}/'
    OUTPUT_BASE_FOLDER = f'./PREPROCESSED_TDM_STEP01_{i}/'
    
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
    
    for f1, f2, f3 in zip(mic1_files, mic2_files, mic3_files):
        # Read and calculate RMS for mic1 current file
        data1 = pd.read_csv(f1, header=None, names=['秒數', '波的大小'])
        rms1 = np.sqrt(np.mean(data1['波的大小']**2))

        # Normalize mic2 using mic1's current RMS
        data2 = pd.read_csv(f2, header=None, names=['秒數', '波的大小'])
        rms2 = np.sqrt(np.mean(data2['波的大小']**2))
        data2['波的大小'] = data2['波的大小'] * (rms1 / rms2)

        # Normalize mic3 using mic1's current RMS
        data3 = pd.read_csv(f3, header=None, names=['秒數', '波的大小'])
        rms3 = np.sqrt(np.mean(data3['波的大小']**2))
        data3['波的大小'] = data3['波的大小'] * (rms1 / rms3)

        # Save the normalized data
        data1.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic1', os.path.basename(f1)), index=False, header=True)
        data2.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic2', os.path.basename(f2)), index=False, header=True)
        data3.to_csv(os.path.join(OUTPUT_BASE_FOLDER, 'mic3', os.path.basename(f3)), index=False, header=True)

        print(f'Processed and saved: {os.path.basename(f1)}, {os.path.basename(f2)}, {os.path.basename(f3)}')
