import pandas as pd
import numpy as np
import glob
import os

# mic-準位均化
# Iterate over i from 1 to 4
for i in range(1, 5):
	DATA_FOLDER = f'./TDM{i}/'
	OUTPUT_BASE_FOLDER = f'./MIC_RMS_PREPROCESSED_TDM{i}/'
	
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

	# Read and process each mic file
	for mic, file_pattern in mic_patterns.items():
		output_folder = os.path.join(OUTPUT_BASE_FOLDER, mic)
		all_files = sorted(glob.glob(file_pattern))

		for file in all_files:
			data = pd.read_csv(file, header=None, names=['秒數', '波的大小'])
			
			# Calculate RMS value
			rms_value = np.sqrt(np.mean(data['波的大小']**2))
			
			# Normalize the data
			data['波的大小'] = data['波的大小'] / rms_value

			data_with_header = pd.DataFrame({'time': data['秒數'], 'Amplitude': data['波的大小']})

			
			# Generate output file name
			output_file = os.path.join(output_folder, os.path.basename(file))
			
			# Save the normalized data
			data_with_header.to_csv(output_file, index=False, header=True)

			print(f'Processed and saved: {output_file}')
