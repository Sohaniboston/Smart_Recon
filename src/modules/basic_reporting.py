"""
SmartRecon Basic Reporting Module

This module provides essential reporting functionality for data ingestion and 
basic reconciliation analysis including:
- Data quality reports
- File ingestion summaries
- Basic matching statistics
- Simple visualizations
- Excel/CSV export capabilities

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path
import json

from ..utils.exceptions import ReportingError
from ..utils.helpers import ensure_directory_exists, format_currency

logger = logging.getLogger(__name__)


class BasicReporter:
    """
    Basic reporting functionality for SmartRecon data processing.
    
    Features:
    - Data ingestion summary reports
    - Data quality assessment reports
    - Basic reconciliation statistics
    - Simple visualizations
    - Excel/CSV export
    - HTML summary reports
    """
    
    def __init__(self, config=None):
        """
        Initialize BasicReporter.
        
        Args:
            config: Configuration object (optional)
        """
        self.config = config
        self.reports_generated = []
        
        # Default report parameters
        self.default_params = {
            'output_directory': 'reports',
            'include_charts': True,
            'chart_format': 'png',
            'chart_dpi': 300,
            'excel_export': True,
            'csv_export': True,
            'html_export': True
        }
        
        # Load configuration parameters
        self.params = self._load_report_parameters()
        
        logger.info("BasicReporter initialized")
    
    def generate_ingestion_report(self, 
                                 ingestion_results: List[Dict[str, Any]],
                                 output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive data ingestion report.
        
        Args:
            ingestion_results: List of ingestion results from DataIngestion.load_file()
            output_dir: Output directory for reports
            
        Returns:
            Dict[str, Any]: Report generation results
        """
        try:
            logger.info("Generating data ingestion report")
            
            # Setup output directory
            report_dir = output_dir or self.params['output_directory']
            ensure_directory_exists(report_dir)
            
            # Initialize report structure
            report_data = {
                'report_type': 'data_ingestion',
                'generated_at': datetime.now(),
                'file_summary': [],
                'overall_statistics': {},
                'data_quality_summary': {},
                'warnings_and_errors': [],
                'files_processed': len(ingestion_results)
            }
            
            # Process each ingestion result
            total_rows = 0
            total_columns = 0
            quality_scores = []
            all_warnings = []
            all_errors = []
            
            for result in ingestion_results:
                file_info = result.get('file_info', {})
                processing_stats = result.get('processing_stats', {})
                data_quality = result.get('data_quality', {})
                
                # File summary
                file_summary = {
                    'file_name': file_info.get('name', 'Unknown'),
                    'file_size_mb': file_info.get('size_mb', 0),
                    'rows_loaded': processing_stats.get('rows_loaded', 0),
                    'columns_loaded': processing_stats.get('columns_loaded', 0),
                    'processing_time': processing_stats.get('processing_time_seconds', 0),
                    'encoding': processing_stats.get('encoding_used', 'Unknown'),
                    'data_quality_score': data_quality.get('overall_score', 0)
                }
                report_data['file_summary'].append(file_summary)
                
                # Accumulate statistics
                total_rows += processing_stats.get('rows_loaded', 0)
                total_columns += processing_stats.get('columns_loaded', 0)
                quality_scores.append(data_quality.get('overall_score', 0))
                
                # Collect warnings and errors
                all_warnings.extend(result.get('warnings', []))
                all_errors.extend(result.get('errors', []))
            
            # Calculate overall statistics
            report_data['overall_statistics'] = {
                'total_files_processed': len(ingestion_results),
                'total_rows_loaded': total_rows,
                'average_columns_per_file': total_columns / len(ingestion_results) if ingestion_results else 0,
                'average_data_quality_score': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                'total_warnings': len(all_warnings),
                'total_errors': len(all_errors)
            }
            
            # Data quality summary
            if quality_scores:
                report_data['data_quality_summary'] = {
                    'highest_quality_score': max(quality_scores),
                    'lowest_quality_score': min(quality_scores),
                    'files_above_threshold': sum(1 for score in quality_scores if score >= 0.8),
                    'files_needing_attention': sum(1 for score in quality_scores if score < 0.8)
                }
            
            # Store warnings and errors
            report_data['warnings_and_errors'] = {
                'warnings': all_warnings[:10],  # Limit to first 10
                'errors': all_errors[:10],
                'total_warning_count': len(all_warnings),
                'total_error_count': len(all_errors)
            }
            
            # Generate outputs
            output_files = []
            
            # Excel export
            if self.params['excel_export']:
                excel_file = self._export_ingestion_to_excel(report_data, report_dir)
                output_files.append(excel_file)
            
            # HTML export
            if self.params['html_export']:
                html_file = self._export_ingestion_to_html(report_data, report_dir)
                output_files.append(html_file)
            
            # Generate charts
            if self.params['include_charts']:
                chart_files = self._generate_ingestion_charts(report_data, report_dir)
                output_files.extend(chart_files)
            
            logger.info(f"Ingestion report generated with {len(output_files)} files")
            return {
                'success': True,
                'report_data': report_data,
                'output_files': output_files,
                'report_directory': report_dir
            }
            
        except Exception as e:
            logger.error(f"Failed to generate ingestion report: {e}")
            raise ReportingError(f"Ingestion report generation failed: {e}") from e
    
    def generate_basic_reconciliation_report(self,
                                           gl_data: pd.DataFrame,
                                           bank_data: pd.DataFrame,
                                           matches: List[Dict[str, Any]],
                                           output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate basic reconciliation analysis report.
        
        Args:
            gl_data: General Ledger DataFrame
            bank_data: Bank statement DataFrame
            matches: List of match records
            output_dir: Output directory for reports
            
        Returns:
            Dict[str, Any]: Report generation results
        """
        try:
            logger.info("Generating basic reconciliation report")
            
            # Setup output directory
            report_dir = output_dir or self.params['output_directory']
            ensure_directory_exists(report_dir)
            
            # Calculate basic statistics
            total_gl_records = len(gl_data)
            total_bank_records = len(bank_data)
            total_matches = len(matches)
            
            # Calculate match rates
            gl_match_rate = (total_matches / total_gl_records * 100) if total_gl_records > 0 else 0
            bank_match_rate = (total_matches / total_bank_records * 100) if total_bank_records > 0 else 0
            
            # Amount analysis
            gl_total_amount = gl_data['amount'].sum() if 'amount' in gl_data.columns else 0
            bank_total_amount = bank_data['amount'].sum() if 'amount' in bank_data.columns else 0
            
            matched_amount = 0
            if matches:
                for match in matches:
                    matched_amount += match.get('gl_record', {}).get('amount', 0)
            
            # Create report structure
            report_data = {
                'report_type': 'basic_reconciliation',
                'generated_at': datetime.now(),
                'summary_statistics': {
                    'total_gl_records': total_gl_records,
                    'total_bank_records': total_bank_records,
                    'total_matches': total_matches,
                    'gl_match_rate': round(gl_match_rate, 2),
                    'bank_match_rate': round(bank_match_rate, 2),
                    'gl_total_amount': gl_total_amount,
                    'bank_total_amount': bank_total_amount,
                    'matched_amount': matched_amount,
                    'unmatched_gl_records': total_gl_records - total_matches,
                    'unmatched_bank_records': total_bank_records - total_matches
                },
                'amount_analysis': {
                    'gl_amount_range': {
                        'min': gl_data['amount'].min() if 'amount' in gl_data.columns and not gl_data.empty else 0,
                        'max': gl_data['amount'].max() if 'amount' in gl_data.columns and not gl_data.empty else 0,
                        'average': gl_data['amount'].mean() if 'amount' in gl_data.columns and not gl_data.empty else 0
                    },
                    'bank_amount_range': {
                        'min': bank_data['amount'].min() if 'amount' in bank_data.columns and not bank_data.empty else 0,
                        'max': bank_data['amount'].max() if 'amount' in bank_data.columns and not bank_data.empty else 0,
                        'average': bank_data['amount'].mean() if 'amount' in bank_data.columns and not bank_data.empty else 0
                    }
                }
            }
            
            # Analyze match types if available
            if matches:
                match_types = {}
                confidence_distribution = {'high': 0, 'medium': 0, 'low': 0}
                
                for match in matches:
                    match_type = match.get('match_strategy', match.get('match_type', 'unknown'))
                    match_types[match_type] = match_types.get(match_type, 0) + 1
                    
                    confidence = match.get('confidence', 0)
                    if confidence >= 0.9:
                        confidence_distribution['high'] += 1
                    elif confidence >= 0.7:
                        confidence_distribution['medium'] += 1
                    else:
                        confidence_distribution['low'] += 1
                
                report_data['match_analysis'] = {
                    'match_types': match_types,
                    'confidence_distribution': confidence_distribution
                }
            
            # Generate outputs
            output_files = []
            
            # Excel export
            if self.params['excel_export']:
                excel_file = self._export_reconciliation_to_excel(report_data, matches, report_dir)
                output_files.append(excel_file)
            
            # HTML export
            if self.params['html_export']:
                html_file = self._export_reconciliation_to_html(report_data, report_dir)
                output_files.append(html_file)
            
            # Generate charts
            if self.params['include_charts']:
                chart_files = self._generate_reconciliation_charts(report_data, report_dir)
                output_files.extend(chart_files)
            
            logger.info(f"Basic reconciliation report generated with {len(output_files)} files")
            return {
                'success': True,
                'report_data': report_data,
                'output_files': output_files,
                'report_directory': report_dir
            }
            
        except Exception as e:
            logger.error(f"Failed to generate reconciliation report: {e}")
            raise ReportingError(f"Reconciliation report generation failed: {e}") from e
    
    def _export_ingestion_to_excel(self, report_data: Dict[str, Any], output_dir: str) -> str:
        """Export ingestion report to Excel format."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_ingestion_report_{timestamp}.xlsx"
            filepath = os.path.join(output_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([report_data['overall_statistics']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # File details sheet
                files_df = pd.DataFrame(report_data['file_summary'])
                files_df.to_excel(writer, sheet_name='File_Details', index=False)
                
                # Data quality sheet
                if report_data.get('data_quality_summary'):
                    quality_df = pd.DataFrame([report_data['data_quality_summary']])
                    quality_df.to_excel(writer, sheet_name='Data_Quality', index=False)
                
                # Issues sheet
                if report_data['warnings_and_errors']['warnings'] or report_data['warnings_and_errors']['errors']:
                    issues_data = []
                    for warning in report_data['warnings_and_errors']['warnings']:
                        issues_data.append({'Type': 'Warning', 'Message': warning})
                    for error in report_data['warnings_and_errors']['errors']:
                        issues_data.append({'Type': 'Error', 'Message': error})
                    
                    if issues_data:
                        issues_df = pd.DataFrame(issues_data)
                        issues_df.to_excel(writer, sheet_name='Issues', index=False)
            
            logger.info(f"Ingestion report exported to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export ingestion report to Excel: {e}")
            raise ReportingError(f"Excel export failed: {e}") from e
    
    def _export_ingestion_to_html(self, report_data: Dict[str, Any], output_dir: str) -> str:
        """Export ingestion report to HTML format."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_ingestion_report_{timestamp}.html"
            filepath = os.path.join(output_dir, filename)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>SmartRecon Data Ingestion Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .section {{ margin: 20px 0; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                    .stat-card {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center; }}
                    .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                    .stat-label {{ font-size: 14px; color: #666; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .success {{ color: #27ae60; }}
                    .warning {{ color: #f39c12; }}
                    .error {{ color: #e74c3c; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>SmartRecon Data Ingestion Report</h1>
                    <p>Generated on: {report_data['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>Overall Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{report_data['overall_statistics']['total_files_processed']}</div>
                            <div class="stat-label">Files Processed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{report_data['overall_statistics']['total_rows_loaded']:,}</div>
                            <div class="stat-label">Total Rows Loaded</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{report_data['overall_statistics']['average_data_quality_score']:.2f}</div>
                            <div class="stat-label">Avg Quality Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value {'success' if report_data['overall_statistics']['total_errors'] == 0 else 'error'}">{report_data['overall_statistics']['total_errors']}</div>
                            <div class="stat-label">Total Errors</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>File Processing Details</h2>
                    <table>
                        <tr>
                            <th>File Name</th>
                            <th>Size (MB)</th>
                            <th>Rows</th>
                            <th>Columns</th>
                            <th>Quality Score</th>
                            <th>Processing Time (s)</th>
                        </tr>
            """
            
            for file_info in report_data['file_summary']:
                quality_class = 'success' if file_info['data_quality_score'] >= 0.8 else 'warning' if file_info['data_quality_score'] >= 0.6 else 'error'
                html_content += f"""
                        <tr>
                            <td>{file_info['file_name']}</td>
                            <td>{file_info['file_size_mb']:.2f}</td>
                            <td>{file_info['rows_loaded']:,}</td>
                            <td>{file_info['columns_loaded']}</td>
                            <td class="{quality_class}">{file_info['data_quality_score']:.2f}</td>
                            <td>{file_info['processing_time']:.2f}</td>
                        </tr>
                """
            
            html_content += """
                    </table>
                </div>
            </body>
            </html>
            """
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Ingestion report exported to HTML: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export ingestion report to HTML: {e}")
            raise ReportingError(f"HTML export failed: {e}") from e
    
    def _export_reconciliation_to_excel(self, report_data: Dict[str, Any], matches: List[Dict[str, Any]], output_dir: str) -> str:
        """Export reconciliation report to Excel format."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reconciliation_report_{timestamp}.xlsx"
            filepath = os.path.join(output_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([report_data['summary_statistics']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Matches sheet
                if matches:
                    matches_data = []
                    for match in matches:
                        gl_record = match.get('gl_record', {})
                        bank_record = match.get('bank_record', {})
                        
                        matches_data.append({
                            'Match_Type': match.get('match_strategy', match.get('match_type', 'Unknown')),
                            'Confidence': match.get('confidence', 0),
                            'GL_Date': gl_record.get('date', ''),
                            'GL_Amount': gl_record.get('amount', 0),
                            'GL_Description': gl_record.get('description', ''),
                            'Bank_Date': bank_record.get('date', ''),
                            'Bank_Amount': bank_record.get('amount', 0),
                            'Bank_Description': bank_record.get('description', ''),
                            'Amount_Difference': abs(gl_record.get('amount', 0) - bank_record.get('amount', 0))
                        })
                    
                    matches_df = pd.DataFrame(matches_data)
                    matches_df.to_excel(writer, sheet_name='Matches', index=False)
                
                # Amount analysis sheet
                if report_data.get('amount_analysis'):
                    amount_data = []
                    gl_range = report_data['amount_analysis']['gl_amount_range']
                    bank_range = report_data['amount_analysis']['bank_amount_range']
                    
                    amount_data.extend([
                        {'Source': 'GL', 'Metric': 'Min Amount', 'Value': gl_range['min']},
                        {'Source': 'GL', 'Metric': 'Max Amount', 'Value': gl_range['max']},
                        {'Source': 'GL', 'Metric': 'Average Amount', 'Value': gl_range['average']},
                        {'Source': 'Bank', 'Metric': 'Min Amount', 'Value': bank_range['min']},
                        {'Source': 'Bank', 'Metric': 'Max Amount', 'Value': bank_range['max']},
                        {'Source': 'Bank', 'Metric': 'Average Amount', 'Value': bank_range['average']},
                    ])
                    
                    amount_df = pd.DataFrame(amount_data)
                    amount_df.to_excel(writer, sheet_name='Amount_Analysis', index=False)
            
            logger.info(f"Reconciliation report exported to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export reconciliation report to Excel: {e}")
            raise ReportingError(f"Excel export failed: {e}") from e
    
    def _export_reconciliation_to_html(self, report_data: Dict[str, Any], output_dir: str) -> str:
        """Export reconciliation report to HTML format."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reconciliation_report_{timestamp}.html"
            filepath = os.path.join(output_dir, filename)
            
            stats = report_data['summary_statistics']
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>SmartRecon Basic Reconciliation Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .section {{ margin: 20px 0; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                    .stat-card {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center; }}
                    .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                    .stat-label {{ font-size: 14px; color: #666; }}
                    .progress-bar {{ width: 100%; height: 20px; background-color: #ecf0f1; border-radius: 10px; margin: 5px 0; }}
                    .progress-fill {{ height: 100%; border-radius: 10px; transition: width 0.3s ease; }}
                    .success {{ background-color: #27ae60; }}
                    .warning {{ background-color: #f39c12; }}
                    .info {{ background-color: #3498db; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>SmartRecon Basic Reconciliation Report</h1>
                    <p>Generated on: {report_data['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>Reconciliation Summary</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{stats['total_matches']}</div>
                            <div class="stat-label">Total Matches</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['gl_match_rate']:.1f}%</div>
                            <div class="stat-label">GL Match Rate</div>
                            <div class="progress-bar">
                                <div class="progress-fill success" style="width: {stats['gl_match_rate']}%"></div>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['bank_match_rate']:.1f}%</div>
                            <div class="stat-label">Bank Match Rate</div>
                            <div class="progress-bar">
                                <div class="progress-fill info" style="width: {stats['bank_match_rate']}%"></div>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{format_currency(stats['matched_amount'])}</div>
                            <div class="stat-label">Matched Amount</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Record Counts</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{stats['total_gl_records']}</div>
                            <div class="stat-label">GL Records</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['total_bank_records']}</div>
                            <div class="stat-label">Bank Records</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['unmatched_gl_records']}</div>
                            <div class="stat-label">Unmatched GL</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['unmatched_bank_records']}</div>
                            <div class="stat-label">Unmatched Bank</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Reconciliation report exported to HTML: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export reconciliation report to HTML: {e}")
            raise ReportingError(f"HTML export failed: {e}") from e
    
    def _generate_ingestion_charts(self, report_data: Dict[str, Any], output_dir: str) -> List[str]:
        """Generate charts for ingestion report."""
        chart_files = []
        
        try:
            # Data quality distribution chart
            if report_data['file_summary']:
                quality_scores = [file_info['data_quality_score'] for file_info in report_data['file_summary']]
                
                plt.figure(figsize=(10, 6))
                plt.hist(quality_scores, bins=10, edgecolor='black', alpha=0.7)
                plt.title('Data Quality Score Distribution')
                plt.xlabel('Quality Score')
                plt.ylabel('Number of Files')
                plt.grid(True, alpha=0.3)
                
                chart_file = os.path.join(output_dir, 'data_quality_distribution.png')
                plt.savefig(chart_file, dpi=self.params['chart_dpi'], bbox_inches='tight')
                plt.close()
                chart_files.append(chart_file)
                
                # File size vs processing time scatter plot
                sizes = [file_info['file_size_mb'] for file_info in report_data['file_summary']]
                times = [file_info['processing_time'] for file_info in report_data['file_summary']]
                
                plt.figure(figsize=(10, 6))
                plt.scatter(sizes, times, alpha=0.7)
                plt.title('File Size vs Processing Time')
                plt.xlabel('File Size (MB)')
                plt.ylabel('Processing Time (seconds)')
                plt.grid(True, alpha=0.3)
                
                chart_file = os.path.join(output_dir, 'size_vs_time.png')
                plt.savefig(chart_file, dpi=self.params['chart_dpi'], bbox_inches='tight')
                plt.close()
                chart_files.append(chart_file)
            
        except Exception as e:
            logger.warning(f"Failed to generate some ingestion charts: {e}")
        
        return chart_files
    
    def _generate_reconciliation_charts(self, report_data: Dict[str, Any], output_dir: str) -> List[str]:
        """Generate charts for reconciliation report."""
        chart_files = []
        
        try:
            stats = report_data['summary_statistics']
            
            # Match rate comparison chart
            plt.figure(figsize=(8, 6))
            categories = ['GL Records', 'Bank Records']
            match_rates = [stats['gl_match_rate'], stats['bank_match_rate']]
            
            bars = plt.bar(categories, match_rates, color=['#3498db', '#2ecc71'])
            plt.title('Match Rates Comparison')
            plt.ylabel('Match Rate (%)')
            plt.ylim(0, 100)
            
            # Add value labels on bars
            for bar, rate in zip(bars, match_rates):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                        f'{rate:.1f}%', ha='center', va='bottom')
            
            chart_file = os.path.join(output_dir, 'match_rates.png')
            plt.savefig(chart_file, dpi=self.params['chart_dpi'], bbox_inches='tight')
            plt.close()
            chart_files.append(chart_file)
            
            # Record counts pie chart
            plt.figure(figsize=(8, 8))
            labels = ['Matched Records', 'Unmatched GL', 'Unmatched Bank']
            sizes = [stats['total_matches'], stats['unmatched_gl_records'], stats['unmatched_bank_records']]
            colors = ['#27ae60', '#e74c3c', '#f39c12']
            
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('Record Distribution')
            
            chart_file = os.path.join(output_dir, 'record_distribution.png')
            plt.savefig(chart_file, dpi=self.params['chart_dpi'], bbox_inches='tight')
            plt.close()
            chart_files.append(chart_file)
            
        except Exception as e:
            logger.warning(f"Failed to generate some reconciliation charts: {e}")
        
        return chart_files
    
    def _load_report_parameters(self) -> Dict[str, Any]:
        """Load reporting parameters from configuration."""
        params = self.default_params.copy()
        
        # Override with configuration values if available
        if self.config and hasattr(self.config, 'get_reporting_config'):
            config_params = self.config.get_reporting_config()
            params.update(config_params)
        
        return params
    
    def export_dataframe_to_excel(self, df: pd.DataFrame, filename: str, output_dir: Optional[str] = None) -> str:
        """
        Export DataFrame to Excel with basic formatting.
        
        Args:
            df: DataFrame to export
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            str: Path to exported file
        """
        try:
            report_dir = output_dir or self.params['output_directory']
            ensure_directory_exists(report_dir)
            
            filepath = os.path.join(report_dir, filename)
            df.to_excel(filepath, index=False)
            
            logger.info(f"DataFrame exported to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export DataFrame to Excel: {e}")
            raise ReportingError(f"Excel export failed: {e}") from e
    
    def export_dataframe_to_csv(self, df: pd.DataFrame, filename: str, output_dir: Optional[str] = None) -> str:
        """
        Export DataFrame to CSV format.
        
        Args:
            df: DataFrame to export
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            str: Path to exported file
        """
        try:
            report_dir = output_dir or self.params['output_directory']
            ensure_directory_exists(report_dir)
            
            filepath = os.path.join(report_dir, filename)
            df.to_csv(filepath, index=False)
            
            logger.info(f"DataFrame exported to CSV: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export DataFrame to CSV: {e}")
            raise ReportingError(f"CSV export failed: {e}") from e
