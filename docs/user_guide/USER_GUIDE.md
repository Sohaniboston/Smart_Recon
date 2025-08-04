# SmartRecon User Guide

**Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Target Audience:** End Users, Financial Analysts, Data Professionals  

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Data Preparation](#data-preparation)
4. [Basic Operations](#basic-operations)
5. [Advanced Features](#advanced-features)
6. [Configuration](#configuration)
7. [Reports and Analysis](#reports-and-analysis)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Appendices](#appendices)

---

## 🎯 Introduction

### **What is SmartRecon?**

SmartRecon is a comprehensive financial data reconciliation tool designed to automate the process of matching transactions between different financial data sources. It uses advanced algorithms to identify exact matches, fuzzy matches, and exceptions in financial data.

### **Key Features**

- **Automated Data Ingestion** - Support for CSV, Excel files with automatic encoding detection
- **Intelligent Data Cleaning** - Standardization of dates, amounts, and descriptions
- **Multi-Level Matching** - Exact matching followed by fuzzy matching algorithms
- **Exception Management** - Comprehensive handling of unmatched transactions
- **Performance Monitoring** - Real-time tracking of processing performance
- **Comprehensive Reporting** - Detailed reconciliation reports and analytics
- **User-Friendly Interface** - Interactive command-line interface with menu system

### **Use Cases**

- **Bank Reconciliation** - Match bank statements with general ledger entries
- **Credit Card Reconciliation** - Reconcile credit card transactions with accounting records
- **Inter-company Reconciliation** - Match transactions between related entities
- **Cash Management** - Reconcile cash positions across multiple sources
- **Audit Support** - Provide detailed audit trails and exception analysis

---

## 🚀 Getting Started

### **Quick Start Workflow**

1. **Prepare Your Data Files**
   - Export bank data to CSV or Excel format
   - Export general ledger data to CSV or Excel format
   - Ensure data includes date, amount, and description columns

2. **Launch SmartRecon**
   ```bash
   python run_smartrecon.py
   ```

3. **Follow the Interactive Menu**
   - Select data ingestion to load your files
   - Run data cleaning to standardize formats
   - Execute exact matching for high-confidence matches
   - Apply fuzzy matching for potential matches
   - Generate comprehensive reports

### **First-Time Setup**

#### **Step 1: Configuration Check**
```bash
# Verify configuration is working
python run_smartrecon.py --test
```

#### **Step 2: Generate Sample Data**
```bash
# Create sample data for testing
python generate_financial_data.py
```

#### **Step 3: Test Run**
```bash
# Process sample data
python run_smartrecon.py --auto --input examples/sample_bank_data.csv --gl examples/sample_gl_data.csv
```

---

## 📊 Data Preparation

### **Supported File Formats**

#### **CSV Files**
- **Encoding:** UTF-8, Latin-1, Windows-1252 (auto-detected)
- **Delimiters:** Comma, semicolon, tab (auto-detected)
- **Headers:** First row should contain column names
- **Size Limit:** 500MB per file (configurable)

#### **Excel Files**
- **Formats:** .xlsx, .xls
- **Sheets:** Multiple sheet support with sheet selection
- **Size Limit:** 200MB per file (configurable)
- **Headers:** First row should contain column names

### **Required Data Columns**

#### **Bank Data Requirements**
| Column Type | Required | Examples | Description |
|-------------|----------|----------|-------------|
| Date | Yes | "Transaction Date", "Value Date" | Transaction date |
| Amount | Yes | "Amount", "Debit", "Credit" | Transaction amount |
| Description | Yes | "Description", "Details", "Memo" | Transaction description |
| Reference | Optional | "Reference", "Check Number" | Transaction reference |

#### **General Ledger Data Requirements**
| Column Type | Required | Examples | Description |
|-------------|----------|----------|-------------|
| Date | Yes | "GL Date", "Posting Date" | Posting date |
| Amount | Yes | "Amount", "Debit Amount", "Credit Amount" | Transaction amount |
| Description | Yes | "Description", "GL Description" | Account description |
| Account | Optional | "Account", "Account Number" | Account identifier |

### **Data Quality Guidelines**

#### **Date Formats**
- **Recommended:** YYYY-MM-DD (2025-07-29)
- **Supported:** MM/DD/YYYY, DD/MM/YYYY, DD-MM-YYYY
- **Avoid:** Text dates, partial dates, invalid dates

#### **Amount Formats**
- **Recommended:** Numeric format (1234.56)
- **Supported:** Currency symbols ($1,234.56), parentheses for negatives
- **Avoid:** Text in amount fields, multiple currencies in same file

#### **Description Quality**
- **Best:** Detailed, consistent descriptions
- **Good:** Standardized abbreviations
- **Avoid:** Empty descriptions, excessive special characters

---

## 🔧 Basic Operations

### **Interactive Mode**

Start SmartRecon in interactive mode for step-by-step processing:

```bash
python run_smartrecon.py
```

#### **Main Menu Options**

```
SmartRecon - Financial Data Reconciliation Tool v1.1.0
========================================================

1. Data Ingestion       - Load and validate data files
2. Data Cleaning        - Standardize and clean data
3. Exact Matching       - High-confidence matching
4. Fuzzy Matching       - Similarity-based matching  
5. Generate Reports     - Create reconciliation reports
6. Configuration        - Modify settings
7. Performance Monitor  - View processing metrics
8. Help                 - Access documentation
Q. Quit                 - Exit application

Select an option:
```

### **Batch Mode**

Process files automatically without interaction:

```bash
# Basic batch processing
python run_smartrecon.py --auto --input bank_data.csv --gl gl_data.csv --output results/

# Advanced batch processing with options
python run_smartrecon.py --auto \
  --input bank_data.csv \
  --gl gl_data.csv \
  --output results/ \
  --config config/custom_config.json \
  --exact-match \
  --fuzzy-match \
  --generate-reports
```

### **Data Ingestion Process**

#### **Step 1: File Selection**
```
Data Ingestion Menu
==================
1. Load Bank Data        - Select bank statement file
2. Load GL Data          - Select general ledger file
3. View Loaded Data      - Preview loaded datasets
4. Data Quality Check    - Validate data completeness
5. Return to Main Menu

Select an option: 1

Enter bank data file path: data/input/bank_statement_july.csv
```

#### **Step 2: Column Mapping**
```
Column Mapping for Bank Data
===========================
Detected columns: ['Date', 'Description', 'Amount', 'Reference']

Map to standard columns:
Date column: Date ✓
Amount column: Amount ✓
Description column: Description ✓
Reference column: Reference ✓

Mapping confirmed. Loading data...
✅ Loaded 1,247 bank transactions
```

#### **Step 3: Data Validation**
```
Data Quality Report
==================
📊 Bank Data Summary:
   Total Records: 1,247
   Date Range: 2025-07-01 to 2025-07-31
   Amount Range: -$5,432.10 to $12,890.45
   
✅ Data Quality Checks:
   Valid dates: 100% (1,247/1,247)
   Valid amounts: 100% (1,247/1,247)
   Non-empty descriptions: 98.5% (1,228/1,247)
   Unique transactions: 99.8% (1,244/1,247)
```

### **Data Cleaning Process**

#### **Automatic Cleaning**
```
Data Cleaning Options
====================
1. Standard Cleaning     - Apply default cleaning rules
2. Custom Cleaning       - Configure cleaning parameters
3. Preview Changes       - See cleaning effects before applying
4. Undo Last Cleaning    - Revert to original data

Select an option: 1

Applying standard cleaning...
📊 Date Standardization:
   Converted 1,247 dates to YYYY-MM-DD format
   
💰 Amount Normalization:
   Removed currency symbols from 892 entries
   Converted parentheses to negative signs: 47 entries
   
📝 Description Cleaning:
   Trimmed whitespace: 1,247 entries
   Standardized case: 1,247 entries
   
✅ Data cleaning completed successfully
```

#### **Quality Improvement Metrics**
```
Data Quality Improvement
=======================
Before Cleaning → After Cleaning
Date Format Consistency: 67% → 100%
Amount Format Consistency: 78% → 100%
Description Standardization: 45% → 95%
Overall Data Quality Score: 63% → 98%
```

---

## 🎯 Advanced Features

### **Exact Matching Engine**

#### **Configuration Options**
```json
{
  "exact_matching": {
    "amount_tolerance": 0.01,           // Allow 1 cent difference
    "date_range_days": 3,               // Match within 3 days
    "require_reference_match": false,   // Reference matching optional
    "case_sensitive_description": false // Ignore case in descriptions
  }
}
```

#### **Matching Strategies**
1. **Perfect Match** - Exact amount, date, and description
2. **Amount + Date Match** - Exact amount within date range
3. **Amount + Reference Match** - Exact amount with matching reference
4. **Tolerance Match** - Amount within tolerance, exact date

#### **Results Interpretation**
```
Exact Matching Results
=====================
📊 Matching Summary:
   Total Bank Transactions: 1,247
   Total GL Entries: 1,189
   
✅ Perfect Matches: 892 (71.5%)
✅ Amount+Date Matches: 167 (13.4%)
✅ Tolerance Matches: 89 (7.1%)
❓ Unmatched Bank: 99 (7.9%)
❓ Unmatched GL: 41 (3.4%)

🎯 Match Quality: 92.1% success rate
```

### **Fuzzy Matching Engine**

#### **Algorithm Types**
1. **Levenshtein Distance** - Character-based similarity
2. **Token Set Ratio** - Word-based matching
3. **Partial Ratio** - Substring matching
4. **Token Sort Ratio** - Order-independent matching

#### **Configuration Options**
```json
{
  "fuzzy_matching": {
    "similarity_threshold": 0.8,        // 80% similarity required
    "confidence_threshold": 0.85,       // 85% confidence for auto-match
    "max_suggestions": 10,              // Maximum suggestions per item
    "algorithms": ["token_set", "levenshtein"],
    "weight_description": 0.6,          // Description importance
    "weight_amount": 0.3,               // Amount importance  
    "weight_date": 0.1                  // Date importance
  }
}
```

#### **Interactive Fuzzy Matching**
```
Fuzzy Matching Review
====================
Unmatched Bank Transaction:
Date: 2025-07-15
Amount: $1,234.56
Description: "PAYROLL DEPOSIT COMPANY ABC"

Potential GL Matches:
1. [89%] PAYROLL DEP ABC CORP      | $1,234.56 | 2025-07-15
2. [76%] SALARY PAYMENT COMPANY A  | $1,234.56 | 2025-07-16
3. [71%] PAYROLL DEPOSIT           | $1,234.56 | 2025-07-14

Accept match? (1-3, N for none, S for skip): 1
✅ Match accepted with 89% confidence
```

### **Performance Monitoring**

#### **Real-Time Metrics**
```
Performance Monitor
==================
📊 Current Operation: Fuzzy Matching
⏱️  Elapsed Time: 00:02:34
🔄 Progress: 67% (834/1,247 items)
⚡ Processing Rate: 8.2 items/second
💾 Memory Usage: 245 MB / 1,000 MB limit
🎯 ETA: 00:01:23

🔍 Performance Insights:
   ✅ Memory usage: Normal
   ✅ Processing speed: Optimal
   ⚠️  Large descriptions detected: Consider pre-filtering
```

#### **Performance Optimization**
```json
{
  "performance": {
    "enable_monitoring": true,
    "batch_size": 1000,
    "parallel_processing": true,
    "memory_limit_mb": 1000,
    "optimize_large_datasets": true,
    "cache_similarity_results": true
  }
}
```

---

## ⚙️ Configuration

### **Configuration File Structure**

SmartRecon uses JSON-based configuration files located in the `config/` directory.

#### **Main Configuration Sections**
```json
{
  "data_ingestion": { },      // File loading settings
  "data_cleaning": { },       // Data standardization rules  
  "exact_matching": { },      // Exact matching parameters
  "fuzzy_matching": { },      // Fuzzy matching algorithms
  "exception_handling": { },  // Unmatched item processing
  "reporting": { },           // Report generation options
  "performance": { },         // Performance optimization
  "logging": { }              // Logging configuration
}
```

### **Custom Configuration Creation**

#### **Step 1: Copy Default Configuration**
```bash
cp config/default_config.json config/my_config.json
```

#### **Step 2: Modify Settings**
```json
{
  "data_cleaning": {
    "date_formats": [
      "%m/%d/%Y",              // US format: 07/29/2025
      "%d/%m/%Y"               // EU format: 29/07/2025
    ],
    "amount_tolerance": 0.05,  // 5 cent tolerance
    "duplicate_threshold": 0.98
  },
  "exact_matching": {
    "amount_tolerance": 0.05,  // Match tolerance
    "date_range_days": 5,      // 5-day matching window
    "require_reference_match": true
  }
}
```

#### **Step 3: Use Custom Configuration**
```bash
python run_smartrecon.py --config config/my_config.json
```

### **Column Mapping Templates**

Create custom column mappings for different data sources:

```json
{
  "column_mappings": {
    "chase_bank": {
      "date": "Transaction Date",
      "amount": "Amount", 
      "description": "Description",
      "reference": "Check Number"
    },
    "quickbooks_gl": {
      "date": "Date",
      "amount": "Amount",
      "description": "Memo/Description",
      "account": "Account"
    }
  }
}
```

---

## 📊 Reports and Analysis

### **Report Types**

#### **1. Reconciliation Summary Report**
```
SmartRecon Reconciliation Summary
================================
📅 Report Date: July 29, 2025
📊 Processing Period: July 1-31, 2025
🔄 Processing Time: 00:04:32

📈 Overall Results:
   Bank Transactions: 1,247
   GL Entries: 1,189
   Total Matches: 1,148 (92.1%)
   Unmatched Items: 99 (7.9%)

💰 Amount Reconciliation:
   Matched Amount: $2,847,392.45
   Unmatched Bank: $23,847.89
   Unmatched GL: $15,234.67
   Net Difference: $8,613.22

🎯 Match Quality Distribution:
   Perfect Matches: 892 (78.0%)
   Fuzzy Matches: 256 (22.0%)
   Average Confidence: 94.3%
```

#### **2. Exception Analysis Report**
```
Exception Analysis Report
========================
❓ Unmatched Bank Items: 99

📊 Exception Categories:
   Timing Differences: 47 (47.5%)
   Amount Discrepancies: 23 (23.2%)
   Missing GL Entries: 18 (18.2%)
   Data Quality Issues: 11 (11.1%)

🔍 Top Exception Patterns:
   1. "BANK FEE" descriptions (12 items)
   2. Weekend processing delays (8 items)
   3. Rounding differences < $0.10 (7 items)

💡 Recommendations:
   ✅ Create bank fee GL entries
   ✅ Extend date matching to 7 days
   ✅ Increase amount tolerance to $0.10
```

#### **3. Performance Analysis Report**
```
Performance Analysis Report
==========================
⚡ Processing Performance:
   Total Processing Time: 00:04:32
   Data Ingestion: 00:00:12 (4.4%)
   Data Cleaning: 00:00:08 (2.9%)
   Exact Matching: 00:01:45 (38.5%)
   Fuzzy Matching: 00:02:15 (49.5%)
   Report Generation: 00:00:12 (4.4%)

💾 Memory Usage:
   Peak Memory: 387 MB
   Average Memory: 245 MB
   Memory Efficiency: 95.2%

🎯 Optimization Opportunities:
   ✅ Consider parallel processing for fuzzy matching
   ✅ Enable similarity result caching
   ✅ Implement data pre-filtering
```

### **Report Formats**

#### **Excel Reports**
- Multiple worksheets for different report sections
- Conditional formatting for highlighting exceptions
- Charts and graphs for visual analysis
- Filtering and sorting capabilities

#### **CSV Reports**
- Separate files for each report type
- Machine-readable format for further analysis
- Compatible with other data tools

#### **PDF Reports**
- Executive summary format
- Professional presentation layout
- Charts and visualizations included

### **Custom Report Generation**

```bash
# Generate specific report types
python run_smartrecon.py --report summary --output reports/
python run_smartrecon.py --report exceptions --format excel
python run_smartrecon.py --report performance --format pdf

# Generate all reports
python run_smartrecon.py --report all --output reports/monthly/
```

---

## 💡 Best Practices

### **Data Preparation Best Practices**

#### **1. Data Quality**
- **Consistent Date Formats** - Use standard date formats across all files
- **Clean Amount Data** - Remove currency symbols and formatting before processing
- **Descriptive Descriptions** - Ensure transaction descriptions are meaningful
- **Unique References** - Use unique reference numbers where possible

#### **2. File Organization**
```
data/
├── input/
│   ├── bank_statements/
│   │   ├── 2025-07-bank.csv
│   │   └── 2025-07-cc.csv
│   └── gl_data/
│       └── 2025-07-gl.csv
├── processed/
│   └── cleaned_data/
└── output/
    └── reports/
```

#### **3. Regular Processing Schedule**
- **Daily Processing** - For high-volume transactions
- **Weekly Processing** - For moderate transaction volumes
- **Monthly Processing** - For comprehensive reconciliation

### **Performance Optimization**

#### **1. Large Dataset Handling**
```json
{
  "performance": {
    "batch_size": 2000,
    "parallel_processing": true,
    "memory_limit_mb": 2000,
    "cache_results": true
  }
}
```

#### **2. Processing Optimization**
- **Pre-filter Data** - Remove obviously non-matching items before fuzzy matching
- **Use Exact Matching First** - Complete exact matching before fuzzy matching
- **Monitor Memory Usage** - Adjust batch sizes based on available memory

### **Quality Control Procedures**

#### **1. Validation Checks**
- Review match confidence scores
- Investigate low-confidence fuzzy matches
- Analyze exception patterns for systematic issues
- Verify amount reconciliation totals

#### **2. Exception Management**
- Categorize exceptions by type and cause
- Implement systematic resolution procedures
- Track exception resolution over time
- Document recurring exception patterns

### **Security and Compliance**

#### **1. Data Protection**
- Store sensitive data in secure locations
- Use appropriate file permissions
- Remove or mask sensitive data in logs
- Follow organizational data retention policies

#### **2. Audit Trail**
- Maintain detailed processing logs
- Document configuration changes
- Track match approval decisions
- Preserve original data files

---

## 🔍 Troubleshooting

### **Common Issues and Solutions**

#### **Issue 1: No Matches Found**
**Symptoms:** All transactions remain unmatched after processing

**Solutions:**
1. Check amount tolerance settings
2. Verify date format consistency
3. Review column mapping configuration
4. Examine data quality issues

#### **Issue 2: Performance Issues**
**Symptoms:** Processing takes extremely long or system becomes unresponsive

**Solutions:**
1. Reduce batch size in configuration
2. Enable performance monitoring
3. Increase memory limits
4. Use data pre-filtering

#### **Issue 3: Encoding Problems**
**Symptoms:** Special characters appear garbled or cause errors

**Solutions:**
1. Detect and specify correct file encoding
2. Save files in UTF-8 format
3. Update encoding configuration

### **Diagnostic Tools**

```bash
# Run comprehensive diagnostics
python run_smartrecon.py --diagnostic

# Check configuration validity
python run_smartrecon.py --validate-config

# Test with sample data
python run_smartrecon.py --test
```

For detailed troubleshooting information, see `docs/TROUBLESHOOTING_GUIDE.md`.

---

## 📚 Appendices

### **Appendix A: Keyboard Shortcuts**

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl+C` | Cancel operation | Any long-running process |
| `Q` | Quit current menu | Interactive mode |
| `H` | Show help | Interactive mode |
| `R` | Refresh display | Report viewing |

### **Appendix B: File Format Specifications**

#### **CSV Format Requirements**
- **Delimiter:** Comma (,) preferred, semicolon (;) and tab supported
- **Text Qualifier:** Double quotes (") for text containing delimiters
- **Encoding:** UTF-8 recommended, auto-detection available
- **Headers:** First row must contain column names

#### **Excel Format Requirements**
- **Versions:** Excel 2007+ (.xlsx), Excel 97-2003 (.xls)
- **Sheets:** Data must be in first sheet or specify sheet name
- **Headers:** First row must contain column names
- **Data Types:** Numbers as numbers, dates as dates, text as text

### **Appendix C: Error Codes**

| Code | Description | Resolution |
|------|-------------|------------|
| ERR_001 | Configuration file not found | Check config directory |
| ERR_002 | Invalid file format | Verify file format and encoding |
| ERR_003 | Column mapping failed | Update column mappings |
| ERR_004 | Memory limit exceeded | Increase memory limits or reduce batch size |
| ERR_005 | Processing timeout | Increase timeout settings |

### **Appendix D: Sample Configuration Files**

Complete sample configuration files are available in the `config/examples/` directory:

- `bank_reconciliation_config.json` - Standard bank reconciliation
- `credit_card_config.json` - Credit card reconciliation
- `high_volume_config.json` - Large dataset processing
- `strict_matching_config.json` - Conservative matching settings

---

## 📞 Additional Resources

### **Documentation**
- **Installation Guide:** `docs/INSTALLATION_GUIDE.md`
- **Troubleshooting Guide:** `docs/TROUBLESHOOTING_GUIDE.md`
- **API Reference:** `docs/api/`
- **Quick Start:** `QUICKSTART.md`

### **Examples and Templates**
- **Sample Data:** `examples/sample_data/`
- **Configuration Templates:** `config/examples/`
- **Usage Examples:** `examples/scripts/`

### **Support**
- **GitHub Issues:** https://github.com/yourusername/SmartRecon/issues
- **Documentation Wiki:** https://github.com/yourusername/SmartRecon/wiki
- **Community Forum:** https://groups.google.com/g/smartrecon-users

---

**User Guide Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Compatible with:** SmartRecon v1.0+  
**Document Status:** Complete and Current
