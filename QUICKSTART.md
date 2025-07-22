# 🚀 SmartRecon Quick Start Guide

This guide shows you how to quickly start using SmartRecon with the provided startup scripts.

## 📋 Quick Start Options

### Option 1: Interactive Mode (Recommended for beginners)
```bash
# Windows
run_smartrecon.bat

# Mac/Linux  
./run_smartrecon.sh

# Direct Python
python run_smartrecon.py
```

### Option 2: Automatic Mode (For quick testing)
```bash
# Windows
run_smartrecon.bat --auto

# Mac/Linux
./run_smartrecon.sh --auto

# Direct Python
python run_smartrecon.py --auto
```

### Option 3: Test Mode (Check if everything works)
```bash
python run_smartrecon.py --test
```

## 🎯 What Each Mode Does

### Interactive Mode
- Shows a menu with options 1-6
- Lets you explore SmartRecon step by step
- Perfect for learning and experimenting

**Menu Options:**
1. **🔍 Check environment** - Verifies all files are in place
2. **🧪 Test basic functionality** - Tests core SmartRecon modules  
3. **📊 Process bank data** - Runs SmartRecon on your data
4. **📁 List available data files** - Shows what data files you have
5. **📈 Generate sample data** - Creates test data to work with
6. **🔬 Run simple test** - Runs the existing test suite

### Automatic Mode (`--auto`)
- Runs all checks automatically
- Generates sample data if none exists
- Processes data and shows results
- Perfect for quick validation

### Test Mode (`--test`)
- Only runs system tests
- Shows pass/fail results
- Good for troubleshooting

## 📁 Expected Directory Structure

```
Smart_Recon/
├── run_smartrecon.py      ← Main startup script
├── run_smartrecon.bat     ← Windows batch file
├── run_smartrecon.sh      ← Unix/Linux/Mac shell script
├── src/                   ← Core SmartRecon code
│   ├── config.py
│   └── modules/
│       ├── data_cleaning.py
│       └── data_ingestion.py
├── bank_data/             ← Your bank CSV files
│   └── *.csv
├── GL_data/              ← Your GL CSV files (optional)
│   └── *.csv
└── generate_financial_data.py  ← Sample data generator
```

## 📊 Sample Data

If you don't have data files, the startup script can generate sample data:

1. **In Interactive Mode:** Choose option 5
2. **Command line:** `python run_smartrecon.py --generate`

This creates:
- `bank_data/YYYYMMDD_HHMMSS_bank_data.csv` - Sample bank transactions
- `GL_data/YYYYMMDD_HHMMSS_gl_data.csv` - Sample GL entries

## 🔧 Troubleshooting

### "Python not found" Error
- **Windows:** Install Python from python.org, make sure "Add to PATH" is checked
- **Mac:** Install via Homebrew: `brew install python`
- **Linux:** Install via package manager: `sudo apt install python3` (Ubuntu/Debian)

### "Module not found" Error
- Make sure you're in the SmartRecon directory
- Check that `src/` folder exists with the required files

### "No data files found" Error  
- Run with option 5 in interactive mode to generate sample data
- Or place your CSV files in `bank_data/` folder

### Permission Denied (Unix/Mac)
```bash
chmod +x run_smartrecon.sh
./run_smartrecon.sh
```

## 📈 Expected Output

When everything works correctly, you should see:

```
🎯 SMARTRECON v1.0
Intelligent Financial Reconciliation Assistant

🔍 Checking environment setup...
✅ Environment check passed!

🧪 Testing basic functionality...
✅ Core modules imported successfully
✅ Core components initialized successfully

📊 Processing bank data: 20250621_bank_data.csv
📥 Loaded 48 records from 20250621_bank_data.csv
📋 Columns: ['date', 'description', 'withdrawal', 'deposit', 'balance']

✅ Data processing completed!
📊 Records processed: 48 → 48
🎯 Data quality score: 0.876
⚙️ Operations performed: 2
  ✓ column_name_standardization
  ✓ date_standardization_date
```

## 🎯 Next Steps

Once the startup script works:

1. **Try with your own data** - Place CSV files in `bank_data/` folder
2. **Explore the results** - Look at the cleaned data output
3. **Check the main README.md** - Learn about advanced features
4. **Customize configuration** - Modify `config/default_config.json`

## 🆘 Getting Help

If you encounter issues:

1. Run `python run_smartrecon.py --test` to diagnose problems
2. Check the main README.md for detailed documentation  
3. Look at the generated log files for error details
4. Ensure all dependencies are installed

**Happy reconciling! 🎉**
