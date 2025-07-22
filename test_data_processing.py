#!/usr/bin/env python3
"""
Direct test of data processing fixes
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config import Config
    from modules.data_cleaning import DataCleaner
    
    print("Loading test data...")
    # Load the sample CSV file we saw earlier
    df = pd.read_csv("bank_data/20250612_135232_bank_data.csv")
    print(f"Loaded {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    print("\nInitializing DataCleaner...")
    config = Config()
    cleaner = DataCleaner(config)
    
    print("\nProcessing data...")
    result = cleaner.clean_data(df)
    
    print(f"\n=== RESULTS ===")
    print(f"Original records: {result['original_records']}")
    print(f"Final records: {result['final_records']}")
    print(f"Data quality score: {result['data_quality_score']}")
    print(f"Operations performed: {len(result['operations_performed'])}")
    
    for op in result['operations_performed']:
        print(f"  - {op}")
    
    print(f"\n=== CLEANED DATA SAMPLE ===")
    cleaned_df = result['cleaned_data']
    print(cleaned_df.head(3).to_string(index=False))
    
    print(f"\n=== COLUMN TYPES ===")
    for col in cleaned_df.columns:
        print(f"  {col}: {cleaned_df[col].dtype}")
    
    print(f"\n[SUCCESS] Data processing completed successfully!")
    
except Exception as e:
    import traceback
    print(f"[ERROR] {e}")
    traceback.print_exc()
