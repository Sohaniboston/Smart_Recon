# SmartRecon Usage Examples

**Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Purpose:** Comprehensive usage examples for common scenarios  

---

## 📋 Table of Contents

1. [Basic Bank Reconciliation](#basic-bank-reconciliation)
2. [Credit Card Reconciliation](#credit-card-reconciliation)
3. [Large Dataset Processing](#large-dataset-processing)
4. [Custom Configuration Examples](#custom-configuration-examples)
5. [Batch Processing Scripts](#batch-processing-scripts)
6. [Advanced Matching Scenarios](#advanced-matching-scenarios)
7. [Integration Examples](#integration-examples)

---

## 🏦 Basic Bank Reconciliation

### **Scenario: Monthly Bank Statement Reconciliation**

**Business Case:** Reconcile monthly bank statement with general ledger entries for cash account.

#### **Step 1: Prepare Data Files**

**Bank Statement Format (bank_july_2025.csv):**
```csv
Transaction Date,Description,Amount,Reference
2025-07-01,OPENING BALANCE,15000.00,
2025-07-02,CHECK #1001,-1250.00,1001
2025-07-03,DEPOSIT PAYROLL,8500.00,DEP001
2025-07-05,BANK FEE,-25.00,FEE001
2025-07-08,CHECK #1002,-750.00,1002
```

**General Ledger Format (gl_cash_july_2025.csv):**
```csv
GL Date,Account,Description,Debit Amount,Credit Amount,Reference
2025-07-01,1001,Cash - Opening Balance,15000.00,,BAL001
2025-07-02,1001,Payment to Vendor A,,1250.00,CHK1001
2025-07-03,1001,Payroll Deposit,8500.00,,PAY001
2025-07-08,1001,Payment to Vendor B,,750.00,CHK1002
```

#### **Step 2: Configuration Setup**

```python
# Create configuration for bank reconciliation
config_data = {
    "data_ingestion": {
        "supported_formats": ["csv", "xlsx"],
        "encoding": "utf-8",
        "auto_detect_delimiter": True
    },
    "column_mappings": {
        "bank_data": {
            "date": "Transaction Date",
            "amount": "Amount",
            "description": "Description",
            "reference": "Reference"
        },
        "gl_data": {
            "date": "GL Date",
            "amount": ["Debit Amount", "Credit Amount"],
            "description": "Description",
            "reference": "Reference"
        }
    },
    "exact_matching": {
        "amount_tolerance": 0.01,
        "date_range_days": 3,
        "require_reference_match": False
    },
    "fuzzy_matching": {
        "similarity_threshold": 0.8,
        "confidence_threshold": 0.85
    }
}

# Save configuration
import json
with open('config/bank_reconciliation.json', 'w') as f:
    json.dump(config_data, f, indent=2)
```

#### **Step 3: Execute Reconciliation**

```python
#!/usr/bin/env python3
"""
Basic Bank Reconciliation Example
"""

from src.config import Config
from src.modules.data_ingestion import DataIngestion
from src.modules.data_cleaning import DataCleaner
from src.modules.exact_matching_engine import ExactMatchingEngine
from src.modules.fuzzy_matching import FuzzyMatcher
from src.modules.reporting import ReportGenerator
from src.utils.performance import PerformanceMonitor

def basic_bank_reconciliation():
    """Perform basic bank reconciliation."""
    
    # Initialize components
    config = Config('config/bank_reconciliation.json')
    monitor = PerformanceMonitor()
    
    print("🏦 Starting Bank Reconciliation...")
    
    with monitor.monitor_operation("bank_reconciliation"):
        # Step 1: Data Ingestion
        print("📊 Loading data files...")
        ingestion = DataIngestion(config)
        
        bank_data = ingestion.load_file('data/input/bank_july_2025.csv')
        gl_data = ingestion.load_file('data/input/gl_cash_july_2025.csv')
        
        print(f"   Bank transactions: {len(bank_data)}")
        print(f"   GL entries: {len(gl_data)}")
        
        # Step 2: Data Cleaning
        print("🧹 Cleaning data...")
        cleaner = DataCleaner(config)
        
        bank_clean = cleaner.clean_data(bank_data, 'bank')
        gl_clean = cleaner.clean_data(gl_data, 'gl')
        
        # Step 3: Exact Matching
        print("🎯 Performing exact matching...")
        engine = ExactMatchingEngine(config)
        exact_results = engine.match_transactions(bank_clean, gl_clean)
        
        print(f"   Exact matches: {len(exact_results['matches'])}")
        print(f"   Unmatched bank: {len(exact_results['unmatched_bank'])}")
        print(f"   Unmatched GL: {len(exact_results['unmatched_gl'])}")
        
        # Step 4: Fuzzy Matching (if needed)
        if len(exact_results['unmatched_bank']) > 0:
            print("🔍 Performing fuzzy matching...")
            fuzzy = FuzzyMatcher(config)
            fuzzy_results = fuzzy.find_matches(
                exact_results['unmatched_bank'],
                exact_results['unmatched_gl']
            )
            print(f"   Fuzzy matches: {len(fuzzy_results['matches'])}")
        
        # Step 5: Generate Reports
        print("📋 Generating reports...")
        generator = ReportGenerator(config)
        
        # Combine results
        all_results = {
            'exact_matches': exact_results['matches'],
            'fuzzy_matches': fuzzy_results['matches'] if 'fuzzy_results' in locals() else [],
            'unmatched_bank': exact_results['unmatched_bank'],
            'unmatched_gl': exact_results['unmatched_gl']
        }
        
        # Generate reports
        summary_path = generator.generate_summary_report(all_results, 'reports/bank_reconciliation_summary.xlsx')
        exceptions_path = generator.generate_exception_report(
            {'bank': all_results['unmatched_bank'], 'gl': all_results['unmatched_gl']},
            'reports/bank_reconciliation_exceptions.xlsx'
        )
        
        print(f"📊 Summary report: {summary_path}")
        print(f"❓ Exception report: {exceptions_path}")
    
    # Performance summary
    performance = monitor.get_performance_summary()
    print(f"\n⚡ Processing completed in {performance['total_time']:.2f} seconds")
    
    return all_results

if __name__ == "__main__":
    results = basic_bank_reconciliation()
```

#### **Expected Output**
```
🏦 Starting Bank Reconciliation...
📊 Loading data files...
   Bank transactions: 5
   GL entries: 4
🧹 Cleaning data...
🎯 Performing exact matching...
   Exact matches: 3
   Unmatched bank: 2
   Unmatched GL: 1
🔍 Performing fuzzy matching...
   Fuzzy matches: 1
📋 Generating reports...
📊 Summary report: reports/bank_reconciliation_summary.xlsx
❓ Exception report: reports/bank_reconciliation_exceptions.xlsx

⚡ Processing completed in 2.34 seconds
```

---

## 💳 Credit Card Reconciliation

### **Scenario: Credit Card Statement vs. Expense Reports**

**Business Case:** Reconcile corporate credit card statements with employee expense reports.

#### **Data Preparation**

**Credit Card Statement (cc_statement_july.csv):**
```csv
Transaction Date,Merchant,Amount,Card Number
2025-07-01,OFFICE DEPOT #123,156.78,****1234
2025-07-02,UBER TRIP,45.32,****1234
2025-07-03,HOTEL MARRIOTT,289.50,****1234
2025-07-05,RESTAURANT ABC,78.95,****1234
```

**Expense Reports (expense_reports_july.csv):**
```csv
Report Date,Employee,Vendor,Amount,Category,Receipt ID
2025-07-01,John Smith,Office Depot,156.78,Office Supplies,R001
2025-07-02,John Smith,Uber,45.32,Transportation,R002
2025-07-03,John Smith,Marriott Hotel,289.50,Lodging,R003
```

#### **Implementation**

```python
#!/usr/bin/env python3
"""
Credit Card Reconciliation Example
"""

def credit_card_reconciliation():
    """Reconcile credit card with expense reports."""
    
    # Custom configuration for credit card reconciliation
    config_data = {
        "column_mappings": {
            "bank_data": {  # Credit card data
                "date": "Transaction Date",
                "amount": "Amount",
                "description": "Merchant"
            },
            "gl_data": {  # Expense reports
                "date": "Report Date",
                "amount": "Amount", 
                "description": "Vendor"
            }
        },
        "exact_matching": {
            "amount_tolerance": 0.01,
            "date_range_days": 5,  # Allow longer date range
            "case_sensitive_description": False
        },
        "fuzzy_matching": {
            "similarity_threshold": 0.7,  # Lower threshold for merchant names
            "confidence_threshold": 0.8
        }
    }
    
    # Save configuration
    with open('config/cc_reconciliation.json', 'w') as f:
        json.dump(config_data, f, indent=2)
    
    # Load configuration and perform reconciliation
    config = Config('config/cc_reconciliation.json')
    monitor = PerformanceMonitor()
    
    print("💳 Starting Credit Card Reconciliation...")
    
    with monitor.monitor_operation("cc_reconciliation"):
        # Load data
        ingestion = DataIngestion(config)
        cc_data = ingestion.load_file('data/input/cc_statement_july.csv')
        expense_data = ingestion.load_file('data/input/expense_reports_july.csv')
        
        # Data cleaning with enhanced merchant name cleaning
        cleaner = DataCleaner(config)
        cc_clean = cleaner.clean_data(cc_data, 'bank')
        expense_clean = cleaner.clean_data(expense_data, 'gl')
        
        # Enhanced description cleaning for merchant names
        cc_clean['description'] = cc_clean['description'].str.upper().str.strip()
        expense_clean['description'] = expense_clean['description'].str.upper().str.strip()
        
        # Exact matching
        engine = ExactMatchingEngine(config)
        exact_results = engine.match_transactions(cc_clean, expense_clean)
        
        # Fuzzy matching with focus on merchant name similarity
        fuzzy = FuzzyMatcher(config)
        fuzzy_results = fuzzy.find_matches(
            exact_results['unmatched_bank'],
            exact_results['unmatched_gl']
        )
        
        # Generate specialized credit card reports
        generator = ReportGenerator(config)
        
        # Create comprehensive results
        results = {
            'cc_transactions': len(cc_clean),
            'expense_reports': len(expense_clean),
            'exact_matches': exact_results['matches'],
            'fuzzy_matches': fuzzy_results['matches'],
            'unmatched_cc': exact_results['unmatched_bank'],
            'unmatched_expenses': exact_results['unmatched_gl']
        }
        
        # Generate reports
        summary_path = generator.generate_summary_report(results, 'reports/cc_reconciliation_summary.xlsx')
        
        print(f"💳 Credit Card Reconciliation Complete")
        print(f"   CC Transactions: {results['cc_transactions']}")
        print(f"   Expense Reports: {results['expense_reports']}")
        print(f"   Matched: {len(results['exact_matches']) + len(results['fuzzy_matches'])}")
        print(f"   Unmatched CC: {len(results['unmatched_cc'])}")
        print(f"   Unmatched Expenses: {len(results['unmatched_expenses'])}")
        print(f"📊 Report: {summary_path}")
    
    return results

if __name__ == "__main__":
    results = credit_card_reconciliation()
```

---

## 📈 Large Dataset Processing

### **Scenario: Processing 50,000+ Transactions**

**Business Case:** Handle large monthly reconciliation with performance optimization.

```python
#!/usr/bin/env python3
"""
Large Dataset Processing Example
"""

def large_dataset_reconciliation():
    """Process large datasets with optimization."""
    
    # High-performance configuration
    config_data = {
        "performance": {
            "enable_monitoring": True,
            "batch_size": 5000,
            "parallel_processing": True,
            "memory_limit_mb": 2000,
            "cache_similarity_results": True,
            "optimize_large_datasets": True
        },
        "data_ingestion": {
            "chunk_size": 10000,  # Process in chunks
            "max_file_size_mb": 500
        },
        "fuzzy_matching": {
            "use_fast_algorithm": True,
            "pre_filter_by_amount": True,
            "max_comparisons": 100000
        }
    }
    
    # Save high-performance configuration
    with open('config/large_dataset.json', 'w') as f:
        json.dump(config_data, f, indent=2)
    
    config = Config('config/large_dataset.json')
    monitor = PerformanceMonitor(enable_memory_tracking=True)
    
    print("📈 Starting Large Dataset Reconciliation...")
    print("⚡ Performance optimizations enabled")
    
    with monitor.monitor_operation("large_dataset_reconciliation"):
        # Load large datasets
        print("📊 Loading large datasets...")
        ingestion = DataIngestion(config)
        
        # Load in chunks to manage memory
        bank_data = ingestion.load_file('data/input/large_bank_data.csv')
        gl_data = ingestion.load_file('data/input/large_gl_data.csv')
        
        print(f"   Bank transactions: {len(bank_data):,}")
        print(f"   GL entries: {len(gl_data):,}")
        
        # Memory-efficient data cleaning
        print("🧹 Cleaning data (batch processing)...")
        cleaner = DataCleaner(config)
        
        bank_clean = cleaner.clean_data(bank_data, 'bank')
        gl_clean = cleaner.clean_data(gl_data, 'gl')
        
        # Optimized exact matching
        print("🎯 Performing optimized exact matching...")
        engine = ExactMatchingEngine(config)
        exact_results = engine.match_transactions(bank_clean, gl_clean)
        
        print(f"   Exact matches: {len(exact_results['matches']):,}")
        print(f"   Unmatched bank: {len(exact_results['unmatched_bank']):,}")
        print(f"   Unmatched GL: {len(exact_results['unmatched_gl']):,}")
        
        # Memory status check
        memory_usage = monitor.get_memory_usage()
        print(f"💾 Memory usage: {memory_usage['used_mb']:.1f} MB / {memory_usage['limit_mb']} MB")
        
        # Selective fuzzy matching (only if reasonable number of unmatched items)
        if len(exact_results['unmatched_bank']) < 10000:
            print("🔍 Performing selective fuzzy matching...")
            fuzzy = FuzzyMatcher(config)
            fuzzy_results = fuzzy.find_matches(
                exact_results['unmatched_bank'],
                exact_results['unmatched_gl']
            )
            print(f"   Fuzzy matches: {len(fuzzy_results['matches']):,}")
        else:
            print("⚠️  Too many unmatched items for fuzzy matching - recommend data review")
            fuzzy_results = {'matches': []}
        
        # Generate optimized reports
        print("📋 Generating optimized reports...")
        generator = ReportGenerator(config)
        
        results = {
            'total_bank': len(bank_clean),
            'total_gl': len(gl_clean),
            'exact_matches': exact_results['matches'],
            'fuzzy_matches': fuzzy_results['matches'],
            'unmatched_bank': exact_results['unmatched_bank'],
            'unmatched_gl': exact_results['unmatched_gl']
        }
        
        # Generate summary report only for large datasets
        summary_path = generator.generate_summary_report(results, 'reports/large_dataset_summary.xlsx')
        
        print(f"📊 Summary report: {summary_path}")
    
    # Detailed performance analysis
    performance = monitor.get_performance_summary()
    recommendations = monitor.get_optimization_recommendations()
    
    print(f"\n⚡ Performance Summary:")
    print(f"   Total processing time: {performance['total_time']:.2f} seconds")
    print(f"   Peak memory usage: {performance['peak_memory_mb']:.1f} MB")
    print(f"   Processing rate: {performance['records_per_second']:.1f} records/second")
    
    if recommendations:
        print(f"\n💡 Optimization Recommendations:")
        for rec in recommendations:
            print(f"   • {rec}")
    
    return results

if __name__ == "__main__":
    results = large_dataset_reconciliation()
```

---

## ⚙️ Custom Configuration Examples

### **Conservative Matching Configuration**

```json
{
  "name": "Conservative Matching",
  "description": "High-precision matching with minimal false positives",
  "exact_matching": {
    "amount_tolerance": 0.00,
    "date_range_days": 0,
    "require_reference_match": true,
    "case_sensitive_description": true
  },
  "fuzzy_matching": {
    "similarity_threshold": 0.95,
    "confidence_threshold": 0.98,
    "max_suggestions": 3,
    "require_manual_approval": true
  },
  "data_cleaning": {
    "strict_date_parsing": true,
    "amount_validation": "strict"
  }
}
```

### **Aggressive Matching Configuration**

```json
{
  "name": "Aggressive Matching",
  "description": "High-recall matching to find maximum possible matches",
  "exact_matching": {
    "amount_tolerance": 0.10,
    "date_range_days": 7,
    "require_reference_match": false,
    "case_sensitive_description": false
  },
  "fuzzy_matching": {
    "similarity_threshold": 0.6,
    "confidence_threshold": 0.7,
    "max_suggestions": 20,
    "auto_accept_threshold": 0.9
  },
  "data_cleaning": {
    "aggressive_description_cleaning": true,
    "normalize_whitespace": true
  }
}
```

---

## 🔄 Batch Processing Scripts

### **Monthly Reconciliation Script**

```python
#!/usr/bin/env python3
"""
Monthly Reconciliation Batch Script
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

def monthly_reconciliation_batch(month_year: str):
    """
    Perform monthly reconciliation for specified month.
    
    Args:
        month_year (str): Month in format 'YYYY-MM' (e.g., '2025-07')
    """
    
    # Setup logging
    log_file = f"logs/reconciliation_{month_year}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting monthly reconciliation for {month_year}")
    
    # Define file paths
    input_dir = Path(f"data/input/{month_year}")
    output_dir = Path(f"data/output/{month_year}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    bank_file = input_dir / f"bank_statement_{month_year}.csv"
    gl_file = input_dir / f"gl_cash_{month_year}.csv"
    
    # Verify input files exist
    if not bank_file.exists():
        logger.error(f"Bank file not found: {bank_file}")
        return False
    
    if not gl_file.exists():
        logger.error(f"GL file not found: {gl_file}")
        return False
    
    try:
        # Import SmartRecon modules
        from src.config import Config
        from src.modules.data_ingestion import DataIngestion
        from src.modules.data_cleaning import DataCleaner
        from src.modules.exact_matching_engine import ExactMatchingEngine
        from src.modules.fuzzy_matching import FuzzyMatcher
        from src.modules.reporting import ReportGenerator
        from src.utils.performance import PerformanceMonitor
        
        # Load configuration
        config = Config('config/monthly_reconciliation.json')
        monitor = PerformanceMonitor()
        
        with monitor.monitor_operation(f"monthly_reconciliation_{month_year}"):
            # Data ingestion
            logger.info("Loading data files...")
            ingestion = DataIngestion(config)
            bank_data = ingestion.load_file(str(bank_file))
            gl_data = ingestion.load_file(str(gl_file))
            
            logger.info(f"Loaded {len(bank_data)} bank transactions")
            logger.info(f"Loaded {len(gl_data)} GL entries")
            
            # Data cleaning
            logger.info("Cleaning data...")
            cleaner = DataCleaner(config)
            bank_clean = cleaner.clean_data(bank_data, 'bank')
            gl_clean = cleaner.clean_data(gl_data, 'gl')
            
            # Exact matching
            logger.info("Performing exact matching...")
            engine = ExactMatchingEngine(config)
            exact_results = engine.match_transactions(bank_clean, gl_clean)
            
            exact_matches = len(exact_results['matches'])
            logger.info(f"Found {exact_matches} exact matches")
            
            # Fuzzy matching
            fuzzy_matches = 0
            if len(exact_results['unmatched_bank']) > 0:
                logger.info("Performing fuzzy matching...")
                fuzzy = FuzzyMatcher(config)
                fuzzy_results = fuzzy.find_matches(
                    exact_results['unmatched_bank'],
                    exact_results['unmatched_gl']
                )
                fuzzy_matches = len(fuzzy_results['matches'])
                logger.info(f"Found {fuzzy_matches} fuzzy matches")
            
            # Generate reports
            logger.info("Generating reports...")
            generator = ReportGenerator(config)
            
            # Combine results
            all_results = {
                'exact_matches': exact_results['matches'],
                'fuzzy_matches': fuzzy_results['matches'] if fuzzy_matches > 0 else [],
                'unmatched_bank': exact_results['unmatched_bank'],
                'unmatched_gl': exact_results['unmatched_gl'],
                'processing_date': datetime.now().isoformat(),
                'month_year': month_year
            }
            
            # Generate reports
            summary_path = output_dir / f"reconciliation_summary_{month_year}.xlsx"
            exceptions_path = output_dir / f"reconciliation_exceptions_{month_year}.xlsx"
            
            generator.generate_summary_report(all_results, str(summary_path))
            generator.generate_exception_report(
                {'bank': all_results['unmatched_bank'], 'gl': all_results['unmatched_gl']},
                str(exceptions_path)
            )
            
            # Log final results
            total_matches = exact_matches + fuzzy_matches
            total_items = len(bank_data)
            match_percentage = (total_matches / total_items) * 100 if total_items > 0 else 0
            
            logger.info("Reconciliation completed successfully")
            logger.info(f"Total matches: {total_matches} ({match_percentage:.1f}%)")
            logger.info(f"Unmatched bank items: {len(all_results['unmatched_bank'])}")
            logger.info(f"Unmatched GL items: {len(all_results['unmatched_gl'])}")
            logger.info(f"Summary report: {summary_path}")
            logger.info(f"Exceptions report: {exceptions_path}")
        
        # Performance summary
        performance = monitor.get_performance_summary()
        logger.info(f"Processing completed in {performance['total_time']:.2f} seconds")
        
        return True
        
    except Exception as e:
        logger.error(f"Reconciliation failed: {str(e)}", exc_info=True)
        return False

def batch_reconciliation_multiple_months(start_month: str, end_month: str):
    """
    Process multiple months in batch.
    
    Args:
        start_month (str): Start month in format 'YYYY-MM'
        end_month (str): End month in format 'YYYY-MM'
    """
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    
    # Parse dates
    start_date = datetime.strptime(start_month, '%Y-%m')
    end_date = datetime.strptime(end_month, '%Y-%m')
    
    current_date = start_date
    results = []
    
    while current_date <= end_date:
        month_year = current_date.strftime('%Y-%m')
        print(f"\n{'='*50}")
        print(f"Processing {month_year}")
        print(f"{'='*50}")
        
        success = monthly_reconciliation_batch(month_year)
        results.append({
            'month': month_year,
            'success': success
        })
        
        current_date += relativedelta(months=1)
    
    # Summary
    print(f"\n{'='*50}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*50}")
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total months processed: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    if total - successful > 0:
        print("\nFailed months:")
        for result in results:
            if not result['success']:
                print(f"  - {result['month']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monthly_batch.py <YYYY-MM> [end_YYYY-MM]")
        sys.exit(1)
    
    start_month = sys.argv[1]
    
    if len(sys.argv) > 2:
        end_month = sys.argv[2]
        batch_reconciliation_multiple_months(start_month, end_month)
    else:
        monthly_reconciliation_batch(start_month)
```

### **Usage:**
```bash
# Process single month
python examples/monthly_batch.py 2025-07

# Process multiple months
python examples/monthly_batch.py 2025-01 2025-07
```

---

## 🔧 Integration Examples

### **Database Integration Example**

```python
#!/usr/bin/env python3
"""
Database Integration Example
"""

import sqlite3
import pandas as pd
from src.config import Config
from src.modules.exact_matching_engine import ExactMatchingEngine

def database_integration_example():
    """Integrate SmartRecon with database systems."""
    
    # Database connection
    conn = sqlite3.connect('financial_data.db')
    
    try:
        # Load data from database
        bank_query = """
        SELECT transaction_date as date, 
               amount, 
               description, 
               reference_number as reference
        FROM bank_transactions 
        WHERE transaction_date BETWEEN '2025-07-01' AND '2025-07-31'
        """
        
        gl_query = """
        SELECT posting_date as date,
               CASE WHEN debit_amount > 0 THEN debit_amount 
                    ELSE -credit_amount END as amount,
               description,
               document_number as reference
        FROM general_ledger
        WHERE account_number = '1001'
        AND posting_date BETWEEN '2025-07-01' AND '2025-07-31'
        """
        
        # Load data into DataFrames
        bank_data = pd.read_sql_query(bank_query, conn)
        gl_data = pd.read_sql_query(gl_query, conn)
        
        print(f"Loaded {len(bank_data)} bank transactions from database")
        print(f"Loaded {len(gl_data)} GL entries from database")
        
        # Perform reconciliation
        config = Config()
        engine = ExactMatchingEngine(config)
        results = engine.match_transactions(bank_data, gl_data)
        
        # Store results back to database
        matches_df = pd.DataFrame(results['matches'])
        if not matches_df.empty:
            matches_df.to_sql('reconciliation_matches', conn, if_exists='replace', index=False)
        
        unmatched_bank = results['unmatched_bank']
        if not unmatched_bank.empty:
            unmatched_bank.to_sql('unmatched_bank_items', conn, if_exists='replace', index=False)
        
        unmatched_gl = results['unmatched_gl']
        if not unmatched_gl.empty:
            unmatched_gl.to_sql('unmatched_gl_items', conn, if_exists='replace', index=False)
        
        print("Results stored in database tables:")
        print("  - reconciliation_matches")
        print("  - unmatched_bank_items")
        print("  - unmatched_gl_items")
        
        # Create reconciliation summary
        summary = {
            'reconciliation_date': pd.Timestamp.now(),
            'total_bank_transactions': len(bank_data),
            'total_gl_entries': len(gl_data),
            'matched_items': len(results['matches']),
            'unmatched_bank_items': len(unmatched_bank),
            'unmatched_gl_items': len(unmatched_gl),
            'match_percentage': (len(results['matches']) / len(bank_data)) * 100
        }
        
        summary_df = pd.DataFrame([summary])
        summary_df.to_sql('reconciliation_summary', conn, if_exists='append', index=False)
        
        print(f"Match percentage: {summary['match_percentage']:.1f}%")
        
    finally:
        conn.close()

if __name__ == "__main__":
    database_integration_example()
```

### **API Integration Example**

```python
#!/usr/bin/env python3
"""
API Integration Example
"""

import requests
import pandas as pd
from datetime import datetime
from src.config import Config
from src.modules.data_ingestion import DataIngestion
from src.modules.exact_matching_engine import ExactMatchingEngine

def api_integration_example():
    """Integrate SmartRecon with external APIs."""
    
    # Example: Fetch bank data from banking API
    def fetch_bank_data_from_api(account_id: str, start_date: str, end_date: str):
        """Fetch bank data from external API."""
        
        # Mock API call (replace with actual API)
        api_url = f"https://api.bank.com/v1/accounts/{account_id}/transactions"
        headers = {
            'Authorization': 'Bearer YOUR_API_TOKEN',
            'Content-Type': 'application/json'
        }
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'limit': 1000
        }
        
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            
            transactions = response.json()['transactions']
            
            # Convert to DataFrame
            bank_data = pd.DataFrame([
                {
                    'date': tx['transaction_date'],
                    'amount': float(tx['amount']),
                    'description': tx['description'],
                    'reference': tx['transaction_id']
                }
                for tx in transactions
            ])
            
            return bank_data
            
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return pd.DataFrame()
    
    # Example: Fetch GL data from accounting system API
    def fetch_gl_data_from_api(account_number: str, start_date: str, end_date: str):
        """Fetch GL data from accounting system API."""
        
        # Mock API call (replace with actual API)
        api_url = f"https://api.accounting.com/v1/gl_entries"
        headers = {
            'Authorization': 'Bearer YOUR_ACCOUNTING_API_TOKEN',
            'Content-Type': 'application/json'
        }
        params = {
            'account_number': account_number,
            'start_date': start_date,
            'end_date': end_date
        }
        
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            
            entries = response.json()['gl_entries']
            
            # Convert to DataFrame
            gl_data = pd.DataFrame([
                {
                    'date': entry['posting_date'],
                    'amount': float(entry['debit_amount']) if entry['debit_amount'] else -float(entry['credit_amount']),
                    'description': entry['description'],
                    'reference': entry['document_number']
                }
                for entry in entries
            ])
            
            return gl_data
            
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return pd.DataFrame()
    
    # Main integration workflow
    print("🌐 Starting API Integration Reconciliation...")
    
    # Fetch data from APIs
    print("📡 Fetching bank data from API...")
    bank_data = fetch_bank_data_from_api('12345', '2025-07-01', '2025-07-31')
    
    print("📡 Fetching GL data from API...")
    gl_data = fetch_gl_data_from_api('1001', '2025-07-01', '2025-07-31')
    
    if bank_data.empty or gl_data.empty:
        print("❌ Failed to fetch data from APIs")
        return
    
    print(f"📊 Fetched {len(bank_data)} bank transactions")
    print(f"📊 Fetched {len(gl_data)} GL entries")
    
    # Perform reconciliation using SmartRecon
    config = Config()
    engine = ExactMatchingEngine(config)
    results = engine.match_transactions(bank_data, gl_data)
    
    print(f"🎯 Found {len(results['matches'])} matches")
    print(f"❓ {len(results['unmatched_bank'])} unmatched bank items")
    print(f"❓ {len(results['unmatched_gl'])} unmatched GL items")
    
    # Post results back to API (optional)
    def post_results_to_api(results: dict):
        """Post reconciliation results back to API."""
        
        api_url = "https://api.reconciliation.com/v1/results"
        headers = {
            'Authorization': 'Bearer YOUR_RECON_API_TOKEN',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'reconciliation_date': datetime.now().isoformat(),
            'matches': len(results['matches']),
            'unmatched_bank': len(results['unmatched_bank']),
            'unmatched_gl': len(results['unmatched_gl']),
            'match_details': results['matches'][:10]  # Send first 10 matches as sample
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            print("📤 Results posted to reconciliation API successfully")
        except requests.RequestException as e:
            print(f"❌ Failed to post results: {e}")
    
    post_results_to_api(results)
    
    return results

if __name__ == "__main__":
    results = api_integration_example()
```

---

**Usage Examples Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Coverage:** Comprehensive real-world scenarios  
**Support:** Complete implementation examples
