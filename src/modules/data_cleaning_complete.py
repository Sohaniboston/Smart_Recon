"""
SmartRecon Data Cleaning Module

This module handles data standardization, normalization, and quality enhancement for
financial reconciliation data including:
- Date standardization and validation
- Amount format standardization
- Text normalization and cleaning
- Duplicate detection and handling
- Missing value treatment
- Data type conversions

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, date
import warnings

try:
    from ..utils.exceptions import DataCleaningError, DataValidationError
    from ..utils.helpers import normalize_text
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.exceptions import DataCleaningError, DataValidationError
    from utils.helpers import normalize_text

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Handles comprehensive data cleaning and standardization for financial data.
    
    Features:
    - Date standardization with multiple format detection
    - Amount normalization with currency handling
    - Text cleaning and standardization
    - Duplicate detection and resolution
    - Missing value imputation
    - Data type validation and conversion
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
    
    def clean_data(self, df: pd.DataFrame, data_type: str = 'auto') -> Dict[str, Any]:
        """
        Perform comprehensive data cleaning pipeline.
        
        Args:
            df (pd.DataFrame): Input dataframe to clean
            data_type (str): Type of data ('gl', 'bank', 'auto')
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - cleaned_data: Cleaned and standardized dataframe
                - cleaning_stats: Statistics about the cleaning process
                - operations_performed: List of operations performed
                - data_quality_score: Quality score after cleaning
            
        Raises:
            DataCleaningError: If cleaning process fails
        """
        try:
            logger.info(f"Starting data cleaning for {len(df)} records")
            
            # Create a copy to avoid modifying original
            df_clean = df.copy()
            
            # Initialize cleaning statistics
            self.cleaning_stats = {
                'original_records': len(df),
                'operations_performed': [],
                'data_quality_improvements': {},
                'errors_encountered': []
            }
            
            # 1. Clean column names
            df_clean = self._clean_column_names(df_clean)
            
            # 2. Handle missing values
            df_clean = self._handle_missing_values(df_clean)
            
            # 3. Standardize dates
            df_clean = self._standardize_dates(df_clean)
            
            # 4. Standardize amounts
            df_clean = self._standardize_amounts(df_clean)
            
            # 5. Clean text fields
            df_clean = self._clean_text_fields(df_clean)
            
            # 6. Handle duplicates
            df_clean = self._handle_duplicates(df_clean)
            
            # 7. Validate data types
            df_clean = self._validate_data_types(df_clean)
            
            # 8. Final quality checks
            self._perform_quality_checks(df_clean)
            
            self.cleaning_stats['final_records'] = len(df_clean)
            self.cleaning_stats['records_removed'] = len(df) - len(df_clean)
            
            # Calculate final data quality score
            data_quality_score = self._calculate_quality_score(df_clean)
            self.cleaning_stats['data_quality_score'] = data_quality_score
            
            logger.info(f"Data cleaning completed. {len(df_clean)} records processed")
            
            # Return comprehensive results
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
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values based on column types and business rules."""
        missing_before = df.isnull().sum().sum()
        
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                # Different strategies for different column types
                if col in ['date', 'transaction_date', 'posting_date']:
                    # Don't impute dates - flag for review
                    continue
                    
                elif col in ['amount', 'debit', 'credit', 'balance']:
                    # For amounts, consider 0 as default if appropriate
                    fill_value = getattr(self.config, 'default_amount_fill', 0.0)
                    df[col] = df[col].fillna(fill_value)
                    
                elif col in ['description', 'memo', 'narrative']:
                    # Fill text fields with standard placeholder
                    df[col] = df[col].fillna('NO_DESCRIPTION')
                    
                elif col in ['reference', 'ref', 'id']:
                    # Generate reference IDs if missing
                    mask = df[col].isnull()
                    df.loc[mask, col] = df.loc[mask].apply(
                        lambda x: f"AUTO_REF_{x.name}", axis=1
                    )
        
        missing_after = df.isnull().sum().sum()
        
        self.cleaning_stats['operations_performed'].append('missing_value_handling')
        self.cleaning_stats['data_quality_improvements']['missing_values_filled'] = missing_before - missing_after
        
        logger.debug(f"Filled {missing_before - missing_after} missing values")
        
        return df
    
    def _standardize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize date columns to consistent format."""
        date_columns = self._identify_date_columns(df)
        
        for col in date_columns:
            try:
                original_values = df[col].copy()
                
                # Try pandas auto-detection first
                try:
                    df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
                except:
                    # Try manual format detection
                    df[col] = self._parse_dates_with_formats(df[col])
                
                # Validate date ranges (e.g., reasonable business dates)
                current_year = datetime.now().year
                valid_range = pd.date_range(
                    start=f'{current_year-10}-01-01',
                    end=f'{current_year+1}-12-31'
                )
                
                # Flag suspicious dates
                suspicious_dates = ~df[col].dt.date.between(
                    valid_range.min().date(),
                    valid_range.max().date()
                )
                
                if suspicious_dates.any():
                    logger.warning(f"Found {suspicious_dates.sum()} dates outside reasonable range in column '{col}'")
                
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
            
            if len(unparsed) == 0:
                break
                
            try:
                parsed_values = pd.to_datetime(unparsed, format=date_format, errors='coerce')
                valid_parsed = ~parsed_values.isnull()
                parsed_series.loc[unparsed.index[valid_parsed]] = parsed_values[valid_parsed]
            except:
                continue
        
        return parsed_series
    
    def _standardize_amounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize amount columns to consistent numeric format."""
        amount_columns = self._identify_amount_columns(df)
        
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
    
    def _clean_text_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize text fields."""
        text_columns = self._identify_text_columns(df)
        
        for col in text_columns:
            try:
                # Apply text normalization
                df[col] = df[col].apply(lambda x: normalize_text(x) if pd.notnull(x) else x)
                
                # Remove excessive whitespace
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Strip leading/trailing whitespace
                df[col] = df[col].str.strip()
                
                # Standardize common abbreviations
                df[col] = self._standardize_abbreviations(df[col])
                
                self.cleaning_stats['operations_performed'].append(f'text_cleaning_{col}')
                
            except Exception as e:
                logger.warning(f"Failed to clean text in column '{col}': {str(e)}")
        
        return df
    
    def _standardize_abbreviations(self, series: pd.Series) -> pd.Series:
        """Standardize common abbreviations in text."""
        # Common financial abbreviations
        abbreviations = {
            r'\bDEP\b': 'DEPOSIT',
            r'\bWD\b': 'WITHDRAWAL',
            r'\bTFR\b': 'TRANSFER',
            r'\bCHK\b': 'CHECK',
            r'\bACH\b': 'ACH',
            r'\bEFT\b': 'ELECTRONIC_TRANSFER',
            r'\bPOS\b': 'POINT_OF_SALE',
            r'\bATM\b': 'ATM',
            r'\bINT\b': 'INTEREST',
            r'\bFEE\b': 'FEE'
        }
        
        for pattern, replacement in abbreviations.items():
            series = series.str.replace(pattern, replacement, regex=True, case=False)
        
        return series
    
    def _handle_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect and handle duplicate records."""
        initial_count = len(df)
        
        # Identify potential duplicate columns
        key_columns = []
        for col in df.columns:
            if col in ['date', 'amount', 'reference', 'description']:
                key_columns.append(col)
        
        if not key_columns:
            logger.warning("No key columns found for duplicate detection")
            return df
        
        # Check for exact duplicates
        exact_duplicates = df.duplicated(subset=key_columns, keep='first')
        
        if exact_duplicates.any():
            duplicate_count = exact_duplicates.sum()
            logger.info(f"Removing {duplicate_count} exact duplicate records")
            
            df = df[~exact_duplicates]
            
            self.cleaning_stats['operations_performed'].append('duplicate_removal')
            self.cleaning_stats['data_quality_improvements']['duplicates_removed'] = duplicate_count
        
        # Check for near-duplicates (same date and amount, similar description)
        near_duplicates = self._identify_near_duplicates(df, key_columns)
        
        if len(near_duplicates) > 0:
            logger.warning(f"Identified {len(near_duplicates)} potential near-duplicate groups")
            # For now, just log them - could implement fuzzy matching resolution
        
        final_count = len(df)
        logger.debug(f"Duplicate handling: {initial_count} -> {final_count} records")
        
        return df
    
    def _identify_near_duplicates(self, df: pd.DataFrame, key_columns: List[str]) -> List[Dict]:
        """Identify potential near-duplicate records."""
        # This is a simplified implementation
        # In production, you might use more sophisticated fuzzy matching
        near_duplicates = []
        
        # Group by date and amount, look for similar descriptions
        if 'date' in key_columns and 'amount' in key_columns:
            grouped = df.groupby(['date', 'amount'])
            for (date, amount), group in grouped:
                if len(group) > 1:
                    near_duplicates.append({
                        'date': date,
                        'amount': amount,
                        'records': group.index.tolist(),
                        'descriptions': group.get('description', pd.Series()).tolist()
                    })
        
        return near_duplicates
    
    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and ensure correct data types."""
        for col in df.columns:
            try:
                if col in ['date', 'transaction_date', 'posting_date']:
                    if not pd.api.types.is_datetime64_any_dtype(df[col]):
                        logger.warning(f"Column '{col}' should be datetime type")
                
                elif col in ['amount', 'debit', 'credit', 'balance']:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        logger.warning(f"Column '{col}' should be numeric type")
                        # Attempt conversion
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                elif col in ['description', 'memo', 'reference']:
                    if not pd.api.types.is_string_dtype(df[col]):
                        df[col] = df[col].astype(str)
                        
            except Exception as e:
                logger.warning(f"Data type validation failed for column '{col}': {str(e)}")
        
        self.cleaning_stats['operations_performed'].append('data_type_validation')
        return df
    
    def _perform_quality_checks(self, df: pd.DataFrame):
        """Perform final data quality checks."""
        issues = []
        
        # Check for remaining missing values in critical columns
        critical_columns = ['date', 'amount']
        for col in critical_columns:
            if col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Column '{col}' has {missing_count} missing values")
        
        # Check for zero or negative amounts where inappropriate
        if 'amount' in df.columns:
            zero_amounts = (df['amount'] == 0).sum()
            if zero_amounts > 0:
                issues.append(f"Found {zero_amounts} zero-amount transactions")
        
        # Check date ranges
        if 'date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['date']):
            date_range = df['date'].max() - df['date'].min()
            if date_range.days > 3650:  # More than 10 years
                issues.append(f"Date range spans {date_range.days} days")
        
        self.cleaning_stats['quality_issues'] = issues
        
        if issues:
            logger.warning(f"Quality check identified {len(issues)} issues: {issues}")
    
    def _identify_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify columns that likely contain dates."""
        date_columns = []
        
        for col in df.columns:
            # Check column name patterns
            if any(pattern in col.lower() for pattern in ['date', 'time', 'day']):
                date_columns.append(col)
                continue
            
            # Check data content
            sample = df[col].dropna().head(10)
            if len(sample) > 0:
                # Try to parse a few values as dates
                parsed_count = 0
                for val in sample:
                    try:
                        pd.to_datetime(val)
                        parsed_count += 1
                    except:
                        pass
                
                # If more than half parse as dates, consider it a date column
                if parsed_count > len(sample) / 2:
                    date_columns.append(col)
        
        return date_columns
    
    def _identify_amount_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify columns that likely contain amounts."""
        amount_columns = []
        
        for col in df.columns:
            # Check column name patterns
            if any(pattern in col.lower() for pattern in ['amount', 'debit', 'credit', 'balance', 'value']):
                amount_columns.append(col)
                continue
            
            # Check data content
            sample = df[col].dropna().head(10)
            if len(sample) > 0:
                # Check if values look like amounts
                numeric_count = 0
                for val in sample:
                    try:
                        # Try to parse as number (including with currency symbols)
                        cleaned = self._clean_amount_string(str(val))
                        float(cleaned)
                        numeric_count += 1
                    except:
                        pass
                
                # If more than half parse as numbers, consider it an amount column
                if numeric_count > len(sample) / 2:
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
    
    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """
        Calculate overall data quality score after cleaning.
        
        Args:
            df: Cleaned DataFrame
            
        Returns:
            float: Quality score between 0 and 1
        """
        try:
            if len(df) == 0:
                return 0.0
            
            # Calculate various quality metrics
            total_cells = len(df) * len(df.columns)
            null_cells = df.isnull().sum().sum()
            
            # Completeness score (1.0 - null ratio)
            completeness_score = 1.0 - (null_cells / total_cells) if total_cells > 0 else 0.0
            
            # Consistency score (1.0 - duplicate ratio)
            duplicate_rows = df.duplicated().sum()
            consistency_score = 1.0 - (duplicate_rows / len(df)) if len(df) > 0 else 0.0
            
            # Format validity score (estimate based on data types)
            validity_score = 0.9  # Assume 90% validity after cleaning
            
            # Calculate weighted overall score
            overall_score = (
                completeness_score * 0.4 +
                consistency_score * 0.3 +
                validity_score * 0.3
            )
            
            return round(overall_score, 3)
            
        except Exception:
            return 0.5  # Return moderate score if calculation fails
    
    def get_cleaning_statistics(self) -> Dict[str, Any]:
        """Return comprehensive cleaning statistics."""
        return self.cleaning_stats.copy()
