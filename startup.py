"""
SmartRecon Startup and Environment Setup

This module handles application initialization, environment validation,
and configuration setup for the SmartRecon application.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import platform
import importlib

# Application metadata
APP_INFO = {
    'name': 'SmartRecon',
    'version': '1.0.0',
    'description': 'Intelligent Financial Reconciliation Assistant',
    'author': 'SmartRecon Development Team',
    'license': 'MIT',
    'python_min_version': '3.8'
}

# Required dependencies
REQUIRED_PACKAGES = [
    'pandas>=1.3.0',
    'numpy>=1.21.0',
    'click>=8.0.0',
    'openpyxl>=3.0.0',
    'matplotlib>=3.4.0',
    'seaborn>=0.11.0',
    'chardet>=4.0.0',
    'fuzzywuzzy>=0.18.0',
    'python-levenshtein>=0.12.0',
    'jsonschema>=3.2.0'
]

# Optional dependencies  
OPTIONAL_PACKAGES = [
    'xlrd>=2.0.0',  # For older Excel files
    'xlsxwriter>=1.4.0',  # Alternative Excel writer
    'jinja2>=3.0.0',  # For HTML templates
    'plotly>=5.0.0',  # Interactive charts
    'dash>=2.0.0'  # Web dashboard
]


class EnvironmentValidator:
    """Validates and sets up the SmartRecon environment."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.python_version = platform.python_version()
        self.platform_info = platform.platform()
    
    def validate_python_version(self) -> bool:
        """Check if Python version meets requirements."""
        try:
            import sys
            
            major, minor = map(int, self.python_version.split('.')[:2])
            required_major, required_minor = map(int, APP_INFO['python_min_version'].split('.'))
            
            if (major, minor) >= (required_major, required_minor):
                return True
            else:
                self.issues.append(
                    f"Python {APP_INFO['python_min_version']}+ required, found {self.python_version}"
                )
                return False
                
        except Exception as e:
            self.issues.append(f"Could not determine Python version: {e}")
            return False
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are installed."""
        dependency_status = {}
        
        # Check required packages
        for package_spec in REQUIRED_PACKAGES:
            package_name = package_spec.split('>=')[0].split('==')[0]
            try:
                importlib.import_module(package_name)
                dependency_status[package_name] = True
            except ImportError:
                dependency_status[package_name] = False
                self.issues.append(f"Required package missing: {package_spec}")
        
        # Check optional packages
        for package_spec in OPTIONAL_PACKAGES:
            package_name = package_spec.split('>=')[0].split('==')[0]
            try:
                importlib.import_module(package_name)
                dependency_status[package_name] = True
            except ImportError:
                dependency_status[package_name] = False
                self.warnings.append(f"Optional package missing: {package_spec}")
        
        return dependency_status
    
    def validate_file_structure(self, base_path: Path) -> bool:
        """Validate SmartRecon file structure."""
        required_directories = [
            'src',
            'src/modules',
            'src/utils',
            'config'
        ]
        
        required_files = [
            'src/__init__.py',
            'src/main.py',
            'src/config.py',
            'src/modules/__init__.py',
            'src/modules/data_ingestion.py',
            'src/utils/__init__.py',
            'src/utils/logger.py'
        ]
        
        # Check directories
        for directory in required_directories:
            dir_path = base_path / directory
            if not dir_path.exists():
                self.issues.append(f"Missing directory: {directory}")
        
        # Check files
        for file_path in required_files:
            full_path = base_path / file_path
            if not full_path.exists():
                self.issues.append(f"Missing file: {file_path}")
        
        return len(self.issues) == 0
    
    def validate_configuration(self, config_path: Optional[Path] = None) -> bool:
        """Validate configuration files."""
        if config_path is None:
            config_path = Path('config/default_config.json')
        
        if not config_path.exists():
            self.warnings.append(f"Configuration file not found: {config_path}")
            return False
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Basic configuration validation
            required_sections = ['data_ingestion', 'matching', 'reporting']
            for section in required_sections:
                if section not in config_data:
                    self.warnings.append(f"Missing configuration section: {section}")
            
            return True
            
        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON in configuration file: {e}")
            return False
        except Exception as e:
            self.issues.append(f"Error reading configuration: {e}")
            return False
    
    def create_default_directories(self, base_path: Path):
        """Create default directories if they don't exist."""
        default_dirs = [
            'config',
            'data',
            'output',
            'logs',
            'reports',
            'temp'
        ]
        
        for directory in default_dirs:
            dir_path = base_path / directory
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"📁 Created directory: {directory}")
                except Exception as e:
                    self.warnings.append(f"Could not create directory {directory}: {e}")
    
    def generate_report(self) -> str:
        """Generate environment validation report."""
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                SmartRecon Environment Validation Report         ║
╚════════════════════════════════════════════════════════════════╝

