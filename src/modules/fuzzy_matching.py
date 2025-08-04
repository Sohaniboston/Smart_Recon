"""
SmartRecon Fuzzy Matching Module

This module implements intelligent fuzzy matching algorithms for financial reconciliation
with configurable confidence thresholds and multiple matching strategies including:
- String similarity matching using various algorithms
- Confidence scoring (0-100%)
- Threshold-based auto-matching
- Manual review workflows for uncertain matches
- Multiple fuzzy matching strategies

Author: SmartRecon Development Team
Date: 2025-07-28
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
import re
from collections import defaultdict

# Fuzzy matching libraries
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
import jellyfish

from ..utils.exceptions import MatchingEngineError, DataValidationError
from ..utils.helpers import normalize_text, format_currency

logger = logging.getLogger(__name__)


class FuzzyMatcher:
    """
    Advanced fuzzy matching engine for financial transaction reconciliation.
    
    Features:
    - Multiple string similarity algorithms
    - Configurable confidence thresholds
    - Automated matching for high-confidence matches
    - Manual review queue for uncertain matches
    - Detailed match scoring and justification
    - Performance optimization for large datasets
    """
    
    def __init__(self, config):
        """
        Initialize FuzzyMatcher with configuration.
        
        Args:
            config: Configuration object containing fuzzy matching parameters
        """
        self.config = config
        self.fuzzy_params = config.get('fuzzy_matching', {})
        
        # Default parameters if not in config
        self.min_confidence = self.fuzzy_params.get('min_confidence_threshold', 70)
        self.auto_match_threshold = self.fuzzy_params.get('auto_match_threshold', 85)
        self.amount_tolerance = self.fuzzy_params.get('amount_tolerance', 0.01)
        self.date_tolerance_days = self.fuzzy_params.get('date_tolerance_days', 5)
        
        # Matching algorithms weights
        self.algorithm_weights = self.fuzzy_params.get('algorithm_weights', {
            'ratio': 0.3,
            'partial_ratio': 0.2,
            'token_sort_ratio': 0.2,
            'token_set_ratio': 0.2,
            'jaro_winkler': 0.1
        })
        
        # Results storage
        self.fuzzy_matches = []
        self.potential_matches = []
        self.match_statistics = {}
        
        logger.info("FuzzyMatcher initialized with confidence threshold: %d", self.min_confidence)
    
    def calculate_string_similarity(self, str1: str, str2: str) -> Dict[str, float]:
        """
        Calculate similarity scores using multiple algorithms.
        
        Args:
            str1: First string to compare
            str2: Second string to compare
            
        Returns:
            Dictionary with similarity scores from different algorithms
        """
        if not str1 or not str2:
            return {algo: 0.0 for algo in self.algorithm_weights.keys()}
        
        # Normalize strings
        norm_str1 = normalize_text(str1)
        norm_str2 = normalize_text(str2)
        
        scores = {}
        
        try:
            # FuzzyWuzzy algorithms
            scores['ratio'] = fuzz.ratio(norm_str1, norm_str2)
            scores['partial_ratio'] = fuzz.partial_ratio(norm_str1, norm_str2)
            scores['token_sort_ratio'] = fuzz.token_sort_ratio(norm_str1, norm_str2)
            scores['token_set_ratio'] = fuzz.token_set_ratio(norm_str1, norm_str2)
            
            # Jaro-Winkler similarity
            scores['jaro_winkler'] = jellyfish.jaro_winkler_similarity(norm_str1, norm_str2) * 100
            
        except Exception as e:
            logger.warning(f"Error calculating string similarity: {e}")
            scores = {algo: 0.0 for algo in self.algorithm_weights.keys()}
        
        return scores
    
    def calculate_composite_confidence(self, similarity_scores: Dict[str, float], 
                                     amount_match: bool, date_match: bool) -> float:
        """
        Calculate composite confidence score from multiple factors.
        
        Args:
            similarity_scores: Dictionary of similarity scores
            amount_match: Whether amounts match within tolerance
            date_match: Whether dates match within tolerance
            
        Returns:
            Composite confidence score (0-100)
        """
        # Calculate weighted string similarity score
        string_score = sum(
            scores * self.algorithm_weights.get(algo, 0)
            for algo, scores in similarity_scores.items()
        )
        
        # Apply bonuses for amount and date matches
        confidence = string_score
        
        if amount_match:
            confidence *= 1.2  # 20% bonus for amount match
        
        if date_match:
            confidence *= 1.1  # 10% bonus for date match
        
        # Cap at 100
        return min(confidence, 100.0)
    
    def check_amount_match(self, amount1: float, amount2: float) -> bool:
        """
        Check if two amounts match within tolerance.
        
        Args:
            amount1: First amount
            amount2: Second amount
            
        Returns:
            True if amounts match within tolerance
        """
        if pd.isna(amount1) or pd.isna(amount2):
            return False
        
        diff = abs(amount1 - amount2)
        tolerance = max(abs(amount1), abs(amount2)) * self.amount_tolerance
        
        return diff <= tolerance
    
    def check_date_match(self, date1: pd.Timestamp, date2: pd.Timestamp) -> bool:
        """
        Check if two dates match within tolerance.
        
        Args:
            date1: First date
            date2: Second date
            
        Returns:
            True if dates match within tolerance
        """
        if pd.isna(date1) or pd.isna(date2):
            return False
        
        diff = abs((date1 - date2).days)
        return diff <= self.date_tolerance_days
    
    def find_fuzzy_matches(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Find fuzzy matches between GL and bank data.
        
        Args:
            gl_data: Cleaned GL data
            bank_data: Cleaned bank data
            
        Returns:
            Dictionary containing matches, potential matches, and statistics
        """
        logger.info("Starting fuzzy matching process...")
        start_time = datetime.now()
        
        # Reset results
        self.fuzzy_matches = []
        self.potential_matches = []
        
        # Get column mappings from config
        gl_desc_col = self.config.get('column_mapping', {}).get('gl', {}).get('description', 'description')
        bank_desc_col = self.config.get('column_mapping', {}).get('bank', {}).get('description', 'description')
        gl_amount_col = self.config.get('column_mapping', {}).get('gl', {}).get('amount', 'debit')
        bank_amount_col = self.config.get('column_mapping', {}).get('bank', {}).get('amount', 'deposit')
        gl_date_col = self.config.get('column_mapping', {}).get('gl', {}).get('date', 'transaction_date')
        bank_date_col = self.config.get('column_mapping', {}).get('bank', {}).get('date', 'date')
        
        total_comparisons = 0
        high_confidence_matches = 0
        potential_matches_count = 0
        
        # Process each GL record
        for gl_idx, gl_row in gl_data.iterrows():
            best_matches = []
            
            # Compare with each bank record
            for bank_idx, bank_row in bank_data.iterrows():
                total_comparisons += 1
                
                # Calculate string similarity
                gl_desc = str(gl_row.get(gl_desc_col, ''))
                bank_desc = str(bank_row.get(bank_desc_col, ''))
                
                similarity_scores = self.calculate_string_similarity(gl_desc, bank_desc)
                
                # Check amount and date matches
                gl_amount = gl_row.get(gl_amount_col, 0)
                bank_amount = bank_row.get(bank_amount_col, 0)
                amount_match = self.check_amount_match(gl_amount, bank_amount)
                
                gl_date = gl_row.get(gl_date_col)
                bank_date = bank_row.get(bank_date_col)
                date_match = self.check_date_match(gl_date, bank_date)
                
                # Calculate composite confidence
                confidence = self.calculate_composite_confidence(
                    similarity_scores, amount_match, date_match
                )
                
                # Only consider matches above minimum threshold
                if confidence >= self.min_confidence:
                    match_info = {
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'gl_record': gl_row.to_dict(),
                        'bank_record': bank_row.to_dict(),
                        'confidence': confidence,
                        'similarity_scores': similarity_scores,
                        'amount_match': amount_match,
                        'date_match': date_match,
                        'amount_difference': abs(gl_amount - bank_amount) if pd.notna(gl_amount) and pd.notna(bank_amount) else None,
                        'date_difference': abs((gl_date - bank_date).days) if pd.notna(gl_date) and pd.notna(bank_date) else None
                    }
                    
                    best_matches.append(match_info)
            
            # Sort matches by confidence and take the best ones
            best_matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Process best matches
            for match in best_matches[:3]:  # Consider top 3 matches
                if match['confidence'] >= self.auto_match_threshold:
                    self.fuzzy_matches.append(match)
                    high_confidence_matches += 1
                elif match['confidence'] >= self.min_confidence:
                    self.potential_matches.append(match)
                    potential_matches_count += 1
        
        # Calculate statistics
        processing_time = (datetime.now() - start_time).total_seconds()
        
        self.match_statistics = {
            'total_comparisons': total_comparisons,
            'high_confidence_matches': high_confidence_matches,
            'potential_matches': potential_matches_count,
            'processing_time_seconds': processing_time,
            'gl_records_processed': len(gl_data),
            'bank_records_processed': len(bank_data)
        }
        
        logger.info(f"Fuzzy matching completed: {high_confidence_matches} high-confidence matches, "
                   f"{potential_matches_count} potential matches found in {processing_time:.2f} seconds")
        
        return {
            'fuzzy_matches': self.fuzzy_matches,
            'potential_matches': self.potential_matches,
            'statistics': self.match_statistics
        }
    
    def export_matches_to_dataframe(self) -> pd.DataFrame:
        """
        Export fuzzy matches to a pandas DataFrame.
        
        Returns:
            DataFrame containing all fuzzy matches
        """
        if not self.fuzzy_matches:
            return pd.DataFrame()
        
        match_records = []
        
        for match in self.fuzzy_matches:
            record = {
                'match_type': 'fuzzy',
                'confidence': match['confidence'],
                'gl_index': match['gl_index'],
                'bank_index': match['bank_index'],
                'gl_description': match['gl_record'].get('description', ''),
                'bank_description': match['bank_record'].get('description', ''),
                'gl_amount': match['gl_record'].get('debit', match['gl_record'].get('credit', 0)),
                'bank_amount': match['bank_record'].get('deposit', match['bank_record'].get('withdrawal', 0)),
                'amount_difference': match['amount_difference'],
                'date_difference': match['date_difference'],
                'amount_match': match['amount_match'],
                'date_match': match['date_match']
            }
            
            # Add similarity scores
            for algo, score in match['similarity_scores'].items():
                record[f'similarity_{algo}'] = score
            
            match_records.append(record)
        
        return pd.DataFrame(match_records)
    
    def export_potential_matches_to_dataframe(self) -> pd.DataFrame:
        """
        Export potential matches to a pandas DataFrame for manual review.
        
        Returns:
            DataFrame containing potential matches for manual review
        """
        if not self.potential_matches:
            return pd.DataFrame()
        
        potential_records = []
        
        for match in self.potential_matches:
            record = {
                'match_type': 'potential',
                'confidence': match['confidence'],
                'gl_index': match['gl_index'],
                'bank_index': match['bank_index'],
                'gl_description': match['gl_record'].get('description', ''),
                'bank_description': match['bank_record'].get('description', ''),
                'gl_amount': match['gl_record'].get('debit', match['gl_record'].get('credit', 0)),
                'bank_amount': match['bank_record'].get('deposit', match['bank_record'].get('withdrawal', 0)),
                'amount_difference': match['amount_difference'],
                'date_difference': match['date_difference'],
                'amount_match': match['amount_match'],
                'date_match': match['date_match'],
                'needs_review': True
            }
            
            # Add similarity scores
            for algo, score in match['similarity_scores'].items():
                record[f'similarity_{algo}'] = score
            
            potential_records.append(record)
        
        return pd.DataFrame(potential_records)
    
    def get_unmatched_records(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Get records that remain unmatched after fuzzy matching.
        
        Args:
            gl_data: Original GL data
            bank_data: Original bank data
            
        Returns:
            Dictionary with unmatched GL and bank records
        """
        # Get indices of matched records
        matched_gl_indices = set()
        matched_bank_indices = set()
        
        for match in self.fuzzy_matches:
            matched_gl_indices.add(match['gl_index'])
            matched_bank_indices.add(match['bank_index'])
        
        # Filter out matched records
        unmatched_gl = gl_data[~gl_data.index.isin(matched_gl_indices)].copy()
        unmatched_bank = bank_data[~bank_data.index.isin(matched_bank_indices)].copy()
        
        return {
            'gl': unmatched_gl,
            'bank': unmatched_bank
        }
    
    def generate_match_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive fuzzy matching report.
        
        Returns:
            Dictionary containing match statistics and analysis
        """
        if not self.match_statistics:
            return {}
        
        report = {
            'fuzzy_matching_summary': {
                'total_fuzzy_matches': len(self.fuzzy_matches),
                'potential_matches_requiring_review': len(self.potential_matches),
                'processing_statistics': self.match_statistics
            },
            'confidence_distribution': self._analyze_confidence_distribution(),
            'match_quality_metrics': self._calculate_match_quality_metrics(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _analyze_confidence_distribution(self) -> Dict[str, Any]:
        """Analyze the distribution of confidence scores."""
        if not self.fuzzy_matches and not self.potential_matches:
            return {}
        
        all_matches = self.fuzzy_matches + self.potential_matches
        confidences = [match['confidence'] for match in all_matches]
        
        return {
            'average_confidence': np.mean(confidences),
            'median_confidence': np.median(confidences),
            'min_confidence': np.min(confidences),
            'max_confidence': np.max(confidences),
            'std_confidence': np.std(confidences)
        }
    
    def _calculate_match_quality_metrics(self) -> Dict[str, Any]:
        """Calculate quality metrics for the matches."""
        if not self.fuzzy_matches:
            return {}
        
        amount_matches = sum(1 for match in self.fuzzy_matches if match['amount_match'])
        date_matches = sum(1 for match in self.fuzzy_matches if match['date_match'])
        total_matches = len(self.fuzzy_matches)
        
        return {
            'amount_match_rate': (amount_matches / total_matches) * 100 if total_matches > 0 else 0,
            'date_match_rate': (date_matches / total_matches) * 100 if total_matches > 0 else 0,
            'average_amount_difference': np.mean([
                match['amount_difference'] for match in self.fuzzy_matches 
                if match['amount_difference'] is not None
            ]) if any(match['amount_difference'] is not None for match in self.fuzzy_matches) else 0
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on matching results."""
        recommendations = []
        
        if len(self.potential_matches) > len(self.fuzzy_matches):
            recommendations.append(
                "Consider lowering the auto-match threshold to automatically accept more matches"
            )
        
        if self.match_statistics.get('processing_time_seconds', 0) > 30:
            recommendations.append(
                "Consider implementing performance optimizations for large datasets"
            )
        
        if not self.fuzzy_matches and not self.potential_matches:
            recommendations.append(
                "No fuzzy matches found. Consider adjusting similarity thresholds or matching criteria"
            )
        
        return recommendations
