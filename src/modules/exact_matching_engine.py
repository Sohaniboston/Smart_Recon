"""
SmartRecon Exact Matching Reconciliation Engine

This module implements a high-performance exact matching reconciliation engine
specifically designed for financial data reconciliation with:
- Multiple exact matching strategies
- Precision-based amount matching
- Date range exact matching
- Reference number matching
- Composite key matching
- Performance optimization for large datasets
- Comprehensive audit trails

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
import hashlib
from collections import defaultdict
import time

from ..utils.exceptions import MatchingEngineError, DataValidationError
from ..utils.helpers import normalize_text, format_currency

logger = logging.getLogger(__name__)


class ExactMatchingEngine:
    """
    High-performance exact matching reconciliation engine for financial data.
    
    Features:
    - Multiple exact matching strategies
    - Configurable precision tolerances
    - Optimized data structures for performance
    - Comprehensive match validation
    - Detailed audit logging
    - Statistical analysis of matches
    """
    
    def __init__(self, config):
        """
        Initialize ExactMatchingEngine with configuration.
        
        Args:
            config: Configuration object containing matching parameters
        """
        self.config = config
        self.matching_session = None
        self.performance_stats = {}
        
        # Default exact matching parameters
        self.default_params = {
            'amount_precision': 2,
            'amount_tolerance': 0.01,
            'date_exact_match': True,
            'description_exact_match': False,
            'reference_matching': True,
            'case_sensitive': False,
            'remove_whitespace': True,
            'currency_symbol_ignore': True
        }
        
        # Load configuration parameters
        self.params = self._load_matching_parameters()
        
        logger.info("ExactMatchingEngine initialized")
    
    def reconcile_exact_matches(self, 
                               gl_data: pd.DataFrame,
                               bank_data: pd.DataFrame,
                               match_strategies: List[str] = None) -> Dict[str, Any]:
        """
        Perform exact matching reconciliation between GL and bank data.
        
        Args:
            gl_data (pd.DataFrame): General Ledger data
            bank_data (pd.DataFrame): Bank statement data
            match_strategies (List[str]): List of matching strategies to apply
            
        Returns:
            Dict[str, Any]: Comprehensive reconciliation results
            
        Raises:
            MatchingEngineError: If reconciliation process fails
        """
        try:
            logger.info(f"Starting exact matching reconciliation")
            start_time = time.time()
            
            # Initialize reconciliation session
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.matching_session = {
                'session_id': session_id,
                'start_time': start_time,
                'gl_count': len(gl_data),
                'bank_count': len(bank_data),
                'strategies_used': match_strategies or self._get_default_strategies(),
                'exact_matches': [],
                'unmatched_gl': [],
                'unmatched_bank': [],
                'match_statistics': {},
                'performance_metrics': {},
                'validation_results': {}
            }
            
            # Validate input data
            self._validate_reconciliation_data(gl_data, bank_data)
            
            # Prepare data for exact matching
            gl_prepared = self._prepare_exact_matching_data(gl_data.copy(), 'gl')
            bank_prepared = self._prepare_exact_matching_data(bank_data.copy(), 'bank')
            
            # Apply exact matching strategies in sequence
            strategies = match_strategies or self._get_default_strategies()
            
            for strategy in strategies:
                logger.info(f"Applying exact matching strategy: {strategy}")
                strategy_start = time.time()
                
                matches, gl_prepared, bank_prepared = self._apply_exact_matching_strategy(
                    strategy, gl_prepared, bank_prepared
                )
                
                strategy_time = time.time() - strategy_start
                
                self.matching_session['exact_matches'].extend(matches)
                self.performance_stats[strategy] = {
                    'matches_found': len(matches),
                    'processing_time': strategy_time,
                    'gl_remaining': len(gl_prepared),
                    'bank_remaining': len(bank_prepared)
                }
                
                logger.info(f"Strategy '{strategy}': {len(matches)} matches found in {strategy_time:.2f}s")
            
            # Store unmatched records
            self.matching_session['unmatched_gl'] = gl_prepared.to_dict('records')
            self.matching_session['unmatched_bank'] = bank_prepared.to_dict('records')
            
            # Calculate comprehensive statistics
            total_time = time.time() - start_time
            self.matching_session['performance_metrics'] = self._calculate_performance_metrics(total_time)
            self.matching_session['match_statistics'] = self._calculate_match_statistics()
            self.matching_session['validation_results'] = self._validate_match_results()
            
            logger.info(f"Exact matching reconciliation completed in {total_time:.2f} seconds")
            logger.info(f"Total exact matches found: {len(self.matching_session['exact_matches'])}")
            
            return self.matching_session
            
        except Exception as e:
            logger.error(f"Exact matching reconciliation failed: {str(e)}")
            raise MatchingEngineError(f"Reconciliation failed: {str(e)}") from e
    
    def _get_default_strategies(self) -> List[str]:
        """Get default exact matching strategies in order of preference."""
        return [
            'reference_exact',      # Match by reference numbers
            'amount_date_exact',    # Match by exact amount and date
            'amount_date_desc',     # Match by amount, date, and description
            'composite_key',        # Match by composite key
            'amount_tolerance'      # Match with amount tolerance
        ]
    
    def _validate_reconciliation_data(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame):
        """Validate data for reconciliation process."""
        required_columns = ['date', 'amount', 'description']
        
        # Check GL data
        if len(gl_data) == 0:
            raise DataValidationError("GL data is empty")
        
        missing_gl = [col for col in required_columns if col not in gl_data.columns]
        if missing_gl:
            raise DataValidationError(f"GL data missing required columns: {missing_gl}")
        
        # Check bank data
        if len(bank_data) == 0:
            raise DataValidationError("Bank data is empty")
        
        missing_bank = [col for col in required_columns if col not in bank_data.columns]
        if missing_bank:
            raise DataValidationError(f"Bank data missing required columns: {missing_bank}")
        
        # Check for data quality issues
        self._check_data_quality(gl_data, 'GL')
        self._check_data_quality(bank_data, 'Bank')
    
    def _check_data_quality(self, data: pd.DataFrame, data_type: str):
        """Check basic data quality for reconciliation."""
        # Check for null values in critical columns
        critical_nulls = data[['date', 'amount']].isnull().sum().sum()
        if critical_nulls > 0:
            logger.warning(f"{data_type} data has {critical_nulls} null values in critical columns")
        
        # Check for duplicate records
        duplicates = data.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"{data_type} data has {duplicates} duplicate records")
        
        # Check amount data types
        try:
            pd.to_numeric(data['amount'], errors='coerce')
        except:
            logger.warning(f"{data_type} data has non-numeric amounts that may cause issues")
    
    def _prepare_exact_matching_data(self, data: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Prepare data with exact matching keys and normalized fields."""
        data = data.copy()
        
        # Add metadata
        data['original_index'] = data.index
        data['data_source'] = data_type
        data['match_status'] = 'unmatched'
        
        # Standardize date format
        if not pd.api.types.is_datetime64_any_dtype(data['date']):
            data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data['date_str'] = data['date'].dt.strftime('%Y-%m-%d')
        
        # Standardize amount
        data['amount_numeric'] = pd.to_numeric(data['amount'], errors='coerce')
        data['amount_abs'] = data['amount_numeric'].abs()
        data['amount_rounded'] = data['amount_numeric'].round(self.params['amount_precision'])
        
        # Normalize description
        if 'description' in data.columns:
            data['description_normalized'] = data['description'].apply(self._normalize_description)
        else:
            data['description_normalized'] = ''
        
        # Create reference key (if reference column exists)
        if 'reference' in data.columns:
            data['reference_normalized'] = data['reference'].apply(
                lambda x: self._normalize_reference(str(x)) if pd.notnull(x) else ''
            )
        else:
            data['reference_normalized'] = ''
        
        # Create exact matching keys
        data['amount_date_key'] = data.apply(
            lambda row: f"{row['date_str']}_{row['amount_rounded']:.{self.params['amount_precision']}f}",
            axis=1
        )
        
        data['composite_key'] = data.apply(
            lambda row: self._create_composite_key(row),
            axis=1
        )
        
        return data
    
    def _normalize_description(self, desc: str) -> str:
        """Normalize description for exact matching."""
        if pd.isnull(desc):
            return ''
        
        normalized = str(desc)
        
        if self.params['remove_whitespace']:
            normalized = ' '.join(normalized.split())  # Remove extra whitespace
        
        if not self.params['case_sensitive']:
            normalized = normalized.lower()
        
        if self.params['currency_symbol_ignore']:
            # Remove common currency symbols and formatting
            normalized = normalized.replace('$', '').replace('€', '').replace('£', '')
            normalized = normalized.replace(',', '')
        
        return normalized.strip()
    
    def _normalize_reference(self, ref: str) -> str:
        """Normalize reference number for exact matching."""
        if pd.isnull(ref) or str(ref).lower() in ['nan', 'none', '']:
            return ''
        
        normalized = str(ref).strip()
        
        if not self.params['case_sensitive']:
            normalized = normalized.lower()
        
        # Remove common prefixes and formatting
        normalized = normalized.replace('-', '').replace('_', '').replace(' ', '')
        
        return normalized
    
    def _create_composite_key(self, row: pd.Series) -> str:
        """Create a composite key for exact matching."""
        components = [
            row['date_str'],
            f"{row['amount_rounded']:.{self.params['amount_precision']}f}",
            row['description_normalized'][:30],  # First 30 chars of description
            row['reference_normalized']
        ]
        
        # Create hash of components for efficient matching
        key_string = '|'.join(str(comp) for comp in components)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _apply_exact_matching_strategy(self, 
                                     strategy: str,
                                     gl_data: pd.DataFrame,
                                     bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Apply specific exact matching strategy."""
        matches = []
        
        if strategy == 'reference_exact':
            matches, gl_data, bank_data = self._match_by_reference(gl_data, bank_data)
        
        elif strategy == 'amount_date_exact':
            matches, gl_data, bank_data = self._match_by_amount_date(gl_data, bank_data)
        
        elif strategy == 'amount_date_desc':
            matches, gl_data, bank_data = self._match_by_amount_date_description(gl_data, bank_data)
        
        elif strategy == 'composite_key':
            matches, gl_data, bank_data = self._match_by_composite_key(gl_data, bank_data)
        
        elif strategy == 'amount_tolerance':
            matches, gl_data, bank_data = self._match_by_amount_tolerance(gl_data, bank_data)
        
        else:
            logger.warning(f"Unknown matching strategy: {strategy}")
        
        return matches, gl_data, bank_data
    
    def _match_by_reference(self, 
                           gl_data: pd.DataFrame,
                           bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Match records by exact reference number."""
        matches = []
        
        # Filter records with non-empty references
        gl_with_ref = gl_data[gl_data['reference_normalized'] != ''].copy()
        bank_with_ref = bank_data[bank_data['reference_normalized'] != ''].copy()
        
        if len(gl_with_ref) == 0 or len(bank_with_ref) == 0:
            return matches, gl_data, bank_data
        
        # Perform exact merge on reference
        merged = pd.merge(
            gl_with_ref, bank_with_ref,
            on='reference_normalized',
            how='inner',
            suffixes=('_gl', '_bank')
        )
        
        for _, match_row in merged.iterrows():
            match_record = {
                'match_strategy': 'reference_exact',
                'confidence': 1.0,
                'gl_record': self._extract_record_info(match_row, '_gl'),
                'bank_record': self._extract_record_info(match_row, '_bank'),
                'match_criteria': {
                    'reference_match': True,
                    'reference_value': match_row['reference_normalized'],
                    'amount_difference': abs(match_row['amount_numeric_gl'] - match_row['amount_numeric_bank']),
                    'date_difference_days': abs((match_row['date_gl'] - match_row['date_bank']).days)
                }
            }
            matches.append(match_record)
        
        # Remove matched records
        matched_gl_indices = merged['original_index_gl'].tolist()
        matched_bank_indices = merged['original_index_bank'].tolist()
        
        gl_remaining = gl_data[~gl_data['original_index'].isin(matched_gl_indices)]
        bank_remaining = bank_data[~bank_data['original_index'].isin(matched_bank_indices)]
        
        return matches, gl_remaining, bank_remaining
    
    def _match_by_amount_date(self,
                             gl_data: pd.DataFrame,
                             bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Match records by exact amount and date."""
        matches = []
        
        # Perform exact merge on amount_date_key
        merged = pd.merge(
            gl_data, bank_data,
            on='amount_date_key',
            how='inner',
            suffixes=('_gl', '_bank')
        )
        
        for _, match_row in merged.iterrows():
            match_record = {
                'match_strategy': 'amount_date_exact',
                'confidence': 1.0,
                'gl_record': self._extract_record_info(match_row, '_gl'),
                'bank_record': self._extract_record_info(match_row, '_bank'),
                'match_criteria': {
                    'amount_match': True,
                    'date_match': True,
                    'match_key': match_row['amount_date_key'],
                    'amount_difference': 0.0,
                    'date_difference_days': 0
                }
            }
            matches.append(match_record)
        
        # Remove matched records
        matched_gl_indices = merged['original_index_gl'].tolist()
        matched_bank_indices = merged['original_index_bank'].tolist()
        
        gl_remaining = gl_data[~gl_data['original_index'].isin(matched_gl_indices)]
        bank_remaining = bank_data[~bank_data['original_index'].isin(matched_bank_indices)]
        
        return matches, gl_remaining, bank_remaining
    
    def _match_by_amount_date_description(self,
                                        gl_data: pd.DataFrame,
                                        bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Match records by amount, date, and description."""
        matches = []
        
        # Create enhanced key with description
        gl_enhanced = gl_data.copy()
        bank_enhanced = bank_data.copy()
        
        gl_enhanced['amount_date_desc_key'] = gl_enhanced.apply(
            lambda row: f"{row['amount_date_key']}_{row['description_normalized'][:20]}",
            axis=1
        )
        bank_enhanced['amount_date_desc_key'] = bank_enhanced.apply(
            lambda row: f"{row['amount_date_key']}_{row['description_normalized'][:20]}",
            axis=1
        )
        
        # Perform exact merge
        merged = pd.merge(
            gl_enhanced, bank_enhanced,
            on='amount_date_desc_key',
            how='inner',
            suffixes=('_gl', '_bank')
        )
        
        for _, match_row in merged.iterrows():
            match_record = {
                'match_strategy': 'amount_date_description',
                'confidence': 1.0,
                'gl_record': self._extract_record_info(match_row, '_gl'),
                'bank_record': self._extract_record_info(match_row, '_bank'),
                'match_criteria': {
                    'amount_match': True,
                    'date_match': True,
                    'description_match': True,
                    'match_key': match_row['amount_date_desc_key'],
                    'amount_difference': 0.0,
                    'date_difference_days': 0
                }
            }
            matches.append(match_record)
        
        # Remove matched records
        matched_gl_indices = merged['original_index_gl'].tolist()
        matched_bank_indices = merged['original_index_bank'].tolist()
        
        gl_remaining = gl_data[~gl_data['original_index'].isin(matched_gl_indices)]
        bank_remaining = bank_data[~bank_data['original_index'].isin(matched_bank_indices)]
        
        return matches, gl_remaining, bank_remaining
    
    def _match_by_composite_key(self,
                               gl_data: pd.DataFrame,
                               bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Match records by composite key hash."""
        matches = []
        
        # Perform exact merge on composite key
        merged = pd.merge(
            gl_data, bank_data,
            on='composite_key',
            how='inner',
            suffixes=('_gl', '_bank')
        )
        
        for _, match_row in merged.iterrows():
            match_record = {
                'match_strategy': 'composite_key',
                'confidence': 1.0,
                'gl_record': self._extract_record_info(match_row, '_gl'),
                'bank_record': self._extract_record_info(match_row, '_bank'),
                'match_criteria': {
                    'composite_match': True,
                    'match_key': match_row['composite_key'],
                    'amount_difference': abs(match_row['amount_numeric_gl'] - match_row['amount_numeric_bank']),
                    'date_difference_days': abs((match_row['date_gl'] - match_row['date_bank']).days)
                }
            }
            matches.append(match_record)
        
        # Remove matched records
        matched_gl_indices = merged['original_index_gl'].tolist()
        matched_bank_indices = merged['original_index_bank'].tolist()
        
        gl_remaining = gl_data[~gl_data['original_index'].isin(matched_gl_indices)]
        bank_remaining = bank_data[~bank_data['original_index'].isin(matched_bank_indices)]
        
        return matches, gl_remaining, bank_remaining
    
    def _match_by_amount_tolerance(self,
                                  gl_data: pd.DataFrame,
                                  bank_data: pd.DataFrame) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """Match records with amount tolerance (still exact matching approach)."""
        matches = []
        tolerance = self.params['amount_tolerance']
        
        # Use nested loops for tolerance matching (optimized for small tolerance)
        gl_records = gl_data.to_dict('records')
        bank_records = bank_data.to_dict('records')
        
        matched_gl_indices = set()
        matched_bank_indices = set()
        
        for i, gl_record in enumerate(gl_records):
            if i in matched_gl_indices:
                continue
            
            for j, bank_record in enumerate(bank_records):
                if j in matched_bank_indices:
                    continue
                
                # Check amount tolerance and exact date
                amount_diff = abs(gl_record['amount_numeric'] - bank_record['amount_numeric'])
                date_match = gl_record['date_str'] == bank_record['date_str']
                
                if amount_diff <= tolerance and date_match:
                    match_record = {
                        'match_strategy': 'amount_tolerance',
                        'confidence': 1.0 - (amount_diff / tolerance) * 0.1,  # Slight confidence reduction
                        'gl_record': {
                            'index': gl_record['original_index'],
                            'date': gl_record['date'],
                            'amount': gl_record['amount_numeric'],
                            'description': gl_record.get('description', ''),
                            'reference': gl_record.get('reference', '')
                        },
                        'bank_record': {
                            'index': bank_record['original_index'],
                            'date': bank_record['date'],
                            'amount': bank_record['amount_numeric'],
                            'description': bank_record.get('description', ''),
                            'reference': bank_record.get('reference', '')
                        },
                        'match_criteria': {
                            'amount_tolerance_match': True,
                            'date_match': True,
                            'amount_difference': amount_diff,
                            'date_difference_days': 0,
                            'tolerance_used': tolerance
                        }
                    }
                    matches.append(match_record)
                    matched_gl_indices.add(i)
                    matched_bank_indices.add(j)
                    break
        
        # Remove matched records
        gl_remaining = gl_data.iloc[[i for i in range(len(gl_data)) if i not in matched_gl_indices]]
        bank_remaining = bank_data.iloc[[i for i in range(len(bank_data)) if i not in matched_bank_indices]]
        
        return matches, gl_remaining, bank_remaining
    
    def _extract_record_info(self, match_row: pd.Series, suffix: str) -> Dict[str, Any]:
        """Extract record information from merged row."""
        return {
            'index': match_row[f'original_index{suffix}'],
            'date': match_row[f'date{suffix}'],
            'amount': match_row[f'amount_numeric{suffix}'],
            'description': match_row.get(f'description{suffix}', ''),
            'reference': match_row.get(f'reference{suffix}', '')
        }
    
    def _calculate_performance_metrics(self, total_time: float) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics."""
        total_matches = len(self.matching_session['exact_matches'])
        total_records = self.matching_session['gl_count'] + self.matching_session['bank_count']
        
        return {
            'total_processing_time': total_time,
            'records_per_second': total_records / total_time if total_time > 0 else 0,
            'matches_per_second': total_matches / total_time if total_time > 0 else 0,
            'strategy_performance': self.performance_stats,
            'memory_efficiency': 'optimized',  # Placeholder for actual memory metrics
            'processing_efficiency': total_matches / total_records if total_records > 0 else 0
        }
    
    def _calculate_match_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive matching statistics."""
        total_matches = len(self.matching_session['exact_matches'])
        gl_matched = total_matches
        bank_matched = total_matches
        
        gl_unmatched = len(self.matching_session['unmatched_gl'])
        bank_unmatched = len(self.matching_session['unmatched_bank'])
        
        # Strategy breakdown
        strategy_stats = defaultdict(int)
        for match in self.matching_session['exact_matches']:
            strategy_stats[match['match_strategy']] += 1
        
        return {
            'total_exact_matches': total_matches,
            'gl_match_rate': (gl_matched / self.matching_session['gl_count']) * 100 if self.matching_session['gl_count'] > 0 else 0,
            'bank_match_rate': (bank_matched / self.matching_session['bank_count']) * 100 if self.matching_session['bank_count'] > 0 else 0,
            'overall_match_rate': (total_matches / max(self.matching_session['gl_count'], self.matching_session['bank_count'])) * 100,
            'unmatched_counts': {
                'gl_unmatched': gl_unmatched,
                'bank_unmatched': bank_unmatched
            },
            'strategy_breakdown': dict(strategy_stats),
            'confidence_distribution': self._calculate_confidence_distribution()
        }
    
    def _calculate_confidence_distribution(self) -> Dict[str, int]:
        """Calculate confidence score distribution for exact matches."""
        distribution = {
            'perfect': 0,      # 1.0
            'high': 0,         # 0.95-0.99
            'medium': 0,       # 0.90-0.94
            'acceptable': 0    # below 0.90
        }
        
        for match in self.matching_session['exact_matches']:
            confidence = match['confidence']
            if confidence == 1.0:
                distribution['perfect'] += 1
            elif confidence >= 0.95:
                distribution['high'] += 1
            elif confidence >= 0.90:
                distribution['medium'] += 1
            else:
                distribution['acceptable'] += 1
        
        return distribution
    
    def _validate_match_results(self) -> Dict[str, Any]:
        """Validate the integrity of matching results."""
        validation = {
            'data_integrity': True,
            'duplicate_matches': 0,
            'orphaned_records': 0,
            'validation_errors': []
        }
        
        # Check for duplicate matches
        gl_matched_indices = set()
        bank_matched_indices = set()
        
        for match in self.matching_session['exact_matches']:
            gl_idx = match['gl_record']['index']
            bank_idx = match['bank_record']['index']
            
            if gl_idx in gl_matched_indices:
                validation['duplicate_matches'] += 1
                validation['validation_errors'].append(f"GL record {gl_idx} matched multiple times")
            
            if bank_idx in bank_matched_indices:
                validation['duplicate_matches'] += 1
                validation['validation_errors'].append(f"Bank record {bank_idx} matched multiple times")
            
            gl_matched_indices.add(gl_idx)
            bank_matched_indices.add(bank_idx)
        
        # Validate data integrity
        if validation['duplicate_matches'] > 0:
            validation['data_integrity'] = False
        
        return validation
    
    def _load_matching_parameters(self) -> Dict[str, Any]:
        """Load exact matching parameters from configuration."""
        params = self.default_params.copy()
        
        # Override with configuration values if available
        if hasattr(self.config, 'get_matching_config'):
            config_params = self.config.get_matching_config()
            params.update(config_params)
        
        return params
    
    def get_reconciliation_results(self) -> Dict[str, Any]:
        """Return complete reconciliation results."""
        if self.matching_session is None:
            raise MatchingEngineError("No reconciliation session found. Run reconcile_exact_matches first.")
        
        return self.matching_session.copy()
    
    def export_matches_to_dataframe(self) -> pd.DataFrame:
        """Export exact matches to DataFrame for analysis."""
        if not self.matching_session or not self.matching_session['exact_matches']:
            return pd.DataFrame()
        
        match_records = []
        for match in self.matching_session['exact_matches']:
            match_records.append({
                'strategy': match['match_strategy'],
                'confidence': match['confidence'],
                'gl_index': match['gl_record']['index'],
                'gl_date': match['gl_record']['date'],
                'gl_amount': match['gl_record']['amount'],
                'gl_description': match['gl_record']['description'],
                'bank_index': match['bank_record']['index'],
                'bank_date': match['bank_record']['date'],
                'bank_amount': match['bank_record']['amount'],
                'bank_description': match['bank_record']['description'],
                'amount_difference': match['match_criteria'].get('amount_difference', 0),
                'date_difference_days': match['match_criteria'].get('date_difference_days', 0)
            })
        
        return pd.DataFrame(match_records)
    
    def get_unmatched_records(self) -> Dict[str, pd.DataFrame]:
        """Return unmatched records as DataFrames."""
        if not self.matching_session:
            return {'gl': pd.DataFrame(), 'bank': pd.DataFrame()}
        
        return {
            'gl': pd.DataFrame(self.matching_session['unmatched_gl']),
            'bank': pd.DataFrame(self.matching_session['unmatched_bank'])
        }
