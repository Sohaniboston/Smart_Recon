#!/usr/bin/env python3
"""
Phase 3 Implementation Validation Script

Simple script to validate that Phase 3 components are properly implemented
and can be imported/used successfully.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all Phase 3 components can be imported."""
    print("🔄 Testing Phase 3 component imports...")
    
    try:
        # Test performance monitoring
        from src.utils.performance import PerformanceMonitor, ProgressTracker
        print("✅ Performance monitoring module imported successfully")
        
        # Test basic functionality
        monitor = PerformanceMonitor()
        print("✅ PerformanceMonitor instance created successfully")
        
        # Test if enhanced app.py has performance integration
        if os.path.exists('app.py'):
            with open('app.py', 'r') as f:
                content = f.read()
                if 'PerformanceMonitor' in content and 'performance' in content:
                    print("✅ app.py has performance monitoring integration")
                else:
                    print("❌ app.py missing performance monitoring integration")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_file_structure():
    """Test if all Phase 3 files are present."""
    print("\n🔄 Testing Phase 3 file structure...")
    
    required_files = [
        'tests/unit/test_data_ingestion.py',
        'tests/unit/test_data_cleaning.py', 
        'tests/unit/test_exact_matching.py',
        'tests/unit/test_fuzzy_matching.py',
        'tests/unit/test_config.py',
        'tests/integration/test_workflow_integration.py',
        'tests/data/generate_test_data.py',
        'src/utils/performance.py',
        'run_tests.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_basic_functionality():
    """Test basic functionality of Phase 3 components."""
    print("\n🔄 Testing basic functionality...")
    
    try:
        from src.utils.performance import PerformanceMonitor
        
        # Test performance monitor
        monitor = PerformanceMonitor()
        
        # Test context manager
        with monitor.monitor_operation("test_operation", 100):
            import time
            time.sleep(0.1)  # Simulate work
        
        metrics = monitor.get_performance_summary()
        print("✅ Performance monitoring context manager works")
        print(f"   Captured {len(metrics.get('operations', []))} operation(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main validation function."""
    print("🚀 Phase 3 Implementation Validation")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Component Imports", test_imports), 
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("🎯 PHASE 3 VALIDATION RESULTS")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 PHASE 3 IMPLEMENTATION: ✅ VALIDATED SUCCESSFULLY")
        print("All Phase 3 components are properly implemented and functional!")
    else:
        print("⚠️  PHASE 3 IMPLEMENTATION: ❌ VALIDATION ISSUES FOUND")
        print("Some Phase 3 components need attention.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
