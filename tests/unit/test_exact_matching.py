#!/usr/bin/env python3
"""
Unit tests for ExactMatchingEngine module.

Tests cover:
- Exact matching algorithms
- Amount tolerance matching
- Date range matching
- Reference number matching
- Performance optimization
- Match result export

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.modules.exact_matching_engine import ExactMatchingEngine
from src.config import Config
from src.utils.exceptions import MatchingEngineError


class TestExactMatchingEngine(unittest.TestCase):
    """Test cases for ExactMatchingEngine class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.engine = ExactMatchingEngine(self.config)
        
        # Sample GL data
        self.gl_data = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04']),
            'amount': [100.50, -75.25, 250.00, 300.75],
            'description': ['Payment received', 'Service charge', 'Deposit', 'Transfer'],
            'reference': ['REF001', 'REF002', 'REF003', 'REF004']
        })
        
        # Sample Bank data with some matching transactions
        self.bank_data = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-05', '2025-01-06']),
            'amount': [100.50, -75.25, 450.00, 300.75],
            'description': ['Payment received', 'Service charge', 'New deposit', 'Transfer'],
            'reference': ['REF001', 'REF002', 'REF005', 'REF004']
        })
        
        # Data with tolerance testing
        self.tolerance_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, 200.00],
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
        
        self.tolerance_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.51, 199.99],  # Slightly different amounts
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
    
    def test_exact_amount_matching(self):
        """Test exact amount matching."""
        matches = self.engine.find_exact_amount_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(matches, list)
        
        # Should find exact matches for 100.50 and -75.25
        match_amounts = [match['gl_amount'] for match in matches]
        self.assertIn(100.50, match_amounts)
        self.assertIn(-75.25, match_amounts)
    
    def test_amount_tolerance_matching(self):
        """Test amount matching with tolerance."""
        # Set tolerance to 0.02
        self.engine.params['amount_tolerance'] = 0.02
        
        matches = self.engine.find_amount_tolerance_matches(
            self.tolerance_gl, self.tolerance_bank
        )
        
        self.assertIsInstance(matches, list)
        
        # Should find matches within tolerance
        self.assertGreater(len(matches), 0)
    
    def test_date_range_matching(self):
        """Test date range matching."""
        # Set date tolerance to 1 day
        self.engine.params['date_tolerance_days'] = 1
        
        matches = self.engine.find_date_range_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(matches, list)
        
        # Should find matches within date range
        for match in matches:
            self.assertIn('gl_date', match)
            self.assertIn('bank_date', match)
            self.assertIn('date_difference', match)
    
    def test_reference_matching(self):
        """Test reference number matching."""
        matches = self.engine.find_reference_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(matches, list)
        
        # Should find matches for REF001, REF002, REF004
        reference_matches = [match['reference'] for match in matches]
        self.assertIn('REF001', reference_matches)
        self.assertIn('REF002', reference_matches)
        self.assertIn('REF004', reference_matches)
    
    def test_composite_matching(self):
        """Test composite matching strategy."""
        matches = self.engine.find_composite_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(matches, list)
        
        # Composite matches should consider multiple factors
        for match in matches:
            self.assertIn('match_score', match)
            self.assertIn('match_factors', match)
            self.assertGreater(match['match_score'], 0)
    
    def test_reconcile_exact_matches(self):
        """Test complete exact reconciliation."""
        results = self.engine.reconcile_exact_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(results, dict)
        self.assertIn('matches', results)
        self.assertIn('statistics', results)
        
        # Check statistics
        stats = results['statistics']
        self.assertIn('total_matches', stats)
        self.assertIn('gl_matched_count', stats)
        self.assertIn('bank_matched_count', stats)
        self.assertIn('match_rate', stats)
    
    def test_export_matches_to_dataframe(self):
        """Test exporting matches to DataFrame."""
        # First perform matching
        self.engine.reconcile_exact_matches(self.gl_data, self.bank_data)
        
        # Export matches
        matches_df = self.engine.export_matches_to_dataframe()
        
        self.assertIsInstance(matches_df, pd.DataFrame)
        
        # Check required columns
        expected_columns = [
            'gl_date', 'gl_amount', 'gl_description', 'gl_reference',
            'bank_date', 'bank_amount', 'bank_description', 'bank_reference',
            'match_type', 'match_score'
        ]
        
        for col in expected_columns:
            self.assertIn(col, matches_df.columns)
    
    def test_get_unmatched_records(self):
        """Test getting unmatched records."""
        # Perform matching first
        self.engine.reconcile_exact_matches(self.gl_data, self.bank_data)
        
        unmatched = self.engine.get_unmatched_records()
        
        self.assertIsInstance(unmatched, dict)
        self.assertIn('gl', unmatched)
        self.assertIn('bank', unmatched)
        
        # Should be DataFrames
        self.assertIsInstance(unmatched['gl'], pd.DataFrame)
        self.assertIsInstance(unmatched['bank'], pd.DataFrame)
    
    def test_performance_with_large_dataset(self):
        """Test performance with larger datasets."""
        # Create larger datasets
        large_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01'] * 1000),
            'amount': np.random.uniform(10, 1000, 1000),
            'description': [f'Transaction {i}' for i in range(1000)],
            'reference': [f'REF{i:06d}' for i in range(1000)]
        })
        
        large_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01'] * 1000),
            'amount': np.random.uniform(10, 1000, 1000),
            'description': [f'Transaction {i}' for i in range(1000)],
            'reference': [f'REF{i:06d}' for i in range(1000)]
        })
        
        # Should complete within reasonable time
        import time
        start_time = time.time()
        
        results = self.engine.reconcile_exact_matches(large_gl, large_bank)
        
        execution_time = time.time() - start_time
        
        # Should complete in less than 10 seconds for 1000 records
        self.assertLess(execution_time, 10.0)
        self.assertIsInstance(results, dict)
    
    def test_match_quality_scoring(self):
        """Test match quality scoring."""
        # Perform matching
        self.engine.reconcile_exact_matches(self.gl_data, self.bank_data)
        
        matches_df = self.engine.export_matches_to_dataframe()
        
        if not matches_df.empty:
            # All matches should have quality scores
            self.assertTrue('match_score' in matches_df.columns)
            
            # Scores should be between 0 and 100
            for score in matches_df['match_score']:
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 100)
    
    def test_empty_dataset_handling(self):
        """Test handling of empty datasets."""
        empty_df = pd.DataFrame()
        
        # Should handle empty GL data
        results = self.engine.reconcile_exact_matches(empty_df, self.bank_data)
        self.assertEqual(len(results['matches']), 0)
        
        # Should handle empty bank data
        results = self.engine.reconcile_exact_matches(self.gl_data, empty_df)
        self.assertEqual(len(results['matches']), 0)
        
        # Should handle both empty
        results = self.engine.reconcile_exact_matches(empty_df, empty_df)
        self.assertEqual(len(results['matches']), 0)
    
    def test_duplicate_amount_handling(self):
        """Test handling of duplicate amounts."""
        # Create data with duplicate amounts
        duplicate_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-01', '2025-01-02']),
            'amount': [100.00, 100.00, 200.00],
            'description': ['Payment A', 'Payment B', 'Payment C'],
            'reference': ['REF001', 'REF002', 'REF003']
        })
        
        duplicate_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-01']),
            'amount': [100.00, 100.00],
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
        
        results = self.engine.reconcile_exact_matches(duplicate_gl, duplicate_bank)
        
        # Should handle duplicates appropriately
        self.assertIsInstance(results, dict)
        self.assertIn('matches', results)
    
    def test_different_data_types(self):
        """Test handling different data types in amount columns."""
        # Create data with different amount formats
        mixed_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': ['100.50', 200],  # String and int
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
        
        mixed_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, '200.00'],  # Float and string
            'description': ['Payment A', 'Payment B'],
            'reference': ['REF001', 'REF002']
        })
        
        # Should handle type conversion
        results = self.engine.reconcile_exact_matches(mixed_gl, mixed_bank)
        self.assertIsInstance(results, dict)
    
    def test_missing_data_handling(self):
        """Test handling of missing data."""
        # Create data with missing values
        missing_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
            'amount': [100.50, np.nan, 300.00],
            'description': ['Payment A', None, 'Payment C'],
            'reference': ['REF001', 'REF002', None]
        })
        
        missing_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', None, '2025-01-03']),
            'amount': [100.50, 200.00, 300.00],
            'description': ['Payment A', 'Payment B', 'Payment C'],
            'reference': ['REF001', 'REF002', 'REF003']
        })
        
        # Should handle missing data gracefully
        results = self.engine.reconcile_exact_matches(missing_gl, missing_bank)
        self.assertIsInstance(results, dict)


class TestExactMatchingEngineConfiguration(unittest.TestCase):
    """Test ExactMatchingEngine with different configurations."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        
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
    
    def test_custom_tolerance_settings(self):
        """Test matching with custom tolerance settings."""
        # Create engine with custom tolerance
        engine = ExactMatchingEngine(self.config)
        engine.params['amount_tolerance'] = 0.05
        engine.params['date_tolerance_days'] = 2
        
        results = engine.reconcile_exact_matches(self.sample_gl, self.sample_bank)
        
        self.assertIsInstance(results, dict)
        self.assertIn('matches', results)
    
    def test_different_matching_strategies(self):
        """Test different matching strategy configurations."""
        strategies = ['exact_amount', 'amount_tolerance', 'reference', 'composite']
        
        for strategy in strategies:
            engine = ExactMatchingEngine(self.config)
            engine.params['preferred_strategy'] = strategy
            
            results = engine.reconcile_exact_matches(self.sample_gl, self.sample_bank)
            self.assertIsInstance(results, dict)


if __name__ == '__main__':
    unittest.main()
