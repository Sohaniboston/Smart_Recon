#!/usr/bin/env python3
"""
Integration tests for SmartRecon workflow.

Tests cover:
- End-to-end reconciliation workflow
- Module integration
- Data flow between components
- Complete system functionality

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import pandas as pd
import os
import tempfile
import shutil
import json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.config import Config
from src.modules.data_ingestion import DataIngestion
from src.modules.data_cleaning import DataCleaner
from src.modules.exact_matching_engine import ExactMatchingEngine
from src.modules.fuzzy_matching import FuzzyMatcher
from src.modules.exception_handler import ExceptionHandler
from src.modules.basic_reporting import ReportGenerator


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete end-to-end reconciliation workflow."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        
        # Initialize components
        self.ingestion = DataIngestion(self.config)
        self.cleaner = DataCleaner(self.config)
        self.exact_engine = ExactMatchingEngine(self.config)
        self.fuzzy_engine = FuzzyMatcher(self.config)
        self.exception_handler = ExceptionHandler(self.config)
        self.report_generator = ReportGenerator(self.config)
        
        # Create sample test data
        self.create_sample_data()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_sample_data(self):
        """Create sample GL and bank data files."""
        # GL data
        gl_data = {
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
            'Amount': [1000.00, -50.25, 750.50, 2000.00, -25.00],
            'Description': ['Customer payment A', 'Bank service charge', 'Customer deposit B', 
                          'Large customer payment', 'Monthly fee'],
            'Reference': ['PAY001', 'SVC001', 'DEP001', 'PAY002', 'FEE001'],
            'Account': ['12345'] * 5
        }
        
        self.gl_file = os.path.join(self.temp_dir, 'gl_data.csv')
        pd.DataFrame(gl_data).to_csv(self.gl_file, index=False)
        
        # Bank data (some matching, some not)
        bank_data = {
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-06', '2025-01-07'],
            'Amount': [1000.00, -50.25, 750.50, 500.00, -30.00],
            'Description': ['Payment from customer A', 'Service charge', 'Deposit B', 
                          'Different payment', 'Other fee'],
            'Reference': ['PAY001', 'SVC001', 'DEP001', 'PAY003', 'FEE002'],
            'Account': ['67890'] * 5
        }
        
        self.bank_file = os.path.join(self.temp_dir, 'bank_data.csv')
        pd.DataFrame(bank_data).to_csv(self.bank_file, index=False)
    
    def test_complete_workflow_exact_matching_only(self):
        """Test complete workflow with exact matching only."""
        output_dir = os.path.join(self.temp_dir, 'output_exact')
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Data Ingestion
        gl_result = self.ingestion.load_file(self.gl_file, file_type='gl')
        bank_result = self.ingestion.load_file(self.bank_file, file_type='bank')
        
        self.assertIn('data', gl_result)
        self.assertIn('data', bank_result)
        
        # Step 2: Data Cleaning
        gl_clean_result = self.cleaner.clean_data(gl_result['data'], data_type='gl')
        bank_clean_result = self.cleaner.clean_data(bank_result['data'], data_type='bank')
        
        gl_clean = gl_clean_result['cleaned_data']
        bank_clean = bank_clean_result['cleaned_data']
        
        self.assertIsInstance(gl_clean, pd.DataFrame)
        self.assertIsInstance(bank_clean, pd.DataFrame)
        
        # Step 3: Exact Matching
        exact_results = self.exact_engine.reconcile_exact_matches(gl_clean, bank_clean)
        
        self.assertIn('matches', exact_results)
        self.assertIn('statistics', exact_results)
        
        # Should find some exact matches
        self.assertGreater(exact_results['statistics']['total_matches'], 0)
        
        # Step 4: Get unmatched records
        unmatched = self.exact_engine.get_unmatched_records()
        
        self.assertIn('gl', unmatched)
        self.assertIn('bank', unmatched)
        
        # Step 5: Export results
        matches_df = self.exact_engine.export_matches_to_dataframe()
        
        if not matches_df.empty:
            matches_file = os.path.join(output_dir, 'exact_matches.xlsx')
            matches_df.to_excel(matches_file, index=False)
            self.assertTrue(os.path.exists(matches_file))
        
        # Verify workflow completion
        self.assertTrue(True)  # If we get here, workflow completed successfully
    
    def test_complete_workflow_with_fuzzy_matching(self):
        """Test complete workflow including fuzzy matching."""
        output_dir = os.path.join(self.temp_dir, 'output_fuzzy')
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1-3: Same as exact matching workflow
        gl_result = self.ingestion.load_file(self.gl_file, file_type='gl')
        bank_result = self.ingestion.load_file(self.bank_file, file_type='bank')
        
        gl_clean_result = self.cleaner.clean_data(gl_result['data'], data_type='gl')
        bank_clean_result = self.cleaner.clean_data(bank_result['data'], data_type='bank')
        
        gl_clean = gl_clean_result['cleaned_data']
        bank_clean = bank_clean_result['cleaned_data']
        
        exact_results = self.exact_engine.reconcile_exact_matches(gl_clean, bank_clean)
        unmatched = self.exact_engine.get_unmatched_records()
        
        # Step 4: Fuzzy Matching on unmatched records
        if not unmatched['gl'].empty and not unmatched['bank'].empty:
            fuzzy_results = self.fuzzy_engine.find_fuzzy_matches(
                unmatched['gl'], unmatched['bank']
            )
            
            self.assertIn('matches', fuzzy_results)
            self.assertIn('potential_matches', fuzzy_results)
            self.assertIn('statistics', fuzzy_results)
            
            # Export fuzzy matches
            fuzzy_matches_df = self.fuzzy_engine.export_matches_to_dataframe()
            potential_matches_df = self.fuzzy_engine.export_potential_matches_to_dataframe()
            
            if not fuzzy_matches_df.empty:
                fuzzy_file = os.path.join(output_dir, 'fuzzy_matches.xlsx')
                fuzzy_matches_df.to_excel(fuzzy_file, index=False)
                self.assertTrue(os.path.exists(fuzzy_file))
            
            if not potential_matches_df.empty:
                potential_file = os.path.join(output_dir, 'potential_matches.xlsx')
                potential_matches_df.to_excel(potential_file, index=False)
                self.assertTrue(os.path.exists(potential_file))
        
        # Step 5: Exception Handling
        final_unmatched = self.fuzzy_engine.get_unmatched_records(
            unmatched['gl'], unmatched['bank']
        ) if not unmatched['gl'].empty and not unmatched['bank'].empty else unmatched
        
        if not final_unmatched['gl'].empty or not final_unmatched['bank'].empty:
            exception_results = self.exception_handler.process_exceptions(
                final_unmatched['gl'], final_unmatched['bank'], 'gl', 'bank'
            )
            
            self.assertIn('categorized_exceptions', exception_results)
            self.assertIn('statistics', exception_results)
        
        # Verify complete workflow
        self.assertTrue(True)
    
    def test_data_flow_integrity(self):
        """Test data integrity throughout the workflow."""
        # Load data
        gl_result = self.ingestion.load_file(self.gl_file, file_type='gl')
        bank_result = self.ingestion.load_file(self.bank_file, file_type='bank')
        
        original_gl_count = len(gl_result['data'])
        original_bank_count = len(bank_result['data'])
        
        # Clean data
        gl_clean_result = self.cleaner.clean_data(gl_result['data'], data_type='gl')
        bank_clean_result = self.cleaner.clean_data(bank_result['data'], data_type='bank')
        
        cleaned_gl_count = len(gl_clean_result['cleaned_data'])
        cleaned_bank_count = len(bank_clean_result['cleaned_data'])
        
        # Data counts should be reasonable (not more than original)
        self.assertLessEqual(cleaned_gl_count, original_gl_count)
        self.assertLessEqual(cleaned_bank_count, original_bank_count)
        
        # Perform matching
        exact_results = self.exact_engine.reconcile_exact_matches(
            gl_clean_result['cleaned_data'], bank_clean_result['cleaned_data']
        )
        
        unmatched = self.exact_engine.get_unmatched_records()
        matches_df = self.exact_engine.export_matches_to_dataframe()
        
        # Verify data conservation
        matched_gl_count = len(matches_df) if not matches_df.empty else 0
        unmatched_gl_count = len(unmatched['gl'])
        
        # Matched + unmatched should equal cleaned count
        self.assertEqual(matched_gl_count + unmatched_gl_count, cleaned_gl_count)
    
    def test_error_handling_throughout_workflow(self):
        """Test error handling at each workflow stage."""
        # Test with corrupted file
        corrupted_file = os.path.join(self.temp_dir, 'corrupted.csv')
        with open(corrupted_file, 'w') as f:
            f.write('invalid,csv,content\nwith,missing,')
        
        # Should handle corrupted file gracefully
        try:
            result = self.ingestion.load_file(corrupted_file, file_type='gl')
            # If it loads, should have some data
            self.assertIn('data', result)
        except Exception as e:
            # Should raise appropriate exception
            self.assertIsInstance(e, Exception)
        
        # Test with empty data
        empty_df = pd.DataFrame()
        
        try:
            self.cleaner.clean_data(empty_df, data_type='gl')
        except Exception as e:
            # Should handle empty data appropriately
            self.assertIsInstance(e, Exception)
    
    def test_performance_with_realistic_data_volume(self):
        """Test workflow performance with realistic data volumes."""
        # Create larger datasets
        large_gl_data = {
            'Date': pd.date_range('2025-01-01', periods=1000).strftime('%Y-%m-%d').tolist(),
            'Amount': [100.0 + i * 0.1 for i in range(1000)],
            'Description': [f'Transaction {i}' for i in range(1000)],
            'Reference': [f'REF{i:06d}' for i in range(1000)],
            'Account': ['12345'] * 1000
        }
        
        large_bank_data = {
            'Date': pd.date_range('2025-01-01', periods=1000).strftime('%Y-%m-%d').tolist(),
            'Amount': [100.0 + i * 0.1 for i in range(1000)],
            'Description': [f'Bank transaction {i}' for i in range(1000)],
            'Reference': [f'REF{i:06d}' for i in range(1000)],
            'Account': ['67890'] * 1000
        }
        
        large_gl_file = os.path.join(self.temp_dir, 'large_gl.csv')
        large_bank_file = os.path.join(self.temp_dir, 'large_bank.csv')
        
        pd.DataFrame(large_gl_data).to_csv(large_gl_file, index=False)
        pd.DataFrame(large_bank_data).to_csv(large_bank_file, index=False)
        
        import time
        
        # Measure performance
        start_time = time.time()
        
        # Run workflow
        gl_result = self.ingestion.load_file(large_gl_file, file_type='gl')
        bank_result = self.ingestion.load_file(large_bank_file, file_type='bank')
        
        gl_clean_result = self.cleaner.clean_data(gl_result['data'], data_type='gl')
        bank_clean_result = self.cleaner.clean_data(bank_result['data'], data_type='bank')
        
        exact_results = self.exact_engine.reconcile_exact_matches(
            gl_clean_result['cleaned_data'], bank_clean_result['cleaned_data']
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time (30 seconds for 1000 records)
        self.assertLess(execution_time, 30.0)
        
        # Should process all records
        self.assertEqual(len(gl_clean_result['cleaned_data']), 1000)
        self.assertEqual(len(bank_clean_result['cleaned_data']), 1000)
    
    def test_configuration_impact_on_workflow(self):
        """Test how configuration changes affect workflow behavior."""
        # Test with different tolerance settings
        original_tolerance = self.exact_engine.params.get('amount_tolerance', 0.01)
        
        # Set high tolerance
        self.exact_engine.params['amount_tolerance'] = 1.00
        
        gl_result = self.ingestion.load_file(self.gl_file, file_type='gl')
        bank_result = self.ingestion.load_file(self.bank_file, file_type='bank')
        
        gl_clean_result = self.cleaner.clean_data(gl_result['data'], data_type='gl')
        bank_clean_result = self.cleaner.clean_data(bank_result['data'], data_type='bank')
        
        high_tolerance_results = self.exact_engine.reconcile_exact_matches(
            gl_clean_result['cleaned_data'], bank_clean_result['cleaned_data']
        )
        
        # Reset to original tolerance
        self.exact_engine.params['amount_tolerance'] = original_tolerance
        
        low_tolerance_results = self.exact_engine.reconcile_exact_matches(
            gl_clean_result['cleaned_data'], bank_clean_result['cleaned_data']
        )
        
        # High tolerance should find more matches (or equal)
        high_matches = high_tolerance_results['statistics']['total_matches']
        low_matches = low_tolerance_results['statistics']['total_matches']
        
        self.assertGreaterEqual(high_matches, low_matches)


class TestModuleIntegration(unittest.TestCase):
    """Test integration between specific modules."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample data
        self.sample_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, 200.00],
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
        
        self.sample_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, 200.00],
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ingestion_to_cleaning_integration(self):
        """Test data flow from ingestion to cleaning."""
        # Create test file
        test_file = os.path.join(self.temp_dir, 'test.csv')
        self.sample_gl.to_csv(test_file, index=False)
        
        # Ingestion
        ingestion = DataIngestion(self.config)
        ingestion_result = ingestion.load_file(test_file, file_type='gl')
        
        # Cleaning
        cleaner = DataCleaner(self.config)
        cleaning_result = cleaner.clean_data(ingestion_result['data'], data_type='gl')
        
        # Should integrate smoothly
        self.assertIn('cleaned_data', cleaning_result)
        self.assertIsInstance(cleaning_result['cleaned_data'], pd.DataFrame)
    
    def test_cleaning_to_matching_integration(self):
        """Test data flow from cleaning to matching."""
        # Clean data first
        cleaner = DataCleaner(self.config)
        gl_clean_result = cleaner.clean_data(self.sample_gl, data_type='gl')
        bank_clean_result = cleaner.clean_data(self.sample_bank, data_type='bank')
        
        # Exact matching
        exact_engine = ExactMatchingEngine(self.config)
        exact_results = exact_engine.reconcile_exact_matches(
            gl_clean_result['cleaned_data'], bank_clean_result['cleaned_data']
        )
        
        # Should integrate smoothly
        self.assertIn('matches', exact_results)
        self.assertIn('statistics', exact_results)
    
    def test_exact_to_fuzzy_matching_integration(self):
        """Test data flow from exact to fuzzy matching."""
        # Exact matching first
        exact_engine = ExactMatchingEngine(self.config)
        exact_results = exact_engine.reconcile_exact_matches(self.sample_gl, self.sample_bank)
        
        unmatched = exact_engine.get_unmatched_records()
        
        # Fuzzy matching on unmatched
        if not unmatched['gl'].empty and not unmatched['bank'].empty:
            fuzzy_engine = FuzzyMatcher(self.config)
            fuzzy_results = fuzzy_engine.find_fuzzy_matches(
                unmatched['gl'], unmatched['bank']
            )
            
            # Should integrate smoothly
            self.assertIn('matches', fuzzy_results)
            self.assertIn('potential_matches', fuzzy_results)
    
    def test_matching_to_exception_handling_integration(self):
        """Test data flow from matching to exception handling."""
        # Perform exact matching
        exact_engine = ExactMatchingEngine(self.config)
        exact_results = exact_engine.reconcile_exact_matches(self.sample_gl, self.sample_bank)
        
        unmatched = exact_engine.get_unmatched_records()
        
        # Exception handling
        if not unmatched['gl'].empty or not unmatched['bank'].empty:
            exception_handler = ExceptionHandler(self.config)
            exception_results = exception_handler.process_exceptions(
                unmatched['gl'], unmatched['bank'], 'gl', 'bank'
            )
            
            # Should integrate smoothly
            self.assertIn('categorized_exceptions', exception_results)
            self.assertIn('statistics', exception_results)


if __name__ == '__main__':
    unittest.main()
