#!/usr/bin/env python3
"""
Test script to check SmartRecon imports
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all module imports."""
    print("Testing SmartRecon module imports...")
    
    try:
        print("1. Testing config import...")
        from src.config import Config
        print("   ✅ Config imported successfully")
    except Exception as e:
        print(f"   ❌ Config import failed: {e}")
        return False
    
    try:
        print("2. Testing data_ingestion import...")
        from src.modules.data_ingestion import DataIngestion
        print("   ✅ DataIngestion imported successfully")
    except Exception as e:
        print(f"   ❌ DataIngestion import failed: {e}")
        return False
    
    try:
        print("3. Testing data_cleaning import...")
        from src.modules.data_cleaning import DataCleaner
        print("   ✅ DataCleaner imported successfully")
    except Exception as e:
        print(f"   ❌ DataCleaner import failed: {e}")
        return False
    
    try:
        print("4. Testing exact_matching_engine import...")
        from src.modules.exact_matching_engine import ExactMatchingEngine
        print("   ✅ ExactMatchingEngine imported successfully")
    except Exception as e:
        print(f"   ❌ ExactMatchingEngine import failed: {e}")
        return False
    
    try:
        print("5. Testing basic_reporting import...")
        from src.modules.basic_reporting import BasicReporter
        print("   ✅ BasicReporter imported successfully")
    except Exception as e:
        print(f"   ❌ BasicReporter import failed: {e}")
        return False
    
    try:
        print("6. Testing utils imports...")
        from src.utils.logger import setup_logger
        from src.utils.exceptions import SmartReconException
        print("   ✅ Utils imported successfully")
    except Exception as e:
        print(f"   ❌ Utils import failed: {e}")
        return False
    
    print("\n🎉 All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nSmartRecon is ready to use!")
        sys.exit(0)
    else:
        print("\nPlease fix import errors before using SmartRecon.")
        sys.exit(1)
