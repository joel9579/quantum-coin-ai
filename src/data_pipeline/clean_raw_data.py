import os
import pandas as pd

UNPACKED_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\unpacked"
PROCESSED_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\processed"

def clean_dataframe(df):
    # Standardize column names
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    
    # Convert date columns
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows with null dates
    df = df.dropna(subset=['date']) if 'date' in df.columns else df

    # Sort by date if available
    if 'date' in df.columns:
        df = df.sort_values(by='date')

    # Fill or drop missing values
    df = df.fillna(method='ffill').fillna(method='bfill')

    return df

def clean_all_csvs(unpacked_dir=UNPACKED_DIR, processed_dir=PROCESSED_DIR):
    os.makedirs(processed_dir, exist_ok=True)

    for file_name in os.listdir(unpacked_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(unpacked_dir, file_name)
            print(f"Cleaning: {file_name}")

            df = pd.read_csv(file_path)
            cleaned_df = clean_dataframe(df)

            base_name = os.path.splitext(file_name)[0].lower()
            out_path = os.path.join(processed_dir, f"{base_name}.parquet")
            cleaned_df.to_parquet(out_path, index=False)
    
    print(f"Cleaned files saved to: {processed_dir}")

if __name__ == "__main__":
    clean_all_csvs()