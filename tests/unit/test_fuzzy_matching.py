#!/usr/bin/env python3
"""
Unit tests for FuzzyMatcher module.

Tests cover:
- Fuzzy matching algorithms
- String similarity functions
- Confidence scoring
- Threshold-based matching
- Potential match suggestions
- Performance optimization

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.modules.fuzzy_matching import FuzzyMatcher
from src.config import Config
from src.utils.exceptions import MatchingEngineError


class TestFuzzyMatcher(unittest.TestCase):
    """Test cases for FuzzyMatcher class."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        self.fuzzy_matcher = FuzzyMatcher(self.config)
        
        # Sample unmatched GL data
        self.gl_data = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
            'amount': [105.50, 75.00, 250.25],
            'description': ['Payment received from client', 'Bank service charge', 'Customer deposit'],
            'reference': ['PAY001', 'SVC002', 'DEP003']
        })
        
        # Sample unmatched bank data with similar but not exact matches
        self.bank_data = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-03', '2025-01-04']),
            'amount': [105.00, 75.50, 250.00],
            'description': ['Payment from client ABC', 'Service charge fee', 'Deposit from customer'],
            'reference': ['PAY-001', 'SVC-002', 'DEP-003']
        })
        
        # Test data for string similarity
        self.similar_descriptions = [
            ('Payment received from client', 'Payment from client ABC'),
            ('Bank service charge', 'Service charge fee'),
            ('Customer deposit', 'Deposit from customer'),
            ('Wire transfer', 'Electronic transfer'),
            ('ATM withdrawal', 'Cash withdrawal ATM')
        ]
    
    def test_string_similarity_ratio(self):
        """Test basic string similarity ratio calculation."""
        for desc1, desc2 in self.similar_descriptions:
            similarity = self.fuzzy_matcher.calculate_string_similarity(desc1, desc2, method='ratio')
            
            self.assertIsInstance(similarity, (int, float))
            self.assertGreaterEqual(similarity, 0)
            self.assertLessEqual(similarity, 100)
            
            # Similar strings should have high similarity
            self.assertGreater(similarity, 50)
    
    def test_string_similarity_partial_ratio(self):
        """Test partial ratio string similarity."""
        desc1 = "Payment received from client ABC Corp"
        desc2 = "Payment from client ABC"
        
        similarity = self.fuzzy_matcher.calculate_string_similarity(desc1, desc2, method='partial_ratio')
        
        self.assertGreater(similarity, 80)  # Should be high due to partial match
    
    def test_string_similarity_token_sort(self):
        """Test token sort ratio string similarity."""
        desc1 = "ABC Corp payment received"
        desc2 = "Payment received ABC Corp"
        
        similarity = self.fuzzy_matcher.calculate_string_similarity(desc1, desc2, method='token_sort_ratio')
        
        self.assertGreater(similarity, 90)  # Should be very high due to same tokens
    
    def test_string_similarity_token_set(self):
        """Test token set ratio string similarity."""
        desc1 = "Payment received from ABC Corp client"
        desc2 = "ABC Corp client payment"
        
        similarity = self.fuzzy_matcher.calculate_string_similarity(desc1, desc2, method='token_set_ratio')
        
        self.assertGreater(similarity, 80)  # Should be high due to common tokens
    
    def test_jaro_winkler_similarity(self):
        """Test Jaro-Winkler similarity algorithm."""
        desc1 = "Payment received"
        desc2 = "Payment processing"
        
        similarity = self.fuzzy_matcher.calculate_string_similarity(desc1, desc2, method='jaro_winkler')
        
        self.assertIsInstance(similarity, (int, float))
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)
    
    def test_calculate_match_confidence(self):
        """Test match confidence calculation."""
        gl_record = self.gl_data.iloc[0]
        bank_record = self.bank_data.iloc[0]
        
        confidence = self.fuzzy_matcher.calculate_match_confidence(gl_record, bank_record)
        
        self.assertIsInstance(confidence, (int, float))
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
        
        # Should be reasonably high for similar records
        self.assertGreater(confidence, 30)
    
    def test_find_fuzzy_matches(self):
        """Test finding fuzzy matches."""
        results = self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        self.assertIsInstance(results, dict)
        self.assertIn('matches', results)
        self.assertIn('potential_matches', results)
        self.assertIn('statistics', results)
        
        # Check statistics
        stats = results['statistics']
        self.assertIn('total_potential_matches', stats)
        self.assertIn('high_confidence_matches', stats)
        self.assertIn('medium_confidence_matches', stats)
        self.assertIn('processing_time', stats)
    
    def test_auto_match_threshold(self):
        """Test automatic matching based on confidence threshold."""
        # Set high auto-match threshold
        self.fuzzy_matcher.auto_match_threshold = 90
        
        results = self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        auto_matches = results['matches']
        
        # All auto matches should have high confidence
        for match in auto_matches:
            self.assertGreaterEqual(match['confidence'], 90)
    
    def test_potential_matches_threshold(self):
        """Test potential matches within confidence range."""
        # Set thresholds for potential matches
        self.fuzzy_matcher.potential_match_threshold = 50
        self.fuzzy_matcher.auto_match_threshold = 85
        
        results = self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        potential_matches = results['potential_matches']
        
        # All potential matches should be within threshold range
        for match in potential_matches:
            self.assertGreaterEqual(match['confidence'], 50)
            self.assertLess(match['confidence'], 85)
    
    def test_export_matches_to_dataframe(self):
        """Test exporting fuzzy matches to DataFrame."""
        # First find matches
        self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        # Export matches
        matches_df = self.fuzzy_matcher.export_matches_to_dataframe()
        
        self.assertIsInstance(matches_df, pd.DataFrame)
        
        # Check required columns
        expected_columns = [
            'gl_date', 'gl_amount', 'gl_description', 'gl_reference',
            'bank_date', 'bank_amount', 'bank_description', 'bank_reference',
            'confidence_score', 'match_factors', 'similarity_scores'
        ]
        
        for col in expected_columns:
            self.assertIn(col, matches_df.columns)
    
    def test_export_potential_matches_to_dataframe(self):
        """Test exporting potential matches for review."""
        # First find matches
        self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        # Export potential matches
        potential_df = self.fuzzy_matcher.export_potential_matches_to_dataframe()
        
        self.assertIsInstance(potential_df, pd.DataFrame)
        
        # Should have confidence scores for review
        if not potential_df.empty:
            self.assertIn('confidence_score', potential_df.columns)
            self.assertIn('review_priority', potential_df.columns)
    
    def test_get_unmatched_records(self):
        """Test getting records that remain unmatched after fuzzy matching."""
        # Perform fuzzy matching
        self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, self.bank_data)
        
        # Get unmatched records
        unmatched = self.fuzzy_matcher.get_unmatched_records(self.gl_data, self.bank_data)
        
        self.assertIsInstance(unmatched, dict)
        self.assertIn('gl', unmatched)
        self.assertIn('bank', unmatched)
        
        # Should be DataFrames
        self.assertIsInstance(unmatched['gl'], pd.DataFrame)
        self.assertIsInstance(unmatched['bank'], pd.DataFrame)
    
    def test_amount_similarity_calculation(self):
        """Test amount similarity calculation with tolerance."""
        amount1 = 100.50
        amount2 = 100.00
        
        similarity = self.fuzzy_matcher.calculate_amount_similarity(amount1, amount2)
        
        self.assertIsInstance(similarity, (int, float))
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)
        
        # Similar amounts should have high similarity
        self.assertGreater(similarity, 70)
    
    def test_date_similarity_calculation(self):
        """Test date similarity calculation with tolerance."""
        date1 = pd.to_datetime('2025-01-01')
        date2 = pd.to_datetime('2025-01-02')
        
        similarity = self.fuzzy_matcher.calculate_date_similarity(date1, date2)
        
        self.assertIsInstance(similarity, (int, float))
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)
        
        # Close dates should have high similarity
        self.assertGreater(similarity, 80)
    
    def test_reference_similarity_calculation(self):
        """Test reference number similarity calculation."""
        ref1 = "PAY001"
        ref2 = "PAY-001"
        
        similarity = self.fuzzy_matcher.calculate_reference_similarity(ref1, ref2)
        
        self.assertIsInstance(similarity, (int, float))
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)
        
        # Similar references should have high similarity
        self.assertGreater(similarity, 80)
    
    def test_performance_with_large_dataset(self):
        """Test fuzzy matching performance with larger datasets."""
        # Create larger datasets
        large_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01'] * 500),
            'amount': np.random.uniform(10, 1000, 500),
            'description': [f'Transaction description {i}' for i in range(500)],
            'reference': [f'REF{i:06d}' for i in range(500)]
        })
        
        large_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01'] * 500),
            'amount': np.random.uniform(10, 1000, 500),
            'description': [f'Bank transaction desc {i}' for i in range(500)],
            'reference': [f'BNK{i:06d}' for i in range(500)]
        })
        
        # Should complete within reasonable time
        import time
        start_time = time.time()
        
        results = self.fuzzy_matcher.find_fuzzy_matches(large_gl, large_bank)
        
        execution_time = time.time() - start_time
        
        # Should complete in reasonable time (allowing more time for fuzzy matching)
        self.assertLess(execution_time, 30.0)
        self.assertIsInstance(results, dict)
    
    def test_empty_dataset_handling(self):
        """Test handling of empty datasets."""
        empty_df = pd.DataFrame()
        
        # Should handle empty GL data
        results = self.fuzzy_matcher.find_fuzzy_matches(empty_df, self.bank_data)
        self.assertEqual(len(results['matches']), 0)
        
        # Should handle empty bank data
        results = self.fuzzy_matcher.find_fuzzy_matches(self.gl_data, empty_df)
        self.assertEqual(len(results['matches']), 0)
        
        # Should handle both empty
        results = self.fuzzy_matcher.find_fuzzy_matches(empty_df, empty_df)
        self.assertEqual(len(results['matches']), 0)
    
    def test_identical_records_similarity(self):
        """Test similarity calculation for identical records."""
        record = self.gl_data.iloc[0]
        
        confidence = self.fuzzy_matcher.calculate_match_confidence(record, record)
        
        # Identical records should have maximum confidence
        self.assertGreater(confidence, 95)
    
    def test_completely_different_records(self):
        """Test similarity calculation for completely different records."""
        gl_record = pd.Series({
            'date': pd.to_datetime('2025-01-01'),
            'amount': 100.00,
            'description': 'Payment received',
            'reference': 'PAY001'
        })
        
        bank_record = pd.Series({
            'date': pd.to_datetime('2025-12-31'),
            'amount': 9999.99,
            'description': 'Completely different transaction',
            'reference': 'XYZ999'
        })
        
        confidence = self.fuzzy_matcher.calculate_match_confidence(gl_record, bank_record)
        
        # Completely different records should have low confidence
        self.assertLess(confidence, 30)
    
    def test_confidence_score_consistency(self):
        """Test that confidence scores are consistent."""
        gl_record = self.gl_data.iloc[0]
        bank_record = self.bank_data.iloc[0]
        
        # Calculate confidence multiple times
        scores = []
        for _ in range(5):
            score = self.fuzzy_matcher.calculate_match_confidence(gl_record, bank_record)
            scores.append(score)
        
        # All scores should be identical (deterministic)
        self.assertTrue(all(score == scores[0] for score in scores))
    
    def test_missing_data_handling(self):
        """Test handling of records with missing data."""
        # Create records with missing values
        gl_missing = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, np.nan],
            'description': ['Payment A', None],
            'reference': ['REF001', 'REF002']
        })
        
        bank_missing = pd.DataFrame({
            'date': pd.to_datetime([None, '2025-01-02']),
            'amount': [100.50, 200.00],
            'description': ['Payment A', 'Payment B'],
            'reference': [None, 'REF002']
        })
        
        # Should handle missing data gracefully
        results = self.fuzzy_matcher.find_fuzzy_matches(gl_missing, bank_missing)
        self.assertIsInstance(results, dict)


