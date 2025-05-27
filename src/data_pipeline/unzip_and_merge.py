import os
import zipfile

RAW_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\raw"
UNPACKED_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\unpacked"

def unzip_all_archives(raw_dir=RAW_DIR, unpacked_dir=UNPACKED_DIR):
    os.makedirs(unpacked_dir, exist_ok=True)
    
    for file_name in os.listdir(raw_dir):
        if file_name.endswith(".zip"):
            file_path = os.path.join(raw_dir, file_name)
            print(f"Unzipping: {file_name}")

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(unpacked_dir)
    
    print(f"All files extracted to: {unpacked_dir}")

if __name__ == "__main__":
    unzip_all_archives()
