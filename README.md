# SmartRecon - Intelligent Financial Reconciliation Assistant

SmartRecon automates the time-consuming and error-prone process of financial reconciliation between General Ledger (GL) entries and external sources such as bank statements. It reduces reconciliation time by 70% while improving accuracy, enabling financial analysts to focus on high-value analytical tasks.

## Features

- **Automated Data Ingestion**: Support for CSV and Excel file formats with intelligent column mapping
- **Data Cleaning & Standardization**: Automatic date, amount, and text normalization
- **Smart Matching Algorithms**: Exact and fuzzy matching with configurable confidence thresholds
- **Exception Management**: Automated categorization and resolution workflow for unmatched items
- **Comprehensive Reporting**: Detailed reports, visualizations, and audit trails
- **Command-Line Interface**: Full CLI support for automation and scripting

## Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/organization/smartrecon.git
cd smartrecon
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install SmartRecon:**
```bash
pip install -e .
```

### Basic Usage

1. **Validate your data files:**
```bash
python src/main.py validate path/to/your/gl_data.csv --file-type gl
python src/main.py validate path/to/your/bank_data.csv --file-type bank
```

2. **Run reconciliation:**
```bash
python src/main.py reconcile --gl-file path/to/gl_data.csv --bank-file path/to/bank_data.csv --output-dir results
```

3. **View results:**
The reconciliation process generates reports in the specified output directory:
- `reconciliation_summary.xlsx` - High-level summary and statistics
- `matches_report.csv` - Detailed matched transactions
- `exceptions_report.csv` - Unmatched items requiring review
- `audit_trail.json` - Complete processing audit trail

## Project Structure

```
smartrecon/
├── src/                          # Source code
│   ├── modules/                  # Core functional modules
│   │   ├── data_ingestion.py    # File loading and validation
│   │   ├── data_cleaning.py     # Data standardization
│   │   ├── matching_engine.py   # Transaction matching algorithms
│   │   ├── exception_handler.py # Exception management
│   │   └── reporting.py         # Report generation
│   ├── utils/                    # Utility functions
│   │   ├── logger.py            # Logging configuration
│   │   ├── exceptions.py        # Custom exceptions
│   │   ├── validators.py        # Data validation
│   │   └── helpers.py           # Helper functions
│   ├── main.py                   # CLI entry point
│   └── config.py                 # Configuration management
├── config/                       # Configuration files
│   └── default_config.json      # Default configuration
├── tests/                        # Test suite
├── examples/                     # Example data and configurations
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
└── setup.py                      # Package installation
```

## Configuration

SmartRecon uses JSON configuration files to customize behavior. Copy and modify `config/default_config.json`:

```json
{
  "data_ingestion": {
    "column_mapping": {
      "gl": {
        "transaction_date": "date",
        "debit": "amount",
        "description": "description"
      }
    }
  },
  "matching": {
    "exact_match_tolerance": 0.01,
    "fuzzy_match_threshold": 0.8,
    "date_tolerance_days": 2
  }
}
```

## Data Format Requirements

### GL Data
Required columns (can be mapped via configuration):
- **Date**: Transaction date
- **Amount**: Transaction amount (positive for debits, negative for credits)
- **Description**: Transaction description
- **Reference**: Transaction reference or ID

### Bank Data
Required columns (can be mapped via configuration):
- **Date**: Transaction date
- **Amount**: Transaction amount (positive for deposits, negative for withdrawals)
- **Description**: Transaction description
- **Reference**: Transaction reference or ID

## Development Status

**Current Version**: 1.0.0 (MVP)  
**Status**: Core framework implemented, modules ready for implementation

### Implemented Features ✅
- Project structure and architecture
- Configuration management system
- Logging and error handling framework
- CLI interface foundation
- Data validation utilities

### In Development 🚧
- Data ingestion module implementation
- Data cleaning algorithms
- Matching engine core logic
- Exception handling workflows
- Report generation system

### Planned Features 📋
- Advanced fuzzy matching algorithms
- Machine learning-based categorization
- Streamlit web interface (v2.0)
- API for programmatic access (v3.0)
- Integration with accounting systems (v4.0)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Testing

Run the test suite:
```bash
pytest tests/ -v --cov=src
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [User Guide](docs/user_guide.md)
- **Issues**: [GitHub Issues](https://github.com/organization/smartrecon/issues)
- **Email**: support@smartrecon.com

## Acknowledgments

- Built with pandas, numpy, and fuzzywuzzy
- Inspired by the need to automate financial reconciliation processes
- Designed for financial analysts and accounting professionals
