import pandas as pd
import numpy as np
import os

# Define the pattern for your input file
INPUT_EXCEL_PATTERN = "micAll_wear{}_filtered_{}s.csv"
FIRST_EXCEL = "micAll_wear1_filtered_1s.csv"

# Iterate over i from 1 to 2 (adjust the range as needed)
for i in range(5, 6):
    DATA_FOLDER = f"./MVDR_TDM{i}/"
    OUTPUT_BASE_FOLDER = f"./MVDR_TDM_ADJESTED_{i}/"

    # Ensure the output folders exist
    output_folder = os.path.join(OUTPUT_BASE_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

    counter = 1
    first_data = pd.read_csv(
        os.path.join(DATA_FOLDER, FIRST_EXCEL),
        header=None,
        names=["Time", "Amplitude"],
        skiprows=1,
    )
    rms1 = np.sqrt(np.mean(first_data["Amplitude"] ** 2))
    DATA_LENGTH = 20
    SECEOND_LENGTH = 17
    for j in range(1, DATA_LENGTH + 1):
        for k in range(1, SECEOND_LENGTH + 1):
            print(f"Processing i={i}, j={j}")

            # Manually create the file path using the pattern
            file_path = os.path.join(DATA_FOLDER, INPUT_EXCEL_PATTERN.format(j, k))

            # Read and calculate RMS for mic1 current file
            data1 = pd.read_csv(
                file_path, header=None, names=["Time", "Amplitude"], skiprows=1
            )

            # Calculate RMS of the first waveform
            # if counter == 1:
            #     rms1 = np.sqrt(np.mean(data1["Amplitude"] ** 2))

            # Normalize the amplitude using rms1
            data1["Amplitude"] = data1["Amplitude"] / rms1

            # Save the normalized data
            output_file_name = os.path.basename(file_path)
            output_file_path = os.path.join(output_folder, output_file_name)
            data1.to_csv(output_file_path, index=False, header=True)

            counter += 1
            print("rms1", rms1)
