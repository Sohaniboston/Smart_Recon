#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from modules.data_cleaning import DataCleaner
import pandas as pd

# Load test data
df = pd.read_csv("bank_data/20250612_135232_bank_data.csv")
print("Original data:")
print(df.head())
print(f"Original columns: {list(df.columns)}")
print(f"Original dtypes:\n{df.dtypes}")

# Process with DataCleaner
config = Config()
cleaner = DataCleaner(config)
result = cleaner.clean_data(df)

print(f"\n=== PROCESSING RESULTS ===")
print(f"Operations performed: {result['operations_performed']}")

cleaned_df = result['cleaned_data']
print(f"\nCleaned data:")
print(cleaned_df.head())
print(f"Cleaned columns: {list(cleaned_df.columns)}")
print(f"Cleaned dtypes:\n{cleaned_df.dtypes}")

# Check if numeric columns are still numeric
print(f"\nColumn analysis:")
for col in cleaned_df.columns:
    sample_val = cleaned_df[col].iloc[0]
    print(f"  {col}: {type(sample_val)} = {sample_val}")

print(f"\n[SUCCESS] Data processing test completed!")
