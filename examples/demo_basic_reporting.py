"""
SmartRecon Basic Reporting Demo

This script demonstrates the basic reporting capabilities including
data ingestion reports, quality assessments, and file summaries.

Run from examples directory: python demo_basic_reporting.py
"""

import sys
import os
from pathlib import Path

# Add the parent directory (Smart_Recon) to Python path to find src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_data_for_reporting():
    """Create sample data files for reporting demonstration."""
    print("🎯 Creating Sample Data for Basic Reporting Demo")
    print("=" * 50)
    
    # Create sample directory in examples folder
    examples_dir = Path(__file__).parent
    sample_dir = examples_dir / 'sample_data'
    sample_dir.mkdir(exist_ok=True)
    
    # Sample GL data with varying quality
    print("📊 Creating GL sample data...")
    
    # High quality GL data
    gl_high_quality = pd.DataFrame({
        'date': [datetime(2024, 1, i) for i in range(1, 21)],
        'description': [f'GL Transaction {i} - High Quality' for i in range(1, 21)],
        'amount': np.random.uniform(-5000, 5000, 20).round(2),
        'reference': [f'GL{i:03d}' for i in range(1, 21)],
        'account': [f'ACC{(i % 5) + 1:02d}' for i in range(1, 21)]
    })
    gl_high_quality.to_csv(sample_dir / 'gl_high_quality.csv', index=False)
    
    # Medium quality GL data (with some missing values)
    gl_medium_quality = pd.DataFrame({
        'date': [datetime(2024, 1, i) if i % 3 != 0 else None for i in range(1, 16)],
        'description': [f'GL Transaction {i} - Medium Quality' if i % 4 != 0 else None for i in range(1, 16)],
        'amount': np.random.uniform(-3000, 3000, 15).round(2),
        'reference': [f'GL{i:03d}' if i % 5 != 0 else None for i in range(1, 16)],
        'account': [f'ACC{(i % 3) + 1:02d}' for i in range(1, 16)]
    })
    gl_medium_quality.to_csv(sample_dir / 'gl_medium_quality.csv', index=False)
    
    # Low quality GL data (many issues)
    gl_low_quality = pd.DataFrame({
        'transaction_date': [datetime(2024, 1, i) if i % 2 == 0 else 'invalid_date' for i in range(1, 11)],
        'memo': [f'Poor Quality Transaction {i}' if i % 3 != 0 else '' for i in range(1, 11)],
        'value': ['$' + str(round(np.random.uniform(-1000, 1000), 2)) if i % 4 != 0 else 'invalid' for i in range(1, 11)],
        'ref_number': [f'GL{i:03d}' if i % 6 != 0 else None for i in range(1, 11)]
    })
    gl_low_quality.to_csv(sample_dir / 'gl_low_quality.csv', index=False)
    
    # Sample Bank data
    print("🏦 Creating Bank sample data...")
    
    bank_data = pd.DataFrame({
        'date': [datetime(2024, 1, i) for i in range(1, 26)],
        'description': [f'Bank Transaction {i} - Payment' for i in range(1, 26)],
        'amount': np.random.uniform(-4000, 4000, 25).round(2),
        'balance': np.cumsum(np.random.uniform(-100, 100, 25)).round(2),
        'reference': [f'BK{i:03d}' for i in range(1, 26)]
    })
    bank_data.to_csv(sample_dir / 'bank_statements.csv', index=False)
    
    # Create an Excel file with multiple sheets
    print("📈 Creating Excel sample data...")
    
    with pd.ExcelWriter(sample_dir / 'financial_data.xlsx', engine='openpyxl') as writer:
        gl_high_quality.to_excel(writer, sheet_name='GL_Data', index=False)
        bank_data.to_excel(writer, sheet_name='Bank_Data', index=False)
        
        # Summary sheet
        summary_data = pd.DataFrame({
            'Metric': ['Total GL Records', 'Total Bank Records', 'Date Range Start', 'Date Range End'],
            'Value': [len(gl_high_quality), len(bank_data), '2024-01-01', '2024-01-31']
        })
        summary_data.to_excel(writer, sheet_name='Summary', index=False)
    
    print("\n✅ Sample data files created in examples/sample_data/:")
    print("  📁 gl_high_quality.csv")
    print("  📁 gl_medium_quality.csv") 
    print("  📁 gl_low_quality.csv")
    print("  📁 bank_statements.csv")
    print("  📁 financial_data.xlsx")
    
    return {
        'high_quality_files': [str(sample_dir / 'gl_high_quality.csv'), str(sample_dir / 'bank_statements.csv')],
        'mixed_quality_files': [str(sample_dir / 'gl_high_quality.csv'), str(sample_dir / 'gl_medium_quality.csv'), str(sample_dir / 'gl_low_quality.csv')],
        'excel_file': [str(sample_dir / 'financial_data.xlsx')],
        'all_files': [
            str(sample_dir / 'gl_high_quality.csv'),
            str(sample_dir / 'gl_medium_quality.csv'), 
            str(sample_dir / 'gl_low_quality.csv'),
            str(sample_dir / 'bank_statements.csv'),
            str(sample_dir / 'financial_data.xlsx')
        ]
    }

