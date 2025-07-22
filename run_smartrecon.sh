#!/bin/bash
# SmartRecon Unix/Linux/Mac Startup Script
# This script makes it easy to run SmartRecon on Unix-like systems

echo ""
echo "==============================================="
echo "           SmartRecon Quick Start"
echo "==============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.7+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we have the run script
if [ ! -f "run_smartrecon.py" ]; then
    echo "ERROR: run_smartrecon.py not found"
    echo "Please ensure you're running this from the SmartRecon directory"
    exit 1
fi

# Run SmartRecon
echo "Starting SmartRecon..."
echo ""
$PYTHON_CMD run_smartrecon.py "$@"

echo ""
echo "SmartRecon session ended."
