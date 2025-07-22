"""
SmartRecon Data Ingestion Module

This module handles the ingestion of financial data from various sources including:
- CSV files (GL and Bank statements)
- Excel files with multiple sheets
- Text files with different delimiters
- Automatic encoding detection and format validation
- Column mapping and data quality assessment
- File integrity checking and audit logging

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
import os
import chardet
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import json
from datetime import datetime
import hashlib

try:
    from ..utils.exceptions import DataIngestionError, DataValidationError, FileProcessingError
    from ..utils.helpers import ensure_directory_exists, get_file_hash, normalize_text
    from ..utils.validators import validate_file_path, validate_dataframe
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.exceptions import DataIngestionError, DataValidationError, FileProcessingError
    from utils.helpers import ensure_directory_exists, get_file_hash, normalize_text
    from utils.validators import validate_file_path, validate_dataframe

logger = logging.getLogger(__name__)


class DataIngestion:
    """
    Comprehensive data ingestion system for financial reconciliation data.
    
    Features:
    - Multi-format file support (CSV, Excel, TXT)
    - Automatic encoding detection
    - Smart column mapping and validation
    - Data quality assessment and reporting
    - File integrity checking
    - Comprehensive audit logging
    - Error handling and recovery
    """
    
    def __init__(self, config):
        """
        Initialize DataIngestion with configuration.
        
        Args:
            config: Configuration object containing ingestion parameters
        """
        self.config = config
        self.ingestion_log = []
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.txt']
        self.encoding_cache = {}
        
        # Default configuration parameters
        self.default_params = {
            'max_file_size_mb': 100,
            'encoding_detection': True,
            'auto_column_mapping': True,
            'data_quality_threshold': 0.8,
            'duplicate_tolerance': 0.95,
            'date_formats': [
                '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
                '%d-%m-%Y', '%m-%d-%Y', '%Y%m%d', '%d.%m.%Y'
            ]
        }
        
        # Load configuration parameters
        self.params = self._load_ingestion_parameters()
        
        logger.info("DataIngestion module initialized")
    
    def load_file(self, 
                  file_path: str,
                  file_type: str = 'auto',
                  encoding: Optional[str] = None,
                  sheet_name: Optional[str] = None,
                  delimiter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load and process data file with comprehensive validation.
        
        Args:
            file_path (str): Path to the data file
            file_type (str): Expected file type ('gl', 'bank', 'auto')
            encoding (str, optional): File encoding (auto-detected if None)
            sheet_name (str, optional): Excel sheet name
            delimiter (str, optional): CSV delimiter (auto-detected if None)
            
        Returns:
            Dict[str, Any]: Comprehensive ingestion results
            
        Raises:
            DataIngestionError: If file loading fails
            FileProcessingError: If file processing encounters errors
        """
        try:
            logger.info(f"Starting file ingestion: {file_path}")
            
            # Initialize ingestion session
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            ingestion_result = {
                'session_id': session_id,
                'file_info': {},
                'data': None,
                'validation_result': {},
                'column_mapping': {},
                'data_quality': {},
                'processing_stats': {},
                'warnings': [],
                'errors': []
            }
            
            start_time = datetime.now()
            
            # Step 1: Validate file path and basic properties
            file_info = self._validate_file_path(file_path)
            ingestion_result['file_info'] = file_info
            
            # Step 2: Detect file encoding if not provided
            if encoding is None and self.params['encoding_detection']:
                encoding = self._detect_encoding(file_path)
            
            # Step 3: Load file data based on format
            raw_data = self._load_file_data(
                file_path, encoding, sheet_name, delimiter
            )
            
            # Step 4: Validate basic data structure
            validation_result = self._validate_data_structure(raw_data, file_type)
            ingestion_result['validation_result'] = validation_result
            
            if not validation_result['is_valid']:
                ingestion_result['errors'].extend(validation_result['errors'])
                raise DataValidationError(f"Data validation failed: {validation_result['errors']}")
            
            # Step 5: Apply column mapping
            if self.params['auto_column_mapping']:
                mapped_data, column_mapping = self._apply_column_mapping(raw_data, file_type)
                ingestion_result['column_mapping'] = column_mapping
            else:
                mapped_data = raw_data
                ingestion_result['column_mapping'] = {'applied': False}
            
            # Step 6: Perform data quality assessment
            data_quality = self._assess_data_quality(mapped_data)
            ingestion_result['data_quality'] = data_quality
            
            # Step 7: Final data preparation
            processed_data = self._prepare_final_data(mapped_data)
            ingestion_result['data'] = processed_data
            
            # Step 8: Calculate processing statistics
            processing_time = (datetime.now() - start_time).total_seconds()
            ingestion_result['processing_stats'] = {
                'processing_time_seconds': processing_time,
                'rows_loaded': len(processed_data),
                'columns_loaded': len(processed_data.columns),
                'file_size_mb': file_info['size_mb'],
                'encoding_used': encoding or 'auto-detected'
            }
            
            # Add warnings for data quality issues
            if data_quality['overall_score'] < self.params['data_quality_threshold']:
                ingestion_result['warnings'].append(
                    f"Data quality score ({data_quality['overall_score']:.2f}) below threshold ({self.params['data_quality_threshold']})"
                )
            
            logger.info(f"File ingestion completed successfully in {processing_time:.2f} seconds")
            return ingestion_result
            
        except Exception as e:
            logger.error(f"File ingestion failed: {str(e)}")
            raise DataIngestionError(f"Failed to load file {file_path}: {str(e)}") from e
    
    def validate_file(self, file_path: str, expected_type: str = 'auto') -> Dict[str, Any]:
        """
        Validate file without full loading for quick checks.
        
        Args:
            file_path (str): Path to the file
            expected_type (str): Expected file type
            
        Returns:
            Dict[str, Any]: Validation results
        """
        try:
            validation_result = {
                'is_valid': False,
                'file_type': None,
                'file_size': 0,
                'encoding': None,
                'column_count': 0,
                'row_count': 0,
                'errors': [],
                'warnings': []
            }
            
            # Basic file validation
            file_info = self._validate_file_path(file_path)
            validation_result['file_size'] = file_info['size_bytes']
            
            # Quick encoding detection
            encoding = self._detect_encoding(file_path)
            validation_result['encoding'] = encoding
            
            # Load first few rows for structure validation
            try:
                if file_path.lower().endswith(('.xlsx', '.xls')):
                    sample_data = pd.read_excel(file_path, nrows=5)
                else:
                    sample_data = pd.read_csv(file_path, nrows=5, encoding=encoding)
                
                validation_result['column_count'] = len(sample_data.columns)
                validation_result['row_count'] = len(sample_data)
                
                # Detect file type based on columns
                detected_type = self._detect_file_type(sample_data.columns.tolist())
                validation_result['file_type'] = detected_type
                
                # Validate against expected type
                if expected_type != 'auto' and detected_type != expected_type:
                    validation_result['warnings'].append(
                        f"Detected type '{detected_type}' doesn't match expected type '{expected_type}'"
                    )
                
                validation_result['is_valid'] = True
                
            except Exception as e:
                validation_result['errors'].append(f"Failed to read file sample: {str(e)}")
            
            return validation_result
            
        except Exception as e:
            return {
                'is_valid': False,
                'errors': [f"Validation failed: {str(e)}"]
            }
    
    def _load_ingestion_parameters(self) -> Dict[str, Any]:
        """Load ingestion parameters from configuration."""
        params = self.default_params.copy()
        
        # Override with configuration values if available
        if hasattr(self.config, 'get_data_ingestion_config'):
            config_params = self.config.get_data_ingestion_config()
            params.update(config_params)
        
        return params
    
    def _validate_file_path(self, file_path: str) -> Dict[str, Any]:
        """Validate file path and extract basic information."""
        if not os.path.exists(file_path):
            raise FileProcessingError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise FileProcessingError(f"Path is not a file: {file_path}")
        
        # Get file information
        file_stat = os.stat(file_path)
        file_size_bytes = file_stat.st_size
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        # Check file size limits
        if file_size_mb > self.params['max_file_size_mb']:
            raise FileProcessingError(
                f"File size ({file_size_mb:.2f} MB) exceeds limit ({self.params['max_file_size_mb']} MB)"
            )
        
        # Check file format
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_formats:
            raise FileProcessingError(
                f"Unsupported file format: {file_extension}. Supported: {self.supported_formats}"
            )
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'extension': file_extension,
            'size_bytes': file_size_bytes,
            'size_mb': file_size_mb,
            'modified_time': datetime.fromtimestamp(file_stat.st_mtime),
            'file_hash': get_file_hash(file_path)
        }
    
    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using chardet."""
        if file_path in self.encoding_cache:
            return self.encoding_cache[file_path]
        
        try:
            # Read a sample of the file for encoding detection
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
            
            detection_result = chardet.detect(raw_data)
            encoding = detection_result['encoding']
            confidence = detection_result['confidence']
            
            # Fallback to common encodings if confidence is low
            if confidence < 0.7:
                common_encodings = ['utf-8', 'latin-1', 'windows-1252', 'cp1252']
                for enc in common_encodings:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            f.read(1000)  # Try to read some data
                        encoding = enc
                        break
                    except:
                        continue
            
            # Cache the result
            self.encoding_cache[file_path] = encoding
            logger.debug(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
            return encoding
            
        except Exception as e:
            logger.warning(f"Encoding detection failed, using utf-8: {e}")
            return 'utf-8'
    
    def _load_file_data(self, 
                       file_path: str,
                       encoding: str,
                       sheet_name: Optional[str] = None,
                       delimiter: Optional[str] = None) -> pd.DataFrame:
        """Load data from file based on format."""
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension in ['.xlsx', '.xls']:
                # Excel file handling
                if sheet_name:
                    data = pd.read_excel(file_path, sheet_name=sheet_name)
                else:
                    # Try to load the first sheet
                    excel_file = pd.ExcelFile(file_path)
                    if len(excel_file.sheet_names) > 1:
                        logger.warning(f"Multiple sheets found, using first sheet: {excel_file.sheet_names[0]}")
                    data = pd.read_excel(file_path, sheet_name=0)
            
            elif file_extension == '.csv':
                # CSV file handling
                if delimiter is None:
                    # Auto-detect delimiter
                    delimiter = self._detect_delimiter(file_path, encoding)
                
                data = pd.read_csv(
                    file_path,
                    encoding=encoding,
                    delimiter=delimiter,
                    parse_dates=False,  # We'll handle date parsing later
                    dtype=str,  # Load as strings initially
                    na_values=['', 'NULL', 'null', 'N/A', 'n/a', '#N/A']
                )
            
            elif file_extension == '.txt':
                # Text file handling (assume tab-delimited or detect)
                if delimiter is None:
                    delimiter = self._detect_delimiter(file_path, encoding)
                
                data = pd.read_csv(
                    file_path,
                    encoding=encoding,
                    delimiter=delimiter,
                    dtype=str,
                    na_values=['', 'NULL', 'null', 'N/A', 'n/a', '#N/A']
                )
            
            else:
                raise FileProcessingError(f"Unsupported file format: {file_extension}")
            
            # Basic data cleaning
            data = data.dropna(how='all')  # Remove completely empty rows
            data.columns = data.columns.str.strip()  # Clean column names
            
            logger.info(f"Loaded {len(data)} rows and {len(data.columns)} columns")
            return data
            
        except Exception as e:
            raise FileProcessingError(f"Failed to load file data: {str(e)}") from e
    
    def _detect_delimiter(self, file_path: str, encoding: str) -> str:
        """Detect delimiter for CSV/text files."""
        common_delimiters = [',', '\t', ';', '|', ':']
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                sample_lines = [f.readline() for _ in range(5)]
            
            delimiter_scores = {}
            
            for delimiter in common_delimiters:
                scores = []
                for line in sample_lines:
                    if line.strip():
                        count = line.count(delimiter)
                        scores.append(count)
                
                if scores:
                    # Check for consistency
                    avg_count = sum(scores) / len(scores)
                    variance = sum((x - avg_count) ** 2 for x in scores) / len(scores)
                    
                    # Prefer delimiters with higher average count and lower variance
                    delimiter_scores[delimiter] = avg_count - variance
            
            if delimiter_scores:
                best_delimiter = max(delimiter_scores, key=delimiter_scores.get)
                logger.debug(f"Detected delimiter: '{best_delimiter}'")
                return best_delimiter
            else:
                return ','  # Default to comma
                
        except Exception as e:
            logger.warning(f"Delimiter detection failed, using comma: {e}")
            return ','
    
    def _validate_data_structure(self, data: pd.DataFrame, file_type: str) -> Dict[str, Any]:
        """Validate basic data structure and requirements."""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'detected_type': None,
            'column_analysis': {}
        }
        
        # Check if data is not empty
        if len(data) == 0:
            validation_result['is_valid'] = False
            validation_result['errors'].append("File contains no data rows")
            return validation_result
        
        # Detect file type based on columns
        detected_type = self._detect_file_type(data.columns.tolist())
        validation_result['detected_type'] = detected_type
        
        # Get expected columns based on file type
        expected_columns = self._get_expected_columns(file_type if file_type != 'auto' else detected_type)
        
        # Check for required columns
        missing_required = []
        for col in expected_columns.get('required', []):
            if not any(self._column_name_matches(col, data_col) for data_col in data.columns):
                missing_required.append(col)
        
        if missing_required:
            validation_result['warnings'].append(f"Missing expected columns: {missing_required}")
        
        # Analyze each column
        for col in data.columns:
            analysis = self._analyze_column(data[col])
            validation_result['column_analysis'][col] = analysis
        
        return validation_result
    
    def _detect_file_type(self, columns: List[str]) -> str:
        """Detect file type based on column names."""
        gl_indicators = ['account', 'journal', 'posting', 'debit', 'credit', 'gl']
        bank_indicators = ['balance', 'bank', 'statement', 'cleared', 'reconciled']
        
        gl_score = sum(1 for col in columns if any(indicator in col.lower() for indicator in gl_indicators))
        bank_score = sum(1 for col in columns if any(indicator in col.lower() for indicator in bank_indicators))
        
        if gl_score > bank_score:
            return 'gl'
        elif bank_score > gl_score:
            return 'bank'
        else:
            return 'unknown'
    
    def _get_expected_columns(self, file_type: str) -> Dict[str, List[str]]:
        """Get expected columns for file type."""
        if hasattr(self.config, 'get_file_mapping'):
            return self.config.get_file_mapping(file_type)
        
        # Default expectations
        if file_type == 'gl':
            return {
                'required': ['date', 'description', 'amount'],
                'optional': ['account', 'reference', 'department']
            }
        elif file_type == 'bank':
            return {
                'required': ['date', 'description', 'amount'],
                'optional': ['balance', 'reference']
            }
        else:
            return {
                'required': ['date', 'description', 'amount'],
                'optional': []
            }
    
    def _column_name_matches(self, expected: str, actual: str) -> bool:
        """Check if column names match (fuzzy matching)."""
        expected_norm = normalize_text(expected)
        actual_norm = normalize_text(actual)
        
        # Direct match
        if expected_norm == actual_norm:
            return True
        
        # Contains match
        if expected_norm in actual_norm or actual_norm in expected_norm:
            return True
        
        # Common variations
        variations = {
            'date': ['date', 'transaction_date', 'trans_date', 'posting_date', 'value_date'],
            'description': ['description', 'memo', 'narrative', 'details', 'reference'],
            'amount': ['amount', 'value', 'debit_credit', 'net_amount', 'transaction_amount'],
            'reference': ['reference', 'ref', 'document_number', 'doc_ref', 'check_number']
        }
        
        for standard, variants in variations.items():
            if expected_norm == standard and actual_norm in variants:
                return True
        
        return False
    
    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze individual column characteristics."""
        analysis = {
            'data_type': str(series.dtype),
            'null_count': series.isnull().sum(),
            'unique_count': series.nunique(),
            'sample_values': series.dropna().head(3).tolist(),
            'likely_type': 'unknown'
        }
        
        # Determine likely data type
        non_null_series = series.dropna()
        if len(non_null_series) > 0:
            # Check for dates
            if self._is_likely_date_column(non_null_series):
                analysis['likely_type'] = 'date'
            # Check for amounts
            elif self._is_likely_amount_column(non_null_series):
                analysis['likely_type'] = 'amount'
            # Check for text
            elif non_null_series.dtype == 'object':
                analysis['likely_type'] = 'text'
        
        return analysis
    
    def _is_likely_date_column(self, series: pd.Series) -> bool:
        """Check if column likely contains dates."""
        sample_values = series.head(10)
        date_count = 0
        
        for value in sample_values:
            for date_format in self.params['date_formats']:
                try:
                    datetime.strptime(str(value).strip(), date_format)
                    date_count += 1
                    break
                except:
                    continue
        
        return date_count / len(sample_values) > 0.7
    
    def _is_likely_amount_column(self, series: pd.Series) -> bool:
        """Check if column likely contains monetary amounts."""
        sample_values = series.head(10)
        amount_count = 0
        
        for value in sample_values:
            try:
                # Try to parse as float after cleaning
                cleaned = str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', '').strip()
                float(cleaned)
                amount_count += 1
            except:
                continue
        
        return amount_count / len(sample_values) > 0.7
    
    def _apply_column_mapping(self, data: pd.DataFrame, file_type: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Apply intelligent column mapping."""
        mapping_result = {
            'applied': True,
            'mappings': {},
            'unmapped_columns': [],
            'confidence_scores': {}
        }
        
        # Get column mapping configuration
        if hasattr(self.config, 'get_file_mapping'):
            mapping_config = self.config.get_file_mapping(file_type)
            column_mapping = mapping_config.get('column_mapping', {})
        else:
            column_mapping = self._get_default_column_mapping(file_type)
        
        mapped_data = data.copy()
        
        # Apply mappings
        for standard_name, possible_names in column_mapping.items():
            best_match = None
            best_score = 0
            
            for col in data.columns:
                for possible_name in possible_names:
                    if self._column_name_matches(possible_name, col):
                        score = len(possible_name) / len(col)  # Prefer more specific matches
                        if score > best_score:
                            best_match = col
                            best_score = score
            
            if best_match:
                if standard_name != best_match:
                    mapped_data.rename(columns={best_match: standard_name}, inplace=True)
                mapping_result['mappings'][standard_name] = best_match
                mapping_result['confidence_scores'][standard_name] = best_score
            else:
                mapping_result['unmapped_columns'].append(standard_name)
        
        return mapped_data, mapping_result
    
    def _get_default_column_mapping(self, file_type: str) -> Dict[str, List[str]]:
        """Get default column mapping for file type."""
        if file_type == 'gl':
            return {
                'date': ['date', 'transaction_date', 'trans_date', 'posting_date'],
                'description': ['description', 'memo', 'narrative', 'details'],
                'amount': ['amount', 'value', 'debit_credit', 'net_amount'],
                'reference': ['reference', 'ref', 'document_number', 'doc_ref'],
                'account': ['account', 'account_number', 'gl_account']
            }
        elif file_type == 'bank':
            return {
                'date': ['date', 'value_date', 'booking_date', 'transaction_date'],
                'description': ['description', 'reference', 'memo', 'narrative'],
                'amount': ['amount', 'debit', 'credit', 'transaction_amount'],
                'balance': ['balance', 'running_balance', 'account_balance']
            }
        else:
            return {
                'date': ['date'],
                'description': ['description'],
                'amount': ['amount']
            }
    
    def _assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess overall data quality."""
        quality_metrics = {
            'completeness': {},
            'consistency': {},
            'validity': {},
            'overall_score': 0.0
        }
        
        # Completeness assessment
        total_cells = len(data) * len(data.columns)
        null_cells = data.isnull().sum().sum()
        completeness_score = 1 - (null_cells / total_cells) if total_cells > 0 else 0
        
        quality_metrics['completeness'] = {
            'score': completeness_score,
            'null_percentage': (null_cells / total_cells) * 100 if total_cells > 0 else 0,
            'columns_with_nulls': data.columns[data.isnull().any()].tolist()
        }
        
        # Consistency assessment (check for duplicates)
        duplicate_rows = data.duplicated().sum()
        consistency_score = 1 - (duplicate_rows / len(data)) if len(data) > 0 else 0
        
        quality_metrics['consistency'] = {
            'score': consistency_score,
            'duplicate_rows': duplicate_rows,
            'duplicate_percentage': (duplicate_rows / len(data)) * 100 if len(data) > 0 else 0
        }
        
        # Validity assessment (basic format checking)
        validity_scores = []
        
        for col in data.columns:
            if 'date' in col.lower():
                valid_dates = self._count_valid_dates(data[col])
                validity_scores.append(valid_dates / len(data.dropna(subset=[col])) if len(data.dropna(subset=[col])) > 0 else 0)
            elif 'amount' in col.lower() or 'value' in col.lower():
                valid_amounts = self._count_valid_amounts(data[col])
                validity_scores.append(valid_amounts / len(data.dropna(subset=[col])) if len(data.dropna(subset=[col])) > 0 else 0)
        
        validity_score = sum(validity_scores) / len(validity_scores) if validity_scores else 0
        
        quality_metrics['validity'] = {
            'score': validity_score,
            'column_validity_count': len(validity_scores)
        }
        
        # Calculate overall score
        quality_metrics['overall_score'] = (
            completeness_score * 0.4 +
            consistency_score * 0.3 +
            validity_score * 0.3
        )
        
        return quality_metrics
    
    def _count_valid_dates(self, series: pd.Series) -> int:
        """Count valid dates in series."""
        valid_count = 0
        for value in series.dropna():
            for date_format in self.params['date_formats']:
                try:
                    datetime.strptime(str(value).strip(), date_format)
                    valid_count += 1
                    break
                except:
                    continue
        return valid_count
    
    def _count_valid_amounts(self, series: pd.Series) -> int:
        """Count valid amounts in series."""
        valid_count = 0
        for value in series.dropna():
            try:
                cleaned = str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', '').strip()
                float(cleaned)
                valid_count += 1
            except:
                continue
        return valid_count
    
    def _prepare_final_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare final cleaned data for processing."""
        final_data = data.copy()
        
        # Remove completely empty rows and columns
        final_data = final_data.dropna(how='all')
        final_data = final_data.loc[:, ~final_data.isnull().all()]
        
        # Reset index
        final_data.reset_index(drop=True, inplace=True)
        
        return final_data
    
    def get_ingestion_log(self) -> List[Dict[str, Any]]:
        """Return comprehensive ingestion log."""
        return self.ingestion_log.copy()
    
    def clear_cache(self):
        """Clear encoding cache."""
        self.encoding_cache.clear()
        logger.info("Encoding cache cleared")
