# SmartRecon Installation Guide

**Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Prerequisites:** Python 3.8+, Windows/Linux/macOS  

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Environment Setup](#environment-setup)
4. [Verification](#verification)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### **Minimum Requirements**
- **Operating System:** Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python Version:** 3.8 or higher
- **Memory:** 4GB RAM minimum (8GB recommended)
- **Storage:** 2GB free disk space
- **Processor:** Intel i3 or equivalent

### **Recommended Requirements**
- **Operating System:** Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python Version:** 3.9 or higher
- **Memory:** 8GB RAM or more
- **Storage:** 5GB free disk space
- **Processor:** Intel i5 or equivalent (for large datasets)

### **Required Dependencies**
SmartRecon requires the following Python packages (automatically installed):
- pandas (>= 1.5.0) - Data manipulation and analysis
- numpy (>= 1.21.0) - Numerical computing
- openpyxl (>= 3.0.0) - Excel file handling
- python-Levenshtein (>= 0.12.0) - String similarity algorithms
- fuzzywuzzy (>= 0.18.0) - Fuzzy string matching
- psutil (>= 5.8.0) - Performance monitoring
- click (>= 8.0.0) - Command line interface

---

## 🚀 Installation Methods

### **Method 1: Standard Installation (Recommended)**

#### **Step 1: Download SmartRecon**
```bash
# Option A: Git Clone (if you have git)
git clone https://github.com/yourusername/SmartRecon.git
cd SmartRecon

# Option B: Download ZIP file
# Download from GitHub and extract to desired directory
```

#### **Step 2: Install Python Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt

# Alternative: Install with setup.py
python setup.py install
```

#### **Step 3: Verify Installation**
```bash
# Run the installation verification
python run_smartrecon.py --test

# Or run a simple test
python -c "from src.config import Config; print('Installation successful!')"
```

### **Method 2: Conda Environment Installation (Recommended for Data Scientists)**

#### **Step 1: Create Conda Environment**
```bash
# Create environment from provided YAML file
conda env create -f smart_recon_environment.yml

# Activate the environment
conda activate smart_recon_apps
```

#### **Step 2: Verify Conda Installation**
```bash
# Test the conda environment
python run_smartrecon.py --version
```

### **Method 3: Virtual Environment Installation**

#### **Step 1: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv smartrecon_env

# Activate environment (Windows)
smartrecon_env\Scripts\activate

# Activate environment (macOS/Linux)
source smartrecon_env/bin/activate
```

#### **Step 2: Install Dependencies**
```bash
# Install SmartRecon in virtual environment
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup

### **Configuration File Setup**

#### **Step 1: Create Configuration Directory**
```bash
# Configuration files are located in config/
ls config/
# Should show: default_config.json
```

#### **Step 2: Customize Configuration (Optional)**
```bash
# Copy default configuration for customization
cp config/default_config.json config/my_config.json

# Edit your custom configuration
# See Configuration section below for details
```

### **Data Directory Setup**

#### **Step 1: Create Data Directories**
```bash
# Create directories for your data files
mkdir -p data/input
mkdir -p data/output
mkdir -p data/samples
```

#### **Step 2: Test Data Generation**
```bash
# Generate sample data for testing
python generate_financial_data.py
```

---

## ✅ Verification

### **Quick Verification Test**

#### **Step 1: Run Installation Test**
```bash
# Run the built-in test mode
python run_smartrecon.py --test

# Expected output:
# ✅ SmartRecon Installation Test
# ✅ Configuration loaded successfully
# ✅ All modules imported successfully
# ✅ Sample data generated successfully
# ✅ Installation verified - Ready to use!
```

#### **Step 2: Run Interactive Mode**
```bash
# Start SmartRecon interactive mode
python run_smartrecon.py

# You should see the main menu:
# SmartRecon - Financial Data Reconciliation Tool
# 1. Data Ingestion
# 2. Data Cleaning  
# 3. Exact Matching
# 4. Fuzzy Matching
# 5. Generate Reports
# 6. Configuration
# Q. Quit
```

### **Advanced Verification Test**

#### **Step 1: Process Sample Data**
```bash
# Run a complete reconciliation test
python run_smartrecon.py --auto --input examples/sample_bank_data.csv --gl examples/sample_gl_data.csv --output data/output/
```

#### **Step 2: Check Output Files**
```bash
# Verify output files were created
ls data/output/
# Should show reconciliation reports and match results
```

---

## 🔧 Configuration

### **Basic Configuration**

SmartRecon uses JSON-based configuration files located in the `config/` directory.

#### **Default Configuration Structure**
```json
{
  "data_ingestion": {
    "supported_formats": ["csv", "xlsx", "xls"],
    "encoding": "utf-8",
    "max_file_size_mb": 100
  },
  "data_cleaning": {
    "date_formats": ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"],
    "amount_tolerance": 0.01,
    "duplicate_threshold": 0.95
  },
  "exact_matching": {
    "amount_tolerance": 0.01,
    "date_range_days": 3,
    "require_reference_match": false
  },
  "fuzzy_matching": {
    "similarity_threshold": 0.8,
    "confidence_threshold": 0.85,
    "max_suggestions": 10
  },
  "performance": {
    "enable_monitoring": true,
    "batch_size": 1000,
    "memory_limit_mb": 1000
  }
}
```

#### **Custom Configuration**
```bash
# Create your own configuration file
cp config/default_config.json config/production_config.json

# Use custom configuration
python run_smartrecon.py --config config/production_config.json
```

### **Column Mapping Configuration**

Configure how SmartRecon maps columns in your data files:

```json
{
  "column_mappings": {
    "bank_data": {
      "date": ["Date", "Transaction Date", "Value Date"],
      "amount": ["Amount", "Debit", "Credit", "Transaction Amount"],
      "description": ["Description", "Details", "Memo", "Reference"],
      "reference": ["Reference", "Transaction ID", "Check Number"]
    },
    "gl_data": {
      "date": ["GL Date", "Posting Date", "Transaction Date"],
      "amount": ["Amount", "Debit Amount", "Credit Amount"],
      "description": ["Description", "GL Description", "Account Description"],
      "account": ["Account", "Account Number", "GL Account"]
    }
  }
}
```

---

## 🔍 Troubleshooting

### **Common Installation Issues**

#### **Issue 1: Python Not Found**
```bash
# Error: 'python' is not recognized as an internal or external command
# Solution: Install Python or check PATH environment variable

# Check if Python is installed
python --version
# or
python3 --version

# If not installed, download from https://python.org
```

#### **Issue 2: Permission Denied**
```bash
# Error: PermissionError: [Errno 13] Permission denied
# Solution: Run with appropriate permissions

# Windows: Run as Administrator
# macOS/Linux: Use sudo if necessary
sudo pip install -r requirements.txt
```

#### **Issue 3: Package Installation Failures**
```bash
# Error: Failed building wheel for python-Levenshtein
# Solution: Install Microsoft Visual C++ Build Tools (Windows)

# Windows: Install Visual Studio Build Tools
# macOS: Install Xcode Command Line Tools
xcode-select --install

# Linux: Install build essentials
sudo apt-get install build-essential
```

#### **Issue 4: Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Run from correct directory and check PYTHONPATH

# Ensure you're in the SmartRecon root directory
pwd
# Should end with /SmartRecon

# Check if src directory exists
ls src/
```

### **Runtime Issues**

#### **Issue 1: Configuration File Not Found**
```bash
# Error: Configuration file not found
# Solution: Ensure config/default_config.json exists

# Check config directory
ls config/
# If missing, reinstall or download from repository
```

#### **Issue 2: Memory Errors with Large Files**
```bash
# Error: MemoryError or out of memory
# Solution: Adjust batch size in configuration

# Edit config file to reduce batch_size
{
  "performance": {
    "batch_size": 500,
    "memory_limit_mb": 500
  }
}
```

#### **Issue 3: Encoding Errors**
```bash
# Error: UnicodeDecodeError
# Solution: Specify correct encoding in configuration

# Try different encodings
{
  "data_ingestion": {
    "encoding": "utf-8-sig"  // or "latin-1", "cp1252"
  }
}
```

### **Performance Issues**

#### **Issue 1: Slow Processing**
```bash
# Solution: Enable performance monitoring and optimization
{
  "performance": {
    "enable_monitoring": true,
    "batch_size": 2000,
    "parallel_processing": true
  }
}
```

#### **Issue 2: Large File Handling**
```bash
# For files larger than 100MB, increase limits
{
  "data_ingestion": {
    "max_file_size_mb": 500,
    "chunk_size": 10000
  }
}
```

---

## 📞 Getting Help

### **Built-in Help**
```bash
# Access built-in help system
python run_smartrecon.py --help

# Interactive help within the application
python run_smartrecon.py
# Select option 'H' for Help
```

### **Log Files**
SmartRecon creates detailed log files for troubleshooting:
```bash
# Check log files in logs/ directory
ls logs/
# smartrecon_YYYY-MM-DD.log contains detailed execution logs
```

### **Documentation Resources**
- **User Guide:** `docs/user_guide/`
- **API Reference:** `docs/api/`
- **Examples:** `examples/`
- **Configuration Templates:** `config/`

### **Support Channels**
- **GitHub Issues:** Report bugs and request features
- **Documentation:** Check `STARTUP_MANUAL.md` for detailed usage instructions
- **Examples:** Review sample implementations in `examples/` directory

---

## 🔄 Updates and Maintenance

### **Updating SmartRecon**
```bash
# Pull latest updates (if using git)
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Verify update
python run_smartrecon.py --version
```

### **Backup Configuration**
```bash
# Backup your custom configurations
cp config/my_config.json config/backup/my_config_backup.json
```

---

## ✅ Next Steps

After successful installation:

1. **Read the Quick Start Guide:** `QUICKSTART.md`
2. **Review the User Manual:** `STARTUP_MANUAL.md`
3. **Explore Examples:** Check `examples/` directory
4. **Generate Sample Data:** Run `generate_financial_data.py`
5. **Start Reconciliation:** Begin with `python run_smartrecon.py`

**Congratulations! SmartRecon is now installed and ready to use.**

---

**Installation Guide Version:** 1.1.0  
**Last Updated:** July 29, 2025  
**Compatible with:** SmartRecon v1.0+
