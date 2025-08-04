#!/usr/bin/env python3
"""
SmartRecon Quick Start Script

This script provides an easy way to run SmartRecon with your data.
It handles environment setup, data validation, and execution.

Usage:
    python run_smartrecon.py                    # Interactive mode
    python run_smartrecon.py -    while True:
        print("\n🚀 Available options:")
        print("1. � List the available data files")
        print("2. 📊 Process bank data")
        print("3. � Generate sample data")
        print("4. � Check environment")
        print("5. 🧪 Test basic functionality")
        print("6. 🔬 Run simple test")
        print("7. 🔍 Test fuzzy matching")
        print("8. 🎯 Run full reconciliation")
        print("0. 👋 Exit")        # Auto mode with default files
    python run_smartrecon.py --help             # Show help
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def print_banner():
    """Print SmartRecon banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    🎯 SMARTRECON v1.0                        ║
║           Intelligent Financial Reconciliation Assistant     ║
║                                                               ║
║   Ready to process your financial data with AI precision!    ║
╚═══════════════════════════════════════════════════════════════╝
    """)

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking environment setup...")
    
    # Check if we're in the right directory
    if not (project_root / "src").exists():
        print("❌ Error: src/ directory not found. Please run from project root.")
        return False
    
    # Check if required modules exist
    required_modules = [
        "src/config.py",
        "src/modules/data_ingestion.py", 
        "src/modules/data_cleaning.py"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not (project_root / module).exists():
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {missing_modules}")
        return False
    
    print("✅ Environment check passed!")
    return True

def check_data_files():
    """Check for available data files."""
    print("📁 Checking for data files...")
    
    # Look for bank data
    bank_data_dir = project_root / "bank_data"
    gl_data_dir = project_root / "GL_data"
    
    bank_files = []
    gl_files = []
    
    if bank_data_dir.exists():
        bank_files = list(bank_data_dir.glob("*.csv"))
        print(f"   Found {len(bank_files)} bank data files in bank_data/")
        for f in bank_files:
            print(f"     📄 {f.name}")
    else:
        print("   📁 bank_data/ directory not found")
    
    if gl_data_dir.exists():
        gl_files = list(gl_data_dir.glob("*.csv"))
        print(f"   Found {len(gl_files)} GL data files in GL_data/")
        for f in gl_files:
            print(f"     📄 {f.name}")
    else:
        print("   📁 GL_data/ directory not found")
    
    return bank_files, gl_files

def test_basic_functionality():
    """Test basic SmartRecon functionality."""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test imports
        # Import modules from src path
        sys.path.insert(0, str(src_path))
        from src.config import Config
        from src.modules.data_cleaning import DataCleaner
        from src.modules.data_ingestion import DataIngestion
        
        print("✅ Core modules imported successfully")
        
        # Test basic initialization
        config = Config()
        cleaner = DataCleaner(config)
        ingestion = DataIngestion(config)
        
        print("✅ Core components initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def run_with_bank_data(bank_file=None):
    """Run SmartRecon with bank data."""
    if bank_file is None:
        bank_files, _ = check_data_files()
        if not bank_files:
            print("❌ No bank data files found in bank_data/ directory")
            return False
        bank_file = bank_files[0]
    
    print(f"📊 Processing bank data: {bank_file.name}")
    
    try:
        # Import and run basic cleaning
        from src.config import Config
        from src.modules.data_cleaning import DataCleaner
        import pandas as pd
        
        # Load and process data
        print("🔄 Loading and processing data...")
        config = Config()
        cleaner = DataCleaner(config)
        
        # Load bank data
        df = pd.read_csv(bank_file)
        print(f"   📥 Loaded {len(df)} records from {bank_file.name}")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Clean data
        result = cleaner.clean_data(df)
        
        print("\n✅ Data processing completed!")
        
        # Check which keys are available in the result
        available_keys = list(result.keys())
        print(f"   🔧 Result keys available: {available_keys}")
        
        # Use safe key access with defaults
        original_records = result.get('original_records', len(df))
        final_records = result.get('final_records', len(result.get('cleaned_data', df)))
        data_quality_score = result.get('data_quality_score', 0.0)
        operations_performed = result.get('operations_performed', [])
        
        print(f"   📊 Records processed: {original_records} → {final_records}")
        print(f"   🎯 Data quality score: {data_quality_score:.3f}")
        print(f"   ⚙️  Operations performed: {len(operations_performed)}")
        
        for operation in operations_performed:
            print(f"     ✓ {operation}")
        
        # Show sample of cleaned data
        cleaned_df = result.get('cleaned_data', df)
        if cleaned_df is not None and not cleaned_df.empty:
            print(f"\n📋 Sample of cleaned data:")
            print(cleaned_df.head(3).to_string(index=False))
        else:
            print("\n⚠️  No cleaned data available to display")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_sample_data():
    """Generate sample data using existing script."""
    print("📈 Generating sample data...")
    
    try:
        # Check if generator script exists
        generator_script = project_root / "generate_financial_data.py"
        if generator_script.exists():
            print("🔄 Running data generator...")
            result = subprocess.run([sys.executable, str(generator_script)], 
                                 capture_output=True, text=True, cwd=project_root)
            
            if result.returncode == 0:
                print("✅ Sample data generated successfully!")
                if result.stdout:
                    print(f"   📤 {result.stdout.strip()}")
                return True
            else:
                print(f"❌ Data generation failed: {result.stderr}")
                return False
        else:
            print("❌ Data generator script (generate_financial_data.py) not found")
            return False
            
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        return False

def run_simple_test():
    """Run a simple test of the current SmartRecon functionality."""
    print("🔬 Running simple SmartRecon test...")
    
    try:
        # Run our existing test
        result = subprocess.run([
            sys.executable, "test_datacleaner.py"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Simple test passed!")
            print(f"   📤 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Simple test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running simple test: {e}")
        return False

def test_fuzzy_matching():
    """Test fuzzy matching functionality with sample data."""
    print("🔍 Testing fuzzy matching functionality...")
    
    try:
        # Import fuzzy matching module
        from src.config import Config
        from src.modules.fuzzy_matching import FuzzyMatcher
        import pandas as pd
        
        print("✅ Fuzzy matching module imported successfully")
        
        # Create sample test data
        gl_data = pd.DataFrame({
            'description': ['Payment to ABC Corp', 'Salary deposit', 'Office supplies'],
            'debit': [1000.00, 0.00, 150.50],
            'credit': [0.00, 5000.00, 0.00],
            'transaction_date': pd.to_datetime(['2025-01-15', '2025-01-16', '2025-01-17'])
        })
        
        bank_data = pd.DataFrame({
            'description': ['Payment ABC Corporation', 'Salary Deposit - Company', 'Office Supply Store'],
            'deposit': [0.00, 5000.00, 0.00],
            'withdrawal': [1000.00, 0.00, 150.50],
            'date': pd.to_datetime(['2025-01-15', '2025-01-16', '2025-01-18'])
        })
        
        print("✅ Sample test data created")
        
        # Initialize fuzzy matcher
        config = Config()
        fuzzy_matcher = FuzzyMatcher(config)
        
        # Run fuzzy matching
        print("🔄 Running fuzzy matching test...")
        results = fuzzy_matcher.find_fuzzy_matches(gl_data, bank_data)
        
        # Display results
        fuzzy_matches = fuzzy_matcher.export_matches_to_dataframe()
        potential_matches = fuzzy_matcher.export_potential_matches_to_dataframe()
        
        print(f"\n📊 Fuzzy Matching Test Results:")
        print(f"   🎯 High-confidence matches: {len(fuzzy_matches)}")
        print(f"   ❓ Potential matches: {len(potential_matches)}")
        print(f"   📈 Processing time: {results['statistics']['processing_time_seconds']:.2f} seconds")
        
        if not fuzzy_matches.empty:
            print(f"\n✅ High-confidence matches found:")
            for _, match in fuzzy_matches.iterrows():
                print(f"   🔍 Confidence: {match['confidence']:.1f}% - GL: '{match['gl_description']}' → Bank: '{match['bank_description']}'")
        
        if not potential_matches.empty:
            print(f"\n❓ Potential matches requiring review:")
            for _, match in potential_matches.iterrows():
                print(f"   🔍 Confidence: {match['confidence']:.1f}% - GL: '{match['gl_description']}' → Bank: '{match['bank_description']}'")
        
        print("\n✅ Fuzzy matching test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Fuzzy matching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_full_reconciliation():
    """Run complete reconciliation with GL and bank data."""
    print("🎯 Starting Full Reconciliation...")
    
    try:
        # Check for available data files
        bank_files, gl_files = check_data_files()
        
        if not bank_files:
            print("❌ No bank data files found in bank_data/ directory")
            return False
            
        if not gl_files:
            print("❌ No GL data files found in gl_data/ directory")
            return False
        
        # Use first available files
        bank_file = bank_files[0]
        gl_file = gl_files[0]
        
        print(f"📊 Using GL file: {gl_file.name}")
        print(f"🏦 Using Bank file: {bank_file.name}")
        
        # Import required modules
        import subprocess
        
        # Run the full reconciliation using app.py
        print("🔄 Executing reconciliation workflow...")
        
        # Create output directory
        output_dir = project_root / "reconciliation_output"
        output_dir.mkdir(exist_ok=True)
        
        # Run the reconciliation command
        cmd = [
            sys.executable, "app.py", "reconcile",
            str(gl_file), str(bank_file),
            "--output-dir", str(output_dir),
            "--export-format", "all",
            "--match-strategy", "all"
        ]
        
        print(f"📋 Command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Reconciliation completed successfully!")
            print(f"📁 Results saved to: {output_dir}")
            if result.stdout:
                print(f"📤 Output:\n{result.stdout}")
            return True
        else:
            print(f"❌ Reconciliation failed: {result.stderr}")
            if result.stdout:
                print(f"📤 Output:\n{result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Reconciliation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_mode():
    """Run SmartRecon in interactive mode."""
    print("\n🎯 SmartRecon Interactive Mode")
    print("=" * 50)
    
    while True:
        print("\n🚀 Available options:")
        print("1. � List the available data files")
        print("2. 📊 Process bank data")
        print("3. � Generate sample data")
        print("4. � Check environment")
        print("5. 🧪 Test basic functionality")
        print("6. 🔬 Run simple test")
        print("7. 🔍 Test fuzzy matching")
        print("0. 👋 Exit")
        
        try:
            choice = input("\nEnter your choice (0-8): ").strip()
            
            if choice == "0":
                print("👋 Goodbye! Thanks for using SmartRecon!")
                break
            elif choice == "1":
                bank_files, gl_files = check_data_files()
                print(f"\n📊 Total files found: {len(bank_files + gl_files)}")
            elif choice == "2":
                run_with_bank_data()
            elif choice == "3":
                if generate_sample_data():
                    print("✅ Sample data ready! You can now try option 2.")
            elif choice == "4":
                check_environment()
            elif choice == "5":
                test_basic_functionality()
            elif choice == "6":
                run_simple_test()
            elif choice == "7":
                test_fuzzy_matching()
            elif choice == "8":
                run_full_reconciliation()
            else:
                print("❌ Invalid choice. Please enter 0-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def auto_mode():
    """Run SmartRecon in automatic mode."""
    print("\n🚀 SmartRecon Automatic Mode")
    print("=" * 50)
    
    # Run all checks and tests
    if not check_environment():
        print("❌ Environment check failed")
        return False
    
    if not test_basic_functionality():
        print("❌ Basic functionality test failed")
        return False
    
    print("✅ All system checks passed!")
    
    # Try to run with existing data
    bank_files, gl_files = check_data_files()
    
    if not bank_files:
        print("🔧 No data files found. Generating sample data...")
        if generate_sample_data():
            bank_files, gl_files = check_data_files()
        else:
            print("❌ Failed to generate sample data")
            return False
    
    if bank_files:
        print(f"🎯 Processing with {bank_files[0].name}...")
        return run_with_bank_data(bank_files[0])
    else:
        print("❌ No data files available for processing")
        return False

def main():
    """Main startup function."""
    parser = argparse.ArgumentParser(
        description="SmartRecon Quick Start Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_smartrecon.py                    # Interactive mode
    python run_smartrecon.py --auto             # Auto mode
    python run_smartrecon.py --test             # Test only
        """
    )
    
    parser.add_argument("--auto", action="store_true", 
                       help="Run in automatic mode")
    parser.add_argument("--test", action="store_true",
                       help="Run tests only")
    parser.add_argument("--generate", action="store_true",
                       help="Generate sample data only")
    
    args = parser.parse_args()
    
    # Always show banner
    print_banner()
    
    if args.test:
        # Test mode only
        success = check_environment() and test_basic_functionality()
        if success:
            success = run_simple_test()
        print(f"\n🎯 Test Results: {'✅ PASSED' if success else '❌ FAILED'}")
        sys.exit(0 if success else 1)
        
    elif args.generate:
        # Generate sample data only
        success = generate_sample_data()
        sys.exit(0 if success else 1)
        
    elif args.auto:
        # Auto mode
        success = auto_mode()
        print(f"\n🎯 Auto Mode Results: {'✅ SUCCESS' if success else '❌ FAILED'}")
        sys.exit(0 if success else 1)
    else:
        # Interactive mode (default)
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n👋 SmartRecon session ended. Goodbye!")

if __name__ == "__main__":
    main()