class TestFuzzyMatcherConfiguration(unittest.TestCase):
    """Test FuzzyMatcher with different configurations."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = Config()
        
        self.sample_gl = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.50, 200.00],
            'description': ['Payment received', 'Transfer processed'],
            'reference': ['REF001', 'REF002']
        })
        
        self.sample_bank = pd.DataFrame({
            'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'amount': [100.00, 200.50],
            'description': ['Payment from client', 'Transfer completed'],
            'reference': ['REF-001', 'REF-002']
        })
    
    def test_custom_threshold_settings(self):
        """Test fuzzy matching with custom threshold settings."""
        # Create matcher with custom thresholds
        matcher = FuzzyMatcher(self.config)
        matcher.auto_match_threshold = 95
        matcher.potential_match_threshold = 60
        
        results = matcher.find_fuzzy_matches(self.sample_gl, self.sample_bank)
        
        self.assertIsInstance(results, dict)
        self.assertIn('matches', results)
        self.assertIn('potential_matches', results)
    
    def test_different_similarity_algorithms(self):
        """Test different similarity algorithm preferences."""
        algorithms = ['ratio', 'partial_ratio', 'token_sort_ratio', 'token_set_ratio', 'jaro_winkler']
        
        for algorithm in algorithms:
            matcher = FuzzyMatcher(self.config)
            matcher.preferred_similarity_method = algorithm
            
            # Test string similarity calculation
            similarity = matcher.calculate_string_similarity(
                'Payment received', 'Payment from client', method=algorithm
            )
            
            self.assertIsInstance(similarity, (int, float))
            self.assertGreaterEqual(similarity, 0)
            self.assertLessEqual(similarity, 100)
    
    def test_weight_customization(self):
        """Test customizing weights for different matching factors."""
        matcher = FuzzyMatcher(self.config)
        
        # Customize weights
        matcher.weights = {
            'amount': 0.4,
            'description': 0.4,
            'date': 0.1,
            'reference': 0.1
        }
        
        results = matcher.find_fuzzy_matches(self.sample_gl, self.sample_bank)
        
        self.assertIsInstance(results, dict)


if __name__ == '__main__':
    unittest.main()