🖥️  System Information:
   Platform: {self.platform_info}
   Python Version: {self.python_version}
   Required: {APP_INFO['python_min_version']}+

📦 Dependency Check:
"""
        
        # Add dependency status
        dependency_status = self.check_dependencies()
        for package, status in dependency_status.items():
            status_icon = "✅" if status else "❌"
            report += f"   {status_icon} {package}\n"
        
        # Add issues
        if self.issues:
            report += f"\n❌ Issues Found ({len(self.issues)}):\n"
            for issue in self.issues:
                report += f"   • {issue}\n"
        else:
            report += f"\n✅ No critical issues found!\n"
        
        # Add warnings
        if self.warnings:
            report += f"\n⚠️  Warnings ({len(self.warnings)}):\n"
            for warning in self.warnings:
                report += f"   • {warning}\n"
        
        return report


class ConfigurationManager:
    """Manages SmartRecon configuration setup and validation."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.config_dir = base_path / 'config'
    
    def create_default_config(self) -> Path:
        """Create default configuration file."""
        self.config_dir.mkdir(exist_ok=True)
        
        default_config = {
            "application": {
                "name": APP_INFO['name'],
                "version": APP_INFO['version'],
                "debug": False,
                "log_level": "INFO"
            },
            "data_ingestion": {
                "max_file_size_mb": 100,
                "encoding_detection": True,
                "auto_column_mapping": True,
                "data_quality_threshold": 0.8,
                "supported_formats": [".csv", ".xlsx", ".xls", ".txt"],
                "date_formats": [
                    "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d",
                    "%d-%m-%Y", "%m-%d-%Y", "%Y%m%d", "%d.%m.%Y"
                ]
            },
            "data_cleaning": {
                "remove_duplicates": True,
                "standardize_dates": True,
                "normalize_amounts": True,
                "handle_missing_values": True,
                "outlier_detection": True
            },
            "matching": {
                "exact_matching": {
                    "amount_tolerance": 0.01,
                    "date_tolerance_days": 3,
                    "reference_matching": True,
                    "description_matching": False
                },
                "fuzzy_matching": {
                    "similarity_threshold": 0.8,
                    "description_weight": 0.4,
                    "amount_weight": 0.4,
                    "date_weight": 0.2,
                    "enable_phonetic": True
                }
            },
            "reporting": {
                "default_format": "excel",
                "include_charts": True,
                "generate_summary": True,
                "export_unmatched": True,
                "chart_theme": "default"
            },
            "file_mappings": {
                "gl": {
                    "required_columns": ["date", "description", "amount"],
                    "optional_columns": ["account", "reference", "department"],
                    "column_mapping": {
                        "date": ["date", "transaction_date", "trans_date", "posting_date"],
                        "description": ["description", "memo", "narrative", "details"],
                        "amount": ["amount", "value", "debit_credit", "net_amount"],
                        "reference": ["reference", "ref", "document_number", "doc_ref"],
                        "account": ["account", "account_number", "gl_account"]
                    }
                },
                "bank": {
                    "required_columns": ["date", "description", "amount"],
                    "optional_columns": ["balance", "reference"],
                    "column_mapping": {
                        "date": ["date", "value_date", "booking_date", "transaction_date"],
                        "description": ["description", "reference", "memo", "narrative"],
                        "amount": ["amount", "debit", "credit", "transaction_amount"],
                        "balance": ["balance", "running_balance", "account_balance"]
                    }
                }
            }
        }
        
        config_file = self.config_dir / 'default_config.json'
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"📄 Created default configuration: {config_file}")
        return config_file
    
    def create_sample_data_config(self) -> Path:
        """Create sample data configuration for testing."""
        sample_config = {
            "sample_data": {
                "gl_sample": {
                    "file_name": "sample_gl.csv",
                    "rows": 100,
                    "columns": ["date", "description", "amount", "account", "reference"],
                    "date_range": ["2024-01-01", "2024-12-31"],
                    "amount_range": [-10000, 10000]
                },
                "bank_sample": {
                    "file_name": "sample_bank.csv", 
                    "rows": 120,
                    "columns": ["date", "description", "amount", "balance"],
                    "date_range": ["2024-01-01", "2024-12-31"],
                    "amount_range": [-8000, 8000]
                }
            }
        }
        
        sample_config_file = self.config_dir / 'sample_config.json'
        with open(sample_config_file, 'w') as f:
            json.dump(sample_config, f, indent=2)
        
        return sample_config_file


