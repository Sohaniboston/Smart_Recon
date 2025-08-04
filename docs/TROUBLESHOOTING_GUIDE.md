# SmartRecon Troubleshooting Guide

**Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Support Level:** Comprehensive Issue Resolution  

---

## 📋 Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Installation Issues](#installation-issues)
3. [Configuration Problems](#configuration-problems)
4. [Data Processing Errors](#data-processing-errors)
5. [Performance Issues](#performance-issues)
6. [Matching Algorithm Problems](#matching-algorithm-problems)
7. [Report Generation Issues](#report-generation-issues)
8. [Environment-Specific Issues](#environment-specific-issues)
9. [Advanced Troubleshooting](#advanced-troubleshooting)
10. [Getting Additional Help](#getting-additional-help)

---

## 🔍 Quick Diagnostics

### **System Health Check**

Run this comprehensive diagnostic to identify common issues:

```bash
# Run built-in diagnostic tool
python run_smartrecon.py --diagnostic

# Alternative: Manual health check
python -c "
import sys
print(f'Python Version: {sys.version}')
try:
    from src.config import Config
    print('✅ Configuration module: OK')
except Exception as e:
    print(f'❌ Configuration module: {e}')

try:
    import pandas as pd
    print(f'✅ Pandas version: {pd.__version__}')
except Exception as e:
    print(f'❌ Pandas: {e}')

try:
    from src.utils.performance import PerformanceMonitor
    print('✅ Performance monitoring: OK')
except Exception as e:
    print(f'❌ Performance monitoring: {e}')
"
```

### **Log File Analysis**

Check recent log files for error patterns:

```bash
# View recent logs
ls -la logs/
tail -50 logs/smartrecon_$(date +%Y-%m-%d).log

# Search for errors
grep -i "error\|exception\|failed" logs/smartrecon_*.log
```

---

## 🚀 Installation Issues

### **Problem 1: Python Not Found**

#### **Symptoms:**
- `'python' is not recognized as an internal or external command`
- `command not found: python`

#### **Solutions:**

**Windows:**
```bash
# Check if Python is installed
where python
# If not found, add Python to PATH or reinstall

# Add Python to PATH permanently
# 1. Open System Properties > Environment Variables
# 2. Add Python installation directory to PATH
# 3. Restart command prompt
```

**macOS:**
```bash
# Check Python installation
which python3
# Install Python via Homebrew if missing
brew install python3

# Create alias for python command
echo 'alias python=python3' >> ~/.zshrc
source ~/.zshrc
```

**Linux:**
```bash
# Install Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip

# Create symbolic link
sudo ln -s /usr/bin/python3 /usr/bin/python
```

### **Problem 2: Package Installation Failures**

#### **Symptoms:**
- `Failed building wheel for python-Levenshtein`
- `Microsoft Visual C++ 14.0 is required`
- `error: command 'gcc' failed`

#### **Solutions:**

**Windows:**
```bash
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Alternative: Install via conda
conda install python-levenshtein

# Or use pre-compiled wheel
pip install --only-binary=all python-Levenshtein
```

**macOS:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install packages with correct compiler
export CC=clang
pip install -r requirements.txt
```

**Linux:**
```bash
# Install build essentials
sudo apt-get install build-essential python3-dev

# Install packages
pip3 install -r requirements.txt
```

### **Problem 3: Permission Denied Errors**

#### **Symptoms:**
- `PermissionError: [Errno 13] Permission denied`
- `Access denied` when installing packages

#### **Solutions:**

```bash
# Use user installation (recommended)
pip install --user -r requirements.txt

# Or create virtual environment
python -m venv smartrecon_env
source smartrecon_env/bin/activate  # Linux/macOS
smartrecon_env\Scripts\activate     # Windows
pip install -r requirements.txt

# Last resort: Use sudo (Linux/macOS only)
sudo pip install -r requirements.txt
```

---

## ⚙️ Configuration Problems

### **Problem 1: Configuration File Not Found**

#### **Symptoms:**
- `Configuration file not found: config/default_config.json`
- `ConfigurationError: Unable to load configuration`

#### **Solutions:**

```bash
# Check if config directory exists
ls -la config/

# If missing, create default configuration
mkdir -p config
python -c "
from src.config import Config
Config.create_default_config('config/default_config.json')
print('Default configuration created')
"

# Alternative: Copy from examples
cp examples/sample_config.json config/default_config.json
```

### **Problem 2: Invalid Configuration Values**

#### **Symptoms:**
- `ValidationError: Invalid configuration parameter`
- Unexpected behavior during processing

#### **Solutions:**

```bash
# Validate configuration file
python -c "
from src.config import Config
try:
    config = Config('config/default_config.json')
    print('✅ Configuration is valid')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"

# Reset to default configuration
cp config/default_config.json config/default_config.json.backup
python -c "
from src.config import Config
Config.create_default_config('config/default_config.json')
"
```

### **Problem 3: Column Mapping Issues**

#### **Symptoms:**
- `KeyError: Unable to find column 'Date'`
- Incorrect data mapping during ingestion

#### **Solutions:**

```bash
# Check your data file headers
python -c "
import pandas as pd
df = pd.read_csv('your_data_file.csv', nrows=1)
print('Available columns:', list(df.columns))
"

# Update column mappings in config
# Edit config/default_config.json
{
  "column_mappings": {
    "bank_data": {
      "date": ["your_date_column_name"],
      "amount": ["your_amount_column_name"],
      "description": ["your_description_column_name"]
    }
  }
}
```

---

## 📊 Data Processing Errors

### **Problem 1: File Encoding Issues**

#### **Symptoms:**
- `UnicodeDecodeError: 'utf-8' codec can't decode`
- Garbled characters in data

#### **Solutions:**

```bash
# Detect file encoding
python -c "
import chardet
with open('your_file.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(f'Detected encoding: {result[\"encoding\"]}')
"

# Update configuration with correct encoding
{
  "data_ingestion": {
    "encoding": "latin-1"  // or "cp1252", "utf-8-sig"
  }
}

# Convert file encoding if needed
iconv -f latin1 -t utf-8 input.csv > output.csv
```

### **Problem 2: Date Parsing Failures**

#### **Symptoms:**
- `ValueError: time data does not match format`
- Dates not recognized correctly

#### **Solutions:**

```bash
# Check date formats in your data
python -c "
import pandas as pd
df = pd.read_csv('your_file.csv')
print('Sample dates:', df['date_column'].head())
"

# Add date formats to configuration
{
  "data_cleaning": {
    "date_formats": [
      "%Y-%m-%d",       // 2025-07-29
      "%m/%d/%Y",       // 07/29/2025
      "%d/%m/%Y",       // 29/07/2025
      "%d-%m-%Y",       // 29-07-2025
      "%Y%m%d"          // 20250729
    ]
  }
}
```

### **Problem 3: Amount Parsing Issues**

#### **Symptoms:**
- `ValueError: could not convert string to float`
- Amounts not processed correctly

#### **Solutions:**

```bash
# Check amount format in data
python -c "
import pandas as pd
df = pd.read_csv('your_file.csv')
print('Sample amounts:', df['amount_column'].head())
print('Amount types:', df['amount_column'].dtype)
"

# Clean amount data
{
  "data_cleaning": {
    "amount_cleaning": {
      "remove_currency_symbols": true,
      "remove_commas": true,
      "handle_parentheses_negative": true
    }
  }
}
```

---

## ⚡ Performance Issues

### **Problem 1: Slow Processing**

#### **Symptoms:**
- Processing takes much longer than expected
- System becomes unresponsive

#### **Solutions:**

```bash
# Enable performance monitoring
{
  "performance": {
    "enable_monitoring": true,
    "profile_operations": true
  }
}

# Reduce batch size for large files
{
  "performance": {
    "batch_size": 500,        // Reduced from default 1000
    "chunk_size": 5000        // Process in smaller chunks
  }
}

# Use performance optimization mode
python run_smartrecon.py --optimize
```

### **Problem 2: Memory Errors**

#### **Symptoms:**
- `MemoryError`
- `Out of memory` errors
- System swap usage increases dramatically

#### **Solutions:**

```bash
# Check memory usage
python -c "
import psutil
print(f'Available memory: {psutil.virtual_memory().available / (1024**3):.1f} GB')
"

# Configure memory limits
{
  "performance": {
    "memory_limit_mb": 1000,
    "batch_size": 500,
    "enable_garbage_collection": true
  }
}

# Process files in chunks
python run_smartrecon.py --chunk-size 1000 --input large_file.csv
```

### **Problem 3: Disk Space Issues**

#### **Symptoms:**
- `No space left on device`
- Temporary files filling disk

#### **Solutions:**

```bash
# Check disk space
df -h

# Clean temporary files
rm -rf /tmp/smartrecon_*
python -c "
import tempfile
import shutil
temp_dir = tempfile.gettempdir()
# Clean SmartRecon temp files
"

# Configure output location
{
  "output": {
    "directory": "/path/to/large/disk",
    "cleanup_temp_files": true
  }
}
```

---

## 🔄 Matching Algorithm Problems

### **Problem 1: No Exact Matches Found**

#### **Symptoms:**
- All transactions reported as unmatched
- Exact matching returns zero results

#### **Solutions:**

```bash
# Check amount tolerance
{
  "exact_matching": {
    "amount_tolerance": 0.01,     // Allow 1 cent difference
    "require_exact_amount": false // Allow tolerance matching
  }
}

# Verify date range settings
{
  "exact_matching": {
    "date_range_days": 7,         // Allow 7-day range
    "strict_date_matching": false
  }
}

# Debug matching process
python run_smartrecon.py --debug --exact-match --input file1.csv --gl file2.csv
```

### **Problem 2: Fuzzy Matching Too Aggressive**

#### **Symptoms:**
- Too many false positive matches
- Low-confidence matches being accepted

#### **Solutions:**

```bash
# Increase confidence thresholds
{
  "fuzzy_matching": {
    "similarity_threshold": 0.9,      // Increase from 0.8
    "confidence_threshold": 0.95,     // Increase from 0.85
    "max_suggestions": 5              // Reduce suggestions
  }
}

# Enable manual review mode
{
  "fuzzy_matching": {
    "require_manual_approval": true,
    "auto_accept_threshold": 0.98
  }
}
```

### **Problem 3: Performance Issues with Fuzzy Matching**

#### **Symptoms:**
- Fuzzy matching takes extremely long
- System becomes unresponsive during matching

#### **Solutions:**

```bash
# Optimize fuzzy matching performance
{
  "fuzzy_matching": {
    "use_fast_algorithm": true,
    "batch_processing": true,
    "parallel_processing": true,
    "max_comparisons": 10000
  }
}

# Reduce dataset size for fuzzy matching
{
  "fuzzy_matching": {
    "pre_filter_by_amount": true,
    "amount_filter_range": 0.1
  }
}
```

---

## 📊 Report Generation Issues

### **Problem 1: Report Files Not Generated**

#### **Symptoms:**
- No output files created
- Empty output directory

#### **Solutions:**

```bash
# Check output directory permissions
ls -la data/output/
mkdir -p data/output
chmod 755 data/output

# Verify output configuration
{
  "reporting": {
    "output_directory": "data/output",
    "generate_excel": true,
    "generate_csv": true
  }
}

# Debug report generation
python run_smartrecon.py --debug --generate-reports
```

### **Problem 2: Corrupted Excel Files**

#### **Symptoms:**
- Excel files won't open
- `File is corrupted` error

#### **Solutions:**

```bash
# Check openpyxl version
python -c "import openpyxl; print(openpyxl.__version__)"

# Update openpyxl
pip install --upgrade openpyxl

# Use alternative Excel engine
{
  "reporting": {
    "excel_engine": "xlsxwriter",  // Instead of openpyxl
    "excel_format": "xlsx"
  }
}
```

### **Problem 3: Large Report Files**

#### **Symptoms:**
- Report files are extremely large
- Excel files exceed row limits

#### **Solutions:**

```bash
# Split large reports
{
  "reporting": {
    "split_large_reports": true,
    "max_rows_per_file": 50000,
    "compression": true
  }
}

# Generate summary reports only
{
  "reporting": {
    "generate_summary_only": true,
    "include_detailed_matches": false
  }
}
```

---

## 🖥️ Environment-Specific Issues

### **Windows-Specific Issues**

#### **Problem 1: Long Path Names**
```bash
# Enable long path support
# Run as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Use shorter paths
mkdir C:\SR
cd C:\SR
git clone <repository>
```

#### **Problem 2: Antivirus Interference**
```bash
# Add SmartRecon directory to antivirus exclusions
# Windows Defender: Settings > Virus & threat protection > Exclusions
# Add folder: C:\path\to\SmartRecon
```

### **macOS-Specific Issues**

#### **Problem 1: Gatekeeper Restrictions**
```bash
# Allow SmartRecon to run
sudo xattr -r -d com.apple.quarantine /path/to/SmartRecon

# Alternative: Allow in System Preferences > Security & Privacy
```

#### **Problem 2: Python Version Conflicts**
```bash
# Use pyenv to manage Python versions
brew install pyenv
pyenv install 3.9.7
pyenv local 3.9.7
```

### **Linux-Specific Issues**

#### **Problem 1: Missing System Dependencies**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Arch Linux
sudo pacman -S base-devel python
```

---

## 🔧 Advanced Troubleshooting

### **Debug Mode Operation**

```bash
# Enable comprehensive debugging
python run_smartrecon.py --debug --verbose --log-level DEBUG

# Enable performance profiling
python run_smartrecon.py --profile --output-profile debug_profile.txt

# Trace execution
python -m trace --trace run_smartrecon.py > execution_trace.txt
```

### **Memory Profiling**

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler run_smartrecon.py

# Generate memory usage graph
mprof run run_smartrecon.py
mprof plot
```

### **Database Debugging (if applicable)**

```bash
# Check database connections
python -c "
from src.utils.database import DatabaseManager
db = DatabaseManager()
print('Database connection:', db.test_connection())
"

# Reset database state
python -c "
from src.utils.database import DatabaseManager
DatabaseManager.reset_database()
"
```

---

## 📞 Getting Additional Help

### **Self-Service Resources**

1. **Built-in Help System**
   ```bash
   python run_smartrecon.py --help
   python run_smartrecon.py --troubleshoot
   ```

2. **Log Analysis Tools**
   ```bash
   # Automated log analysis
   python -c "
   from src.utils.diagnostics import LogAnalyzer
   analyzer = LogAnalyzer()
   analyzer.analyze_recent_logs()
   analyzer.suggest_solutions()
   "
   ```

3. **System Information Collection**
   ```bash
   # Generate system report
   python run_smartrecon.py --system-info > system_report.txt
   ```

### **Documentation Resources**

- **Installation Guide:** `docs/INSTALLATION_GUIDE.md`
- **User Manual:** `STARTUP_MANUAL.md`
- **API Reference:** `docs/api/`
- **Configuration Guide:** `config/README.md`
- **Examples:** `examples/`

### **Community Support**

1. **GitHub Issues**
   - Search existing issues: https://github.com/yourusername/SmartRecon/issues
   - Create new issue with system report and logs

2. **Discussion Forums**
   - GitHub Discussions for general questions
   - Stack Overflow with tag `smartrecon`

### **Professional Support**

For enterprise users requiring dedicated support:

1. **Priority Support Channels**
   - Email: support@smartrecon.dev
   - Enterprise support portal

2. **Consulting Services**
   - Custom implementation assistance
   - Performance optimization consulting
   - Integration support

---

## 📋 Issue Report Template

When reporting issues, please include:

```markdown
## Issue Description
[Brief description of the problem]

## Environment Information
- Operating System: [Windows 10/macOS 12/Ubuntu 20.04]
- Python Version: [3.9.7]
- SmartRecon Version: [1.1.0]
- Installation Method: [pip/conda/source]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Error occurs]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Error Messages
```
[Include full error messages and stack traces]
```

## Log Files
[Attach relevant log files from logs/ directory]

## Configuration
[Include relevant configuration settings]

## Additional Context
[Any other relevant information]
```

---

## ✅ Resolution Checklist

Before seeking additional help, ensure you've tried:

- [ ] Reviewed this troubleshooting guide
- [ ] Checked log files for specific error messages
- [ ] Verified system requirements are met
- [ ] Tested with default configuration
- [ ] Tried with sample data provided
- [ ] Updated to latest version
- [ ] Searched existing documentation
- [ ] Reproduced issue in clean environment

---

**Troubleshooting Guide Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Coverage:** Comprehensive issue resolution for SmartRecon v1.0+  
**Support Level:** Community and Enterprise
