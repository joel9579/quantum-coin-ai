import os
import pandas as pd
from src.data_pipeline.clean_raw_data import clean_combined_data

def test_clean_data_output():
    cleaned_file = "data/processed/combined_dataset.feather"
    assert os.path.exists(cleaned_file), "Cleaned data file does not exist."

    df = pd.read_feather(cleaned_file)
    assert not df.empty, "Cleaned dataframe is empty."
    assert 'date' in df.columns and 'close' in df.columns, "Missing required columns."

    # Check for nulls
    assert df.isnull().sum().sum() == 0, "Data still contains nulls."
