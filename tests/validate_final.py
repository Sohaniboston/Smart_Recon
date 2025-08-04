#!/usr/bin/env python3
"""
SmartRecon Final Validation Script

This script performs the final validation of SmartRecon by:
1. Testing all core modules can be imported
2. Running a complete reconciliation workflow
3. Validating outputs and performance
4. Generating a final validation report
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def print_status(message, status="INFO"):
    """Print formatted status message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbols = {
        "INFO": "🔍",
        "SUCCESS": "✅", 
        "ERROR": "❌",
        "WARNING": "⚠️",
        "STEP": "🎯"
    }
    symbol = status_symbols.get(status, "📋")
    print(f"[{timestamp}] {symbol} {message}")

def test_imports():
    """Test that all required modules can be imported."""
    print_status("Testing module imports...", "STEP")
    
    try:
        from src.config import Config
        print_status("Config module imported", "SUCCESS")
        
        from src.modules.data_ingestion import DataIngestion
        print_status("Data ingestion module imported", "SUCCESS")
        
        from src.modules.data_cleaning import DataCleaner
        print_status("Data cleaning module imported", "SUCCESS")
        
        from src.modules.exact_matching_engine import ExactMatchingEngine
        print_status("Exact matching engine imported", "SUCCESS")
        
        from src.modules.fuzzy_matching import FuzzyMatcher
        print_status("Fuzzy matching engine imported", "SUCCESS")
        
        from src.modules.exception_handler import ExceptionHandler
        print_status("Exception handler imported", "SUCCESS")
        
        from src.modules.basic_reporting import BasicReporter
        print_status("Reporting module imported", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Import failed: {e}", "ERROR")
        return False

def find_sample_files():
    """Find sample GL and bank data files."""
    print_status("Looking for sample data files...", "STEP")
    
    gl_dir = project_root / "gl_data"
    bank_dir = project_root / "bank_data"
    
    if not gl_dir.exists():
        print_status("GL data directory not found", "ERROR")
        return None, None
    
    if not bank_dir.exists():
        print_status("Bank data directory not found", "ERROR")
        return None, None
    
    gl_files = list(gl_dir.glob("*.csv"))
    bank_files = list(bank_dir.glob("*.csv"))
    
    if not gl_files:
        print_status("No GL data files found", "ERROR")
        return None, None
        
    if not bank_files:
        print_status("No bank data files found", "ERROR")
        return None, None
    
    # Use the most recent files
    gl_file = sorted(gl_files)[-1]
    bank_file = sorted(bank_files)[-1]
    
    print_status(f"Using GL file: {gl_file.name}", "SUCCESS")
    print_status(f"Using Bank file: {bank_file.name}", "SUCCESS")
    
    return gl_file, bank_file

def run_reconciliation_test(gl_file, bank_file):
    """Run a complete reconciliation test."""
    print_status("Starting reconciliation test...", "STEP")
    
    try:
        # Import required modules
        from src.config import Config
        from src.modules.data_ingestion import DataIngestion
        from src.modules.data_cleaning import DataCleaner
        from src.modules.exact_matching_engine import ExactMatchingEngine
        from src.modules.fuzzy_matching import FuzzyMatcher
        from src.modules.exception_handler import ExceptionHandler
        
        # Initialize components
        print_status("Initializing components...", "INFO")
        config = Config()
        ingestion = DataIngestion(config)
        cleaner = DataCleaner(config)
        exact_engine = ExactMatchingEngine(config)
        fuzzy_engine = FuzzyMatcher(config)
        exception_handler = ExceptionHandler(config)
        
        # Step 1: Load data
        print_status("Loading GL data...", "INFO")
        start_time = time.time()
        gl_result = ingestion.load_file(str(gl_file), file_type='gl')
        gl_data = gl_result['data']
        print_status(f"Loaded {len(gl_data)} GL records", "SUCCESS")
        
        print_status("Loading bank data...", "INFO")
        bank_result = ingestion.load_file(str(bank_file), file_type='bank')
        bank_data = bank_result['data']
        print_status(f"Loaded {len(bank_data)} bank records", "SUCCESS")
        
        # Step 2: Clean data
        print_status("Cleaning GL data...", "INFO")
        gl_clean_result = cleaner.clean_data(gl_data, data_type='gl')
        gl_clean = gl_clean_result['cleaned_data']
        
        print_status("Cleaning bank data...", "INFO")
        bank_clean_result = cleaner.clean_data(bank_data, data_type='bank')
        bank_clean = bank_clean_result['cleaned_data']
        
        print_status(f"Cleaned data: GL={len(gl_clean)}, Bank={len(bank_clean)}", "SUCCESS")
        
        # Step 3: Exact matching
        print_status("Running exact matching...", "INFO")
        exact_results = exact_engine.reconcile_exact_matches(gl_clean, bank_clean)
        exact_matches = exact_engine.export_matches_to_dataframe()
        unmatched = exact_engine.get_unmatched_records()
        
        print_status(f"Exact matches found: {len(exact_matches)}", "SUCCESS")
        print_status(f"Unmatched GL: {len(unmatched['gl'])}, Bank: {len(unmatched['bank'])}", "INFO")
        
        # Step 4: Fuzzy matching
        print_status("Running fuzzy matching...", "INFO")
        fuzzy_results = fuzzy_engine.find_fuzzy_matches(unmatched['gl'], unmatched['bank'])
        fuzzy_matches = fuzzy_engine.export_matches_to_dataframe()
        
        print_status(f"Fuzzy matches found: {len(fuzzy_matches)}", "SUCCESS")
        
        # Step 5: Exception handling
        print_status("Processing exceptions...", "INFO")
        remaining_unmatched = fuzzy_engine.get_unmatched_records(unmatched['gl'], unmatched['bank'])
        exception_results = exception_handler.process_exceptions(
            remaining_unmatched['gl'], remaining_unmatched['bank'], 'gl', 'bank'
        )
        
        total_exceptions = exception_results['statistics'].get('total_exceptions', 0)
        print_status(f"Exceptions processed: {total_exceptions}", "SUCCESS")
        
        # Calculate performance metrics
        total_time = time.time() - start_time
        total_records = len(gl_data) + len(bank_data)
        
        print_status(f"Processing completed in {total_time:.2f} seconds", "SUCCESS")
        print_status(f"Performance: {total_records/total_time:.1f} records/second", "SUCCESS")
        
        # Create output directory and save results
        output_dir = project_root / "validation_output"
        output_dir.mkdir(exist_ok=True)
        
        # Save exact matches
        if not exact_matches.empty:
            exact_path = output_dir / "exact_matches.xlsx"
            exact_matches.to_excel(str(exact_path), index=False)
            print_status(f"Exact matches saved: {exact_path}", "SUCCESS")
        
        # Save fuzzy matches
        if not fuzzy_matches.empty:
            fuzzy_path = output_dir / "fuzzy_matches.xlsx"
            fuzzy_matches.to_excel(str(fuzzy_path), index=False)
            print_status(f"Fuzzy matches saved: {fuzzy_path}", "SUCCESS")
        
        # Generate validation report
        report = {
            "validation_time": datetime.now().isoformat(),
            "total_processing_time": total_time,
            "gl_records": len(gl_data),
            "bank_records": len(bank_data),
            "exact_matches": len(exact_matches),
            "fuzzy_matches": len(fuzzy_matches),
            "total_exceptions": total_exceptions,
            "performance_records_per_second": total_records/total_time,
            "validation_status": "SUCCESS"
        }
        
        return report
        
    except Exception as e:
        print_status(f"Reconciliation test failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main validation function."""
    print_status("Starting SmartRecon Final Validation", "STEP")
    print("=" * 60)
    
    # Test 1: Module imports
    if not test_imports():
        print_status("Validation FAILED - Import issues", "ERROR")
        return False
    
    # Test 2: Find sample files
    gl_file, bank_file = find_sample_files()
    if not gl_file or not bank_file:
        print_status("Validation FAILED - No sample data", "ERROR")
        return False
    
    # Test 3: Run reconciliation
    report = run_reconciliation_test(gl_file, bank_file)
    if not report:
        print_status("Validation FAILED - Reconciliation error", "ERROR")
        return False
    
    # Final validation summary
    print("\n" + "=" * 60)
    print_status("SMARTRECON VALIDATION COMPLETE!", "SUCCESS")
    print("=" * 60)
    
    print(f"\n📊 VALIDATION RESULTS:")
    print(f"   GL Records Processed: {report['gl_records']}")
    print(f"   Bank Records Processed: {report['bank_records']}")
    print(f"   Exact Matches Found: {report['exact_matches']}")
    print(f"   Fuzzy Matches Found: {report['fuzzy_matches']}")
    print(f"   Exceptions Processed: {report['total_exceptions']}")
    print(f"   Processing Time: {report['total_processing_time']:.2f} seconds")
    print(f"   Performance: {report['performance_records_per_second']:.1f} records/sec")
    
    print(f"\n🎯 VALIDATION STATUS: {report['validation_status']}")
    print(f"🏆 SmartRecon v1.0 MVP is COMPLETE and OPERATIONAL!")
    print(f"📁 Results saved in: validation_output/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Final validation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Final validation failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation script error: {e}")
        sys.exit(1)
