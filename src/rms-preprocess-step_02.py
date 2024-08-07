import pandas as pd
import numpy as np
import glob
import os

# Custom RMS-based adjustment
def adjust_data(data):
    for start_idx in range(4, len(data), 4):
        if start_idx + 4 < len(data):
            # Calculate RMS for the 4th and 5th entries
            rms4 = np.sqrt(np.mean(data['波的大小'][start_idx-1]**2))
            rms5 = np.sqrt(np.mean(data['波的大小'][start_idx]**2))
            
            # Calculate the ratio rms4/rms5
            rms_ratio = rms4 / rms5
            
            # Apply the ratio to the next 4 entries
            data.loc[start_idx:start_idx+3, '波的大小'] *= rms_ratio
            
    return data

# Iterate over i from 1 to 4
for i in range(1, 5):
    DATA_FOLDER = f'./PREPROCESSED_TDM_STEP01_{i}/'
    OUTPUT_BASE_FOLDER = f'./PREPROCESSED_TDM_STEP02_{i}/'
    
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

    # Process each mic's files
    for mic, file_pattern in mic_patterns.items():
        output_folder = os.path.join(OUTPUT_BASE_FOLDER, mic)
        all_files = sorted(glob.glob(file_pattern))

        rate =1
        counter =1
        lastRms = 0
        for file in all_files:
            data = pd.read_csv(file,skiprows=1,names=['秒數', '波的大小'])

            # Apply custom adjustment based on RMS ratio
            #adjusted_data = adjust_data(data)
            if(counter%4 == 1 & counter != 1):
              nowRms=np.sqrt(np.mean(data['波的大小']**2))
              rate = rate*(lastRms/nowRms)
             
             
			  
            adjusted_data  = data*rate
            data_with_header = pd.DataFrame({'time': adjusted_data['秒數'], 'Amplitude': adjusted_data['波的大小']})
            
            # Generate output file name
            output_file = os.path.join(output_folder, os.path.basename(file))
            
            # Save the adjusted data
            data_with_header.to_csv(output_file, index=False, header=True)
            
            #print(f'Processed and saved: {output_file}')
            counter+=1
            lastRms = np.sqrt(np.mean(data['波的大小']**2))
            #print(rate)
            print('lastRms',lastRms)
