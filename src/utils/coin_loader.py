import os

def get_available_coins(parquet_dir="data/processed"):
    coins = []
    for file in os.listdir(parquet_dir):
        if file.endswith(".parquet"):
            coin = file.replace(".parquet", "")
            coins.append(coin)
    return sorted(coins)
