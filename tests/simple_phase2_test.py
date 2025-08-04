#!/usr/bin/env python3
"""
Simple Phase 2 Test Script
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=== SmartRecon Phase 2 Test ===")
    
    # Test 1: Basic imports
    try:
        from config import Config
        from modules.fuzzy_matching import FuzzyMatcher
        from modules.exception_handler import ExceptionHandler
        from modules.exact_matching_engine import ExactMatchingEngine
        print("✅ All modules imported successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Dependencies
    try:
        import fuzzywuzzy
        import jellyfish
        print("✅ Fuzzy matching dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    # Test 3: Basic fuzzy matching
    try:
        import pandas as pd
        config = Config()
        fuzzy_matcher = FuzzyMatcher(config)
        
        # Simple test data
        gl_data = pd.DataFrame({'description': ['Test payment'], 'debit': [100.0]})
        bank_data = pd.DataFrame({'description': ['Test Payment'], 'withdrawal': [100.0]})
        
        result = fuzzy_matcher.find_fuzzy_matches(gl_data, bank_data)
        print(f"✅ Fuzzy matching test completed - {len(fuzzy_matcher.fuzzy_matches)} matches found")
    except Exception as e:
        print(f"❌ Fuzzy matching test failed: {e}")
        return False
    
    print("🎉 Phase 2 tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
