#!/usr/bin/env python3
"""
Unit tests for DataCleaner module.

Tests cover:
- Data cleaning functionality
- Date standardization
- Amount normalization
- Column standardization
- Missing value handling
- Duplicate detection
- Data quality scoring

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.modules.data_cleaning import DataCleaner
from src.config import Config
from src.utils.exceptions import DataCleaningError


class TestDataCleaner(unittest.TestCase):
    """Test cases for DataCleaner class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.cleaner = DataCleaner(self.config)
        
        # Sample test data with various data quality issues
        self.sample_data = pd.DataFrame({
            'Date': ['2025-01-01', '01/02/2025', '2025-1-3', '2025/01/04', None],
            'Amount': ['100.50', '-75.25', '250', '$300.75', ''],
            'Description': ['Payment received', 'SERVICE CHARGE', '  Deposit  ', 'Transfer', None],
            'Reference': ['REF001', 'ref002', 'REF003', '', 'REF005'],
            'Account': ['12345', '12345', '67890', '12345', '67890']
        })
        
        # Data with duplicates
        self.duplicate_data = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-01', '2025-01-02'],
            'Amount': [100.50, 100.50, 200.00],
            'Description': ['Payment', 'Payment', 'Transfer'],
            'Reference': ['REF001', 'REF001', 'REF002']
        })
    
    def test_clean_data_success(self):
        """Test successful data cleaning."""
        result = self.cleaner.clean_data(self.sample_data, data_type='gl')
        
        self.assertIsInstance(result, dict)
        self.assertIn('cleaned_data', result)
        self.assertIn('cleaning_report', result)
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)
        
        cleaned_df = result['cleaned_data']
        
        # Should have same or fewer rows (after cleaning)
        self.assertLessEqual(len(cleaned_df), len(self.sample_data))
        
        # Check that data quality improved
        self.assertIn('data_quality_score', result['cleaning_report'])
    
    def test_standardize_dates(self):
        """Test date standardization."""
        date_series = pd.Series(['2025-01-01', '01/02/2025', '2025-1-3', '2025/01/04'])
        
        standardized = self.cleaner.standardize_dates(date_series)
        
        # All dates should be in standard format
        self.assertTrue(all(pd.notna(standardized)))
        
        # Should be datetime type
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(standardized))
    
    def test_standardize_dates_with_invalid(self):
        """Test date standardization with invalid dates."""
        date_series = pd.Series(['2025-01-01', 'invalid_date', '2025-01-03', None])
        
        standardized = self.cleaner.standardize_dates(date_series)
        
        # Valid dates should be converted, invalid should be NaT
        self.assertTrue(pd.notna(standardized.iloc[0]))
        self.assertTrue(pd.isna(standardized.iloc[1]))  # invalid_date
        self.assertTrue(pd.notna(standardized.iloc[2]))
        self.assertTrue(pd.isna(standardized.iloc[3]))  # None
    
    def test_normalize_amounts(self):
        """Test amount normalization."""
        amount_series = pd.Series(['100.50', '-75.25', '250', '$300.75', '1,500.00'])
        
        normalized = self.cleaner.normalize_amounts(amount_series)
        
        # Should be numeric type
        self.assertTrue(pd.api.types.is_numeric_dtype(normalized))
        
        # Check specific values
        self.assertEqual(normalized.iloc[0], 100.50)
        self.assertEqual(normalized.iloc[1], -75.25)
        self.assertEqual(normalized.iloc[2], 250.00)
        self.assertEqual(normalized.iloc[3], 300.75)
        self.assertEqual(normalized.iloc[4], 1500.00)
    
    def test_normalize_amounts_with_invalid(self):
        """Test amount normalization with invalid amounts."""
        amount_series = pd.Series(['100.50', 'invalid', '', None, 'ABC'])
        
        normalized = self.cleaner.normalize_amounts(amount_series)
        
        # Valid amount should be converted
        self.assertEqual(normalized.iloc[0], 100.50)
        
        # Invalid amounts should be NaN
        self.assertTrue(pd.isna(normalized.iloc[1]))  # 'invalid'
        self.assertTrue(pd.isna(normalized.iloc[2]))  # ''
        self.assertTrue(pd.isna(normalized.iloc[3]))  # None
        self.assertTrue(pd.isna(normalized.iloc[4]))  # 'ABC'
    
    def test_standardize_column_names(self):
        """Test column name standardization."""
        df = pd.DataFrame({
            'Transaction Date': [1, 2, 3],
            'AMOUNT': [1, 2, 3],
            '  Description  ': [1, 2, 3],
            'Ref #': [1, 2, 3]
        })
        
        standardized_df = self.cleaner.standardize_column_names(df)
        
        # Check that column names are standardized
        expected_columns = ['transaction_date', 'amount', 'description', 'ref_#']
        self.assertEqual(list(standardized_df.columns), expected_columns)
    
    def test_handle_missing_values(self):
        """Test missing value handling."""
        df = pd.DataFrame({
            'Date': ['2025-01-01', None, '2025-01-03'],
            'Amount': [100.50, np.nan, 250.00],
            'Description': ['Payment', '', 'Transfer'],
            'Reference': ['REF001', None, 'REF003']
        })
        
        cleaned_df = self.cleaner.handle_missing_values(df, strategy='drop')
        
        # Should have fewer rows after dropping rows with missing values
        self.assertLess(len(cleaned_df), len(df))
    
    def test_handle_missing_values_fill_strategy(self):
        """Test missing value handling with fill strategy."""
        df = pd.DataFrame({
            'Date': ['2025-01-01', None, '2025-01-03'],
            'Amount': [100.50, np.nan, 250.00],
            'Description': ['Payment', '', 'Transfer'],
            'Reference': ['REF001', None, 'REF003']
        })
        
        cleaned_df = self.cleaner.handle_missing_values(df, strategy='fill')
        
        # Should have same number of rows
        self.assertEqual(len(cleaned_df), len(df))
        
        # Missing values should be filled
        self.assertFalse(cleaned_df.isnull().any().any())
    
    def test_detect_duplicates(self):
        """Test duplicate detection."""
        duplicates_info = self.cleaner.detect_duplicates(self.duplicate_data)
        
        self.assertIsInstance(duplicates_info, dict)
        self.assertIn('duplicate_count', duplicates_info)
        self.assertIn('duplicate_indices', duplicates_info)
        
        # Should detect the duplicate row
        self.assertGreater(duplicates_info['duplicate_count'], 0)
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        cleaned_df = self.cleaner.remove_duplicates(self.duplicate_data)
        
        # Should have fewer rows after removing duplicates
        self.assertLess(len(cleaned_df), len(self.duplicate_data))
        
        # Should not have any duplicates remaining
        self.assertEqual(len(cleaned_df), len(cleaned_df.drop_duplicates()))
    
    def test_calculate_data_quality_score(self):
        """Test data quality score calculation."""
        score = self.cleaner.calculate_data_quality_score(self.sample_data)
        
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_clean_text_data(self):
        """Test text data cleaning."""
        text_series = pd.Series(['  Payment Received  ', 'SERVICE CHARGE', 'transfer', None])
        
        cleaned_text = self.cleaner.clean_text_data(text_series)
        
        # Should trim whitespace and standardize case
        self.assertEqual(cleaned_text.iloc[0], 'Payment Received')
        self.assertEqual(cleaned_text.iloc[1], 'Service Charge')
        self.assertEqual(cleaned_text.iloc[2], 'Transfer')
        
        # Should handle None values
        self.assertTrue(pd.isna(cleaned_text.iloc[3]) or cleaned_text.iloc[3] == '')
    
    def test_detect_column_types(self):
        """Test automatic column type detection."""
        column_types = self.cleaner.detect_column_types(self.sample_data)
        
        self.assertIsInstance(column_types, dict)
        
        # Should identify different column types
        for column in self.sample_data.columns:
            self.assertIn(column, column_types)
            self.assertIsInstance(column_types[column], str)
    
    def test_validate_data_integrity(self):
        """Test data integrity validation."""
        validation_result = self.cleaner.validate_data_integrity(self.sample_data, data_type='gl')
        
        self.assertIsInstance(validation_result, dict)
        self.assertIn('is_valid', validation_result)
        self.assertIn('validation_errors', validation_result)
        self.assertIn('warnings', validation_result)
        
        self.assertIsInstance(validation_result['is_valid'], bool)
        self.assertIsInstance(validation_result['validation_errors'], list)
        self.assertIsInstance(validation_result['warnings'], list)
    
    def test_clean_data_with_different_types(self):
        """Test cleaning data with different data types (GL vs Bank)."""
        # Test GL data
        gl_result = self.cleaner.clean_data(self.sample_data, data_type='gl')
        self.assertIn('cleaned_data', gl_result)
        
        # Test Bank data
        bank_result = self.cleaner.clean_data(self.sample_data, data_type='bank')
        self.assertIn('cleaned_data', bank_result)
        
        # Both should work without errors
        self.assertIsInstance(gl_result['cleaned_data'], pd.DataFrame)
        self.assertIsInstance(bank_result['cleaned_data'], pd.DataFrame)
    
    def test_clean_empty_dataframe(self):
        """Test cleaning empty DataFrame."""
        empty_df = pd.DataFrame()
        
        with self.assertRaises(DataCleaningError):
            self.cleaner.clean_data(empty_df, data_type='gl')
    
    def test_clean_single_row_dataframe(self):
        """Test cleaning DataFrame with single row."""
        single_row_df = pd.DataFrame({
            'Date': ['2025-01-01'],
            'Amount': [100.50],
            'Description': ['Test payment']
        })
        
        result = self.cleaner.clean_data(single_row_df, data_type='gl')
        
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)
        self.assertEqual(len(result['cleaned_data']), 1)
    
    def test_extreme_data_values(self):
        """Test handling of extreme data values."""
        extreme_data = pd.DataFrame({
            'Date': ['2025-01-01', '1900-01-01', '2100-01-01'],
            'Amount': [0.01, 999999999.99, -999999999.99],
            'Description': ['A' * 1000, '', 'Normal desc']
        })
        
        result = self.cleaner.clean_data(extreme_data, data_type='gl')
        
        # Should handle extreme values without crashing
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)
    
    def test_mixed_data_types_in_columns(self):
        """Test handling columns with mixed data types."""
        mixed_data = pd.DataFrame({
            'Date': ['2025-01-01', 12345, None, '2025-01-02'],
            'Amount': [100.50, '200', None, 'invalid'],
            'Description': ['Payment', 123, None, 'Transfer']
        })
        
        result = self.cleaner.clean_data(mixed_data, data_type='gl')
        
        # Should handle mixed types gracefully
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)


