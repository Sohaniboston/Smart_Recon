#!/usr/bin/env python3
"""
Unit tests for DataIngestion module.

Tests cover:
- File loading functionality
- Error handling
- Data validation
- Column detection
- Encoding detection
- File format support

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import pandas as pd
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.modules.data_ingestion import DataIngestion
from src.config import Config
from src.utils.exceptions import DataIngestionError, FileValidationError


class TestDataIngestion(unittest.TestCase):
    """Test cases for DataIngestion class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.ingestion = DataIngestion(self.config)
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample test data
        self.sample_data = {
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03'],
            'Amount': [100.50, -75.25, 250.00],
            'Description': ['Payment received', 'Service charge', 'Deposit'],
            'Reference': ['REF001', 'REF002', 'REF003']
        }
    
    def tearDown(self):
        """Clean up test environment."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_csv(self, filename: str, data: dict = None):
        """Create a test CSV file."""
        if data is None:
            data = self.sample_data
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.temp_dir, filename)
        df.to_csv(filepath, index=False)
        return filepath
    
    def create_test_excel(self, filename: str, data: dict = None):
        """Create a test Excel file."""
        if data is None:
            data = self.sample_data
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.temp_dir, filename)
        df.to_excel(filepath, index=False)
        return filepath
    
    def test_load_csv_file_success(self):
        """Test successful CSV file loading."""
        filepath = self.create_test_csv('test.csv')
        
        result = self.ingestion.load_file(filepath, file_type='gl')
        
        self.assertIsInstance(result, dict)
        self.assertIn('data', result)
        self.assertIn('metadata', result)
        self.assertIsInstance(result['data'], pd.DataFrame)
        self.assertEqual(len(result['data']), 3)
        self.assertEqual(result['metadata']['record_count'], 3)
    
    def test_load_excel_file_success(self):
        """Test successful Excel file loading."""
        filepath = self.create_test_excel('test.xlsx')
        
        result = self.ingestion.load_file(filepath, file_type='bank')
        
        self.assertIsInstance(result, dict)
        self.assertIn('data', result)
        self.assertIn('metadata', result)
        self.assertIsInstance(result['data'], pd.DataFrame)
        self.assertEqual(len(result['data']), 3)
    
    def test_load_nonexistent_file(self):
        """Test error handling for non-existent file."""
        with self.assertRaises(FileValidationError):
            self.ingestion.load_file('/nonexistent/file.csv', file_type='gl')
    
    def test_load_unsupported_format(self):
        """Test error handling for unsupported file format."""
        # Create a text file
        filepath = os.path.join(self.temp_dir, 'test.txt')
        with open(filepath, 'w') as f:
            f.write('This is not a CSV or Excel file')
        
        with self.assertRaises(DataIngestionError):
            self.ingestion.load_file(filepath, file_type='gl')
    
    def test_validate_file_structure_success(self):
        """Test successful file structure validation."""
        filepath = self.create_test_csv('test.csv')
        
        # Should not raise an exception
        self.ingestion.validate_file_structure(filepath)
    
    def test_validate_file_structure_missing_file(self):
        """Test file structure validation with missing file."""
        with self.assertRaises(FileValidationError):
            self.ingestion.validate_file_structure('/nonexistent/file.csv')
    
    def test_detect_column_mapping(self):
        """Test automatic column detection."""
        filepath = self.create_test_csv('test.csv')
        df = pd.read_csv(filepath)
        
        mapping = self.ingestion.detect_column_mapping(df, 'gl')
        
        self.assertIsInstance(mapping, dict)
        self.assertIn('date_column', mapping)
        self.assertIn('amount_column', mapping)
        self.assertIn('description_column', mapping)
    
    def test_assess_data_quality(self):
        """Test data quality assessment."""
        df = pd.DataFrame(self.sample_data)
        
        quality = self.ingestion.assess_data_quality(df)
        
        self.assertIsInstance(quality, dict)
        self.assertIn('completeness_score', quality)
        self.assertIn('missing_values', quality)
        self.assertIn('duplicate_rows', quality)
        self.assertGreater(quality['completeness_score'], 0)
    
    def test_load_empty_file(self):
        """Test loading empty file."""
        # Create empty CSV
        filepath = os.path.join(self.temp_dir, 'empty.csv')
        with open(filepath, 'w') as f:
            f.write('')
        
        with self.assertRaises(DataIngestionError):
            self.ingestion.load_file(filepath, file_type='gl')
    
    def test_load_file_with_encoding_issues(self):
        """Test handling files with encoding issues."""
        # Create file with special characters
        filepath = os.path.join(self.temp_dir, 'encoding_test.csv')
        with open(filepath, 'w', encoding='latin-1') as f:
            f.write('Date,Amount,Description\n')
            f.write('2025-01-01,100.50,Café payment\n')
        
        # Should handle encoding detection
        result = self.ingestion.load_file(filepath, file_type='gl')
        self.assertIsInstance(result['data'], pd.DataFrame)
    
    def test_malformed_csv(self):
        """Test handling malformed CSV files."""
        filepath = os.path.join(self.temp_dir, 'malformed.csv')
        with open(filepath, 'w') as f:
            f.write('Date,Amount,Description\n')
            f.write('2025-01-01,100.50\n')  # Missing column
            f.write('2025-01-02,75.25,Payment,Extra\n')  # Extra column
        
        # Should handle malformed data gracefully
        result = self.ingestion.load_file(filepath, file_type='gl')
        self.assertIsInstance(result['data'], pd.DataFrame)
    
    def test_large_file_handling(self):
        """Test handling of large datasets."""
        # Create large dataset
        large_data = {
            'Date': ['2025-01-01'] * 10000,
            'Amount': [100.50] * 10000,
            'Description': ['Test transaction'] * 10000,
            'Reference': [f'REF{i:06d}' for i in range(10000)]
        }
        
        filepath = self.create_test_csv('large_file.csv', large_data)
        
        result = self.ingestion.load_file(filepath, file_type='gl')
        
        self.assertEqual(len(result['data']), 10000)
        self.assertEqual(result['metadata']['record_count'], 10000)
    
    def test_file_type_validation(self):
        """Test file type parameter validation."""
        filepath = self.create_test_csv('test.csv')
        
        # Valid file types
        for file_type in ['gl', 'bank']:
            result = self.ingestion.load_file(filepath, file_type=file_type)
            self.assertIsInstance(result, dict)
        
        # Invalid file type
        with self.assertRaises(ValueError):
            self.ingestion.load_file(filepath, file_type='invalid')
    
    def test_metadata_generation(self):
        """Test metadata generation for loaded files."""
        filepath = self.create_test_csv('test.csv')
        
        result = self.ingestion.load_file(filepath, file_type='gl')
        metadata = result['metadata']
        
        # Check required metadata fields
        required_fields = [
            'filename', 'file_path', 'file_size', 'load_timestamp',
            'record_count', 'column_count', 'data_quality'
        ]
        
        for field in required_fields:
            self.assertIn(field, metadata)
        
        self.assertEqual(metadata['filename'], 'test.csv')
        self.assertEqual(metadata['record_count'], 3)
        self.assertEqual(metadata['column_count'], 4)


class TestDataIngestionEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for DataIngestion."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.ingestion = DataIngestion(self.config)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_corrupted_excel_file(self):
        """Test handling of corrupted Excel files."""
        filepath = os.path.join(self.temp_dir, 'corrupted.xlsx')
        
        # Create a fake Excel file (just binary data)
        with open(filepath, 'wb') as f:
            f.write(b'This is not a valid Excel file')
        
        with self.assertRaises(DataIngestionError):
            self.ingestion.load_file(filepath, file_type='gl')
    
    def test_permission_denied_file(self):
        """Test handling of files with permission issues."""
        if os.name != 'nt':  # Skip on Windows due to permission model differences
            filepath = os.path.join(self.temp_dir, 'no_permission.csv')
            
            # Create file and remove read permissions
            with open(filepath, 'w') as f:
                f.write('Date,Amount\n2025-01-01,100\n')
            
            os.chmod(filepath, 0o000)
            
            try:
                with self.assertRaises(FileValidationError):
                    self.ingestion.load_file(filepath, file_type='gl')
            finally:
                # Restore permissions for cleanup
                os.chmod(filepath, 0o644)
    
    def test_extremely_large_file(self):
        """Test behavior with extremely large files."""
        # This test simulates large file handling without actually creating large files
        with patch('pandas.read_csv') as mock_read_csv:
            # Mock a very large DataFrame
            large_df = pd.DataFrame({
                'Date': ['2025-01-01'] * 1000000,
                'Amount': [100.0] * 1000000
            })
            mock_read_csv.return_value = large_df
            
            filepath = os.path.join(self.temp_dir, 'huge_file.csv')
            
            # Create small actual file for validation
            with open(filepath, 'w') as f:
                f.write('Date,Amount\n2025-01-01,100\n')
            
            result = self.ingestion.load_file(filepath, file_type='gl')
            
            # Should handle large datasets
            self.assertEqual(len(result['data']), 1000000)


if __name__ == '__main__':
    unittest.main()
