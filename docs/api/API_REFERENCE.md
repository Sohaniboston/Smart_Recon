# SmartRecon API Reference

**Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**API Level:** Complete Module Reference  

---

## 📋 Table of Contents

1. [API Overview](#api-overview)
2. [Core Modules](#core-modules)
3. [Configuration API](#configuration-api)
4. [Data Processing API](#data-processing-api)
5. [Matching Engines API](#matching-engines-api)
6. [Reporting API](#reporting-api)
7. [Utilities API](#utilities-api)
8. [Error Handling](#error-handling)
9. [Examples](#examples)

---

## 🎯 API Overview

### **Architecture**

SmartRecon follows a modular architecture with the following main components:

```
src/
├── config.py              # Configuration management
├── main.py                # Main application entry point
├── modules/               # Core business logic modules
│   ├── data_ingestion.py  # Data loading and validation
│   ├── data_cleaning.py   # Data standardization
│   ├── exact_matching_engine.py    # Exact matching algorithms
│   ├── fuzzy_matching.py  # Fuzzy matching algorithms
│   ├── exception_handler.py        # Exception management
│   └── reporting.py       # Report generation
└── utils/                 # Utility modules
    ├── exceptions.py      # Custom exceptions
    ├── helpers.py         # Helper functions
    ├── validators.py      # Data validation
    ├── logger.py          # Logging utilities
    └── performance.py     # Performance monitoring
```

### **Import Structure**

```python
# Main application
from src.main import SmartReconApp

# Configuration
from src.config import Config

# Core modules
from src.modules.data_ingestion import DataIngestion
from src.modules.data_cleaning import DataCleaner
from src.modules.exact_matching_engine import ExactMatchingEngine
from src.modules.fuzzy_matching import FuzzyMatcher
from src.modules.exception_handler import ExceptionHandler
from src.modules.reporting import ReportGenerator

# Utilities
from src.utils.performance import PerformanceMonitor
from src.utils.logger import setup_logger
from src.utils.exceptions import SmartReconError
```

---

## ⚙️ Configuration API

### **Config Class**

Main configuration management class for SmartRecon.

#### **Class Definition**
```python
class Config:
    """
    SmartRecon configuration management.
    
    Handles loading, validation, and access to configuration parameters
    from JSON configuration files.
    """
```

#### **Constructor**
```python
def __init__(self, config_path: str = None):
    """
    Initialize configuration from file.
    
    Args:
        config_path (str, optional): Path to configuration file.
                                   Defaults to 'config/default_config.json'
    
    Raises:
        ConfigurationError: If configuration file is invalid or missing
    """
```

#### **Methods**

##### **get()**
```python
def get(self, key: str, default: Any = None) -> Any:
    """
    Get configuration value by key.
    
    Args:
        key (str): Configuration key in dot notation (e.g., 'data_ingestion.encoding')
        default (Any): Default value if key not found
    
    Returns:
        Any: Configuration value
    
    Example:
        >>> config = Config()
        >>> encoding = config.get('data_ingestion.encoding', 'utf-8')
        >>> tolerance = config.get('exact_matching.amount_tolerance', 0.01)
    """
```

##### **set()**
```python
def set(self, key: str, value: Any) -> None:
    """
    Set configuration value.
    
    Args:
        key (str): Configuration key in dot notation
        value (Any): Value to set
    
    Example:
        >>> config.set('exact_matching.amount_tolerance', 0.05)
    """
```

##### **validate()**
```python
def validate(self) -> bool:
    """
    Validate configuration parameters.
    
    Returns:
        bool: True if configuration is valid
    
    Raises:
        ValidationError: If configuration parameters are invalid
    """
```

##### **save()**
```python
def save(self, path: str = None) -> None:
    """
    Save current configuration to file.
    
    Args:
        path (str, optional): Output file path. Defaults to original file.
    """
```

#### **Configuration Schema**

```python
CONFIG_SCHEMA = {
    "data_ingestion": {
        "supported_formats": ["csv", "xlsx", "xls"],
        "encoding": "utf-8",
        "max_file_size_mb": 100,
        "auto_detect_encoding": True,
        "auto_detect_delimiter": True
    },
    "data_cleaning": {
        "date_formats": ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"],
        "amount_tolerance": 0.01,
        "duplicate_threshold": 0.95,
        "standardize_descriptions": True,
        "remove_special_characters": False
    },
    "exact_matching": {
        "amount_tolerance": 0.01,
        "date_range_days": 3,
        "require_reference_match": False,
        "case_sensitive_description": False,
        "enable_amount_tolerance": True
    },
    "fuzzy_matching": {
        "similarity_threshold": 0.8,
        "confidence_threshold": 0.85,
        "max_suggestions": 10,
        "algorithms": ["token_set", "levenshtein"],
        "enable_caching": True
    }
}
```

---

## 📊 Data Processing API

### **DataIngestion Class**

Handles loading and initial validation of data files.

#### **Class Definition**
```python
class DataIngestion:
    """
    Data ingestion and validation module.
    
    Supports CSV and Excel file formats with automatic encoding detection,
    column mapping, and data quality assessment.
    """
```

#### **Constructor**
```python
def __init__(self, config: Config):
    """
    Initialize data ingestion module.
    
    Args:
        config (Config): SmartRecon configuration object
    """
```

#### **Methods**

##### **load_file()**
```python
def load_file(self, file_path: str, file_type: str = None, 
              sheet_name: str = None) -> pd.DataFrame:
    """
    Load data from file.
    
    Args:
        file_path (str): Path to data file
        file_type (str, optional): File type ('csv' or 'excel'). Auto-detected if None.
        sheet_name (str, optional): Excel sheet name. Defaults to first sheet.
    
    Returns:
        pd.DataFrame: Loaded data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        UnsupportedFormatError: If file format not supported
        DataValidationError: If data structure is invalid
    
    Example:
        >>> ingestion = DataIngestion(config)
        >>> bank_data = ingestion.load_file('data/bank_statement.csv')
        >>> gl_data = ingestion.load_file('data/gl_data.xlsx', sheet_name='GL_July')
    """
```

##### **validate_data()**
```python
def validate_data(self, data: pd.DataFrame, data_type: str) -> Dict[str, Any]:
    """
    Validate data structure and quality.
    
    Args:
        data (pd.DataFrame): Data to validate
        data_type (str): Type of data ('bank' or 'gl')
    
    Returns:
        Dict[str, Any]: Validation results and statistics
    
    Example:
        >>> validation_result = ingestion.validate_data(bank_data, 'bank')
        >>> print(f"Valid records: {validation_result['valid_records']}")
    """
```

##### **detect_columns()**
```python
def detect_columns(self, data: pd.DataFrame, data_type: str) -> Dict[str, str]:
    """
    Automatically detect and map columns.
    
    Args:
        data (pd.DataFrame): Input data
        data_type (str): Type of data ('bank' or 'gl')
    
    Returns:
        Dict[str, str]: Column mapping dictionary
    
    Example:
        >>> column_mapping = ingestion.detect_columns(data, 'bank')
        >>> print(column_mapping)
        {'date': 'Transaction Date', 'amount': 'Amount', 'description': 'Description'}
    """
```

### **DataCleaner Class**

Handles data standardization and cleaning operations.

#### **Class Definition**
```python
class DataCleaner:
    """
    Data cleaning and standardization module.
    
    Provides comprehensive data cleaning including date standardization,
    amount normalization, description cleaning, and duplicate detection.
    """
```

#### **Constructor**
```python
def __init__(self, config: Config):
    """
    Initialize data cleaner.
    
    Args:
        config (Config): SmartRecon configuration object
    """
```

#### **Methods**

##### **clean_data()**
```python
def clean_data(self, data: pd.DataFrame, data_type: str) -> pd.DataFrame:
    """
    Apply comprehensive data cleaning.
    
    Args:
        data (pd.DataFrame): Input data
        data_type (str): Type of data ('bank' or 'gl')
    
    Returns:
        pd.DataFrame: Cleaned data
    
    Example:
        >>> cleaner = DataCleaner(config)
        >>> cleaned_data = cleaner.clean_data(raw_data, 'bank')
    """
```

##### **standardize_dates()**
```python
def standardize_dates(self, data: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Standardize date formats.
    
    Args:
        data (pd.DataFrame): Input data
        date_column (str): Name of date column
    
    Returns:
        pd.DataFrame: Data with standardized dates
    
    Raises:
        DateParsingError: If dates cannot be parsed
    """
```

##### **normalize_amounts()**
```python
def normalize_amounts(self, data: pd.DataFrame, amount_column: str) -> pd.DataFrame:
    """
    Normalize amount formats.
    
    Args:
        data (pd.DataFrame): Input data
        amount_column (str): Name of amount column
    
    Returns:
        pd.DataFrame: Data with normalized amounts
    
    Example:
        >>> # Converts "$1,234.56", "(123.45)" to 1234.56, -123.45
        >>> cleaned = cleaner.normalize_amounts(data, 'Amount')
    """
```

##### **detect_duplicates()**
```python
def detect_duplicates(self, data: pd.DataFrame, threshold: float = 0.95) -> pd.Series:
    """
    Detect duplicate transactions.
    
    Args:
        data (pd.DataFrame): Input data
        threshold (float): Similarity threshold for duplicate detection
    
    Returns:
        pd.Series: Boolean series indicating duplicates
    """
```

---

## 🎯 Matching Engines API

### **ExactMatchingEngine Class**

Performs exact matching between datasets.

#### **Class Definition**
```python
class ExactMatchingEngine:
    """
    Exact matching engine for financial transactions.
    
    Implements multiple exact matching strategies including perfect matches,
    amount tolerance matching, and date range matching.
    """
```

#### **Constructor**
```python
def __init__(self, config: Config):
    """
    Initialize exact matching engine.
    
    Args:
        config (Config): SmartRecon configuration object
    """
```

#### **Methods**

##### **match_transactions()**
```python
def match_transactions(self, bank_data: pd.DataFrame, 
                      gl_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform exact matching between bank and GL data.
    
    Args:
        bank_data (pd.DataFrame): Bank transaction data
        gl_data (pd.DataFrame): General ledger data
    
    Returns:
        Dict[str, Any]: Matching results including matches and unmatched items
    
    Example:
        >>> engine = ExactMatchingEngine(config)
        >>> results = engine.match_transactions(bank_data, gl_data)
        >>> print(f"Matches found: {len(results['matches'])}")
    """
```

##### **perfect_match()**
```python
def perfect_match(self, bank_data: pd.DataFrame, 
                  gl_data: pd.DataFrame) -> pd.DataFrame:
    """
    Find perfect matches (exact amount, date, and description).
    
    Args:
        bank_data (pd.DataFrame): Bank transaction data
        gl_data (pd.DataFrame): General ledger data
    
    Returns:
        pd.DataFrame: Perfect matches
    """
```

##### **amount_tolerance_match()**
```python
def amount_tolerance_match(self, bank_data: pd.DataFrame, 
                          gl_data: pd.DataFrame, 
                          tolerance: float = None) -> pd.DataFrame:
    """
    Find matches within amount tolerance.
    
    Args:
        bank_data (pd.DataFrame): Bank transaction data
        gl_data (pd.DataFrame): General ledger data
        tolerance (float, optional): Amount tolerance. Uses config default if None.
    
    Returns:
        pd.DataFrame: Tolerance matches
    """
```

##### **date_range_match()**
```python
def date_range_match(self, bank_data: pd.DataFrame, 
                     gl_data: pd.DataFrame, 
                     days: int = None) -> pd.DataFrame:
    """
    Find matches within date range.
    
    Args:
        bank_data (pd.DataFrame): Bank transaction data
        gl_data (pd.DataFrame): General ledger data
        days (int, optional): Date range in days. Uses config default if None.
    
    Returns:
        pd.DataFrame: Date range matches
    """
```

### **FuzzyMatcher Class**

Performs fuzzy matching using similarity algorithms.

#### **Class Definition**
```python
class FuzzyMatcher:
    """
    Fuzzy matching engine using string similarity algorithms.
    
    Implements multiple similarity algorithms including Levenshtein distance,
    token-based matching, and composite scoring.
    """
```

#### **Constructor**
```python
def __init__(self, config: Config):
    """
    Initialize fuzzy matcher.
    
    Args:
        config (Config): SmartRecon configuration object
    """
```

#### **Methods**

##### **find_matches()**
```python
def find_matches(self, unmatched_bank: pd.DataFrame, 
                 unmatched_gl: pd.DataFrame) -> Dict[str, Any]:
    """
    Find fuzzy matches for unmatched transactions.
    
    Args:
        unmatched_bank (pd.DataFrame): Unmatched bank transactions
        unmatched_gl (pd.DataFrame): Unmatched GL entries
    
    Returns:
        Dict[str, Any]: Fuzzy matching results with confidence scores
    
    Example:
        >>> fuzzy = FuzzyMatcher(config)
        >>> results = fuzzy.find_matches(unmatched_bank, unmatched_gl)
        >>> for match in results['potential_matches']:
        ...     print(f"Confidence: {match['confidence']}")
    """
```

##### **calculate_similarity()**
```python
def calculate_similarity(self, desc1: str, desc2: str, 
                        algorithm: str = 'token_set') -> float:
    """
    Calculate similarity between two descriptions.
    
    Args:
        desc1 (str): First description
        desc2 (str): Second description
        algorithm (str): Similarity algorithm ('token_set', 'levenshtein', etc.)
    
    Returns:
        float: Similarity score (0.0 to 1.0)
    
    Example:
        >>> similarity = fuzzy.calculate_similarity("PAYROLL DEPOSIT", "PAYROLL DEP")
        >>> print(f"Similarity: {similarity:.2%}")
    """
```

##### **get_suggestions()**
```python
def get_suggestions(self, transaction: pd.Series, 
                   candidates: pd.DataFrame, 
                   max_suggestions: int = None) -> List[Dict[str, Any]]:
    """
    Get ranked suggestions for a transaction.
    
    Args:
        transaction (pd.Series): Transaction to match
        candidates (pd.DataFrame): Candidate matches
        max_suggestions (int, optional): Maximum suggestions to return
    
    Returns:
        List[Dict[str, Any]]: Ranked suggestions with confidence scores
    """
```

---

## 📊 Reporting API

### **ReportGenerator Class**

Generates comprehensive reconciliation reports.

#### **Class Definition**
```python
class ReportGenerator:
    """
    Report generation module for SmartRecon.
    
    Creates comprehensive reconciliation reports in multiple formats
    including Excel, CSV, and PDF.
    """
```

#### **Constructor**
```python
def __init__(self, config: Config):
    """
    Initialize report generator.
    
    Args:
        config (Config): SmartRecon configuration object
    """
```

#### **Methods**

##### **generate_summary_report()**
```python
def generate_summary_report(self, results: Dict[str, Any], 
                           output_path: str = None) -> str:
    """
    Generate reconciliation summary report.
    
    Args:
        results (Dict[str, Any]): Reconciliation results
        output_path (str, optional): Output file path
    
    Returns:
        str: Path to generated report
    
    Example:
        >>> generator = ReportGenerator(config)
        >>> report_path = generator.generate_summary_report(results)
    """
```

##### **generate_exception_report()**
```python
def generate_exception_report(self, unmatched_items: Dict[str, pd.DataFrame], 
                             output_path: str = None) -> str:
    """
    Generate exception analysis report.
    
    Args:
        unmatched_items (Dict[str, pd.DataFrame]): Unmatched transactions
        output_path (str, optional): Output file path
    
    Returns:
        str: Path to generated report
    """
```

##### **generate_match_details()**
```python
def generate_match_details(self, matches: pd.DataFrame, 
                          output_path: str = None) -> str:
    """
    Generate detailed match report.
    
    Args:
        matches (pd.DataFrame): Matched transactions
        output_path (str, optional): Output file path
    
    Returns:
        str: Path to generated report
    """
```

##### **export_to_excel()**
```python
def export_to_excel(self, data: Dict[str, pd.DataFrame], 
                   output_path: str, 
                   include_charts: bool = True) -> None:
    """
    Export data to Excel with multiple worksheets.
    
    Args:
        data (Dict[str, pd.DataFrame]): Data to export
        output_path (str): Output Excel file path
        include_charts (bool): Whether to include charts
    """
```

---

## 🔧 Utilities API

### **PerformanceMonitor Class**

Monitors and tracks performance metrics.

#### **Class Definition**
```python
class PerformanceMonitor:
    """
    Performance monitoring and optimization utilities.
    
    Provides comprehensive performance tracking including execution time,
    memory usage, and optimization recommendations.
    """
```

#### **Constructor**
```python
def __init__(self, enable_memory_tracking: bool = True):
    """
    Initialize performance monitor.
    
    Args:
        enable_memory_tracking (bool): Enable memory usage tracking
    """
```

#### **Methods**

##### **monitor_operation()**
```python
@contextmanager
def monitor_operation(self, operation_name: str, record_count: int = 0):
    """
    Context manager to monitor a specific operation.
    
    Args:
        operation_name (str): Name of operation being monitored
        record_count (int): Number of records being processed
    
    Example:
        >>> monitor = PerformanceMonitor()
        >>> with monitor.monitor_operation("data_cleaning", 1000):
        ...     # Perform data cleaning operations
        ...     cleaned_data = cleaner.clean_data(data)
    """
```

##### **get_performance_summary()**
```python
def get_performance_summary(self) -> Dict[str, Any]:
    """
    Get comprehensive performance summary.
    
    Returns:
        Dict[str, Any]: Performance metrics and statistics
    
    Example:
        >>> summary = monitor.get_performance_summary()
        >>> print(f"Total processing time: {summary['total_time']}")
    """
```

##### **get_optimization_recommendations()**
```python
def get_optimization_recommendations(self) -> List[str]:
    """
    Get performance optimization recommendations.
    
    Returns:
        List[str]: List of optimization suggestions
    """
```

### **Logger Setup**

#### **setup_logger()**
```python
def setup_logger(name: str = 'smartrecon', 
                level: str = 'INFO', 
                log_file: str = None) -> logging.Logger:
    """
    Set up SmartRecon logger.
    
    Args:
        name (str): Logger name
        level (str): Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        log_file (str, optional): Log file path
    
    Returns:
        logging.Logger: Configured logger
    
    Example:
        >>> logger = setup_logger('my_reconciliation', 'DEBUG', 'logs/debug.log')
        >>> logger.info("Starting reconciliation process")
    """
```

---

## ❌ Error Handling

### **Exception Hierarchy**

```python
class SmartReconError(Exception):
    """Base exception for SmartRecon."""
    pass

class ConfigurationError(SmartReconError):
    """Configuration-related errors."""
    pass

class DataValidationError(SmartReconError):
    """Data validation errors."""
    pass

class FileProcessingError(SmartReconError):
    """File processing errors."""
    pass

class MatchingError(SmartReconError):
    """Matching algorithm errors."""
    pass

class ReportGenerationError(SmartReconError):
    """Report generation errors."""
    pass
```

### **Error Handling Examples**

```python
try:
    config = Config('config/my_config.json')
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
    # Handle configuration issues

try:
    data = ingestion.load_file('data/bank_data.csv')
except FileProcessingError as e:
    logger.error(f"File processing error: {e}")
    # Handle file issues

try:
    matches = engine.match_transactions(bank_data, gl_data)
except MatchingError as e:
    logger.error(f"Matching error: {e}")
    # Handle matching issues
```

---

## 💡 Examples

### **Basic Usage Example**

```python
from src.config import Config
from src.modules.data_ingestion import DataIngestion
from src.modules.data_cleaning import DataCleaner
from src.modules.exact_matching_engine import ExactMatchingEngine
from src.modules.reporting import ReportGenerator

# Initialize configuration
config = Config('config/default_config.json')

# Load data
ingestion = DataIngestion(config)
bank_data = ingestion.load_file('data/bank_statement.csv')
gl_data = ingestion.load_file('data/gl_data.csv')

# Clean data
cleaner = DataCleaner(config)
bank_clean = cleaner.clean_data(bank_data, 'bank')
gl_clean = cleaner.clean_data(gl_data, 'gl')

# Perform exact matching
engine = ExactMatchingEngine(config)
results = engine.match_transactions(bank_clean, gl_clean)

# Generate reports
generator = ReportGenerator(config)
report_path = generator.generate_summary_report(results)

print(f"Reconciliation complete. Report saved to: {report_path}")
```

### **Advanced Usage with Performance Monitoring**

```python
from src.utils.performance import PerformanceMonitor
from src.modules.fuzzy_matching import FuzzyMatcher

# Initialize performance monitoring
monitor = PerformanceMonitor(enable_memory_tracking=True)

# Perform reconciliation with monitoring
with monitor.monitor_operation("complete_reconciliation", len(bank_data)):
    # Data cleaning
    with monitor.monitor_operation("data_cleaning", len(bank_data)):
        bank_clean = cleaner.clean_data(bank_data, 'bank')
        gl_clean = cleaner.clean_data(gl_data, 'gl')
    
    # Exact matching
    with monitor.monitor_operation("exact_matching", len(bank_clean)):
        exact_results = engine.match_transactions(bank_clean, gl_clean)
    
    # Fuzzy matching for unmatched items
    if exact_results['unmatched_bank'].shape[0] > 0:
        fuzzy = FuzzyMatcher(config)
        with monitor.monitor_operation("fuzzy_matching", 
                                     len(exact_results['unmatched_bank'])):
            fuzzy_results = fuzzy.find_matches(
                exact_results['unmatched_bank'],
                exact_results['unmatched_gl']
            )

# Get performance summary
performance = monitor.get_performance_summary()
recommendations = monitor.get_optimization_recommendations()

print(f"Processing completed in {performance['total_time']:.2f} seconds")
for rec in recommendations:
    print(f"💡 {rec}")
```

### **Custom Configuration Example**

```python
# Create custom configuration
config = Config()

# Customize matching parameters
config.set('exact_matching.amount_tolerance', 0.05)
config.set('exact_matching.date_range_days', 7)
config.set('fuzzy_matching.similarity_threshold', 0.9)

# Customize performance settings
config.set('performance.batch_size', 2000)
config.set('performance.parallel_processing', True)

# Save custom configuration
config.save('config/my_custom_config.json')
```

---

## 📞 API Support

### **Version Compatibility**

| API Version | SmartRecon Version | Python Version | Status |
|-------------|-------------------|----------------|--------|
| 1.1.x | 1.1.x | 3.8+ | Current |
| 1.0.x | 1.0.x | 3.8+ | Supported |

### **Deprecation Notices**

- No deprecated APIs in current version
- Future deprecations will be announced in release notes

### **API Changes**

#### **Version 1.1.0 Changes**
- Added `PerformanceMonitor` class
- Enhanced `FuzzyMatcher` with additional algorithms
- Improved error handling with specific exception types
- Added batch processing capabilities

---

**API Reference Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**API Stability:** Stable  
**Documentation Status:** Complete
