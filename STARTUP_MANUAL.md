# 📘 SmartRecon Startup Scripts User Manual

**Version:** 1.0  
**Date:** July 21, 2025  
**For:** SmartRecon v1.0 Users

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Available Startup Scripts](#available-startup-scripts)
4. [Detailed Usage Guide](#detailed-usage-guide)
5. [Interactive Mode Guide](#interactive-mode-guide)
6. [Command Line Options](#command-line-options)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)
9. [Examples](#examples)
10. [FAQ](#faq)

---

## 🎯 Overview

SmartRecon provides multiple startup scripts to make it easy for users of all technical levels to run the financial reconciliation system. Whether you prefer clicking files, using command lines, or interactive menus, we have a solution for you.

### What These Scripts Do

The startup scripts handle:
- ✅ **Environment validation** - Check if SmartRecon is properly installed
- ✅ **Data file detection** - Find your CSV files automatically
- ✅ **Sample data generation** - Create test data if you don't have any
- ✅ **Core functionality testing** - Verify everything works correctly
- ✅ **Data processing** - Clean and analyze your financial data
- ✅ **Results presentation** - Show clear, actionable results

---

## 💻 System Requirements

### Operating Systems
- ✅ **Windows** 10/11 (any version)
- ✅ **macOS** 10.12+ (Sierra or later)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+, or equivalent)

### Software Requirements
- 🐍 **Python** 3.7 or higher
- 📦 **pandas** (for data processing)
- 📦 **numpy** (for numerical operations)
- 📦 **Standard library modules** (json, os, sys, pathlib)

### Hardware Requirements
- 💾 **RAM:** 2GB minimum, 4GB recommended
- 💽 **Storage:** 100MB for SmartRecon + space for your data files
- 🖥️ **Display:** Any resolution (terminal-based interface)

---

## 📁 Available Startup Scripts

SmartRecon provides **four** different ways to start the application:

| Script File | Platform | Usage | Best For |
|-------------|----------|--------|----------|
| `run_smartrecon.py` | All platforms | `python run_smartrecon.py` | Command line users |
| `run_smartrecon.bat` | Windows only | Double-click or `run_smartrecon.bat` | Windows GUI users |
| `run_smartrecon.sh` | Mac/Linux | `./run_smartrecon.sh` | Unix/Linux users |
| Direct import | Python environment | `import` statements | Developers |

### File Locations

All startup scripts are located in your SmartRecon root directory:

```
C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon\
├── run_smartrecon.py      ← Main Python script
├── run_smartrecon.bat     ← Windows batch file  
├── run_smartrecon.sh      ← Unix shell script
└── QUICKSTART.md          ← Quick reference guide
```

---

## 📖 Detailed Usage Guide

### Method 1: Python Script (All Platforms)

**Command:**
```bash
python run_smartrecon.py [options]
```

**Examples:**
```bash
# Interactive mode (default)
python run_smartrecon.py

# Automatic processing
python run_smartrecon.py --auto

# System testing only
python run_smartrecon.py --test

# Generate sample data only
python run_smartrecon.py --generate
```

### Method 2: Windows Batch File

**For Windows users who prefer double-clicking:**

1. **Navigate to SmartRecon folder**
   - Open File Explorer
   - Go to: `C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon\`

2. **Double-click** `run_smartrecon.bat`
   - Windows will open a command prompt
   - SmartRecon will start automatically

3. **Command line usage:**
   ```cmd
   cd "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon"
   run_smartrecon.bat --auto
   ```

### Method 3: Unix/Linux/Mac Shell Script

**For Mac and Linux users:**

1. **Make script executable** (first time only):
   ```bash
   chmod +x run_smartrecon.sh
   ```

2. **Run the script:**
   ```bash
   ./run_smartrecon.sh
   ```

3. **With options:**
   ```bash
   ./run_smartrecon.sh --auto
   ./run_smartrecon.sh --test
   ```

---

## 🎮 Interactive Mode Guide

Interactive Mode is the **recommended way** for new users to explore SmartRecon. It provides a user-friendly menu system.

### Starting Interactive Mode

```bash
python run_smartrecon.py
```

### Welcome Screen

```
╔═══════════════════════════════════════════════════════════════╗
║                    🎯 SMARTRECON v1.0                        ║
║           Intelligent Financial Reconciliation Assistant     ║
║                                                               ║
║   Ready to process your financial data with AI precision!    ║
╚═══════════════════════════════════════════════════════════════╝
```

### Menu Options Explained

#### Option 1: 🔍 Check Environment
**Purpose:** Validates your SmartRecon installation  
**What it checks:**
- ✅ Required directories exist (`src/`, `modules/`)
- ✅ Core Python files are present
- ✅ Import paths are correct

**Sample Output:**
```
🔍 Checking environment setup...
   ✅ src/ directory found
   ✅ config.py found
   ✅ data_cleaning.py found
   ✅ data_ingestion.py found
✅ Environment check passed!
```

#### Option 2: 🧪 Test Basic Functionality
**Purpose:** Tests core SmartRecon components  
**What it tests:**
- 📦 Module imports (Config, DataCleaner, DataIngestion)
- 🔧 Object instantiation
- ⚙️ Basic method calls

**Sample Output:**
```
🧪 Testing basic functionality...
✅ Core modules imported successfully
✅ Core components initialized successfully
```

#### Option 3: 📊 Process Bank Data
**Purpose:** Runs SmartRecon on your actual data  
**What it does:**
- 🔍 Finds CSV files in `bank_data/` folder
- 📥 Loads the data into memory
- 🧹 Cleans and standardizes the data
- 📊 Shows quality metrics and results

**Sample Output:**
```
📊 Processing bank data: 20250621_bank_data.csv
🔄 Loading and processing data...
   📥 Loaded 48 records from 20250621_bank_data.csv
   📋 Columns: ['date', 'description', 'withdrawal', 'deposit', 'balance']

✅ Data processing completed!
   🔧 Result keys available: ['cleaned_data', 'cleaning_stats', 'operations_performed', 'data_quality_score', 'original_records', 'final_records']
   📊 Records processed: 48 → 48
   🎯 Data quality score: 0.876
   ⚙️ Operations performed: 2
     ✓ column_name_standardization
     ✓ date_standardization_date

📋 Sample of cleaned data:
       date                                        description  withdrawal  deposit   balance
2025-05-13               DEBIT CARD PURCHASE - Torres PLC      1143.87      0.0   3856.13
2025-05-14                    MORTGAGE PAYMENT - Melendez LLC      1317.93      0.0   2538.20
2025-05-14  MORTGAGE PAYMENT - Morrow, Rivera and Martinez       135.81      0.0   2402.39
```

#### Option 4: 📁 List Available Data Files
**Purpose:** Shows what data files SmartRecon can find  
**Searches in:**
- `bank_data/` folder for bank statements
- `GL_data/` folder for general ledger data

**Sample Output:**
```
📁 Checking for data files...
   Found 2 bank data files in bank_data/
     📄 20250612_135232_bank_data.csv
     📄 20250621_143022_bank_data.csv
   Found 1 GL data files in GL_data/
     📄 20250621_143022_gl_data.csv
📊 Total files found: 3
```

#### Option 5: 📈 Generate Sample Data
**Purpose:** Creates test data for you to experiment with  
**What it creates:**
- Bank statement CSV with realistic transactions
- General ledger CSV with matching entries
- Files saved with timestamps

**Sample Output:**
```
📈 Generating sample data...
🔄 Running data generator...
✅ Sample data generated successfully!
   📤 Generated: bank_data/20250721_145533_bank_data.csv (50 records)
   📤 Generated: GL_data/20250721_145533_gl_data.csv (50 records)
✅ Sample data ready! You can now try option 3.
```

#### Option 6: 🔬 Run Simple Test
**Purpose:** Executes the test suite to verify everything works  
**What it runs:**
- Import tests
- Data processing tests  
- Output validation tests

**Sample Output:**
```
🔬 Running simple SmartRecon test...
✅ Simple test passed!
   📤 DataCleaner imported successfully
   📤 DataCleaner instance created
   📤 DataCleaner.clean_data() worked
   📤 Result keys: ['cleaned_data', 'cleaning_stats', 'operations_performed', 'data_quality_score']
```

#### Option 0: 👋 Exit
**Purpose:** Cleanly exits the interactive session

---

## 🖥️ Command Line Options

### Available Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--auto` | Automatic mode - runs all checks and processes data | `python run_smartrecon.py --auto` |
| `--test` | Test mode - only runs system validation tests | `python run_smartrecon.py --test` |
| `--generate` | Generate sample data and exit | `python run_smartrecon.py --generate` |
| `--help` | Show help message and exit | `python run_smartrecon.py --help` |

### Automatic Mode (`--auto`)

**Purpose:** Runs SmartRecon without user interaction  
**Ideal for:** Batch processing, automated scripts, quick validation

**What it does:**
1. ✅ Checks environment
2. ✅ Tests basic functionality  
3. 🔍 Looks for existing data files
4. 📈 Generates sample data if none found
5. 📊 Processes data automatically
6. 📋 Shows final results

**Example:**
```bash
python run_smartrecon.py --auto
```

**Sample Output:**
```
🎯 SMARTRECON v1.0
Intelligent Financial Reconciliation Assistant

🚀 SmartRecon Automatic Mode
==================================================

🔍 Checking environment setup...
✅ Environment check passed!

🧪 Testing basic functionality...
✅ Core modules imported successfully
✅ Core components initialized successfully

✅ All system checks passed!

📁 Checking for data files...
   Found 1 bank data files in bank_data/

🎯 Processing with 20250612_135232_bank_data.csv...
📊 Processing bank data: 20250612_135232_bank_data.csv
🔄 Loading and processing data...
   📥 Loaded 48 records from 20250612_135232_bank_data.csv
   📋 Columns: ['date', 'description', 'withdrawal', 'deposit', 'balance']

✅ Data processing completed!
   📊 Records processed: 48 → 48
   🎯 Data quality score: 0.876
   ⚙️ Operations performed: 2
     ✓ column_name_standardization
     ✓ date_standardization_date

🎯 Auto Mode Results: ✅ SUCCESS
```

### Test Mode (`--test`)

**Purpose:** Validates SmartRecon installation and functionality  
**Ideal for:** Troubleshooting, system verification, CI/CD

**What it tests:**
- Environment setup
- Module imports
- Basic functionality
- Data processing capability

**Example:**
```bash
python run_smartrecon.py --test
```

**Sample Output:**
```
🎯 SMARTRECON v1.0
Intelligent Financial Reconciliation Assistant

🔍 Checking environment setup...
✅ Environment check passed!

🧪 Testing basic functionality...
✅ Core modules imported successfully
✅ Core components initialized successfully

🔬 Running simple SmartRecon test...
✅ Simple test passed!
   📤 DataCleaner imported successfully
   📤 DataCleaner instance created
   📤 DataCleaner.clean_data() worked

🎯 Test Results: ✅ PASSED
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: "Python is not recognized"
**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Python:**
   - Windows: Download from [python.org](https://python.org)
   - Mac: `brew install python3` or download from python.org
   - Linux: `sudo apt install python3` (Ubuntu) or equivalent

2. **Add Python to PATH:**
   - Windows: Reinstall Python with "Add to PATH" checked
   - Mac/Linux: Add to `~/.bashrc` or `~/.zshrc`

#### Issue: "No module named 'pandas'"
**Symptoms:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solutions:**
```bash
# Install required packages
pip install pandas numpy

# Or install all requirements
pip install -r requirements.txt  # if file exists
```

#### Issue: "KeyError: 'original_records'" or similar key errors
**Symptoms:**
```
❌ Data processing failed: 'original_records'
KeyError: 'original_records'
```

**What this means:**
The SmartRecon data cleaning module returned results in a different format than expected.

**Solutions:**
1. **Updated startup script handles this automatically:**
   - The script now shows available keys for debugging
   - Look for "🔧 Result keys available: [...]" in the output

2. **Check if DataCleaner module needs updates:**
   ```bash
   python run_smartrecon.py --test
   ```

3. **Verify the SmartRecon modules are consistent:**
   - Ensure all modules are from the same version
   - Check if any modules were partially updated

#### Issue: "Permission denied" (Mac/Linux)
**Symptoms:**
```
-bash: ./run_smartrecon.sh: Permission denied
```

**Solution:**
```bash
chmod +x run_smartrecon.sh
./run_smartrecon.sh
```

#### Issue: "No data files found"
**Symptoms:**
```
❌ No bank data files found in bank_data/ directory
```

**Solutions:**
1. **Generate sample data:**
   ```bash
   python run_smartrecon.py --generate
   ```

2. **Add your own data:**
   - Create `bank_data/` folder if it doesn't exist
   - Copy your CSV files into `bank_data/`
   - Ensure CSV has columns like: date, description, amount

#### Issue: Script runs but shows errors
**Symptoms:**
- Import errors
- Processing failures
- KeyError messages
- Unexpected output

**Debugging Steps:**
1. **Run test mode first:**
   ```bash
   python run_smartrecon.py --test
   ```

2. **Check the error details:**
   - The startup script now shows available result keys for debugging
   - Look for messages like "🔧 Result keys available: [...]"

3. **Verify file structure:**
   ```
   Smart_Recon/
   ├── src/
   │   ├── config.py
   │   └── modules/
   │       ├── data_cleaning.py
   │       └── data_ingestion.py
   └── run_smartrecon.py
   ```

4. **Check Python version:**
   ```bash
   python --version  # Should be 3.7+
   ```

5. **Verify SmartRecon modules are working:**
   ```bash
   python run_smartrecon.py --test
   ```

### Getting Detailed Error Information

If you encounter errors, you can get more detailed information:

1. **Run with Python directly** (shows full stack traces):
   ```bash
   python -u run_smartrecon.py --test
   ```

2. **Check current directory:**
   ```bash
   # Windows
   dir

   # Mac/Linux  
   ls -la
   ```

3. **Verify file permissions** (Mac/Linux):
   ```bash
   ls -la run_smartrecon.*
   ```

---

## 🚀 Advanced Usage

### Running from Different Directories

You can run SmartRecon from any directory by specifying the full path:

```bash
# Windows
python "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon\run_smartrecon.py" --auto

# Mac/Linux
python "/path/to/Smart_Recon/run_smartrecon.py" --auto
```

### Integrating with Other Scripts

You can call SmartRecon from other Python scripts:

```python
import subprocess
import sys

# Run SmartRecon in auto mode
result = subprocess.run([
    sys.executable, 
    "run_smartrecon.py", 
    "--auto"
], capture_output=True, text=True)

if result.returncode == 0:
    print("SmartRecon succeeded!")
    print(result.stdout)
else:
    print("SmartRecon failed!")
    print(result.stderr)
```

### Batch Processing Multiple Files

For processing multiple files automatically:

```bash
# Process each CSV file in bank_data/
for file in bank_data/*.csv; do
    echo "Processing $file"
    python run_smartrecon.py --auto
done
```

### Scheduled Execution

You can schedule SmartRecon to run automatically:

**Windows (Task Scheduler):**
- Program: `python`
- Arguments: `"C:\path\to\run_smartrecon.py" --auto`
- Start in: `C:\path\to\Smart_Recon\`

**Mac/Linux (crontab):**
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/Smart_Recon && python run_smartrecon.py --auto >> smartrecon.log 2>&1
```

---

## 📚 Examples

### Example 1: First Time User

**Goal:** New user wants to try SmartRecon

**Steps:**
1. Open terminal/command prompt
2. Navigate to SmartRecon folder:
   ```bash
   cd "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon"
   ```
3. Run interactive mode:
   ```bash
   python run_smartrecon.py
   ```
4. Choose option 5 to generate sample data
5. Choose option 3 to process the data
6. Review results

### Example 2: Quick System Check

**Goal:** Verify SmartRecon is working correctly

**Steps:**
```bash
cd "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon"
python run_smartrecon.py --test
```

**Expected output:**
```
🎯 Test Results: ✅ PASSED
```

### Example 3: Automated Daily Processing

**Goal:** Process new data files automatically

**Steps:**
1. Copy new CSV files to `bank_data/` folder
2. Run automatic mode:
   ```bash
   python run_smartrecon.py --auto
   ```
3. Check results in output

### Example 4: Windows GUI User

**Goal:** User who prefers clicking files

**Steps:**
1. Open Windows Explorer
2. Navigate to `C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon\`
3. Double-click `run_smartrecon.bat`
4. Follow interactive menu

### Example 5: Batch Processing

**Goal:** Process multiple data files in sequence

**Create batch script `process_all.bat`:**
```batch
@echo off
echo Processing all bank data files...

for %%f in (bank_data\*.csv) do (
    echo Processing %%f
    python run_smartrecon.py --auto
    echo.
)

echo All files processed!
pause
```

---

## ❓ FAQ

### Q: Which startup script should I use?
**A:** Choose based on your preference:
- **New users:** Interactive mode (`python run_smartrecon.py`)
- **Windows users:** Double-click `run_smartrecon.bat`
- **Automation:** Use `--auto` flag
- **Developers:** Import modules directly

### Q: Can I run SmartRecon without data files?
**A:** Yes! Use option 5 in interactive mode or `--generate` flag to create sample data.

### Q: How do I add my own data files?
**A:** Copy your CSV files to the `bank_data/` folder. SmartRecon will automatically detect them.

### Q: What if I get import errors?
**A:** 
1. Check Python version (`python --version` should be 3.7+)
2. Install required packages (`pip install pandas numpy`)
3. Run from SmartRecon directory
4. Use test mode to diagnose issues

### Q: Can I customize the data processing?
**A:** Yes! Modify the configuration files in the `config/` folder or edit the Python modules directly.

### Q: How do I know if SmartRecon is working correctly?
**A:** Run `python run_smartrecon.py --test`. You should see "✅ PASSED" at the end.

### Q: What data formats does SmartRecon support?
**A:** Currently CSV files. Your CSV should have columns for date, description, and amount information.

### Q: Can I run SmartRecon on a schedule?
**A:** Yes! Use task schedulers (Windows) or cron jobs (Mac/Linux) with the `--auto` flag.

### Q: Where are the results saved?
**A:** Currently results are displayed on screen. Future versions will save to files automatically.

### Q: How do I update SmartRecon?
**A:** Download the latest version and replace the files, or use git pull if you cloned the repository.

---

## 📞 Support

If you need additional help:

1. **Check the logs** - Look for error messages in the terminal output
2. **Run test mode** - `python run_smartrecon.py --test` to diagnose issues  
3. **Review documentation** - Check `README.md` and `QUICKSTART.md`
4. **Submit issues** - Use GitHub issues for bug reports
5. **Contact support** - Email support@smartrecon.com

---

**📝 Document Version:** 1.0  
**📅 Last Updated:** July 21, 2025  
**✍️ Author:** SmartRecon Development Team  
**📧 Contact:** support@smartrecon.com
