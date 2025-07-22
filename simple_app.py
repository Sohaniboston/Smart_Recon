#!/usr/bin/env python3
"""
Minimal SmartRecon App for testing
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Starting SmartRecon...")

print("Step 1: Testing basic imports...")
try:
    import pandas as pd
    import numpy as np
    import click
    print("✅ Basic dependencies imported")
except Exception as e:
    print(f"❌ Basic dependencies failed: {e}")
    sys.exit(1)

print("Step 2: Testing config import...")
try:
    from config import Config
    print("✅ Config imported")
except Exception as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)

print("Step 3: Testing data_ingestion import...")
try:
    from modules.data_ingestion import DataIngestion
    print("✅ DataIngestion imported")
except Exception as e:
    print(f"❌ DataIngestion import failed: {e}")
    sys.exit(1)

print("Step 4: Testing data_cleaning import...")
try:
    from modules.data_cleaning import DataCleaner
    print("✅ DataCleaner imported")
except Exception as e:
    print(f"❌ DataCleaner import failed: {e}")
    sys.exit(1)

print("Step 5: Creating simple CLI...")
@click.command()
@click.option('--version', is_flag=True, help='Show version')
def simple_app(version):
    """Simple SmartRecon test app."""
    if version:
        click.echo("SmartRecon v1.0.0 - Test Version")
    else:
        click.echo("🎉 SmartRecon is working!")
        click.echo("All imports successful!")
        click.echo("Ready for financial reconciliation!")

if __name__ == '__main__':
    print("Step 6: Running CLI...")
    simple_app()