class TestDataCleanerConfiguration(unittest.TestCase):
    """Test DataCleaner with different configurations."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.sample_data = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-02'],
            'Amount': [100.50, 200.00],
            'Description': ['Payment', 'Transfer']
        })
    
    def test_custom_cleaning_configuration(self):
        """Test DataCleaner with custom configuration."""
        # Modify config for testing
        custom_config = Config()
        custom_config.data_cleaning['missing_value_strategy'] = 'fill'
        custom_config.data_cleaning['duplicate_handling'] = 'keep_first'
        
        cleaner = DataCleaner(custom_config)
        result = cleaner.clean_data(self.sample_data, data_type='gl')
        
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)
    
    def test_cleaning_thresholds(self):
        """Test cleaning with different quality thresholds."""
        # Create data with varying quality
        poor_quality_data = pd.DataFrame({
            'Date': ['2025-01-01', None, None, '2025-01-04'],
            'Amount': [100.50, None, None, 400.00],
            'Description': ['Payment', None, None, 'Transfer']
        })
        
        cleaner = DataCleaner(self.config)
        result = cleaner.clean_data(poor_quality_data, data_type='gl')
        
        # Should handle poor quality data appropriately
        self.assertIsInstance(result['cleaned_data'], pd.DataFrame)
        self.assertIn('data_quality_score', result['cleaning_report'])


if __name__ == '__main__':
    unittest.main()
