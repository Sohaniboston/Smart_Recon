@echo off
REM SmartRecon Windows Startup Script
REM This batch file makes it easy to run SmartRecon on Windows

echo.
echo ===============================================
echo            SmartRecon Quick Start
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check if we have the run script
if not exist "run_smartrecon.py" (
    echo ERROR: run_smartrecon.py not found
    echo Please ensure you're running this from the SmartRecon directory
    pause
    exit /b 1
)

REM Run SmartRecon
echo Starting SmartRecon...
echo.
python run_smartrecon.py %*

echo.
echo SmartRecon session ended.
pause
