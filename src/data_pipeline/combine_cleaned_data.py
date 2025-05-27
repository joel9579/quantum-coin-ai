import os
import pandas as pd

PROCESSED_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\processed"
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "combined_dataset.feather")

def combine_parquet_files(processed_dir=PROCESSED_DIR, output_file=OUTPUT_FILE):
    combined_data = []

    for file_name in os.listdir(processed_dir):
        if file_name.endswith(".parquet") and "combined_dataset" not in file_name:
            file_path = os.path.join(processed_dir, file_name)
            df = pd.read_parquet(file_path)

            # Extract coin name from file name, e.g., 'coin_bitcoin'
            coin_name = file_name.replace(".parquet", "").replace("cleaned_", "")
            df['coin'] = coin_name

            combined_data.append(df)

    if combined_data:
        full_df = pd.concat(combined_data, ignore_index=True)
        full_df.to_feather(output_file)
        print(f"Combined dataset saved to: {output_file}")
    else:
        print("No valid parquet files found for combining.")

if __name__ == "__main__":
    combine_parquet_files()