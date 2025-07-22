"""
Data validation utilities for SmartRecon application.

This module provides functions for validating data files, formats,
and content throughout the reconciliation process.
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from datetime import datetime

from .exceptions import DataValidationError, DataIngestionError


def validate_file_format(filepath: str) -> Dict[str, Any]:
    """
    Validate file format and basic properties.
    
    Args:
        filepath: Path to file to validate
        
    Returns:
        Dictionary with validation results
        
    Raises:
        DataValidationError: If file validation fails
    """
    result = {
        'valid': False,
        'file_exists': False,
        'file_size': 0,
        'file_extension': '',
        'supported_format': False,
        'issues': []
    }
    
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            result['issues'].append(f"File does not exist: {filepath}")
            return result
        
        result['file_exists'] = True
        
        # Check file size
        file_size = os.path.getsize(filepath)
        result['file_size'] = file_size
        
        if file_size == 0:
            result['issues'].append("File is empty")
            return result
        
        # Check file extension
        file_ext = Path(filepath).suffix.lower()
        result['file_extension'] = file_ext
        
        supported_formats = ['.csv', '.xlsx', '.xls']
        if file_ext not in supported_formats:
            result['issues'].append(f"Unsupported file format: {file_ext}")
            result['issues'].append(f"Supported formats: {', '.join(supported_formats)}")
            return result
        
        result['supported_format'] = True
        
        # If all checks pass
        if not result['issues']:
            result['valid'] = True
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"File format validation failed: {e}")


def validate_required_columns(df: pd.DataFrame, required_cols: List[str], 
                            data_type: str = 'unknown') -> Dict[str, Any]:
    """
    Validate that DataFrame contains required columns.
    
    Args:
        df: DataFrame to validate
        required_cols: List of required column names
        data_type: Type of data (for error messages)
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'missing_columns': [],
        'extra_columns': [],
        'column_count': len(df.columns),
        'issues': []
    }
    
    try:
        df_columns = set(df.columns.str.lower())
        required_columns = set(col.lower() for col in required_cols)
        
        # Check for missing columns
        missing = required_columns - df_columns
        if missing:
            result['missing_columns'] = list(missing)
            result['issues'].append(f"Missing required columns for {data_type}: {', '.join(missing)}")
        
        # Check for extra columns (informational, not an error)
        extra = df_columns - required_columns
        if extra:
            result['extra_columns'] = list(extra)
        
        # Validation passes if no missing columns
        result['valid'] = len(missing) == 0
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"Column validation failed: {e}")


def validate_data_types(df: pd.DataFrame, column_types: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate data types in DataFrame columns.
    
    Args:
        df: DataFrame to validate
        column_types: Dictionary mapping column names to expected types
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'type_mismatches': [],
        'issues': []
    }
    
    try:
        for col_name, expected_type in column_types.items():
            if col_name in df.columns:
                actual_type = str(df[col_name].dtype)
                
                # Check type compatibility
                if not _is_type_compatible(actual_type, expected_type):
                    mismatch = {
                        'column': col_name,
                        'expected': expected_type,
                        'actual': actual_type
                    }
                    result['type_mismatches'].append(mismatch)
                    result['issues'].append(
                        f"Column '{col_name}': expected {expected_type}, got {actual_type}"
                    )
        
        # Validation passes if no type mismatches
        result['valid'] = len(result['type_mismatches']) == 0
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"Data type validation failed: {e}")


