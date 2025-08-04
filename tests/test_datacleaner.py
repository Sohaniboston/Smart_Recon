#!/usr/bin/env python3
"""
Test DataCleaner import specifically
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing DataCleaner import...")
    from modules.data_cleaning import DataCleaner
    print("[SUCCESS] DataCleaner imported successfully")
    
    # Try creating an instance
    config = {'test': True}
    cleaner = DataCleaner(config)
    print("[SUCCESS] DataCleaner instance created")
    
    # Test basic functionality
    import pandas as pd
    df = pd.DataFrame({'test_col': [1, 2, 3]})
    result = cleaner.clean_data(df)
    print("[SUCCESS] DataCleaner.clean_data() worked")
    print(f"Result keys: {list(result.keys())}")
    
except Exception as e:
    import traceback
    print(f"[ERROR] Error: {e}")
    print("Full traceback:")
    traceback.print_exc()
