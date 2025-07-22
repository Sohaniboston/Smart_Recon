#!/usr/bin/env python3
"""
SmartRecon Launcher Script

Simple entry point that automatically detects and runs the appropriate
main application module.

Usage:
    python smartrecon.py [COMMAND] [OPTIONS]
    python smartrecon.py --help
"""

import sys
import os
from pathlib import Path

# Add the current directory and src to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / 'src'))

def main():
    """Main launcher function."""
    try:
        # Try to import and run the enhanced app.py
        try:
            from app import main as app_main
            app_main()
        except ImportError:
            # Fallback to original main.py
            from src.main import main as src_main
            src_main()
    
    except KeyboardInterrupt:
        print("\n❌ Application interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Failed to start SmartRecon: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
