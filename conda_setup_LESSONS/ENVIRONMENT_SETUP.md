# SmartRecon Environment Setup Guide

## Prerequisites
- Anaconda or Miniconda installed
- Git (for cloning the repository)

## Option 1: Complete Environment Recreation (Recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sohaniboston/Smart_Recon.git
cd Smart_Recon
```

### Step 2: Create Environment from YAML
```bash
# Create environment from the complete specification
conda env create -f environment_complete.yml

# Activate the environment
conda activate smart_recon2
```

### Step 3: Verify Installation
```bash
# Test that the environment works
python -c "import pandas, numpy, fuzzywuzzy, click; print('Environment setup successful!')"
```

## Option 2: Manual Environment Setup

### Step 1: Create Base Environment
```bash
# Create new conda environment
conda create -n smart_recon2 python=3.9

# Activate environment
conda activate smart_recon2
```

### Step 2: Install Conda Packages
```bash
# Install main dependencies via conda
conda install -c conda-forge pandas numpy matplotlib seaborn openpyxl xlrd click colorama
```

### Step 3: Install Pip Packages
```bash
# Install remaining packages via pip
pip install -r requirements.txt
```

## Option 3: Development Environment

### Step 1: Use Environment File
```bash
# Create from existing environment file
conda env create -f smart_recon_environment.yml

# Rename environment if needed
conda create --name smart_recon2 --clone smart_recon_apps
```

### Step 2: Install Additional Pip Packages
```bash
conda activate smart_recon2
pip install -r requirements.txt
```

## Environment Updates

### Export Updated Environment
```bash
# Export current environment state
conda env export > environment_updated.yml
```

### Share with Team
```bash
# Create portable version (cross-platform) - removes build strings
conda env export --no-builds > environment_portable.yml

# Alternative: Use from-history if environment was built manually
conda env export --from-history > environment_history.yml

# Or use the custom clean export script
python create_clean_env.py
```

## Troubleshooting

### Common Issues
1. **Build strings still showing with --from-history**: Environment may have been created by cloning/importing, use `--no-builds` instead
2. **Platform-specific packages**: Use `conda env export --no-builds` for cross-platform compatibility
3. **Channel conflicts**: Ensure proper channel priority
4. **--from-history shows build strings**: Use `conda env export --no-builds` or the custom clean export script

### Platform Notes
- **Windows**: Use provided environment files directly
- **macOS/Linux**: Use `environment_portable.yml` for better compatibility

## Verification Commands
```bash
# Check conda packages
conda list

# Check pip packages
pip list

# Test core functionality
python -c "
import pandas as pd
import numpy as np
import fuzzywuzzy
import click
from src.config import Config
print('All dependencies loaded successfully!')
"
```

## Quick Start
Once environment is set up:
```bash
# Run the application
python app.py --help

# Or use the startup script
python run_smartrecon.py
```
