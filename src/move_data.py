import os
import shutil

def copy_and_rename_csv_files(src_folder, dest_folder, start_index, end_index, input_filename_template, output_filename_template):
    # 如果目標資料夾不存在，則建立它
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 確認 start_index 和 end_index 在有效範圍內
    if start_index < 1 or end_index < start_index:
        print("Invalid index range.")
        return

    # 複製並重新命名指定範圍的檔案到目標資料夾
    for i in range(start_index, end_index + 1):
        input_filename = input_filename_template.format(i)
        src_path = os.path.join(src_folder, input_filename)
        if not os.path.exists(src_path):
            print(f"File {input_filename} does not exist. Skipping.")
            continue
        new_filename = output_filename_template.format(i)
        dest_path = os.path.join(dest_folder, new_filename)
        shutil.copy(src_path, dest_path)
        print(f"Copied and renamed {input_filename} to {new_filename} in {dest_folder}")

# 使用範例
source_folder = './PREPROCESSED_TDM_ANGLE_30_STEP01_1/mic1'
destination_folder = './WEAR_OUT_NEGATIVE_30deg/'
start_index = 1  # 起始檔案的索引，從1開始
end_index = 4    # 結束檔案的索引，包含這一個
input_filename_template = 'wear{}-1_timeDM.csv'
output_filename_template = 'wear{}-1_timeDM1.csv'
copy_and_rename_csv_files(source_folder, destination_folder, start_index, end_index, input_filename_template, output_filename_template)