#!/usr/bin/env python3
"""
Performance Monitoring and Optimization Utilities

Provides performance monitoring, profiling, and optimization
capabilities for SmartRecon components.

Features:
- Execution time monitoring
- Memory usage tracking
- Performance bottleneck identification
- Optimization recommendations
- Progress tracking for large datasets

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import time
import psutil
import functools
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging
import threading
from contextlib import contextmanager
import gc


class PerformanceMonitor:
    """Monitor and track performance metrics for SmartRecon operations."""
    
    def __init__(self, enable_memory_tracking: bool = True):
        self.enable_memory_tracking = enable_memory_tracking
        self.metrics = []
        self.current_operation = None
        self.logger = logging.getLogger(__name__)
        
        # Performance thresholds
        self.thresholds = {
            'execution_time_warning': 30.0,  # seconds
            'memory_usage_warning': 500.0,   # MB
            'memory_growth_warning': 100.0   # MB
        }
    
    @contextmanager
    def monitor_operation(self, operation_name: str, record_count: int = 0):
        """Context manager to monitor a specific operation."""
        
        start_time = time.time()
        start_memory = self._get_memory_usage() if self.enable_memory_tracking else 0
        
        operation_info = {
            'operation': operation_name,
            'start_time': datetime.now(),
            'start_memory_mb': start_memory,
            'record_count': record_count
        }
        
        self.current_operation = operation_info
        
        try:
            self.logger.info(f"Starting operation: {operation_name}")
            if record_count > 0:
                self.logger.info(f"Processing {record_count:,} records")
            
            yield self
            
            # Operation completed successfully
            end_time = time.time()
            end_memory = self._get_memory_usage() if self.enable_memory_tracking else 0
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Calculate performance metrics
            records_per_second = record_count / execution_time if execution_time > 0 and record_count > 0 else 0
            
            metrics = {
                'operation': operation_name,
                'execution_time': execution_time,
                'start_memory_mb': start_memory,
                'end_memory_mb': end_memory,
                'memory_delta_mb': memory_delta,
                'record_count': record_count,
                'records_per_second': records_per_second,
                'start_time': operation_info['start_time'],
                'end_time': datetime.now(),
                'status': 'completed'
            }
            
            self.metrics.append(metrics)
            
            # Log performance results
            self.logger.info(f"Completed operation: {operation_name}")
            self.logger.info(f"Execution time: {execution_time:.2f} seconds")
            
            if record_count > 0:
                self.logger.info(f"Processing rate: {records_per_second:.2f} records/second")
            
            if self.enable_memory_tracking:
                self.logger.info(f"Memory usage: {start_memory:.1f} → {end_memory:.1f} MB (Δ{memory_delta:+.1f} MB)")
            
            # Check for performance warnings
            self._check_performance_warnings(metrics)
            
        except Exception as e:
            # Operation failed
            end_time = time.time()
            execution_time = end_time - start_time
            
            error_metrics = {
                'operation': operation_name,
                'execution_time': execution_time,
                'start_memory_mb': start_memory,
                'record_count': record_count,
                'start_time': operation_info['start_time'],
                'end_time': datetime.now(),
                'status': 'failed',
                'error': str(e)
            }
            
            self.metrics.append(error_metrics)
            self.logger.error(f"Operation failed: {operation_name} - {e}")
            raise
        
        finally:
            self.current_operation = None
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except Exception:
            return 0.0
    
    def _check_performance_warnings(self, metrics: Dict[str, Any]):
        """Check for performance issues and log warnings."""
        
        # Execution time warning
        if metrics['execution_time'] > self.thresholds['execution_time_warning']:
            self.logger.warning(
                f"Long execution time: {metrics['execution_time']:.2f}s "
                f"(threshold: {self.thresholds['execution_time_warning']}s)"
            )
        
        # Memory usage warning
        if metrics['end_memory_mb'] > self.thresholds['memory_usage_warning']:
            self.logger.warning(
                f"High memory usage: {metrics['end_memory_mb']:.1f}MB "
                f"(threshold: {self.thresholds['memory_usage_warning']}MB)"
            )
        
        # Memory growth warning
        if metrics['memory_delta_mb'] > self.thresholds['memory_growth_warning']:
            self.logger.warning(
                f"Large memory increase: +{metrics['memory_delta_mb']:.1f}MB "
                f"(threshold: {self.thresholds['memory_growth_warning']}MB)"
            )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        
        if not self.metrics:
            return {'message': 'No performance data available'}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(self.metrics)
        
        # Overall statistics
        total_operations = len(df)
        successful_operations = len(df[df['status'] == 'completed'])
        failed_operations = len(df[df['status'] == 'failed'])
        
        summary = {
            'overview': {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'failed_operations': failed_operations,
                'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0
            }
        }
        
        # Completed operations analysis
        completed_df = df[df['status'] == 'completed']
        
        if not completed_df.empty:
            summary['execution_time'] = {
                'total_seconds': completed_df['execution_time'].sum(),
                'average_seconds': completed_df['execution_time'].mean(),
                'min_seconds': completed_df['execution_time'].min(),
                'max_seconds': completed_df['execution_time'].max(),
                'std_seconds': completed_df['execution_time'].std()
            }
            
            if self.enable_memory_tracking:
                summary['memory_usage'] = {
                    'max_usage_mb': completed_df['end_memory_mb'].max(),
                    'average_usage_mb': completed_df['end_memory_mb'].mean(),
                    'total_memory_growth_mb': completed_df['memory_delta_mb'].sum(),
                    'average_memory_growth_mb': completed_df['memory_delta_mb'].mean()
                }
            
            # Processing rate analysis
            processing_df = completed_df[completed_df['record_count'] > 0]
            if not processing_df.empty:
                summary['processing_rate'] = {
                    'total_records': processing_df['record_count'].sum(),
                    'average_records_per_second': processing_df['records_per_second'].mean(),
                    'max_records_per_second': processing_df['records_per_second'].max(),
                    'min_records_per_second': processing_df['records_per_second'].min()
                }
        
        # Operation breakdown
        operation_summary = df.groupby('operation').agg({
            'execution_time': ['count', 'mean', 'sum'],
            'status': lambda x: (x == 'completed').sum()
        }).round(2)
        
        summary['by_operation'] = operation_summary.to_dict() if not operation_summary.empty else {}
        
        return summary
    
    def get_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        
        recommendations = []
        
        if not self.metrics:
            return ["No performance data available for analysis"]
        
        df = pd.DataFrame(self.metrics)
        completed_df = df[df['status'] == 'completed']
        
        if completed_df.empty:
            return ["No successful operations to analyze"]
        
        # Execution time recommendations
        avg_time = completed_df['execution_time'].mean()
        max_time = completed_df['execution_time'].max()
        
        if max_time > self.thresholds['execution_time_warning']:
            slowest_operation = completed_df.loc[completed_df['execution_time'].idxmax(), 'operation']
            recommendations.append(
                f"Optimize '{slowest_operation}' operation - taking {max_time:.2f}s "
                f"(consider parallel processing or algorithm optimization)"
            )
        
        if avg_time > 10.0:
            recommendations.append(
                f"Average execution time is {avg_time:.2f}s - consider vectorization "
                f"or more efficient algorithms"
            )
        
        # Memory recommendations
        if self.enable_memory_tracking:
            max_memory = completed_df['end_memory_mb'].max()
            total_growth = completed_df['memory_delta_mb'].sum()
            
            if max_memory > self.thresholds['memory_usage_warning']:
                recommendations.append(
                    f"High memory usage detected ({max_memory:.1f}MB) - "
                    f"consider processing data in chunks or using more memory-efficient algorithms"
                )
            
            if total_growth > 200:
                recommendations.append(
                    f"Significant memory growth ({total_growth:.1f}MB total) - "
                    f"check for memory leaks or implement garbage collection"
                )
        
        # Processing rate recommendations
        processing_df = completed_df[completed_df['record_count'] > 0]
        if not processing_df.empty:
            avg_rate = processing_df['records_per_second'].mean()
            
            if avg_rate < 100:
                recommendations.append(
                    f"Low processing rate ({avg_rate:.1f} records/second) - "
                    f"consider vectorized operations or parallel processing"
                )
            
            # Check for operations with large datasets but low rates
            slow_large_ops = processing_df[
                (processing_df['record_count'] > 1000) & 
                (processing_df['records_per_second'] < 50)
            ]
            
            if not slow_large_ops.empty:
                recommendations.append(
                    "Large datasets with low processing rates detected - "
                    "implement batch processing or optimize algorithms for large data"
                )
        
        # General recommendations
        if len(completed_df) > 10:
            time_variance = completed_df['execution_time'].std() / completed_df['execution_time'].mean()
            if time_variance > 0.5:
                recommendations.append(
                    "High variance in execution times - investigate inconsistent performance causes"
                )
        
        if not recommendations:
            recommendations.append("Performance looks good! No specific optimizations recommended.")
        
        return recommendations
    
    def export_metrics(self, filepath: str):
        """Export performance metrics to file."""
        
        if not self.metrics:
            raise ValueError("No metrics to export")
        
        df = pd.DataFrame(self.metrics)
        
        # Add summary sheet if Excel
        if filepath.endswith('.xlsx'):
            with pd.ExcelWriter(filepath) as writer:
                df.to_excel(writer, sheet_name='Raw_Metrics', index=False)
                
                # Summary sheet
                summary = self.get_performance_summary()
                summary_df = pd.DataFrame([summary])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Recommendations sheet
                recommendations = self.get_optimization_recommendations()
                rec_df = pd.DataFrame({'Recommendations': recommendations})
                rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
        else:
            df.to_csv(filepath, index=False)
        
        self.logger.info(f"Performance metrics exported to: {filepath}")
    
    def clear_metrics(self):
        """Clear collected metrics."""
        self.metrics.clear()
        gc.collect()  # Force garbage collection


class ProgressTracker:
    """Enhanced progress tracker with performance monitoring."""
    
    def __init__(self, total_steps: int, description: str = "Processing", 
                 enable_eta: bool = True):
        self.total_steps = total_steps
        self.description = description
        self.current_step = 0
        self.start_time = time.time()
        self.enable_eta = enable_eta
        self.step_times = []
        
    def step(self, message: str = "", record_count: int = 0):
        """Advance progress by one step."""
        self.current_step += 1
        current_time = time.time()
        step_duration = current_time - (self.step_times[-1] if self.step_times else self.start_time)
        self.step_times.append(current_time)
        
        percent = (self.current_step / self.total_steps) * 100
        elapsed = current_time - self.start_time
        
        # Calculate ETA
        eta_str = ""
        if self.enable_eta and self.current_step > 0:
            avg_step_time = elapsed / self.current_step
            remaining_steps = self.total_steps - self.current_step
            eta_seconds = avg_step_time * remaining_steps
            eta_str = f" | ETA: {eta_seconds:.1f}s"
        
        # Processing rate
        rate_str = ""
        if record_count > 0 and step_duration > 0:
            rate = record_count / step_duration
            rate_str = f" | Rate: {rate:.1f} rec/s"
        
        progress_msg = f"[{percent:5.1f}%] Step {self.current_step}/{self.total_steps}"
        if message:
            progress_msg += f" - {message}"
        
        progress_msg += f" | Elapsed: {elapsed:.1f}s{eta_str}{rate_str}"
        
        print(progress_msg)
    
    def complete(self, message: str = ""):
        """Mark progress as complete."""
        elapsed = time.time() - self.start_time
        avg_step_time = elapsed / self.total_steps if self.total_steps > 0 else 0
        
        completion_msg = f"[100.0%] ✅ {self.description} completed"
        if message:
            completion_msg += f" - {message}"
        
        completion_msg += f" | Total time: {elapsed:.2f}s | Avg step: {avg_step_time:.2f}s"
        print(completion_msg)


def performance_timer(func: Callable) -> Callable:
    """Decorator to time function execution."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger = logging.getLogger(func.__module__)
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger = logging.getLogger(func.__module__)
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper


