"""
SmartRecon Exact Matching Demo Script

This script demonstrates the exact matching reconciliation engine capabilities
using sample financial data.

Run from examples directory: python demo_exact_matching.py
"""

import sys
import os
from pathlib import Path

# Add the parent directory (Smart_Recon) to Python path to find src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Sample data creation for testing
def create_sample_gl_data():
    """Create sample GL data for testing."""
    np.random.seed(42)
    
    dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(30)]
    
    gl_data = []
    for i in range(50):
        date = np.random.choice(dates)
        amount = round(np.random.uniform(-5000, 5000), 2)
        
        gl_data.append({
            'date': date,
            'description': f'GL Entry {i+1} - Payment Processing',
            'amount': amount,
            'reference': f'GL{i+1:03d}',
            'account': f'ACC{(i % 10) + 1:02d}'
        })
    
    return pd.DataFrame(gl_data)

def create_sample_bank_data():
    """Create sample bank data with some matching records."""
    np.random.seed(42)
    
    dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(30)]
    
    bank_data = []
    for i in range(45):
        date = np.random.choice(dates)
        amount = round(np.random.uniform(-4500, 4500), 2)
        
        # Create some exact matches (30% of records)
        if i < 15:
            # These will be exact matches with GL data
            amount = [1250.50, -875.25, 2100.00, -450.75, 1875.30][i % 5]
            ref = f'GL{(i % 15) + 1:03d}'
        else:
            ref = f'BK{i+1:03d}'
        
        bank_data.append({
            'date': date,
            'description': f'Bank Transaction {i+1} - Wire Transfer',
            'amount': amount,
            'reference': ref,
            'balance': round(np.random.uniform(10000, 50000), 2)
        })
    
    return pd.DataFrame(bank_data)

def demo_exact_matching():
    """Demonstrate exact matching engine capabilities."""
    print("🚀 SmartRecon Exact Matching Engine Demo")
    print("=" * 50)
    
    # Create sample data
    print("📊 Creating sample financial data...")
    gl_data = create_sample_gl_data()
    bank_data = create_sample_bank_data()
    
    print(f"GL Records: {len(gl_data)}")
    print(f"Bank Records: {len(bank_data)}")
    print()
    
    # Save sample data to files in examples directory
    examples_dir = Path(__file__).parent
    sample_dir = examples_dir / 'sample_data'
    sample_dir.mkdir(exist_ok=True)
    
    gl_data.to_csv(sample_dir / 'sample_gl.csv', index=False)
    bank_data.to_csv(sample_dir / 'sample_bank.csv', index=False)
    
    print("📁 Sample data files created in examples/sample_data/:")
    print("  - sample_gl.csv")
    print("  - sample_bank.csv")
    print()
    
    # Display sample records
    print("📋 Sample GL Records:")
    print(gl_data.head().to_string(index=False))
    print()
    
    print("📋 Sample Bank Records:")
    print(bank_data.head().to_string(index=False))
    print()
    
    print("🎯 Exact Matching Engine Features:")
    print("  ✅ Reference-based exact matching")
    print("  ✅ Amount + Date exact matching")
    print("  ✅ Amount + Date + Description matching")
    print("  ✅ Composite key matching")
    print("  ✅ Amount tolerance matching")
    print("  ✅ High-performance processing")
    print("  ✅ Comprehensive audit trails")
    print()
    
    print("🔧 Usage Example:")
    print("cd .. && python -m src.main exact-match examples/sample_data/sample_gl.csv examples/sample_data/sample_bank.csv")
    print("   --strategies reference_exact amount_date_exact")
    print("   --amount-tolerance 0.01")
    print("   --export-format excel")
    print("   --output-dir examples/results")
    print()
    
    print("📈 Expected Results:")
    print("  • Reference matches: High confidence exact matches")
    print("  • Amount/Date matches: Perfect precision matches")
    print("  • Tolerance matches: Near-exact matches within threshold")
    print("  • Comprehensive reporting with statistics")
    print("  • Export to Excel/CSV for further analysis")
    print()
    
    print("✨ Demo completed! Sample data ready in examples/sample_data/")
    print("✨ Run the usage example above to test exact matching reconciliation.")

if __name__ == "__main__":
    demo_exact_matching()
