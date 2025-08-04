#!/usr/bin/env python3
"""
SmartRecon Production Setup Script
Automates the setup of production environment for real-world financial data reconciliation
"""

import os
import sys
from pathlib import Path
import json
import shutil
from datetime import datetime

class ProductionSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.setup_complete = False
        
    def create_production_directories(self):
        """Create all necessary production directories"""
        print("🏗️  Creating production directory structure...")
        
        directories = [
            "prod_data",
            "prod_data/gl_data",
            "prod_data/bank_data", 
            "prod_data/output",
            "prod_data/archive",
            "prod_data/logs",
            "prod_data/backups"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {directory}")
        
        return True
    
    def create_sample_data_templates(self):
        """Create sample data templates for user reference"""
        print("\n📋 Creating sample data templates...")
        
        # GL Template
        gl_template = """Date,Description,Amount,Account,Reference
2025-01-15,"Payment to ABC Corp",1500.00,"1001","GL001"
2025-01-16,"Bank transfer",2250.75,"1001","GL002"
2025-01-17,"Invoice payment",-850.50,"1001","GL003"
2025-01-18,"Deposit",3200.00,"1001","GL004"
2025-01-19,"Service fee",-25.00,"1001","GL005"
"""
        
        # Bank Template
        bank_template = """Date,Description,Debit,Credit,Balance,Reference
2025-01-15,"ABC CORP PAYMENT",0.00,1500.00,25650.00,"BNK001"
2025-01-16,"TRANSFER IN",0.00,2250.75,27900.75,"BNK002"
2025-01-17,"PAYMENT OUT",850.50,0.00,27050.25,"BNK003"
2025-01-18,"DEPOSIT",0.00,3200.00,30250.25,"BNK004"
2025-01-19,"SERVICE FEE",25.00,0.00,30225.25,"BNK005"
"""
        
        # Write templates
        with open(self.project_root / "prod_data" / "gl_data" / "TEMPLATE_GL_Data.csv", "w") as f:
            f.write(gl_template)
        print("   ✅ Created: GL data template")
        
        with open(self.project_root / "prod_data" / "bank_data" / "TEMPLATE_Bank_Data.csv", "w") as f:
            f.write(bank_template)
        print("   ✅ Created: Bank data template")
        
        return True
    
    def create_production_scripts(self):
        """Create production operation scripts"""
        print("\n🔧 Creating production operation scripts...")
        
        # Daily reconciliation script
        daily_script = """@echo off
REM Daily SmartRecon Reconciliation Script
REM Run this script each morning after placing new data files

echo Starting Daily SmartRecon Reconciliation...
echo Date: %date% Time: %time%

REM Navigate to SmartRecon directory
cd /d "c:\\Users\\so_ho\\Desktop\\00_PythonWIP\\Smart_Recon"

REM Activate conda environment
call conda activate smart_recon_env

REM Run quick validation
echo Running system validation...
python quick_test.py

REM Start interactive reconciliation
echo Starting reconciliation process...
python run_smartrecon.py

echo Reconciliation complete!
pause
"""
        
        with open(self.project_root / "daily_reconciliation.bat", "w") as f:
            f.write(daily_script)
        print("   ✅ Created: daily_reconciliation.bat")
        
        # Validation script
        validation_script = """@echo off
REM SmartRecon System Validation Script
REM Run this to verify system is working properly

echo SmartRecon System Validation
echo =============================

cd /d "c:\\Users\\so_ho\\Desktop\\00_PythonWIP\\Smart_Recon"
call conda activate smart_recon_env

echo Running comprehensive validation...
python quick_test.py

echo.
echo Validation complete!
pause
"""
        
        with open(self.project_root / "validate_system.bat", "w") as f:
            f.write(validation_script)
        print("   ✅ Created: validate_system.bat")
        
        return True
    
    def create_readme_for_production(self):
        """Create production-specific README"""
        print("\n📖 Creating production README...")
        
        readme_content = """# SmartRecon Production Environment

## Quick Start
1. Place your GL data files in: `prod_data/gl_data/`
2. Place your bank data files in: `prod_data/bank_data/`
3. Double-click `daily_reconciliation.bat` to start
4. Follow the interactive prompts

## File Naming Convention
- GL files: `GL_YYYY-MM-DD.csv` (e.g., GL_2025-07-30.csv)
- Bank files: `Bank_YYYY-MM-DD.csv` (e.g., Bank_2025-07-30.csv)

## Data Format Requirements
- See TEMPLATE files in gl_data and bank_data directories
- Ensure Date, Description, Amount columns are present
- Use consistent date formats (YYYY-MM-DD recommended)

## Output Locations
- Results: `prod_data/output/`
- Logs: `prod_data/logs/`
- Archives: `prod_data/archive/`

## Daily Workflow
1. Export/download latest financial data
2. Save files in appropriate directories
3. Run `daily_reconciliation.bat`
4. Review reconciliation results
5. Investigate exceptions
6. Archive completed reconciliations

## Troubleshooting
- Run `validate_system.bat` if issues occur
- Check logs in `prod_data/logs/`
- Review configuration in `production_config.json`
- See PRODUCTION_DEPLOYMENT_GUIDE.md for detailed help

## Support
- Complete documentation in project root
- Sample data templates in data directories
- Configuration examples in config files
"""
        
        with open(self.project_root / "prod_data" / "README_PRODUCTION.md", "w") as f:
            f.write(readme_content)
        print("   ✅ Created: Production README")
        
        return True
    
    def verify_configuration(self):
        """Verify production configuration exists and is valid"""
        print("\n⚙️  Verifying production configuration...")
        
        config_file = self.project_root / "production_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print("   ✅ Production configuration verified")
                return True
            except json.JSONDecodeError:
                print("   ❌ Production configuration invalid JSON")
                return False
        else:
            print("   ❌ Production configuration not found")
            return False
    
    def run_setup(self):
        """Execute complete production setup"""
        print("🚀 SMARTRECON PRODUCTION SETUP")
        print("=" * 50)
        print("Setting up production environment for real-world financial data reconciliation...")
        print()
        
        # Execute setup steps
        steps = [
            ("Creating directories", self.create_production_directories),
            ("Creating sample templates", self.create_sample_data_templates),
            ("Creating operation scripts", self.create_production_scripts),
            ("Creating documentation", self.create_readme_for_production),
            ("Verifying configuration", self.verify_configuration)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            try:
                result = step_func()
                if not result:
                    all_success = False
            except Exception as e:
                print(f"   ❌ Error in {step_name}: {e}")
                all_success = False
        
        print("\n" + "=" * 50)
        if all_success:
            print("🎉 PRODUCTION SETUP COMPLETE!")
            print("\n✅ Your SmartRecon production environment is ready!")
            print("\n📋 Next Steps:")
            print("   1. Review PRODUCTION_DEPLOYMENT_GUIDE.md for detailed instructions")
            print("   2. Customize production_config.json for your requirements")
            print("   3. Place your data files in the prod_data directories")
            print("   4. Run daily_reconciliation.bat to start reconciliation")
            print("\n🚀 Ready for real-world financial data reconciliation!")
        else:
            print("❌ SETUP INCOMPLETE - Please review errors above")
        
        return all_success

if __name__ == "__main__":
    setup = ProductionSetup()
    setup.run_setup()
