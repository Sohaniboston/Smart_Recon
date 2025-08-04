"""
SmartRecon Exception Handler Module

This module manages unmatched transactions and provides intelligent categorization,
resolution workflows, and manual review capabilities including:
- Automatic exception categorization
- Pattern-based grouping
- Resolution workflow management
- Manual matching interface
- Exception aging and tracking
- Performance analytics

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
import re
from collections import defaultdict

from ..utils.exceptions import ExceptionHandlerError, DataValidationError
from ..utils.helpers import normalize_text

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """
    Comprehensive exception management for unmatched transactions.
    
    Features:
    - Intelligent categorization of unmatched items
    - Pattern recognition and grouping
    - Aging analysis and tracking
    - Manual resolution workflow
    - Exception reporting and analytics
    - Automated resolution suggestions
    """
    
    def __init__(self, config):
        """
        Initialize ExceptionHandler with configuration.
        
        Args:
            config: Configuration object containing exception handling parameters
        """
        self.config = config
        self.exception_categories = self._initialize_categories()
        self.resolution_workflows = self._initialize_workflows()
        self.exception_stats = {}
        
        logger.info("ExceptionHandler module initialized")
    
    def process_exceptions(self, 
                          unmatched_df1: Union[pd.DataFrame, List[Dict]], 
                          unmatched_df2: Union[pd.DataFrame, List[Dict]],
                          df1_type: str = 'gl',
                          df2_type: str = 'bank') -> Dict[str, Any]:
        """
        Process unmatched transactions and categorize exceptions.
        
        Args:
            unmatched_df1: Unmatched records from first dataset (DataFrame or List of Dict)
            unmatched_df2: Unmatched records from second dataset (DataFrame or List of Dict)
            df1_type (str): Type of first dataset
            df2_type (str): Type of second dataset
            
        Returns:
            Dict[str, Any]: Comprehensive exception analysis results
            
        Raises:
            ExceptionHandlerError: If exception processing fails
        """
        try:
            # Convert inputs to DataFrames if needed
            if isinstance(unmatched_df1, list):
                df1_unmatched = pd.DataFrame(unmatched_df1) if unmatched_df1 else pd.DataFrame()
            else:
                df1_unmatched = unmatched_df1 if unmatched_df1 is not None else pd.DataFrame()
                
            if isinstance(unmatched_df2, list):
                df2_unmatched = pd.DataFrame(unmatched_df2) if unmatched_df2 else pd.DataFrame()
            else:
                df2_unmatched = unmatched_df2 if unmatched_df2 is not None else pd.DataFrame()
                
            logger.info(f"Processing exceptions: {len(df1_unmatched)} + {len(df2_unmatched)} unmatched records")
            
            # Initialize results structure
            results = {
                'session_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
                'input_summary': {
                    'unmatched_df1_count': len(df1_unmatched),
                    'unmatched_df2_count': len(df2_unmatched),
                    'df1_type': df1_type,
                    'df2_type': df2_type
                },
                'categorized_exceptions': {
                    df1_type: {},
                    df2_type: {}
                },
                'pattern_analysis': {},
                'aging_analysis': {},
                'resolution_suggestions': [],
                'statistics': {},
                'processing_time': None
            }
            
            start_time = datetime.now()
            
            # Process each dataset
            if not df1_unmatched.empty:
                results['categorized_exceptions'][df1_type] = self._categorize_exceptions(
                    df1_unmatched, df1_type
                )
            
            if not df2_unmatched.empty:
                results['categorized_exceptions'][df2_type] = self._categorize_exceptions(
                    df2_unmatched, df2_type
                )
            
            # Perform pattern analysis
            results['pattern_analysis'] = self._analyze_patterns(df1_unmatched, df2_unmatched)
            
            # Perform aging analysis
            results['aging_analysis'] = self._analyze_aging(df1_unmatched, df2_unmatched)
            
            # Generate resolution suggestions
            results['resolution_suggestions'] = self._generate_resolution_suggestions(
                df1_unmatched, df2_unmatched, df1_type, df2_type
            )
            
            # Calculate statistics
            processing_time = (datetime.now() - start_time).total_seconds()
            results['processing_time'] = processing_time
            results['statistics'] = self._calculate_exception_statistics(results)
            
            logger.info(f"Exception processing completed in {processing_time:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Exception processing failed: {str(e)}")
            raise ExceptionHandlerError(f"Exception processing failed: {str(e)}") from e
    
    def _initialize_categories(self) -> Dict[str, Dict]:
        """Initialize exception categories with detection patterns."""
        return {
            'timing_differences': {
                'description': 'Transactions with timing mismatches',
                'patterns': [
                    r'pending',
                    r'processing',
                    r'clearing'
                ],
                'resolution_priority': 'low',
                'auto_resolvable': True
            },
            'amount_differences': {
                'description': 'Transactions with amount discrepancies',
                'patterns': [
                    r'fee',
                    r'charge',
                    r'adjustment',
                    r'correction'
                ],
                'resolution_priority': 'high',
                'auto_resolvable': False
            },
            'missing_transactions': {
                'description': 'Transactions present in one system but not the other',
                'patterns': [
                    r'transfer',
                    r'internal',
                    r'journal'
                ],
                'resolution_priority': 'medium',
                'auto_resolvable': False
            },
            'duplicate_transactions': {
                'description': 'Potential duplicate entries',
                'patterns': [
                    r'duplicate',
                    r'reversal',
                    r'void'
                ],
                'resolution_priority': 'medium',
                'auto_resolvable': True
            },
            'system_specific': {
                'description': 'System-specific entries not expected to match',
                'patterns': [
                    r'accrual',
                    r'provision',
                    r'allocation'
                ],
                'resolution_priority': 'low',
                'auto_resolvable': True
            },
            'data_quality_issues': {
                'description': 'Records with data quality problems',
                'patterns': [
                    r'invalid',
                    r'error',
                    r'missing'
                ],
                'resolution_priority': 'high',
                'auto_resolvable': False
            },
            'unknown': {
                'description': 'Unclassified exceptions requiring manual review',
                'patterns': [],
                'resolution_priority': 'medium',
                'auto_resolvable': False
            }
        }
    
    def _initialize_workflows(self) -> Dict[str, Dict]:
        """Initialize resolution workflows for different exception types."""
        return {
            'timing_differences': {
                'steps': [
                    'Check for transactions in subsequent periods',
                    'Verify cut-off procedures',
                    'Review pending transaction reports'
                ],
                'typical_resolution_time': '1-2 days',
                'required_approvals': []
            },
            'amount_differences': {
                'steps': [
                    'Investigate source of discrepancy',
                    'Review supporting documentation',
                    'Prepare journal entry if needed',
                    'Obtain management approval'
                ],
                'typical_resolution_time': '3-5 days',
                'required_approvals': ['manager']
            },
            'missing_transactions': {
                'steps': [
                    'Verify transaction existence in source system',
                    'Check system interface logs',
                    'Research transaction trail',
                    'Create correcting entry if needed'
                ],
                'typical_resolution_time': '2-4 days',
                'required_approvals': ['supervisor']
            },
            'duplicate_transactions': {
                'steps': [
                    'Identify original transaction',
                    'Verify duplicate status',
                    'Remove or reverse duplicate',
                    'Update controls to prevent recurrence'
                ],
                'typical_resolution_time': '1-2 days',
                'required_approvals': []
            }
        }
    
    def _categorize_exceptions(self, df: pd.DataFrame, data_type: str) -> Dict[str, List[Dict]]:
        """Categorize exceptions based on patterns and characteristics."""
        categorized = {category: [] for category in self.exception_categories.keys()}
        
        for _, record in df.iterrows():
            category = self._classify_record(record)
            
            exception_record = {
                'original_index': record.get('original_index', record.name),
                'date': record.get('date'),
                'amount': record.get('amount'),
                'description': record.get('description', ''),
                'reference': record.get('reference', ''),
                'category': category,
                'category_confidence': self._calculate_category_confidence(record, category),
                'data_type': data_type,
                'classification_timestamp': datetime.now().isoformat(),
                'characteristics': self._analyze_record_characteristics(record)
            }
            
            categorized[category].append(exception_record)
        
        return categorized
    
    def _classify_record(self, record: pd.Series) -> str:
        """Classify a single record into an exception category."""
        description = str(record.get('description', '')).lower()
        amount = record.get('amount', 0)
        
        # Check each category's patterns
        for category, config in self.exception_categories.items():
            if category == 'unknown':
                continue
            
            # Check text patterns
            for pattern in config['patterns']:
                if re.search(pattern, description, re.IGNORECASE):
                    return category
        
        # Additional logic-based classification
        
        # Small amounts might be fees or adjustments
        if abs(amount) < 10:
            return 'amount_differences'
        
        # Round amounts might be allocations or provisions
        if amount % 100 == 0 and abs(amount) > 1000:
            return 'system_specific'
        
        # Default to unknown
        return 'unknown'
    
    def _calculate_category_confidence(self, record: pd.Series, category: str) -> float:
        """Calculate confidence score for category classification."""
        if category == 'unknown':
            return 0.5
        
        description = str(record.get('description', '')).lower()
        config = self.exception_categories[category]
        
        # Count pattern matches
        pattern_matches = 0
        for pattern in config['patterns']:
            if re.search(pattern, description, re.IGNORECASE):
                pattern_matches += 1
        
        # Base confidence on pattern matches
        if pattern_matches > 0:
            return min(0.9, 0.6 + (pattern_matches * 0.1))
        
        # Lower confidence for logic-based classifications
        return 0.6
    
    def _analyze_record_characteristics(self, record: pd.Series) -> Dict[str, Any]:
        """Analyze characteristics of a record for additional insights."""
        characteristics = {}
        
        # Amount characteristics
        amount = record.get('amount', 0)
        characteristics['amount_magnitude'] = 'small' if abs(amount) < 100 else 'medium' if abs(amount) < 10000 else 'large'
        characteristics['amount_type'] = 'round' if amount % 100 == 0 else 'precise'
        characteristics['amount_sign'] = 'positive' if amount > 0 else 'negative' if amount < 0 else 'zero'
        
        # Description characteristics
        description = str(record.get('description', ''))
        characteristics['description_length'] = len(description)
        characteristics['contains_numbers'] = bool(re.search(r'\d', description))
        characteristics['contains_special_chars'] = bool(re.search(r'[^a-zA-Z0-9\s]', description))
        
        # Date characteristics
        if 'date' in record and pd.notnull(record['date']):
            try:
                transaction_date = pd.to_datetime(record['date'])
                characteristics['day_of_week'] = transaction_date.strftime('%A')
                characteristics['month'] = transaction_date.strftime('%B')
                characteristics['is_month_end'] = transaction_date.day >= 28
            except:
                pass
        
        return characteristics
    
    def _analyze_patterns(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns in unmatched transactions."""
        patterns = {
            'common_descriptions': {},
            'amount_clusters': {},
            'temporal_patterns': {},
            'correlation_analysis': {}
        }
        
        # Combine datasets for pattern analysis
        all_records = []
        if not df1.empty:
            df1_dict = df1.to_dict('records')
            for record in df1_dict:
                record['source'] = 'df1'
            all_records.extend(df1_dict)
        
        if not df2.empty:
            df2_dict = df2.to_dict('records')
            for record in df2_dict:
                record['source'] = 'df2'
            all_records.extend(df2_dict)
        
        if not all_records:
            return patterns
        
        # Analyze common descriptions
        descriptions = defaultdict(int)
        for record in all_records:
            desc = normalize_text(str(record.get('description', '')))
            if desc:
                descriptions[desc] += 1
        
        patterns['common_descriptions'] = dict(sorted(
            descriptions.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10])
        
        # Analyze amount patterns
        amounts = [record.get('amount', 0) for record in all_records if record.get('amount') is not None]
        if amounts:
            patterns['amount_clusters'] = {
                'min': min(amounts),
                'max': max(amounts),
                'mean': np.mean(amounts),
                'median': np.median(amounts),
                'std': np.std(amounts),
                'round_amounts': len([amt for amt in amounts if amt % 100 == 0])
            }
        
        # Temporal patterns
        dates = []
        for record in all_records:
            if record.get('date'):
                try:
                    dates.append(pd.to_datetime(record['date']))
                except:
                    pass
        
        if dates:
            df_dates = pd.DataFrame({'date': dates})
            patterns['temporal_patterns'] = {
                'date_range': {
                    'start': min(dates).isoformat(),
                    'end': max(dates).isoformat(),
                    'span_days': (max(dates) - min(dates)).days
                },
                'day_of_week_distribution': df_dates['date'].dt.day_name().value_counts().to_dict(),
                'month_distribution': df_dates['date'].dt.month_name().value_counts().to_dict()
            }
        
        return patterns
    
    def _analyze_aging(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, Any]:
        """Analyze aging of unmatched transactions."""
        aging = {
            'df1_aging': {},
            'df2_aging': {},
            'aging_summary': {}
        }
        
        current_date = datetime.now()
        
        for df_name, df in [('df1_aging', df1), ('df2_aging', df2)]:
            if df.empty:
                continue
            
            ages = []
            for _, record in df.iterrows():
                if record.get('date'):
                    try:
                        transaction_date = pd.to_datetime(record['date'])
                        age_days = (current_date - transaction_date).days
                        ages.append(age_days)
                    except:
                        pass
            
            if ages:
                aging[df_name] = {
                    'average_age_days': np.mean(ages),
                    'median_age_days': np.median(ages),
                    'max_age_days': max(ages),
                    'min_age_days': min(ages),
                    'age_buckets': {
                        '0-7_days': len([age for age in ages if age <= 7]),
                        '8-30_days': len([age for age in ages if 8 <= age <= 30]),
                        '31-90_days': len([age for age in ages if 31 <= age <= 90]),
                        '91-365_days': len([age for age in ages if 91 <= age <= 365]),
                        'over_365_days': len([age for age in ages if age > 365])
                    }
                }
        
        return aging
    
    def _generate_resolution_suggestions(self, 
                                       df1: pd.DataFrame, 
                                       df2: pd.DataFrame,
                                       df1_type: str,
                                       df2_type: str) -> List[Dict[str, Any]]:
        """Generate intelligent resolution suggestions."""
        suggestions = []
        
        # Suggestion 1: Near-match opportunities
        suggestions.extend(self._suggest_near_matches(df1, df2, df1_type, df2_type))
        
        # Suggestion 2: Bulk resolution opportunities
        suggestions.extend(self._suggest_bulk_resolutions(df1, df2))
        
        # Suggestion 3: Process improvements
        suggestions.extend(self._suggest_process_improvements(df1, df2))
        
        return suggestions
    
    def _suggest_near_matches(self, df1: pd.DataFrame, df2: pd.DataFrame, df1_type: str, df2_type: str) -> List[Dict]:
        """Suggest potential near matches that might have been missed."""
        suggestions = []
        
        if df1.empty or df2.empty:
            return suggestions
        
        # Look for transactions with similar amounts but different dates
        for _, record1 in df1.iterrows():
            amount1 = record1.get('amount', 0)
            
            for _, record2 in df2.iterrows():
                amount2 = record2.get('amount', 0)
                
                # Check if amounts are very close
                if abs(amount1 - amount2) <= 0.01:
                    try:
                        date1 = pd.to_datetime(record1.get('date'))
                        date2 = pd.to_datetime(record2.get('date'))
                        day_diff = abs((date1 - date2).days)
                        
                        if 3 <= day_diff <= 10:  # Reasonable timing difference
                            suggestions.append({
                                'type': 'near_match_opportunity',
                                'priority': 'medium',
                                'description': f'Potential match with {day_diff} day timing difference',
                                'records': [
                                    {
                                        'source': df1_type,
                                        'index': record1.get('original_index', record1.name),
                                        'date': record1.get('date'),
                                        'amount': amount1,
                                        'description': record1.get('description', '')
                                    },
                                    {
                                        'source': df2_type,
                                        'index': record2.get('original_index', record2.name),
                                        'date': record2.get('date'),
                                        'amount': amount2,
                                        'description': record2.get('description', '')
                                    }
                                ],
                                'confidence': 0.7,
                                'suggested_action': 'manual_review'
                            })
                    except:
                        pass
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def _suggest_bulk_resolutions(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict]:
        """Suggest bulk resolution opportunities."""
        suggestions = []
        
        # Combine datasets for analysis
        all_records = []
        for df, source in [(df1, 'df1'), (df2, 'df2')]:
            if not df.empty:
                records = df.to_dict('records')
                for record in records:
                    record['source'] = source
                all_records.append(record)
        
        if not all_records:
            return suggestions
        
        # Look for records with same description pattern
        description_groups = defaultdict(list)
        for record in all_records:
            desc = normalize_text(str(record.get('description', '')))
            if desc:
                # Group by first few words
                key_words = ' '.join(desc.split()[:3])
                description_groups[key_words].append(record)
        
        # Suggest bulk resolution for groups with multiple items
        for pattern, records in description_groups.items():
            if len(records) >= 3:
                suggestions.append({
                    'type': 'bulk_resolution_opportunity',
                    'priority': 'low',
                    'description': f'Bulk review opportunity for "{pattern}" pattern',
                    'record_count': len(records),
                    'pattern': pattern,
                    'confidence': 0.6,
                    'suggested_action': 'bulk_categorization'
                })
        
        return suggestions[:3]  # Limit to top 3
    
    def _suggest_process_improvements(self, df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict]:
        """Suggest process improvements based on exception patterns."""
        suggestions = []
        
        # High volume suggestion
        total_exceptions = len(df1) + len(df2)
        if total_exceptions > 100:
            suggestions.append({
                'type': 'process_improvement',
                'priority': 'high',
                'description': f'High exception volume ({total_exceptions} items) suggests process review needed',
                'suggested_action': 'process_analysis',
                'confidence': 0.8
            })
        
        # Timing pattern suggestion
        current_date = datetime.now()
        old_records = 0
        
        for df in [df1, df2]:
            if not df.empty:
                for _, record in df.iterrows():
                    if record.get('date'):
                        try:
                            transaction_date = pd.to_datetime(record['date'])
                            if (current_date - transaction_date).days > 30:
                                old_records += 1
                        except:
                            pass
        
        if old_records > 10:
            suggestions.append({
                'type': 'process_improvement',
                'priority': 'medium',
                'description': f'{old_records} exceptions are over 30 days old - consider aging review process',
                'suggested_action': 'aging_policy_review',
                'confidence': 0.7
            })
        
        return suggestions
    
    def _calculate_exception_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive exception statistics."""
        stats = {
            'total_exceptions': results['input_summary']['unmatched_df1_count'] + results['input_summary']['unmatched_df2_count'],
            'category_distribution': {},
            'resolution_priorities': {},
            'auto_resolvable_count': 0,
            'manual_review_count': 0
        }
        
        # Analyze category distribution
        all_categories = defaultdict(int)
        auto_resolvable = 0
        
        for data_type in results['categorized_exceptions']:
            for category, exceptions in results['categorized_exceptions'][data_type].items():
                count = len(exceptions)
                all_categories[category] += count
                
                if self.exception_categories[category]['auto_resolvable']:
                    auto_resolvable += count
        
        stats['category_distribution'] = dict(all_categories)
        stats['auto_resolvable_count'] = auto_resolvable
        stats['manual_review_count'] = stats['total_exceptions'] - auto_resolvable
        
        # Resolution priority distribution
        priority_counts = defaultdict(int)
        for category, count in all_categories.items():
            priority = self.exception_categories[category]['resolution_priority']
            priority_counts[priority] += count
        
        stats['resolution_priorities'] = dict(priority_counts)
        
        return stats
    
    def create_resolution_workflow(self, exception_category: str) -> Dict[str, Any]:
        """Create a resolution workflow for a specific exception category."""
        if exception_category not in self.resolution_workflows:
            exception_category = 'unknown'
        
        workflow = self.resolution_workflows.get(exception_category, {
            'steps': ['Manual investigation required'],
            'typical_resolution_time': 'Variable',
            'required_approvals': ['manager']
        })
        
        return {
            'category': exception_category,
            'workflow_id': f"{exception_category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'steps': workflow['steps'],
            'typical_resolution_time': workflow['typical_resolution_time'],
            'required_approvals': workflow['required_approvals'],
            'progress': {
                'current_step': 0,
                'completed_steps': [],
                'pending_approvals': []
            }
        }
    
    def export_exceptions_to_excel(self, results: Dict[str, Any], file_path: str):
        """Export exception analysis results to Excel file."""
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Summary sheet
                summary_data = []
                for data_type in results['categorized_exceptions']:
                    for category, exceptions in results['categorized_exceptions'][data_type].items():
                        for exception in exceptions:
                            summary_data.append({
                                'Data_Type': data_type,
                                'Category': category,
                                'Index': exception['original_index'],
                                'Date': exception['date'],
                                'Amount': exception['amount'],
                                'Description': exception['description'],
                                'Confidence': exception['category_confidence'],
                                'Priority': self.exception_categories[category]['resolution_priority']
                            })
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Exception_Summary', index=False)
                
                # Statistics sheet
                stats_data = []
                for category, count in results['statistics']['category_distribution'].items():
                    stats_data.append({
                        'Category': category,
                        'Count': count,
                        'Priority': self.exception_categories[category]['resolution_priority'],
                        'Auto_Resolvable': self.exception_categories[category]['auto_resolvable']
                    })
                
                if stats_data:
                    stats_df = pd.DataFrame(stats_data)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
            logger.info(f"Exception analysis exported to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to export exception analysis: {str(e)}")
            raise ExceptionHandlerError(f"Failed to export exception analysis: {str(e)}") from e
