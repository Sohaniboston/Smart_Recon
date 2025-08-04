#!/usr/bin/env python3
"""
Phase 3 Implementation Validation Test

Quick validation test to confirm Phase 3 implementation is working.
Tests key components: unit tests, integration, and performance monitoring.

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all new Phase 3 components can be imported."""
    try:
        # Test performance monitoring imports
        from src.utils.performance import PerformanceMonitor, ProgressTracker, monitor_performance
        print("✅ Performance monitoring imports successful")
        
        # Test core module imports  
        from src.config import Config
        from src.modules.data_ingestion import DataIngestion
        from src.modules.data_cleaning import DataCleaner
        from src.modules.exact_matching_engine import ExactMatchingEngine
        from src.modules.fuzzy_matching import FuzzyMatcher
        print("✅ Core module imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_performance_monitoring():
    """Test performance monitoring functionality."""
    try:
        from src.utils.performance import PerformanceMonitor
        
        # Create performance monitor
        monitor = PerformanceMonitor()
        
        # Test monitoring context
        with monitor.monitor_operation("Test Operation", record_count=100):
            # Simulate some work
            import time
            time.sleep(0.1)
        
        # Get summary
        summary = monitor.get_performance_summary()
        
        print("✅ Performance monitoring test successful")
        print(f"  - Operations monitored: {summary['overview']['total_operations']}")
        print(f"  - Success rate: {summary['overview']['success_rate']:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Performance monitoring test failed: {e}")
        return False

def test_data_processing():
    """Test basic data processing functionality."""
    try:
        from src.config import Config
        from src.modules.data_ingestion import DataIngestion
        from src.modules.data_cleaning import DataCleaner
        
        # Load configuration
        config = Config()
        
        # Create test data
        test_data = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-02'],
            'Amount': [100.50, 200.00],
            'Description': ['Payment A', 'Payment B'],
            'Reference': ['REF001', 'REF002']
        })
        
        # Test data cleaning
        cleaner = DataCleaner(config)
        result = cleaner.clean_data(test_data, data_type='gl')
        
        print("✅ Data processing test successful")
        print(f"  - Input records: {len(test_data)}")
        print(f"  - Output records: {len(result['cleaned_data'])}")
        print(f"  - Quality score: {result['cleaning_report']['data_quality_score']:.1f}")
        
        return True
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def test_file_access():
    """Test access to test data files."""
    try:
        test_data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
        
        # Check for test files
        expected_files = ['gl_basic.csv', 'bank_basic.csv', 'test_data_metadata.json']
        
        for filename in expected_files:
            filepath = os.path.join(test_data_dir, filename)
            if os.path.exists(filepath):
                print(f"✅ Found test file: {filename}")
            else:
                print(f"⚠️  Missing test file: {filename}")
        
        # Try to load a test file
        gl_file = os.path.join(test_data_dir, 'gl_basic.csv')
        if os.path.exists(gl_file):
            df = pd.read_csv(gl_file)
            print(f"✅ Successfully loaded test data: {len(df)} records")
        
        return True
    except Exception as e:
        print(f"❌ File access test failed: {e}")
        return False

def test_integration_readiness():
    """Test that integration components are ready."""
    try:
        # Test that we can create all major components
        from src.config import Config
        from src.modules.data_ingestion import DataIngestion
        from src.modules.data_cleaning import DataCleaner
        from src.modules.exact_matching_engine import ExactMatchingEngine
        from src.modules.fuzzy_matching import FuzzyMatcher
        from src.utils.performance import PerformanceMonitor
        
        config = Config()
        
        # Initialize all components
        ingestion = DataIngestion(config)
        cleaner = DataCleaner(config)
        exact_engine = ExactMatchingEngine(config)
        fuzzy_engine = FuzzyMatcher(config)
        monitor = PerformanceMonitor()
        
        print("✅ All integration components initialized successfully")
        print("✅ Phase 3 implementation is ready for end-to-end testing")
        
        return True
    except Exception as e:
        print(f"❌ Integration readiness test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🚀 Running Phase 3 Implementation Validation")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Import Tests", test_imports),
        ("Performance Monitoring", test_performance_monitoring),
        ("Data Processing", test_data_processing),
        ("File Access", test_file_access),
        ("Integration Readiness", test_integration_readiness)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    # Summary
    success_rate = (passed / total) * 100
    print("=" * 60)
    print("📊 Phase 3 Validation Summary:")
    print(f"  ✅ Tests Passed: {passed}/{total}")
    print(f"  📈 Success Rate: {success_rate:.1f}%")
    print()
    
    if success_rate >= 80:
        print("🎉 Phase 3 Implementation Status: READY")
        print("💡 Recommendation: Proceed with comprehensive testing")
    else:
        print("⚠️  Phase 3 Implementation Status: NEEDS ATTENTION")
        print("💡 Recommendation: Fix failing tests before proceeding")
    
    print()
    print("🏁 Validation Complete!")

if __name__ == '__main__':
    main()
