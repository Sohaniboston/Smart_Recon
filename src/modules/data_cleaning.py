"""
SmartRecon Data Cleaning Module - Minimal Working Version

This module provides basic data cleaning functionality for SmartRecon.
The complete implementation is available in data_cleaning_complete.py.
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, date
import warnings

# Simplified exception handling
class DataCleaningError(Exception):
    """Exception raised for data cleaning errors."""
    pass

class DataValidationError(Exception):
    """Exception raised for data validation errors."""
    pass

def normalize_text(text):
    """Simple text normalization."""
    if text is None:
        return None
    return str(text).strip().upper()

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Handles comprehensive data cleaning and standardization for financial data.
    
    This is a minimal working version. Full implementation available in data_cleaning_complete.py.
    """
    
    def __init__(self, config):
        """
        Initialize DataCleaner with configuration settings.
        
        Args:
            config: Configuration object containing cleaning parameters
        """
        self.config = config
        self.cleaning_stats = {}
        
        # Date format patterns (most common first)
        self.date_formats = [
            '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%m-%d-%Y', '%d-%m-%Y', '%Y%m%d',
            '%m/%d/%y', '%d/%m/%y', '%y-%m-%d',
            '%B %d, %Y', '%d %B %Y', '%b %d, %Y', '%d %b %Y'
        ]
        
        # Currency symbols and patterns
        self.currency_patterns = {
            'symbols': r'[$£€¥¢₹₽₿]',
            'codes': r'\b(USD|EUR|GBP|JPY|CAD|AUD|CHF|CNY)\b',
            'separators': r'[,\s]',
            'negative': r'[()-]'
        }
        
        logger.info("DataCleaner module initialized")
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        original_columns = df.columns.tolist()
        
        # Standardize column names
        new_columns = []
        for col in df.columns:
            # Convert to lowercase, strip whitespace, replace special characters
            clean_col = str(col).lower().strip()
            clean_col = re.sub(r'[^\w\s]', '_', clean_col)
            clean_col = re.sub(r'\s+', '_', clean_col)
            clean_col = re.sub(r'_+', '_', clean_col)
            clean_col = clean_col.strip('_')
            new_columns.append(clean_col)
        
        df.columns = new_columns
        
        self.cleaning_stats['operations_performed'].append('column_name_standardization')
        logger.debug(f"Standardized column names: {dict(zip(original_columns, new_columns))}")
        
        return df
    
    def clean_data(self, df: pd.DataFrame, data_type: str = 'auto') -> Dict[str, Any]:
        """
        Perform basic data cleaning pipeline.
        
        Args:
            df (pd.DataFrame): Input dataframe to clean
            data_type (str): Type of data ('gl', 'bank', 'auto')
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - cleaned_data: Cleaned and standardized dataframe
                - cleaning_stats: Statistics about the cleaning process
                - operations_performed: List of operations performed
                - data_quality_score: Quality score after cleaning
        """
        try:
            logger.info(f"Starting basic data cleaning for {len(df)} records")
            
            # Create a copy to avoid modifying original
            df_clean = df.copy()
            
            # Initialize cleaning statistics
            self.cleaning_stats = {
                'original_records': len(df),
                'operations_performed': [],
                'data_quality_improvements': {},
                'errors_encountered': []
            }
            
            # 1. Clean column names first
            df_clean = self._clean_column_names(df_clean)
            
            # 2. Standardize dates
            df_clean = self._standardize_dates(df_clean)
            
            # 3. Standardize amounts 
            df_clean = self._standardize_amounts(df_clean)
            
            # 4. Basic cleaning: remove completely empty rows/columns
            df_clean = df_clean.dropna(how='all')  # Remove empty rows
            df_clean = df_clean.dropna(axis=1, how='all')  # Remove empty columns
            
            # Calculate basic data quality score
            data_quality_score = self._calculate_basic_quality_score(df_clean)
            
            self.cleaning_stats['final_records'] = len(df_clean)
            self.cleaning_stats['records_removed'] = len(df) - len(df_clean)
            self.cleaning_stats['data_quality_score'] = data_quality_score
            
            logger.info(f"Basic data cleaning completed. {len(df_clean)} records processed")
            
            return {
                'cleaned_data': df_clean,
                'cleaning_stats': self.cleaning_stats.copy(),
                'operations_performed': self.cleaning_stats.get('operations_performed', []),
                'data_quality_score': data_quality_score,
                'original_records': len(df),
                'final_records': len(df_clean),
                'records_removed': len(df) - len(df_clean)
            }
            
        except Exception as e:
            logger.error(f"Data cleaning failed: {str(e)}")
            raise DataCleaningError(f"Data cleaning failed: {str(e)}") from e
    
    def _calculate_basic_quality_score(self, df: pd.DataFrame) -> float:
        """
        Calculate basic data quality score.
        
        Args:
            df: DataFrame to assess
            
        Returns:
            float: Quality score between 0 and 1
        """
        try:
            if len(df) == 0:
                return 0.0
            
            # Simple quality metric based on completeness
            total_cells = len(df) * len(df.columns)
            null_cells = df.isnull().sum().sum()
            completeness_score = 1.0 - (null_cells / total_cells) if total_cells > 0 else 0.0
            
            return round(completeness_score, 3)
            
        except Exception:
            return 0.5  # Return moderate score if calculation fails
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        original_columns = df.columns.tolist()
        
        # Standardize column names
        new_columns = []
        for col in df.columns:
            # Convert to lowercase, strip whitespace, replace special characters
            clean_col = str(col).lower().strip()
            clean_col = re.sub(r'[^\w\s]', '_', clean_col)
            clean_col = re.sub(r'\s+', '_', clean_col)
            clean_col = re.sub(r'_+', '_', clean_col)
            clean_col = clean_col.strip('_')
            new_columns.append(clean_col)
        
        df.columns = new_columns
        
        self.cleaning_stats['operations_performed'].append('column_name_standardization')
        logger.debug(f"Standardized column names: {dict(zip(original_columns, new_columns))}")
        
        return df
    
    def _identify_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify columns that likely contain dates."""
        date_columns = []
        
        for col in df.columns:
            # Only check column name patterns - be more restrictive
            col_name = col.lower()
            
            # Explicitly check for date-related column names
            if any(pattern == col_name or col_name.startswith(pattern) for pattern in ['date', 'time', 'timestamp']):
                # Additional validation: check if values actually look like dates
                sample = df[col].dropna().head(5)
                if len(sample) > 0:
                    date_like_count = 0
                    for val in sample:
                        val_str = str(val)
                        # Check for common date patterns (not just any parseable value)
                        if (re.match(r'\d{4}-\d{1,2}-\d{1,2}', val_str) or 
                            re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', val_str) or
                            re.match(r'\d{8}', val_str)):
                            date_like_count += 1
                    
                    # Only add if most values look like actual dates
                    if date_like_count > len(sample) / 2:
                        date_columns.append(col)
        
        return date_columns
    
    def _identify_amount_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify columns that likely contain amounts."""
        amount_columns = []
        
        for col in df.columns:
            col_name = col.lower()
            
            # Check column name patterns (be more specific)
            amount_keywords = ['amount', 'debit', 'credit', 'balance', 'value', 'withdrawal', 'deposit', 'payment', 'total']
            if any(keyword == col_name or keyword in col_name for keyword in amount_keywords):
                # Validate that values are actually numeric
                sample = df[col].dropna().head(10)
                if len(sample) > 0:
                    numeric_count = 0
                    for val in sample:
                        try:
                            # Clean and try to parse as number
                            clean_val = str(val).replace(',', '').replace('$', '').replace('(', '-').replace(')', '').strip()
                            float(clean_val)
                            numeric_count += 1
                        except:
                            pass
                    
                    # If most values are numeric, it's an amount column
                    if numeric_count >= len(sample) * 0.7:  # 70% threshold
                        amount_columns.append(col)
        
        return amount_columns
    
    def _identify_text_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify columns that contain text descriptions."""
        text_columns = []
        
        for col in df.columns:
            # Skip already identified date/amount columns
            if col in self._identify_date_columns(df) or col in self._identify_amount_columns(df):
                continue
            
            # Check if column contains string data
            if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                text_columns.append(col)
        
        return text_columns
    
    def get_cleaning_statistics(self) -> Dict[str, Any]:
        """Return comprehensive cleaning statistics."""
        return self.cleaning_stats.copy()
    
    def _standardize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize date columns to consistent format."""
        date_columns = self._identify_date_columns(df)
        
        # Debug: Show which columns are identified as dates
        logger.info(f"Identified date columns: {date_columns}")
        
        for col in date_columns:
            try:
                original_values = df[col].copy()
                
                # Try pandas auto-detection first (without deprecated parameter)
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    # Try manual format detection
                    df[col] = self._parse_dates_with_formats(df[col])
                
                # Validate date ranges (e.g., reasonable business dates)
                current_year = datetime.now().year
                valid_start = datetime(current_year-10, 1, 1)
                valid_end = datetime(current_year+1, 12, 31)
                
                # Flag suspicious dates
                if hasattr(df[col], 'dt'):
                    # Count valid dates
                    valid_dates = df[col].between(valid_start, valid_end)
                    invalid_count = (~valid_dates).sum()
                    
                    if invalid_count > 0:
                        logger.warning(f"Found {invalid_count} dates outside reasonable range in column '{col}'")
                        
                        # If too many invalid dates, revert to original values
                        valid_ratio = valid_dates.sum() / len(df[col].dropna())
                        if valid_ratio < 0.5:  # If less than 50% are valid dates
                            logger.warning(f"Reverting column '{col}' - too many invalid dates")
                            df[col] = original_values
                            continue
                
                self.cleaning_stats['operations_performed'].append(f'date_standardization_{col}')
                
            except Exception as e:
                logger.warning(f"Failed to standardize dates in column '{col}': {str(e)}")
                # Keep original values if standardization fails
                df[col] = original_values
        
        return df
    
    def _parse_dates_with_formats(self, series: pd.Series) -> pd.Series:
        """Parse dates using multiple format attempts."""
        parsed_series = series.copy()
        
        for date_format in self.date_formats:
            mask = parsed_series.isnull() if hasattr(parsed_series, 'isnull') else pd.isnull(parsed_series)
            unparsed = series[~mask] if not mask.all() else series
            
            # Try parsing
            try:
                parsed_attempt = pd.to_datetime(unparsed, format=date_format, errors='coerce')
                
                # Retain original where parsing failed
                parsed_series[~mask] = parsed_attempt
            except Exception:
                continue
        
        return parsed_series
    
    def _standardize_amounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize amount columns to consistent numeric format."""
        amount_columns = self._identify_amount_columns(df)
        
        # Debug: Show which columns are identified as amounts
        logger.info(f"Identified amount columns: {amount_columns}")
        
        for col in amount_columns:
            try:
                original_values = df[col].copy()
                
                # Convert to string for processing
                str_values = df[col].astype(str)
                
                # Clean currency symbols and formatting
                cleaned_values = str_values.apply(self._clean_amount_string)
                
                # Convert to numeric
                numeric_values = pd.to_numeric(cleaned_values, errors='coerce')
                
                # Handle negative amounts (common accounting practices)
                # Check for parentheses indicating negative amounts
                negative_mask = str_values.str.contains(r'\([^)]*\)', na=False)
                numeric_values.loc[negative_mask] = -abs(numeric_values.loc[negative_mask])
                
                df[col] = numeric_values
                
                # Round to appropriate decimal places (typically 2 for currency)
                decimal_places = getattr(self.config, 'amount_decimal_places', 2)
                df[col] = df[col].round(decimal_places)
                
                self.cleaning_stats['operations_performed'].append(f'amount_standardization_{col}')
                
            except Exception as e:
                logger.warning(f"Failed to standardize amounts in column '{col}': {str(e)}")
                df[col] = original_values
        
        return df
    
    def _clean_amount_string(self, amount_str: str) -> str:
        """Clean individual amount string."""
        if pd.isnull(amount_str) or amount_str == 'nan':
            return '0'
        
        # Remove currency symbols
        cleaned = re.sub(self.currency_patterns['symbols'], '', str(amount_str))
        
        # Remove currency codes
        cleaned = re.sub(self.currency_patterns['codes'], '', cleaned, flags=re.IGNORECASE)
        
        # Remove thousand separators but preserve decimal points
        cleaned = re.sub(r',(?=\d{3})', '', cleaned)
        
        # Handle parentheses (negative amounts)
        if '(' in cleaned and ')' in cleaned:
            cleaned = re.sub(r'[()]', '', cleaned)
            # Mark as negative (will be handled in caller)
        
        # Remove extra whitespace
        cleaned = cleaned.strip()
        
        # Ensure we have a valid number
        if not re.match(r'^-?\d*\.?\d+$', cleaned):
            return '0'
        
        return cleaned
    
    # ...existing code...
