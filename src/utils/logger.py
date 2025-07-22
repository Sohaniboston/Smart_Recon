"""
Logging utilities for SmartRecon application.

This module provides logging configuration and utilities for consistent
logging throughout the application.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Optional, Callable, Any


def setup_logger(name: str = 'smartrecon', 
                level: int = logging.INFO,
                log_file: Optional[str] = None,
                console_output: bool = True,
                file_output: bool = True) -> logging.Logger:
    """
    Setup and configure logger for SmartRecon application.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log file path (defaults to logs/smartrecon.log)
        console_output: Enable console output
        file_output: Enable file output
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if file_output:
        if log_file is None:
            # Create logs directory if it doesn't exist
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / 'smartrecon.log'
        
        # Create rotating file handler (10MB max, 5 backup files)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with execution time logging
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger('smartrecon')
        start_time = datetime.now()
        
        try:
            logger.debug(f"Starting execution: {func.__name__}")
            result = func(*args, **kwargs)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"Completed execution: {func.__name__} | Duration: {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Failed execution: {func.__name__} | Duration: {execution_time:.2f}s | Error: {e}")
            raise
    
    return wrapper


def log_data_stats(df, operation: str, logger: Optional[logging.Logger] = None):
    """
    Log basic statistics about a DataFrame operation.
    
    Args:
        df: Pandas DataFrame
        operation: Description of the operation
        logger: Logger instance (defaults to 'smartrecon')
    """
    if logger is None:
        logger = logging.getLogger('smartrecon')
    
    if df is not None and hasattr(df, 'shape'):
        rows, cols = df.shape
        logger.info(f"{operation} | Rows: {rows:,} | Columns: {cols}")
    else:
        logger.warning(f"{operation} | No data or invalid DataFrame")


def log_progress(current: int, total: int, operation: str, 
                logger: Optional[logging.Logger] = None,
                log_interval: int = 1000):
    """
    Log progress for long-running operations.
    
    Args:
        current: Current progress count
        total: Total items to process
        operation: Description of the operation
        logger: Logger instance
        log_interval: Log every N items
    """
    if logger is None:
        logger = logging.getLogger('smartrecon')
    
    if current % log_interval == 0 or current == total:
        percentage = (current / total) * 100 if total > 0 else 0
        logger.info(f"{operation} | Progress: {current:,}/{total:,} ({percentage:.1f}%)")


class LoggerContext:
    """Context manager for temporary logger configuration."""
    
    def __init__(self, logger_name: str = 'smartrecon', 
                 temp_level: int = logging.DEBUG):
        """
        Initialize logger context.
        
        Args:
            logger_name: Name of logger to modify
            temp_level: Temporary logging level
        """
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level
        self.temp_level = temp_level
    
    def __enter__(self):
        """Enter context and set temporary logging level."""
        self.logger.setLevel(self.temp_level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original logging level."""
        self.logger.setLevel(self.original_level)
