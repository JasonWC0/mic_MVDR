import os
import shutil

def copy_and_rename_csv_files(src_folder, dest_folder, start_index, end_index,output_filename_template):
	# 如果目標資料夾存在，則先刪除它
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 獲取來源資料夾中的所有檔案名稱，並進行排序以確保順序一致
    files = sorted([f for f in os.listdir(src_folder) if f.endswith('.csv')])

    # 確認 start_index 和 end_index 在有效範圍內
    if start_index < 1 or end_index > len(files) or start_index > end_index:
        print("Invalid index range.")
        return

    # 複製並重新命名指定範圍的檔案到目標資料夾
    for i in range(start_index - 1, end_index):
        src_path = os.path.join(src_folder, files[i])
        #new_filename = f"wear{i+1}-1_timeDM.csv"  # 根據範例格式命名
        new_filename = output_filename_template.format(i+1)
        dest_path = os.path.join(dest_folder, new_filename)
        shutil.copy(src_path, dest_path)
        print(f"Copied and renamed {files[i]} to {new_filename} in {dest_folder}")

# 使用範例
source_folder = './MVDR_TDM1'
destination_folder = './WEAR_OUT_POSITIVE/'
start_index = 15  # 起始檔案的索引，從1開始
end_index = 18    # 結束檔案的索引，包含這一個
output_filename_template='wear{}-1_timeDM1.csv'
copy_and_rename_csv_files(source_folder, destination_folder, start_index, end_index,output_filename_template)
