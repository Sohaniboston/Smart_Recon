"""
SmartRecon - Intelligent Financial Reconciliation Assistant

This package provides automated financial reconciliation capabilities between
General Ledger entries and external sources such as bank statements.

Version: 1.0.0
Author: SmartRecon Development Team
"""

__version__ = "1.0.0"
__author__ = "SmartRecon Development Team"

# Core module imports
# from .main import main  # Commented out to avoid circular imports
from .config import Config

# Module imports - Commented out to avoid circular imports
# These should be imported directly by the application modules
# from .modules.data_ingestion import DataIngestion
# from .modules.data_cleaning import DataCleaner
# from .modules.matching_engine import MatchingEngine
# from .modules.exception_handler import ExceptionHandler
# from .modules.reporting import ReportGenerator

__all__ = [
    # 'main',
    'Config',
    # 'DataIngestion',
    # 'DataCleaner',
    # 'MatchingEngine',
    # 'ExceptionHandler',
    # 'ReportGenerator'
]