def memory_monitor(func: Callable) -> Callable:
    """Decorator to monitor memory usage during function execution."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            
            # Memory after
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_delta = memory_after - memory_before
            
            logger = logging.getLogger(func.__module__)
            logger.info(
                f"{func.__name__} memory: {memory_before:.1f} → {memory_after:.1f} MB "
                f"(Δ{memory_delta:+.1f} MB)"
            )
            
            return result
        except Exception as e:
            # Memory on error
            memory_error = process.memory_info().rss / 1024 / 1024  # MB
            memory_delta = memory_error - memory_before
            
            logger = logging.getLogger(func.__module__)
            logger.error(
                f"{func.__name__} failed - memory: {memory_before:.1f} → {memory_error:.1f} MB "
                f"(Δ{memory_delta:+.1f} MB)"
            )
            raise
    
    return wrapper


def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage by downcasting numeric types."""
    
    if df.empty:
        return df
    
    original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    
    optimized_df = df.copy()
    
    # Optimize numeric columns
    for col in optimized_df.select_dtypes(include=['int64']).columns:
        optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='integer')
    
    for col in optimized_df.select_dtypes(include=['float64']).columns:
        optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
    
    # Optimize object columns that might be categorical
    for col in optimized_df.select_dtypes(include=['object']).columns:
        unique_ratio = optimized_df[col].nunique() / len(optimized_df)
        if unique_ratio < 0.5:  # If less than 50% unique values, convert to category
            optimized_df[col] = optimized_df[col].astype('category')
    
    optimized_memory = optimized_df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    memory_reduction = ((original_memory - optimized_memory) / original_memory) * 100
    
    logger = logging.getLogger(__name__)
    logger.info(
        f"Memory optimization: {original_memory:.2f} → {optimized_memory:.2f} MB "
        f"({memory_reduction:.1f}% reduction)"
    )
    
    return optimized_df


