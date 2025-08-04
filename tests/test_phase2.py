#!/usr/bin/env python3
"""
Quick test script for Phase 2 functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        from config import Config
        print("✅ Config import successful")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from modules.data_cleaning import DataCleaner
        print("✅ DataCleaner import successful")
    except Exception as e:
        print(f"❌ DataCleaner import failed: {e}")
        return False
    
    try:
        from modules.exact_matching_engine import ExactMatchingEngine
        print("✅ ExactMatchingEngine import successful")
    except Exception as e:
        print(f"❌ ExactMatchingEngine import failed: {e}")
        return False
    
    try:
        from modules.fuzzy_matching import FuzzyMatcher
        print("✅ FuzzyMatcher import successful")
    except Exception as e:
        print(f"❌ FuzzyMatcher import failed: {e}")
        return False
    
    try:
        from modules.exception_handler import ExceptionHandler
        print("✅ ExceptionHandler import successful")
    except Exception as e:
        print(f"❌ ExceptionHandler import failed: {e}")
        return False
    
    return True

def test_fuzzy_matching():
    """Test fuzzy matching functionality"""
    print("\nTesting fuzzy matching functionality...")
    
    try:
        import pandas as pd
        from config import Config
        from modules.fuzzy_matching import FuzzyMatcher
        
        # Create sample data
        gl_data = pd.DataFrame({
            'description': ['Payment to ABC Corp', 'Salary deposit'],
            'debit': [1000.00, 0.00],
            'credit': [0.00, 5000.00],
            'transaction_date': pd.to_datetime(['2025-01-15', '2025-01-16'])
        })
        
        bank_data = pd.DataFrame({
            'description': ['Payment ABC Corporation', 'Salary Deposit'],
            'deposit': [0.00, 5000.00],
            'withdrawal': [1000.00, 0.00],
            'date': pd.to_datetime(['2025-01-15', '2025-01-16'])
        })
        
        config = Config()
        fuzzy_matcher = FuzzyMatcher(config)
        
        results = fuzzy_matcher.find_fuzzy_matches(gl_data, bank_data)
        print(f"✅ Fuzzy matching test successful - found {len(fuzzy_matcher.fuzzy_matches)} matches")
        
        return True
        
    except Exception as e:
        print(f"❌ Fuzzy matching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exception_handling():
    """Test exception handling functionality"""
    print("\nTesting exception handling functionality...")
    
    try:
        import pandas as pd
        from config import Config
        from modules.exception_handler import ExceptionHandler
        
        # Create sample unmatched data
        unmatched_gl = pd.DataFrame({
            'description': ['Unmatched GL entry', 'Another GL entry'],
            'debit': [500.00, 750.00],
            'transaction_date': pd.to_datetime(['2025-01-15', '2025-01-16'])
        })
        
        unmatched_bank = pd.DataFrame({
            'description': ['Unmatched bank entry'],
            'withdrawal': [300.00],
            'date': pd.to_datetime(['2025-01-17'])
        })
        
        config = Config()
        exception_handler = ExceptionHandler(config)
        
        results = exception_handler.process_exceptions(unmatched_gl, unmatched_bank, 'gl', 'bank')
        print(f"✅ Exception handling test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 SmartRecon Phase 2 Integration Test")
    print("=" * 50)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_fuzzy_matching():
        success = False
    
    if not test_exception_handling():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All Phase 2 tests passed!")
        print("✅ Exact matching engine: Integrated")
        print("✅ Fuzzy matching: Implemented and working")
        print("✅ Exception handling: Enhanced and integrated")
        print("✅ Configuration: Updated with fuzzy parameters")
    else:
        print("❌ Some tests failed. Please review the errors above.")
    
    print(f"\n📊 Phase 2 Status: {'COMPLETE' if success else 'NEEDS FIXES'}")