def validate_date_column(df: pd.DataFrame, column_name: str) -> Dict[str, Any]:
    """
    Validate date column format and values.
    
    Args:
        df: DataFrame containing the date column
        column_name: Name of the date column
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'parseable_dates': 0,
        'invalid_dates': 0,
        'null_dates': 0,
        'date_range': None,
        'issues': []
    }
    
    try:
        if column_name not in df.columns:
            result['issues'].append(f"Date column '{column_name}' not found")
            return result
        
        col_data = df[column_name]
        
        # Count null values
        result['null_dates'] = col_data.isnull().sum()
        
        # Try to parse dates
        try:
            parsed_dates = pd.to_datetime(col_data, errors='coerce')
            result['parseable_dates'] = parsed_dates.notna().sum()
            result['invalid_dates'] = parsed_dates.isna().sum() - result['null_dates']
            
            # Get date range for valid dates
            valid_dates = parsed_dates.dropna()
            if len(valid_dates) > 0:
                result['date_range'] = {
                    'min_date': valid_dates.min().strftime('%Y-%m-%d'),
                    'max_date': valid_dates.max().strftime('%Y-%m-%d')
                }
        except Exception:
            result['invalid_dates'] = len(col_data) - result['null_dates']
            result['issues'].append(f"Unable to parse dates in column '{column_name}'")
        
        # Add issues for invalid data
        if result['null_dates'] > 0:
            result['issues'].append(f"Found {result['null_dates']} null dates")
        
        if result['invalid_dates'] > 0:
            result['issues'].append(f"Found {result['invalid_dates']} invalid dates")
        
        # Validation passes if most dates are parseable
        total_rows = len(col_data)
        if total_rows > 0:
            valid_percentage = (result['parseable_dates'] / total_rows) * 100
            result['valid'] = valid_percentage >= 80  # 80% threshold
            
            if not result['valid']:
                result['issues'].append(
                    f"Only {valid_percentage:.1f}% of dates are valid (minimum 80% required)"
                )
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"Date validation failed: {e}")


def validate_amount_column(df: pd.DataFrame, column_name: str) -> Dict[str, Any]:
    """
    Validate amount/numeric column format and values.
    
    Args:
        df: DataFrame containing the amount column
        column_name: Name of the amount column
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'numeric_values': 0,
        'non_numeric_values': 0,
        'null_values': 0,
        'negative_values': 0,
        'zero_values': 0,
        'amount_range': None,
        'issues': []
    }
    
    try:
        if column_name not in df.columns:
            result['issues'].append(f"Amount column '{column_name}' not found")
            return result
        
        col_data = df[column_name]
        
        # Count null values
        result['null_values'] = col_data.isnull().sum()
        
        # Try to convert to numeric
        try:
            numeric_data = pd.to_numeric(col_data, errors='coerce')
            result['numeric_values'] = numeric_data.notna().sum()
            result['non_numeric_values'] = numeric_data.isna().sum() - result['null_values']
            
            # Analyze numeric values
            valid_amounts = numeric_data.dropna()
            if len(valid_amounts) > 0:
                result['negative_values'] = (valid_amounts < 0).sum()
                result['zero_values'] = (valid_amounts == 0).sum()
                result['amount_range'] = {
                    'min_amount': float(valid_amounts.min()),
                    'max_amount': float(valid_amounts.max()),
                    'mean_amount': float(valid_amounts.mean())
                }
        except Exception:
            result['non_numeric_values'] = len(col_data) - result['null_values']
            result['issues'].append(f"Unable to parse amounts in column '{column_name}'")
        
        # Add issues for invalid data
        if result['null_values'] > 0:
            result['issues'].append(f"Found {result['null_values']} null amounts")
        
        if result['non_numeric_values'] > 0:
            result['issues'].append(f"Found {result['non_numeric_values']} non-numeric amounts")
        
        # Validation passes if most amounts are numeric
        total_rows = len(col_data)
        if total_rows > 0:
            valid_percentage = (result['numeric_values'] / total_rows) * 100
            result['valid'] = valid_percentage >= 90  # 90% threshold for amounts
            
            if not result['valid']:
                result['issues'].append(
                    f"Only {valid_percentage:.1f}% of amounts are valid (minimum 90% required)"
                )
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"Amount validation failed: {e}")