class BatchProcessor:
    """Process large datasets in optimized batches."""
    
    def __init__(self, batch_size: int = 1000, progress_callback: Optional[Callable] = None):
        self.batch_size = batch_size
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
    
    def process_dataframe(self, df: pd.DataFrame, process_func: Callable, 
                         *args, **kwargs) -> pd.DataFrame:
        """Process DataFrame in batches."""
        
        if df.empty:
            return df
        
        total_rows = len(df)
        total_batches = (total_rows + self.batch_size - 1) // self.batch_size
        
        self.logger.info(f"Processing {total_rows:,} rows in {total_batches} batches")
        
        results = []
        
        for i in range(0, total_rows, self.batch_size):
            batch_end = min(i + self.batch_size, total_rows)
            batch_df = df.iloc[i:batch_end].copy()
            
            # Process batch
            batch_result = process_func(batch_df, *args, **kwargs)
            results.append(batch_result)
            
            # Progress callback
            if self.progress_callback:
                batch_num = (i // self.batch_size) + 1
                self.progress_callback(batch_num, total_batches, len(batch_df))
            
            # Memory management
            del batch_df
            if i % (self.batch_size * 10) == 0:  # Force GC every 10 batches
                gc.collect()
        
        # Combine results
        if results:
            final_result = pd.concat(results, ignore_index=True)
            
            # Optimize memory
            final_result = optimize_dataframe_memory(final_result)
            
            self.logger.info(f"Batch processing completed: {len(final_result):,} rows")
            return final_result
        else:
            return pd.DataFrame()


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


# Convenience functions
def monitor_performance(operation_name: str, record_count: int = 0):
    """Convenience function to get performance monitoring context."""
    return performance_monitor.monitor_operation(operation_name, record_count)


def get_performance_summary():
    """Get current performance summary."""
    return performance_monitor.get_performance_summary()


def get_optimization_recommendations():
    """Get optimization recommendations."""
    return performance_monitor.get_optimization_recommendations()


def export_performance_metrics(filepath: str):
    """Export performance metrics to file."""
    return performance_monitor.export_metrics(filepath)
