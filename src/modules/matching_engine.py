"""
SmartRecon Matching Engine Module

This module implements sophisticated transaction matching algorithms for financial
reconciliation including:
- Exact matching on key identifiers
- Fuzzy matching with configurable thresholds
- Date tolerance matching
- Amount variance matching
- One-to-many and many-to-one matching
- Confidence scoring and ranking

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
import itertools
from fuzzywuzzy import fuzz, process
import re

from ..utils.exceptions import MatchingEngineError, DataValidationError
from ..utils.helpers import normalize_text

logger = logging.getLogger(__name__)


class MatchingEngine:
    """
    Advanced matching engine for financial transaction reconciliation.
    
    Features:
    - Multiple matching algorithms (exact, fuzzy, tolerance-based)
    - Configurable confidence thresholds
    - One-to-many and many-to-one matching
    - Date and amount tolerance handling
    - Performance optimization for large datasets
    - Comprehensive audit trail
    """
    
    def __init__(self, config):
        """
        Initialize MatchingEngine with configuration.
        
        Args:
            config: Configuration object containing matching parameters
        """
        self.config = config
        self.matching_results = {}
        self.audit_trail = []
        
        # Default matching parameters
        self.default_params = {
            'exact_match_tolerance': 0.01,
            'fuzzy_match_threshold': 0.8,
            'date_tolerance_days': 2,
            'amount_tolerance_percent': 0.001,
            'description_weight': 0.4,
            'amount_weight': 0.3,
            'date_weight': 0.3
        }
        
        # Load configuration parameters
        self.params = self._load_matching_parameters()
        
        logger.info("MatchingEngine module initialized")
    
    def run_matching(self, 
                    df1: pd.DataFrame, 
                    df2: pd.DataFrame,
                    df1_type: str = 'gl',
                    df2_type: str = 'bank') -> Dict[str, Any]:
        """
        Execute comprehensive matching process between two datasets.
        
        Args:
            df1 (pd.DataFrame): First dataset (typically GL data)
            df2 (pd.DataFrame): Second dataset (typically bank data)
            df1_type (str): Type of first dataset
            df2_type (str): Type of second dataset
            
        Returns:
            Dict[str, Any]: Comprehensive matching results
            
        Raises:
            MatchingEngineError: If matching process fails
        """
        try:
            logger.info(f"Starting matching process: {len(df1)} vs {len(df2)} records")
            
            # Initialize matching session
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.matching_results = {
                'session_id': session_id,
                'input_stats': {
                    'df1_records': len(df1),
                    'df2_records': len(df2),
                    'df1_type': df1_type,
                    'df2_type': df2_type
                },
                'matches': {
                    'exact': [],
                    'fuzzy': [],
                    'tolerance': []
                },
                'unmatched': {
                    'df1': [],
                    'df2': []
                },
                'statistics': {},
                'processing_time': None
            }
            
            start_time = datetime.now()
            
            # Validate input data
            self._validate_input_data(df1, df2)
            
            # Prepare data for matching
            df1_prepared = self._prepare_data_for_matching(df1.copy(), df1_type)
            df2_prepared = self._prepare_data_for_matching(df2.copy(), df2_type)
            
            # Phase 1: Exact matching
            exact_matches, df1_remaining, df2_remaining = self._perform_exact_matching(
                df1_prepared, df2_prepared
            )
            self.matching_results['matches']['exact'] = exact_matches
            
            logger.info(f"Phase 1 complete: {len(exact_matches)} exact matches found")
            
            # Phase 2: Fuzzy matching on remaining records
            fuzzy_matches, df1_remaining, df2_remaining = self._perform_fuzzy_matching(
                df1_remaining, df2_remaining
            )
            self.matching_results['matches']['fuzzy'] = fuzzy_matches
            
            logger.info(f"Phase 2 complete: {len(fuzzy_matches)} fuzzy matches found")
            
            # Phase 3: Tolerance-based matching on remaining records
            tolerance_matches, df1_remaining, df2_remaining = self._perform_tolerance_matching(
                df1_remaining, df2_remaining
            )
            self.matching_results['matches']['tolerance'] = tolerance_matches
            
            logger.info(f"Phase 3 complete: {len(tolerance_matches)} tolerance matches found")
            
            # Store unmatched records
            self.matching_results['unmatched']['df1'] = df1_remaining.to_dict('records')
            self.matching_results['unmatched']['df2'] = df2_remaining.to_dict('records')
            
            # Calculate final statistics
            processing_time = (datetime.now() - start_time).total_seconds()
            self.matching_results['processing_time'] = processing_time
            self.matching_results['statistics'] = self._calculate_matching_statistics()
            
            logger.info(f"Matching completed in {processing_time:.2f} seconds")
            return self.matching_results
            
        except Exception as e:
            logger.error(f"Matching process failed: {str(e)}")
            raise MatchingEngineError(f"Matching process failed: {str(e)}") from e
    
    def _load_matching_parameters(self) -> Dict[str, Any]:
        """Load matching parameters from configuration."""
        params = self.default_params.copy()
        
        # Override with configuration values if available
        config_params = getattr(self.config, 'matching_parameters', {})
        params.update(config_params)
        
        return params
    
    def _validate_input_data(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """Validate input datasets for matching."""
        required_columns = ['date', 'amount']
        
        for i, df in enumerate([df1, df2], 1):
            if len(df) == 0:
                raise DataValidationError(f"Dataset {i} is empty")
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise DataValidationError(f"Dataset {i} missing required columns: {missing_columns}")
    
    def _prepare_data_for_matching(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Prepare data for matching by adding derived fields."""
        df = df.copy()
        
        # Add matching helper columns
        df['original_index'] = df.index
        df['data_type'] = data_type
        
        # Standardize description for matching
        if 'description' in df.columns:
            df['description_normalized'] = df['description'].apply(
                lambda x: normalize_text(str(x)) if pd.notnull(x) else ''
            )
        else:
            df['description_normalized'] = ''
        
        # Create matching keys
        df['amount_abs'] = df['amount'].abs()
        df['date_str'] = df['date'].dt.strftime('%Y-%m-%d') if pd.api.types.is_datetime64_any_dtype(df['date']) else df['date'].astype(str)
        
        # Create composite key for exact matching
        df['exact_match_key'] = df.apply(
            lambda row: f"{row['date_str']}_{row['amount_abs']:.2f}_{row['description_normalized'][:20]}",
            axis=1
        )
        
        return df
    
    def _perform_exact_matching(self, 
                               df1: pd.DataFrame, 
                               df2: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Perform exact matching on key fields."""
        exact_matches = []
        
        # Find exact matches using composite key
        merged = pd.merge(
            df1, df2, 
            on='exact_match_key', 
            how='inner', 
            suffixes=('_df1', '_df2')
        )
        
        for _, match in merged.iterrows():
            match_record = {
                'match_type': 'exact',
                'confidence': 1.0,
                'df1_record': {
                    'index': match['original_index_df1'],
                    'date': match['date_df1'],
                    'amount': match['amount_df1'],
                    'description': match.get('description_df1', ''),
                    'reference': match.get('reference_df1', '')
                },
                'df2_record': {
                    'index': match['original_index_df2'],
                    'date': match['date_df2'],
                    'amount': match['amount_df2'],
                    'description': match.get('description_df2', ''),
                    'reference': match.get('reference_df2', '')
                },
                'match_criteria': {
                    'date_match': True,
                    'amount_match': True,
                    'description_match': True
                }
            }
            exact_matches.append(match_record)
        
        # Remove matched records from original datasets
        matched_df1_indices = merged['original_index_df1'].tolist()
        matched_df2_indices = merged['original_index_df2'].tolist()
        
        df1_remaining = df1[~df1['original_index'].isin(matched_df1_indices)]
        df2_remaining = df2[~df2['original_index'].isin(matched_df2_indices)]
        
        return exact_matches, df1_remaining, df2_remaining
    
    def _perform_fuzzy_matching(self, 
                               df1: pd.DataFrame, 
                               df2: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Perform fuzzy matching using text similarity and tolerance rules."""
        fuzzy_matches = []
        matched_df1_indices = set()
        matched_df2_indices = set()
        
        # Convert to list for easier iteration
        df1_records = df1.to_dict('records')
        df2_records = df2.to_dict('records')
        
        for i, record1 in enumerate(df1_records):
            if i in matched_df1_indices:
                continue
            
            best_matches = []
            
            for j, record2 in enumerate(df2_records):
                if j in matched_df2_indices:
                    continue
                
                # Calculate match score
                match_score = self._calculate_match_score(record1, record2)
                
                if match_score >= self.params['fuzzy_match_threshold']:
                    best_matches.append({
                        'df2_index': j,
                        'record2': record2,
                        'score': match_score
                    })
            
            # Sort by score and take the best match
            if best_matches:
                best_match = max(best_matches, key=lambda x: x['score'])
                
                # Verify this is truly the best match for record2 as well
                if self._verify_mutual_best_match(record1, best_match['record2'], df1_records, df2_records, matched_df1_indices, matched_df2_indices):
                    
                    match_record = {
                        'match_type': 'fuzzy',
                        'confidence': best_match['score'],
                        'df1_record': {
                            'index': record1['original_index'],
                            'date': record1['date'],
                            'amount': record1['amount'],
                            'description': record1.get('description', ''),
                            'reference': record1.get('reference', '')
                        },
                        'df2_record': {
                            'index': best_match['record2']['original_index'],
                            'date': best_match['record2']['date'],
                            'amount': best_match['record2']['amount'],
                            'description': best_match['record2'].get('description', ''),
                            'reference': best_match['record2'].get('reference', '')
                        },
                        'match_criteria': self._analyze_match_criteria(record1, best_match['record2'])
                    }
                    
                    fuzzy_matches.append(match_record)
                    matched_df1_indices.add(i)
                    matched_df2_indices.add(best_match['df2_index'])
        
        # Remove matched records
        remaining_df1_indices = [rec['original_index'] for i, rec in enumerate(df1_records) if i not in matched_df1_indices]
        remaining_df2_indices = [rec['original_index'] for i, rec in enumerate(df2_records) if i not in matched_df2_indices]
        
        df1_remaining = df1[df1['original_index'].isin(remaining_df1_indices)]
        df2_remaining = df2[df2['original_index'].isin(remaining_df2_indices)]
        
        return fuzzy_matches, df1_remaining, df2_remaining
    
    def _perform_tolerance_matching(self, 
                                   df1: pd.DataFrame, 
                                   df2: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Perform tolerance-based matching with relaxed criteria."""
        tolerance_matches = []
        matched_df1_indices = set()
        matched_df2_indices = set()
        
        # Relax thresholds for tolerance matching
        relaxed_threshold = self.params['fuzzy_match_threshold'] * 0.7
        
        df1_records = df1.to_dict('records')
        df2_records = df2.to_dict('records')
        
        for i, record1 in enumerate(df1_records):
            if i in matched_df1_indices:
                continue
            
            best_matches = []
            
            for j, record2 in enumerate(df2_records):
                if j in matched_df2_indices:
                    continue
                
                # Use more relaxed matching criteria
                if self._is_tolerance_match(record1, record2):
                    match_score = self._calculate_tolerance_score(record1, record2)
                    
                    if match_score >= relaxed_threshold:
                        best_matches.append({
                            'df2_index': j,
                            'record2': record2,
                            'score': match_score
                        })
            
            if best_matches:
                best_match = max(best_matches, key=lambda x: x['score'])
                
                match_record = {
                    'match_type': 'tolerance',
                    'confidence': best_match['score'],
                    'df1_record': {
                        'index': record1['original_index'],
                        'date': record1['date'],
                        'amount': record1['amount'],
                        'description': record1.get('description', ''),
                        'reference': record1.get('reference', '')
                    },
                    'df2_record': {
                        'index': best_match['record2']['original_index'],
                        'date': best_match['record2']['date'],
                        'amount': best_match['record2']['amount'],
                        'description': best_match['record2'].get('description', ''),
                        'reference': best_match['record2'].get('reference', '')
                    },
                    'match_criteria': self._analyze_match_criteria(record1, best_match['record2'])
                }
                
                tolerance_matches.append(match_record)
                matched_df1_indices.add(i)
                matched_df2_indices.add(best_match['df2_index'])
        
        # Remove matched records
        remaining_df1_indices = [rec['original_index'] for i, rec in enumerate(df1_records) if i not in matched_df1_indices]
        remaining_df2_indices = [rec['original_index'] for i, rec in enumerate(df2_records) if i not in matched_df2_indices]
        
        df1_remaining = df1[df1['original_index'].isin(remaining_df1_indices)]
        df2_remaining = df2[df2['original_index'].isin(remaining_df2_indices)]
        
        return tolerance_matches, df1_remaining, df2_remaining
    
    def _calculate_match_score(self, record1: Dict, record2: Dict) -> float:
        """Calculate overall match score between two records."""
        scores = {}
        
        # Date matching score
        scores['date'] = self._calculate_date_score(record1.get('date'), record2.get('date'))
        
        # Amount matching score
        scores['amount'] = self._calculate_amount_score(record1.get('amount'), record2.get('amount'))
        
        # Description matching score
        scores['description'] = self._calculate_description_score(
            record1.get('description_normalized', ''),
            record2.get('description_normalized', '')
        )
        
        # Weighted average
        total_score = (
            scores['date'] * self.params['date_weight'] +
            scores['amount'] * self.params['amount_weight'] +
            scores['description'] * self.params['description_weight']
        )
        
        return min(total_score, 1.0)
    
    def _calculate_date_score(self, date1: Any, date2: Any) -> float:
        """Calculate date matching score."""
        try:
            if pd.isnull(date1) or pd.isnull(date2):
                return 0.0
            
            # Convert to datetime if needed
            dt1 = pd.to_datetime(date1) if not isinstance(date1, datetime) else date1
            dt2 = pd.to_datetime(date2) if not isinstance(date2, datetime) else date2
            
            # Calculate day difference
            day_diff = abs((dt1 - dt2).days)
            
            if day_diff == 0:
                return 1.0
            elif day_diff <= self.params['date_tolerance_days']:
                return max(0.0, 1.0 - (day_diff / self.params['date_tolerance_days']) * 0.5)
            else:
                return 0.0
                
        except:
            return 0.0
    
    def _calculate_amount_score(self, amount1: Any, amount2: Any) -> float:
        """Calculate amount matching score."""
        try:
            if pd.isnull(amount1) or pd.isnull(amount2):
                return 0.0
            
            amt1 = float(amount1)
            amt2 = float(amount2)
            
            # Check for exact match
            if abs(amt1 - amt2) <= self.params['exact_match_tolerance']:
                return 1.0
            
            # Calculate percentage difference
            avg_amount = (abs(amt1) + abs(amt2)) / 2
            if avg_amount == 0:
                return 1.0 if amt1 == amt2 else 0.0
            
            pct_diff = abs(amt1 - amt2) / avg_amount
            
            if pct_diff <= self.params['amount_tolerance_percent']:
                return max(0.0, 1.0 - pct_diff * 10)  # Scale the difference
            else:
                return 0.0
                
        except:
            return 0.0
    
    def _calculate_description_score(self, desc1: str, desc2: str) -> float:
        """Calculate description matching score using fuzzy string matching."""
        try:
            if not desc1 and not desc2:
                return 1.0
            if not desc1 or not desc2:
                return 0.0
            
            # Use fuzzywuzzy for text similarity
            similarity = fuzz.ratio(desc1.lower(), desc2.lower()) / 100.0
            
            # Additional boost for exact substring matches
            if desc1.lower() in desc2.lower() or desc2.lower() in desc1.lower():
                similarity = min(1.0, similarity + 0.1)
            
            return similarity
            
        except:
            return 0.0
    
    def _is_tolerance_match(self, record1: Dict, record2: Dict) -> bool:
        """Check if records meet tolerance matching criteria."""
        # More relaxed date tolerance
        date_tolerance = self.params['date_tolerance_days'] * 2
        
        try:
            # Date check
            dt1 = pd.to_datetime(record1.get('date'))
            dt2 = pd.to_datetime(record2.get('date'))
            
            if abs((dt1 - dt2).days) > date_tolerance:
                return False
            
            # Amount check (more relaxed tolerance)
            amt1 = float(record1.get('amount', 0))
            amt2 = float(record2.get('amount', 0))
            
            avg_amount = (abs(amt1) + abs(amt2)) / 2
            if avg_amount > 0:
                pct_diff = abs(amt1 - amt2) / avg_amount
                if pct_diff > 0.1:  # 10% tolerance
                    return False
            
            return True
            
        except:
            return False
    
    def _calculate_tolerance_score(self, record1: Dict, record2: Dict) -> float:
        """Calculate score for tolerance matching with relaxed criteria."""
        # Similar to regular matching but with more lenient scoring
        return self._calculate_match_score(record1, record2) * 0.8  # Reduce confidence for tolerance matches
    
    def _verify_mutual_best_match(self, record1: Dict, record2: Dict, df1_records: List, df2_records: List, matched_df1: set, matched_df2: set) -> bool:
        """Verify that the match is mutual (best for both records)."""
        # Check if record2 also considers record1 as its best match
        best_score_for_record2 = 0.0
        
        for i, other_record1 in enumerate(df1_records):
            if i in matched_df1:
                continue
            
            score = self._calculate_match_score(other_record1, record2)
            if score > best_score_for_record2:
                best_score_for_record2 = score
        
        current_score = self._calculate_match_score(record1, record2)
        
        # Allow the match if it's within a small margin of the best
        return current_score >= best_score_for_record2 * 0.95
    
    def _analyze_match_criteria(self, record1: Dict, record2: Dict) -> Dict[str, Any]:
        """Analyze which criteria contributed to the match."""
        return {
            'date_score': self._calculate_date_score(record1.get('date'), record2.get('date')),
            'amount_score': self._calculate_amount_score(record1.get('amount'), record2.get('amount')),
            'description_score': self._calculate_description_score(
                record1.get('description_normalized', ''),
                record2.get('description_normalized', '')
            ),
            'date_difference_days': abs((pd.to_datetime(record1.get('date')) - pd.to_datetime(record2.get('date'))).days) if record1.get('date') and record2.get('date') else None,
            'amount_difference': abs(float(record1.get('amount', 0)) - float(record2.get('amount', 0))) if record1.get('amount') is not None and record2.get('amount') is not None else None
        }
    
    def _calculate_matching_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive matching statistics."""
        total_df1 = self.matching_results['input_stats']['df1_records']
        total_df2 = self.matching_results['input_stats']['df2_records']
        
        exact_matches = len(self.matching_results['matches']['exact'])
        fuzzy_matches = len(self.matching_results['matches']['fuzzy'])
        tolerance_matches = len(self.matching_results['matches']['tolerance'])
        
        total_matches = exact_matches + fuzzy_matches + tolerance_matches
        
        unmatched_df1 = len(self.matching_results['unmatched']['df1'])
        unmatched_df2 = len(self.matching_results['unmatched']['df2'])
        
        return {
            'total_matches': total_matches,
            'match_breakdown': {
                'exact': exact_matches,
                'fuzzy': fuzzy_matches,
                'tolerance': tolerance_matches
            },
            'match_rates': {
                'df1_match_rate': round((total_df1 - unmatched_df1) / total_df1 * 100, 2) if total_df1 > 0 else 0,
                'df2_match_rate': round((total_df2 - unmatched_df2) / total_df2 * 100, 2) if total_df2 > 0 else 0,
                'overall_match_rate': round(total_matches / max(total_df1, total_df2) * 100, 2) if max(total_df1, total_df2) > 0 else 0
            },
            'unmatched_counts': {
                'df1_unmatched': unmatched_df1,
                'df2_unmatched': unmatched_df2,
                'total_unmatched': unmatched_df1 + unmatched_df2
            },
            'confidence_distribution': self._calculate_confidence_distribution()
        }
    
    def _calculate_confidence_distribution(self) -> Dict[str, int]:
        """Calculate distribution of confidence scores."""
        all_matches = (
            self.matching_results['matches']['exact'] +
            self.matching_results['matches']['fuzzy'] +
            self.matching_results['matches']['tolerance']
        )
        
        distribution = {
            'very_high': 0,  # 0.95-1.0
            'high': 0,       # 0.85-0.95
            'medium': 0,     # 0.70-0.85
            'low': 0         # below 0.70
        }
        
        for match in all_matches:
            confidence = match['confidence']
            if confidence >= 0.95:
                distribution['very_high'] += 1
            elif confidence >= 0.85:
                distribution['high'] += 1
            elif confidence >= 0.70:
                distribution['medium'] += 1
            else:
                distribution['low'] += 1
        
        return distribution
    
    def get_matching_results(self) -> Dict[str, Any]:
        """Return complete matching results."""
        return self.matching_results.copy()
    
    def export_matches_to_dataframe(self) -> pd.DataFrame:
        """Export matches to a pandas DataFrame for analysis."""
        all_matches = []
        
        for match_type in ['exact', 'fuzzy', 'tolerance']:
            for match in self.matching_results['matches'][match_type]:
                all_matches.append({
                    'match_type': match_type,
                    'confidence': match['confidence'],
                    'df1_index': match['df1_record']['index'],
                    'df1_date': match['df1_record']['date'],
                    'df1_amount': match['df1_record']['amount'],
                    'df1_description': match['df1_record']['description'],
                    'df2_index': match['df2_record']['index'],
                    'df2_date': match['df2_record']['date'],
                    'df2_amount': match['df2_record']['amount'],
                    'df2_description': match['df2_record']['description'],
                    'date_difference_days': match['match_criteria'].get('date_difference_days'),
                    'amount_difference': match['match_criteria'].get('amount_difference')
                })
        
        return pd.DataFrame(all_matches)