def validate_data_quality(df: pd.DataFrame, data_type: str = 'unknown') -> Dict[str, Any]:
    """
    Perform comprehensive data quality validation.
    
    Args:
        df: DataFrame to validate
        data_type: Type of data being validated
        
    Returns:
        Dictionary with comprehensive validation results
    """
    result = {
        'valid': False,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'duplicate_rows': 0,
        'empty_rows': 0,
        'data_quality_score': 0.0,
        'issues': []
    }
    
    try:
        # Check for duplicate rows
        result['duplicate_rows'] = df.duplicated().sum()
        if result['duplicate_rows'] > 0:
            result['issues'].append(f"Found {result['duplicate_rows']} duplicate rows")
        
        # Check for completely empty rows
        result['empty_rows'] = df.isnull().all(axis=1).sum()
        if result['empty_rows'] > 0:
            result['issues'].append(f"Found {result['empty_rows']} completely empty rows")
        
        # Calculate data quality score
        total_cells = result['total_rows'] * result['total_columns']
        if total_cells > 0:
            null_cells = df.isnull().sum().sum()
            result['data_quality_score'] = ((total_cells - null_cells) / total_cells) * 100
        
        # Overall validation
        result['valid'] = (
            result['total_rows'] > 0 and
            result['data_quality_score'] >= 70 and  # 70% data completeness threshold
            result['duplicate_rows'] < (result['total_rows'] * 0.1)  # Less than 10% duplicates
        )
        
        if result['data_quality_score'] < 70:
            result['issues'].append(
                f"Data quality score too low: {result['data_quality_score']:.1f}% (minimum 70%)"
            )
        
        return result
        
    except Exception as e:
        raise DataValidationError(f"Data quality validation failed: {e}")


def _is_type_compatible(actual_type: str, expected_type: str) -> bool:
    """
    Check if actual data type is compatible with expected type.
    
    Args:
        actual_type: Actual pandas dtype as string
        expected_type: Expected type name
        
    Returns:
        True if types are compatible
    """
    type_mappings = {
        'string': ['object', 'string'],
        'numeric': ['int64', 'float64', 'int32', 'float32'],
        'datetime': ['datetime64', 'object'],  # object might contain date strings
        'boolean': ['bool', 'object']
    }
    
    if expected_type in type_mappings:
        return any(actual_type.startswith(t) for t in type_mappings[expected_type])
    
    return actual_type.startswith(expected_type)


def validate_file_path(file_path: str) -> Dict[str, Any]:
    """
    Validate file path and basic file properties.
    
    Args:
        file_path (str): Path to the file to validate
        
    Returns:
        Dict[str, Any]: Validation results including:
            - is_valid: Boolean indicating if file is valid
            - file_exists: Boolean indicating if file exists
            - is_readable: Boolean indicating if file is readable
            - file_size: File size in bytes
            - file_extension: File extension
            - absolute_path: Absolute path to file
            - errors: List of validation errors
            - warnings: List of validation warnings
            
    Raises:
        DataValidationError: If critical validation fails
    """
    result = {
        'is_valid': False,
        'file_exists': False,
        'is_readable': False,
        'file_size': 0,
        'file_extension': '',
        'absolute_path': '',
        'errors': [],
        'warnings': []
    }
    
    try:
        # Convert to Path object for easier handling
        path_obj = Path(file_path)
        result['absolute_path'] = str(path_obj.absolute())
        
        # Check if file exists
        if not path_obj.exists():
            result['errors'].append(f"File does not exist: {file_path}")
            return result
        
        result['file_exists'] = True
        
        # Check if it's actually a file (not a directory)
        if not path_obj.is_file():
            result['errors'].append(f"Path is not a file: {file_path}")
            return result
        
        # Check if file is readable
        try:
            with open(path_obj, 'rb') as f:
                f.read(1)  # Try to read one byte
            result['is_readable'] = True
        except PermissionError:
            result['errors'].append(f"File is not readable (permission denied): {file_path}")
            return result
        except Exception as e:
            result['errors'].append(f"Cannot read file: {file_path} - {str(e)}")
            return result
        
        # Get file size
        result['file_size'] = path_obj.stat().st_size
        
        # Get file extension
        result['file_extension'] = path_obj.suffix.lower()
        
        # Check if file extension is supported
        supported_extensions = ['.csv', '.xlsx', '.xls', '.txt']
        if result['file_extension'] not in supported_extensions:
            result['warnings'].append(
                f"File extension '{result['file_extension']}' may not be supported. "
                f"Supported formats: {', '.join(supported_extensions)}"
            )
        
        # Check file size (warn if very large)
        max_size_mb = 100
        size_mb = result['file_size'] / (1024 * 1024)
        if size_mb > max_size_mb:
            result['warnings'].append(
                f"Large file detected ({size_mb:.2f} MB). Processing may be slow."
            )
        
        # If we get here, file is valid
        result['is_valid'] = True
        
    except Exception as e:
        result['errors'].append(f"Unexpected error validating file path: {str(e)}")
    
    return result


