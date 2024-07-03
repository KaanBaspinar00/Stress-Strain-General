import os
import shutil

# Directories

# If all csv file are in different folders as you send me, you can use this code to collect them all in 1 folder.
# Change base_dir directory with your general folder which contains all the folders (contains csv files) you have

base_dir = r'C:\Users\baspi\OneDrive\Masaüstü\29062024 (1)\29062024'
destination_dir = r'C:\Users\baspi\OneDrive\Masaüstü\29062024 (1)\29062024\DATA99'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Iterate through each folder in the base directory
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)

    if os.path.isdir(folder_path):
        # Find the CSV file in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                old_file_path = os.path.join(folder_path, file_name)
                folder_name = folder_name.replace(".","")
                new_file_name = f"{folder_name}.csv"

                new_file_path = os.path.join(destination_dir, new_file_name)

                # Copy and rename the CSV file
                shutil.copy2(old_file_path, new_file_path)
                print(f"Copied and renamed: {old_file_path} -> {new_file_path}")

print("All files have been processed.")