def setup_smartrecon_environment(force_setup: bool = False) -> bool:
    """
    Set up SmartRecon environment and validate dependencies.
    
    Args:
        force_setup: Force recreation of configuration files
        
    Returns:
        bool: True if setup successful, False otherwise
    """
    try:
        base_path = Path.cwd()
        
        print(f"🚀 Setting up SmartRecon environment in: {base_path}")
        
        # Initialize validator
        validator = EnvironmentValidator()
        
        # Validate Python version
        if not validator.validate_python_version():
            print("❌ Python version check failed!")
            return False
        
        # Validate file structure
        validator.validate_file_structure(base_path)
        
        # Create default directories
        validator.create_default_directories(base_path)
        
        # Check dependencies
        dependency_status = validator.check_dependencies()
        
        # Validate/create configuration
        config_manager = ConfigurationManager(base_path)
        config_file = base_path / 'config' / 'default_config.json'
        
        if not config_file.exists() or force_setup:
            config_manager.create_default_config()
            config_manager.create_sample_data_config()
        
        validator.validate_configuration(config_file)
        
        # Generate and display report
        report = validator.generate_report()
        print(report)
        
        # Check if critical issues exist
        if validator.issues:
            print("\n❌ Critical issues found! Please resolve before using SmartRecon.")
            print("\n💡 Installation help:")
            print("   pip install -r requirements.txt")
            print("   conda install --file conda-requirements.txt")
            return False
        
        if validator.warnings:
            print(f"\n⚠️  {len(validator.warnings)} warnings found, but SmartRecon should work correctly.")
        
        print("\n✅ SmartRecon environment setup completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Validate data files: python smartrecon.py validate your_file.csv")
        print("   2. Run reconciliation: python smartrecon.py reconcile gl.csv bank.csv")
        print("   3. Try interactive mode: python smartrecon.py interactive")
        
        return True
        
    except Exception as e:
        print(f"💥 Environment setup failed: {e}")
        return False


def main():
    """Main function for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartRecon Environment Setup")
    parser.add_argument('--force', action='store_true', 
                       help='Force recreation of configuration files')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check environment, do not create files')
    
    args = parser.parse_args()
    
    if args.check_only:
        validator = EnvironmentValidator()
        base_path = Path.cwd()
        
        validator.validate_python_version()
        validator.validate_file_structure(base_path)
        validator.check_dependencies()
        validator.validate_configuration()
        
        report = validator.generate_report()
        print(report)
        
        if validator.issues:
            sys.exit(1)
    else:
        success = setup_smartrecon_environment(force_setup=args.force)
        if not success:
            sys.exit(1)


if __name__ == '__main__':
    main()
