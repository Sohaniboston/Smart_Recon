@echo off
REM SmartRecon Installation Script for Windows
REM Created on 2025.07.17 
echo 🚀 SmartRecon Installation and Setup
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Display Python version
echo 🐍 Python version:
python --version

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  pip install failed, trying with --user flag...
    pip install --user -r requirements.txt
)

REM Run environment setup
echo ⚙️  Setting up SmartRecon environment...
python startup.py

REM Create sample data directory
echo 📁 Creating sample data directory...
if not exist "data\samples" mkdir "data\samples"

echo ✅ SmartRecon installation completed!
echo.
echo 🎯 Quick start:
echo   python smartrecon.py --help
echo   python smartrecon.py interactive  
echo   python app.py examples
echo.
pause
