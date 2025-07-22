# SmartRecon Application Entry Points

This document describes the various ways to run and interact with the SmartRecon financial reconciliation system.

## 🚀 Quick Start

### Method 1: Enhanced Application Interface (Recommended)
```bash
# Interactive guided workflow
python app.py interactive

# Quick reconciliation
python app.py reconcile data/gl.csv data/bank.csv

# File validation
python app.py validate data/*.csv --detailed

# Show usage examples
python app.py examples
```

### Method 2: Original CLI Interface
```bash
# Complete reconciliation workflow
python -m src.main reconcile --gl-file data/gl.csv --bank-file data/bank.csv

# Exact matching only
python -m src.main exact-match data/gl.csv data/bank.csv

# Basic reporting
python -m src.main basic-report data/*.csv --report-type quality
```

### Method 3: Simple Launcher
```bash
# Automatically detects and runs the appropriate interface
python smartrecon.py interactive
python smartrecon.py reconcile data/gl.csv data/bank.csv
```

## 📂 Entry Point Files

| File | Purpose | Features |
|------|---------|----------|
| `app.py` | Enhanced main application | Interactive mode, batch processing, comprehensive help |
| `src/main.py` | Original CLI interface | Core reconciliation commands, detailed options |
| `smartrecon.py` | Simple launcher | Auto-detection, fallback handling |
| `startup.py` | Environment setup | Dependency checking, configuration creation |

## 🎯 Core Commands

### Data Validation
```bash
# Validate single file
python app.py validate data/gl.csv

# Validate multiple files with details
python app.py validate data/*.csv --detailed

# Save validation results
python app.py validate data/gl.xlsx --output validation_report.json
```

### Reconciliation
```bash
# Interactive guided reconciliation
python app.py interactive

# Quick reconciliation (exact matching only)
python app.py reconcile data/gl.csv data/bank.csv --quick

# Custom reconciliation with options
python app.py reconcile data/gl.csv data/bank.csv \
  --amount-tolerance 0.05 \
  --export-format all \
  --output-dir results/
```

### Batch Processing
```bash
# Process file pairs in batch
python app.py batch "data/monthly_*.csv" --file-pairs

# Validate all files in directory
python app.py batch "input/*.xlsx"
```

### Reporting
```bash
# Generate data quality report
python app.py basic-report data/*.csv --report-type quality

# Create ingestion analysis with charts
python app.py basic-report data/gl.xlsx --include-charts --export-format html
```

## ⚙️ Configuration Options

### Global Options
- `--config`: Specify custom configuration file
- `--verbose`: Enable detailed logging
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `--quiet`: Suppress non-essential output

### Reconciliation Options
- `--quick`: Fast exact matching only
- `--amount-tolerance`: Tolerance for amount matching (default: 0.01)
- `--export-format`: Output format (excel, csv, html, all)
- `--match-strategy`: Matching strategies to use
- `--output-dir`: Custom output directory

## 🔧 Advanced Usage

### Custom Configuration
```bash
# Use custom configuration file
python app.py --config my_config.json reconcile data/gl.csv data/bank.csv

# Override specific settings
python app.py reconcile data/gl.csv data/bank.csv --amount-tolerance 0.02
```

### Development and Debugging
```bash
# Verbose mode with debug logging
python app.py --verbose --log-level DEBUG validate data/gl.csv

# Environment validation
python startup.py --check-only

# Force configuration recreation
python startup.py --force
```

### Integration Examples
```bash
# Complete workflow pipeline
python app.py validate data/*.csv --detailed
python app.py reconcile data/gl.csv data/bank.csv --export-format all
python app.py basic-report output/*.xlsx --report-type summary
```

## 📊 Output Examples

### Successful Reconciliation
```
🎯 Starting Reconciliation Process
GL File: gl_data.csv
Bank File: bank_statements.csv
Output Directory: output

[20.0%] Reconciliation: Loading GL data
[40.0%] Reconciliation: Loading bank data
[60.0%] Reconciliation: Cleaning GL data
[80.0%] Reconciliation: Cleaning bank data
[100.0%] ✅ Reconciliation completed (in 12.34s)

📊 Reconciliation Results:
  ✅ Exact matches: 1,247
  📋 GL records processed: 1,350
  📋 Bank records processed: 1,289
  🎯 GL match rate: 92.4%
  🎯 Bank match rate: 96.7%
  ⚠️  GL unmatched: 103
  ⚠️  Bank unmatched: 42

📁 Output Files:
  📄 exact_matches.xlsx
  📄 unmatched_gl.xlsx
  📄 unmatched_bank.xlsx
  📄 reconciliation_summary.json

💾 All results saved to: output
```

### Interactive Mode
```
🎯 Welcome to SmartRecon Interactive Mode!

This guided workflow will help you through the reconciliation process.

📁 Enter path to GL (General Ledger) file: data/gl.csv
🏦 Enter path to Bank statement file: data/bank.csv
📂 Enter output directory [output_20250717_1430]: 

🔧 Choose reconciliation type:
  1. Quick (exact matching only)
  2. Standard (exact + fuzzy matching)
  3. Comprehensive (all strategies + detailed reports)

Enter choice (1-3): 2
```

## 🆘 Help and Documentation

### Built-in Help
```bash
# Show main help menu
python app.py --help

# Command-specific help
python app.py reconcile --help
python app.py validate --help

# Show examples
python app.py examples

# Interactive tutorial
python app.py tutorial
```

### Troubleshooting
```bash
# Check environment and dependencies
python startup.py --check-only

# Validate file structure
python app.py validate data/your_file.csv --detailed

# Debug mode
python app.py --verbose --log-level DEBUG reconcile data/gl.csv data/bank.csv
```

## 🎓 Learning Path

1. **New Users**: Start with `python app.py tutorial`
2. **File Validation**: Use `python app.py validate your_files`
3. **First Reconciliation**: Try `python app.py interactive`
4. **Advanced Usage**: Explore `python app.py examples`
5. **Automation**: Use batch processing and custom configurations

## 💡 Tips and Best Practices

### Performance
- Use `--quick` mode for large datasets requiring only exact matching
- Enable `--parallel` for batch processing when possible
- Set appropriate `--amount-tolerance` based on your data precision

### Data Quality
- Always validate files before reconciliation
- Review data quality reports to identify issues
- Use detailed validation (`--detailed`) for new data sources

### Output Management
- Use descriptive output directory names with timestamps
- Export to multiple formats (`--export-format all`) for flexibility
- Generate comprehensive reports for audit trails

### Automation
- Create batch scripts for regular processing
- Use configuration files for consistent settings
- Set up logging for production environments

## 🔗 Related Documentation

- [Configuration Guide](config/README.md)
- [Data Format Requirements](docs/data_formats.md)
- [Matching Algorithms](docs/matching_algorithms.md)
- [API Reference](docs/api_reference.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