def validate_dataframe(df: pd.DataFrame, 
                      data_type: str = 'unknown',
                      required_columns: Optional[List[str]] = None,
                      min_rows: int = 1) -> Dict[str, Any]:
    """
    Validate pandas DataFrame structure and content.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        data_type (str): Type of data ('gl', 'bank', 'unknown')
        required_columns (List[str], optional): List of required column names
        min_rows (int): Minimum number of rows required
        
    Returns:
        Dict[str, Any]: Validation results including:
            - is_valid: Boolean indicating if DataFrame is valid
            - row_count: Number of rows
            - column_count: Number of columns
            - missing_columns: List of missing required columns
            - empty_columns: List of completely empty columns
            - data_types: Dictionary of column data types
            - null_counts: Dictionary of null counts per column
            - duplicate_rows: Number of duplicate rows
            - errors: List of validation errors
            - warnings: List of validation warnings
            
    Raises:
        DataValidationError: If DataFrame validation fails critically
    """
    result = {
        'is_valid': False,
        'row_count': 0,
        'column_count': 0,
        'missing_columns': [],
        'empty_columns': [],
        'data_types': {},
        'null_counts': {},
        'duplicate_rows': 0,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Basic DataFrame validation
        if df is None:
            result['errors'].append("DataFrame is None")
            return result
        
        if not isinstance(df, pd.DataFrame):
            result['errors'].append(f"Expected DataFrame, got {type(df)}")
            return result
        
        # Get basic dimensions
        result['row_count'] = len(df)
        result['column_count'] = len(df.columns)
        
        # Check minimum rows requirement
        if result['row_count'] < min_rows:
            result['errors'].append(
                f"DataFrame has {result['row_count']} rows, minimum required: {min_rows}"
            )
            return result
        
        # Check for empty DataFrame
        if result['row_count'] == 0:
            result['errors'].append("DataFrame is empty (no rows)")
            return result
        
        if result['column_count'] == 0:
            result['errors'].append("DataFrame has no columns")
            return result
        
        # Get data types
        result['data_types'] = df.dtypes.to_dict()
        result['data_types'] = {str(k): str(v) for k, v in result['data_types'].items()}
        
        # Get null counts
        result['null_counts'] = df.isnull().sum().to_dict()
        result['null_counts'] = {str(k): int(v) for k, v in result['null_counts'].items()}
        
        # Check for completely empty columns
        for col in df.columns:
            if df[col].isnull().all():
                result['empty_columns'].append(str(col))
        
        if result['empty_columns']:
            result['warnings'].append(
                f"Found {len(result['empty_columns'])} completely empty columns: "
                f"{', '.join(result['empty_columns'])}"
            )
        
        # Check for duplicate rows
        result['duplicate_rows'] = df.duplicated().sum()
        if result['duplicate_rows'] > 0:
            duplicate_pct = (result['duplicate_rows'] / result['row_count']) * 100
            result['warnings'].append(
                f"Found {result['duplicate_rows']} duplicate rows ({duplicate_pct:.1f}%)"
            )
        
        # Check required columns if specified
        if required_columns:
            df_columns = [str(col).lower().strip() for col in df.columns]
            for req_col in required_columns:
                req_col_norm = str(req_col).lower().strip()
                if req_col_norm not in df_columns:
                    # Try fuzzy matching for common variations
                    found_match = False
                    for df_col in df_columns:
                        if any(variant in df_col for variant in [req_col_norm, req_col_norm.replace('_', ''), req_col_norm.replace(' ', '')]):
                            found_match = True
                            result['warnings'].append(
                                f"Required column '{req_col}' not found, but similar column exists: '{df_col}'"
                            )
                            break
                    
                    if not found_match:
                        result['missing_columns'].append(req_col)
        
        if result['missing_columns']:
            result['errors'].append(
                f"Missing required columns: {', '.join(result['missing_columns'])}"
            )
            return result
        
        # Data type specific validations
        if data_type == 'gl':
            gl_validations = _validate_gl_dataframe(df, result)
            result.update(gl_validations)
        elif data_type == 'bank':
            bank_validations = _validate_bank_dataframe(df, result)
            result.update(bank_validations)
        
        # Check for suspicious data patterns
        _check_data_quality_patterns(df, result)
        
        # If we get here without errors, DataFrame is valid
        if not result['errors']:
            result['is_valid'] = True
        
    except Exception as e:
        result['errors'].append(f"Unexpected error validating DataFrame: {str(e)}")
    
    return result


def _validate_gl_dataframe(df: pd.DataFrame, result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate GL-specific DataFrame requirements."""
    gl_result = {}
    
    # Expected GL columns (flexible matching)
    expected_gl_columns = ['date', 'description', 'amount', 'account']
    
    # Check for typical GL patterns
    has_date_col = any('date' in str(col).lower() for col in df.columns)
    has_amount_col = any(term in str(col).lower() for col in df.columns for term in ['amount', 'value', 'debit', 'credit'])
    has_desc_col = any(term in str(col).lower() for col in df.columns for term in ['description', 'memo', 'narrative'])
    
    if not has_date_col:
        result['warnings'].append("No date column detected for GL data")
    if not has_amount_col:
        result['warnings'].append("No amount column detected for GL data")
    if not has_desc_col:
        result['warnings'].append("No description column detected for GL data")
    
    return gl_result


def _validate_bank_dataframe(df: pd.DataFrame, result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Bank-specific DataFrame requirements."""
    bank_result = {}
    
    # Expected Bank columns (flexible matching)
    expected_bank_columns = ['date', 'description', 'amount']
    
    # Check for typical Bank patterns
    has_date_col = any('date' in str(col).lower() for col in df.columns)
    has_amount_col = any(term in str(col).lower() for col in df.columns for term in ['amount', 'value', 'debit', 'credit'])
    has_desc_col = any(term in str(col).lower() for col in df.columns for term in ['description', 'memo', 'reference'])
    has_balance_col = any('balance' in str(col).lower() for col in df.columns)
    
    if not has_date_col:
        result['warnings'].append("No date column detected for Bank data")
    if not has_amount_col:
        result['warnings'].append("No amount column detected for Bank data")
    if not has_desc_col:
        result['warnings'].append("No description column detected for Bank data")
    
    if has_balance_col:
        result['warnings'].append("Balance column detected - this appears to be bank statement data")
    
    return bank_result


def _check_data_quality_patterns(df: pd.DataFrame, result: Dict[str, Any]):
    """Check for common data quality issues."""
    
    # Check for columns with very high null percentage
    high_null_threshold = 0.8
    for col in df.columns:
        null_pct = df[col].isnull().sum() / len(df)
        if null_pct > high_null_threshold:
            result['warnings'].append(
                f"Column '{col}' has {null_pct:.1%} missing values"
            )
    
    # Check for columns with only one unique value
    for col in df.columns:
        if df[col].nunique() == 1 and not df[col].isnull().all():
            unique_val = df[col].dropna().iloc[0]
            result['warnings'].append(
                f"Column '{col}' has only one unique value: '{unique_val}'"
            )
    
    # Check for suspicious date patterns
    for col in df.columns:
        if 'date' in str(col).lower():
            try:
                # Try to identify date format issues
                sample_values = df[col].dropna().head(10)
                non_date_count = 0
                for val in sample_values:
                    try:
                        pd.to_datetime(val)
                    except:
                        non_date_count += 1
                
                if non_date_count > len(sample_values) * 0.5:
                    result['warnings'].append(
                        f"Date column '{col}' may have formatting issues"
                    )
            except:
                pass
    
    # Check for suspicious amount patterns
    for col in df.columns:
        if any(term in str(col).lower() for term in ['amount', 'value', 'debit', 'credit']):
            try:
                # Check if amounts can be converted to numeric
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                non_numeric_count = numeric_series.isnull().sum() - df[col].isnull().sum()
                
                if non_numeric_count > 0:
                    result['warnings'].append(
                        f"Amount column '{col}' has {non_numeric_count} non-numeric values"
                    )
            except:
                pass
