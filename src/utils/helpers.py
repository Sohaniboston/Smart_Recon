"""
Helper utilities for SmartRecon application.

This module provides common utility functions used across different modules.
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import hashlib
import json
from datetime import datetime
import numpy as np

from .exceptions import SmartReconException


def ensure_directory_exists(directory_path: str) -> str:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        Absolute path to directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return str(path.absolute())


def get_file_hash(filepath: str) -> str:
    """
    Calculate MD5 hash of file for integrity checking.
    
    Args:
        filepath: Path to file
        
    Returns:
        MD5 hash string
    """
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise SmartReconException(f"Error calculating file hash: {e}")


def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """
    Format numeric amount as currency string.
    
    Args:
        amount: Numeric amount
        currency_symbol: Currency symbol to use
        
    Returns:
        Formatted currency string
    """
    try:
        if pd.isna(amount) or amount is None:
            return f"{currency_symbol}0.00"
        return f"{currency_symbol}{amount:,.2f}"
    except (ValueError, TypeError):
        return f"{currency_symbol}0.00"


def parse_currency(currency_str: str) -> float:
    """
    Parse currency string to numeric value.
    
    Args:
        currency_str: Currency string (e.g., "$1,234.56")
        
    Returns:
        Numeric value
    """
    try:
        if pd.isna(currency_str) or currency_str is None:
            return 0.0
        
        # Remove common currency symbols and formatting
        cleaned = str(currency_str).replace('$', '').replace(',', '').replace('(', '-').replace(')', '').strip()
        
        # Handle empty strings
        if not cleaned:
            return 0.0
            
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0


def normalize_text(text: str, 
                  remove_special_chars: bool = True,
                  convert_to_lowercase: bool = True,
                  remove_extra_spaces: bool = True) -> str:
    """
    Normalize text for consistent processing.
    
    Args:
        text: Text to normalize
        remove_special_chars: Remove special characters
        convert_to_lowercase: Convert to lowercase
        remove_extra_spaces: Remove extra whitespace
        
    Returns:
        Normalized text
    """
    try:
        if pd.isna(text) or text is None:
            return ""
        
        result = str(text)
        
        if remove_extra_spaces:
            result = ' '.join(result.split())
        
        if convert_to_lowercase:
            result = result.lower()
        
        if remove_special_chars:
            # Keep alphanumeric, spaces, and basic punctuation
            import re
            result = re.sub(r'[^a-zA-Z0-9\s\-\.]', '', result)
        
        return result.strip()
        
    except Exception:
        return ""


def detect_file_encoding(filepath: str) -> str:
    """
    Detect file encoding for proper reading.
    
    Args:
        filepath: Path to file
        
    Returns:
        Detected encoding string
    """
    try:
        import chardet
        
        with open(filepath, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')
    except ImportError:
        # Fallback if chardet not available
        return 'utf-8'
    except Exception:
        return 'utf-8'


def get_column_mapping_suggestions(df_columns: List[str], 
                                 target_columns: List[str]) -> Dict[str, str]:
    """
    Suggest column mapping based on column name similarity.
    
    Args:
        df_columns: Available DataFrame columns
        target_columns: Target column names to map to
        
    Returns:
        Dictionary mapping DataFrame columns to target columns
    """
    from difflib import SequenceMatcher
    
    suggestions = {}
    
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    for df_col in df_columns:
        best_match = None
        best_score = 0.0
        
        for target_col in target_columns:
            score = similarity(df_col, target_col)
            if score > best_score and score > 0.6:  # 60% similarity threshold
                best_score = score
                best_match = target_col
        
        if best_match:
            suggestions[df_col] = best_match
    
    return suggestions


def create_audit_record(operation: str, 
                       details: Dict[str, Any],
                       user: str = "system") -> Dict[str, Any]:
    """
    Create audit record for operation tracking.
    
    Args:
        operation: Description of operation
        details: Operation details
        user: User performing operation
        
    Returns:
        Audit record dictionary
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'operation': operation,
        'user': user,
        'details': details,
        'record_id': hashlib.md5(
            f"{datetime.now().isoformat()}{operation}{user}".encode()
        ).hexdigest()[:8]
    }


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, handling division by zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Value to return if division by zero
        
    Returns:
        Division result or default value
    """
    try:
        if denominator == 0 or pd.isna(denominator):
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def calculate_percentage(part: float, total: float, decimal_places: int = 2) -> float:
    """
    Calculate percentage with safe handling of edge cases.
    
    Args:
        part: Part value
        total: Total value
        decimal_places: Number of decimal places to round to
        
    Returns:
        Percentage value
    """
    try:
        if total == 0 or pd.isna(total) or pd.isna(part):
            return 0.0
        percentage = (part / total) * 100
        return round(percentage, decimal_places)
    except (TypeError, ValueError):
        return 0.0


def dataframe_to_dict_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create summary dictionary from DataFrame for logging/reporting.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Summary dictionary
    """
    try:
        if df is None or df.empty:
            return {
                'rows': 0,
                'columns': 0,
                'memory_usage': 0,
                'has_data': False
            }
        
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'null_counts': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'has_data': True
        }
    except Exception:
        return {'error': 'Unable to generate DataFrame summary'}


def json_serialize_safe(obj: Any) -> str:
    """
    Safely serialize object to JSON, handling non-serializable types.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string
    """
    def default_serializer(o):
        if isinstance(o, (datetime, pd.Timestamp)):
            return o.isoformat()
        elif isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        elif pd.isna(o):
            return None
        else:
            return str(o)
    
    try:
        return json.dumps(obj, default=default_serializer, indent=2)
    except Exception as e:
        return json.dumps({'error': f'Serialization failed: {str(e)}'})


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate that date range is logical (start <= end).
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        True if date range is valid
    """
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return start <= end
    except Exception:
        return False