def demo_basic_reporting():
    """Demonstrate basic reporting functionality."""
    print("\n🚀 SmartRecon Basic Reporting Demo")
    print("=" * 50)
    
    # Create sample data
    sample_files = create_sample_data_for_reporting()
    
    print("\n📋 Basic Reporting Features:")
    print("  ✅ Data ingestion quality reports")
    print("  ✅ File processing summaries")
    print("  ✅ Data quality assessment")
    print("  ✅ Visual charts and graphs")
    print("  ✅ Excel, HTML, and CSV exports")
    print("  ✅ Multi-file batch processing")
    
    print("\n🔧 Usage Examples:")
    print("\n1. Generate Ingestion Report for High-Quality Files:")
    print("   cd .. && python -m src.main basic-report examples/sample_data/gl_high_quality.csv examples/sample_data/bank_statements.csv")
    print("     --report-type ingestion")
    print("     --include-charts")
    print("     --export-format all")
    print("     --output-dir examples/reports/high_quality")
    
    print("\n2. Generate Quality Assessment for Mixed Quality Files:")
    print("   cd .. && python -m src.main basic-report examples/sample_data/gl_*.csv")
    print("     --report-type quality")
    print("     --export-format html")
    print("     --output-dir examples/reports/quality_assessment")
    
    print("\n3. Generate Summary Report for All Files:")
    print("   cd .. && python -m src.main basic-report examples/sample_data/*")
    print("     --report-type summary")
    print("     --output-dir examples/reports/summary")
    
    print("\n4. Excel-Only Report:")
    print("   cd .. && python -m src.main basic-report examples/sample_data/financial_data.xlsx")
    print("     --report-type ingestion")
    print("     --export-format excel")
    print("     --output-dir examples/reports/excel_only")
    
    print("\n📊 Expected Report Contents:")
    
    print("\n📈 Ingestion Reports Include:")
    print("  • File processing statistics")
    print("  • Data quality scores")
    print("  • Processing time analysis")
    print("  • Column and row counts")
    print("  • Encoding detection results")
    print("  • Error and warning summaries")
    
    print("\n📉 Quality Reports Include:")
    print("  • Completeness scores")
    print("  • Data validity assessments")
    print("  • Missing value analysis")
    print("  • Duplicate record detection")
    print("  • Column type analysis")
    print("  • Quality distribution charts")
    
    print("\n📋 Summary Reports Include:")
    print("  • High-level file overview")
    print("  • Total record counts")
    print("  • File size summaries")
    print("  • Quick validation results")
    
    print("\n🎨 Visualization Features:")
    print("  • Data quality distribution histograms")
    print("  • File size vs processing time scatter plots")
    print("  • Match rate comparison bar charts")
    print("  • Record distribution pie charts")
    
    print("\n📁 Output Formats:")
    print("  • Excel workbooks with multiple sheets")
    print("  • Interactive HTML reports")
    print("  • CSV files for data analysis")
    print("  • PNG charts and visualizations")
    
    print("\n🔍 Report Analysis Features:")
    print("  • Automatic file type detection")
    print("  • Column mapping confidence scores")
    print("  • Processing performance metrics")
    print("  • Data integrity validation")
    
    print(f"\n📊 Sample Data Statistics:")
    print(f"  • High Quality GL: 20 records, 5 columns")
    print(f"  • Medium Quality GL: 15 records, some missing data")
    print(f"  • Low Quality GL: 10 records, multiple issues")
    print(f"  • Bank Data: 25 records, 5 columns")
    print(f"  • Excel File: Multi-sheet format")
    
    print("\n✨ Demo completed! Sample data ready in examples/sample_data/")
    print("✨ Run the usage examples above to test basic reporting functionality.")
    
    return sample_files

if __name__ == "__main__":
    demo_basic_reporting()
