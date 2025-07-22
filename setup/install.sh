#!/bin/bash
# SmartRecon Installation Script for Unix/Linux/macOS

echo "🚀 SmartRecon Installation and Setup"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "🐍 Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Run environment setup
echo "⚙️  Setting up SmartRecon environment..."
python3 startup.py

# Create sample data directory
echo "📁 Creating sample data directory..."
mkdir -p data/samples

# Make scripts executable
chmod +x smartrecon.py
chmod +x app.py

echo "✅ SmartRecon installation completed!"
echo ""
echo "🎯 Quick start:"
echo "  python3 smartrecon.py --help"
echo "  python3 smartrecon.py interactive"
echo "  python3 app.py examples"
