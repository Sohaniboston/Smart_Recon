#!/usr/bin/env python3
"""
SmartRecon Quick Start Script

This script provides an easy way to run SmartRecon with your data.
It handles environment setup, data validation, and execution.

Usage:
    python run_smartrecon.py                    # Interactive mode
    python run_smartrecon.py --auto             # Auto mode with default files
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
        from config import Config
        from modules.data_cleaning import DataCleaner
        from modules.data_ingestion import DataIngestion
        
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
        from config import Config
        from modules.data_cleaning import DataCleaner
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

def interactive_mode():
    """Run SmartRecon in interactive mode."""
    print("\n🎯 SmartRecon Interactive Mode")
    print("=" * 50)
    
    while True:
        print("\n🚀 Available options:")
        print("1. 🔍 Check environment")
        print("2. 🧪 Test basic functionality") 
        print("3. 📊 Process bank data")
        print("4. 📁 List available data files")
        print("5. 📈 Generate sample data")
        print("6. 🔬 Run simple test")
        print("0. 👋 Exit")
        
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye! Thanks for using SmartRecon!")
                break
            elif choice == "1":
                check_environment()
            elif choice == "2":
                test_basic_functionality()
            elif choice == "3":
                run_with_bank_data()
            elif choice == "4":
                bank_files, gl_files = check_data_files()
                print(f"\n📊 Total files found: {len(bank_files + gl_files)}")
            elif choice == "5":
                if generate_sample_data():
                    print("✅ Sample data ready! You can now try option 3.")
            elif choice == "6":
                run_simple_test()
            else:
                print("❌ Invalid choice. Please enter 0-6.")
                
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
