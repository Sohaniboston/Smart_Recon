"""
SmartRecon Reporting Module

This module generates comprehensive reconciliation reports and visualizations including:
- Executive summary reports
- Detailed matching analysis
- Exception reports with categorization
- Visual dashboards and charts
- Audit trails and compliance reports
- Performance analytics

Author: SmartRecon Development Team
Date: 2025-07-17
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json

from ..utils.exceptions import ReportingError

logger = logging.getLogger(__name__)

# Set matplotlib style for consistent, professional charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class ReportGenerator:
    """
    Comprehensive reporting engine for reconciliation results.
    
    Features:
    - Executive summary dashboards
    - Detailed match analysis reports
    - Exception categorization reports
    - Visual analytics and charts
    - Audit trail documentation
    - Performance metrics reporting
    - Multiple output formats (Excel, PDF, HTML)
    """
    
    def __init__(self, config):
        """
        Initialize ReportGenerator with configuration.
        
        Args:
            config: Configuration object containing reporting parameters
        """
        self.config = config
        self.report_templates = self._initialize_templates()
        
        # Chart styling configuration
        self.chart_config = {
            'figure_size': (12, 8),
            'dpi': 300,
            'color_palette': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8E6C8A'],
            'font_size': 10
        }
        
        logger.info("ReportGenerator module initialized")
    
    def generate_all_reports(self, 
                           matching_results: Dict[str, Any],
                           exception_results: Dict[str, Any],
                           output_dir: Union[str, Path]) -> Dict[str, str]:
        """
        Generate comprehensive set of reconciliation reports.
        
        Args:
            matching_results (Dict[str, Any]): Results from matching engine
            exception_results (Dict[str, Any]): Results from exception handler
            output_dir (Union[str, Path]): Directory to save reports
            
        Returns:
            Dict[str, str]: Dictionary mapping report types to file paths
            
        Raises:
            ReportingError: If report generation fails
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            generated_reports = {}
            
            logger.info(f"Generating comprehensive reconciliation reports to {output_dir}")
            
            # 1. Executive Summary Report
            exec_summary_path = self.generate_executive_summary(
                matching_results, exception_results, output_dir / "executive_summary.xlsx"
            )
            generated_reports['executive_summary'] = str(exec_summary_path)
            
            # 2. Detailed Matching Report
            detailed_match_path = self.generate_detailed_matching_report(
                matching_results, output_dir / "detailed_matches.xlsx"
            )
            generated_reports['detailed_matches'] = str(detailed_match_path)
            
            # 3. Exception Analysis Report
            exception_path = self.generate_exception_report(
                exception_results, output_dir / "exception_analysis.xlsx"
            )
            generated_reports['exception_analysis'] = str(exception_path)
            
            # 4. Visual Analytics Dashboard
            dashboard_path = self.generate_visual_dashboard(
                matching_results, exception_results, output_dir / "analytics_dashboard.html"
            )
            generated_reports['visual_dashboard'] = str(dashboard_path)
            
            # 5. Audit Trail Report
            audit_path = self.generate_audit_trail(
                matching_results, exception_results, output_dir / "audit_trail.json"
            )
            generated_reports['audit_trail'] = str(audit_path)
            
            # 6. Charts and Visualizations
            charts_dir = output_dir / "charts"
            charts_dir.mkdir(exist_ok=True)
            chart_files = self.generate_charts(matching_results, exception_results, charts_dir)
            generated_reports['charts'] = chart_files
            
            logger.info(f"Successfully generated {len(generated_reports)} reports")
            return generated_reports
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise ReportingError(f"Report generation failed: {str(e)}") from e
    
    def generate_executive_summary(self, 
                                 matching_results: Dict[str, Any],
                                 exception_results: Dict[str, Any],
                                 output_path: Path) -> Path:
        """Generate executive summary Excel report."""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Summary Statistics Sheet
                summary_stats = self._create_summary_statistics(matching_results, exception_results)
                summary_df = pd.DataFrame.from_dict(summary_stats, orient='index', columns=['Value'])
                summary_df.index.name = 'Metric'
                summary_df.to_excel(writer, sheet_name='Summary_Statistics')
                
                # Match Rate Analysis Sheet
                match_analysis = self._create_match_analysis(matching_results)
                match_df = pd.DataFrame(match_analysis)
                match_df.to_excel(writer, sheet_name='Match_Analysis', index=False)
                
                # Exception Overview Sheet
                exception_overview = self._create_exception_overview(exception_results)
                if exception_overview:
                    exception_df = pd.DataFrame(exception_overview)
                    exception_df.to_excel(writer, sheet_name='Exception_Overview', index=False)
                
                # Key Findings Sheet
                key_findings = self._create_key_findings(matching_results, exception_results)
                findings_df = pd.DataFrame(key_findings, columns=['Finding', 'Impact', 'Recommendation'])
                findings_df.to_excel(writer, sheet_name='Key_Findings', index=False)
            
            logger.info(f"Executive summary generated: {output_path}")
            return output_path
            
        except Exception as e:
            raise ReportingError(f"Failed to generate executive summary: {str(e)}") from e
    
    def generate_detailed_matching_report(self, 
                                        matching_results: Dict[str, Any],
                                        output_path: Path) -> Path:
        """Generate detailed matching analysis Excel report."""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # All Matches Sheet
                all_matches = []
                for match_type in ['exact', 'fuzzy', 'tolerance']:
                    for match in matching_results['matches'][match_type]:
                        match_record = {
                            'Match_Type': match_type.title(),
                            'Confidence': match['confidence'],
                            'DF1_Index': match['df1_record']['index'],
                            'DF1_Date': match['df1_record']['date'],
                            'DF1_Amount': match['df1_record']['amount'],
                            'DF1_Description': match['df1_record']['description'],
                            'DF2_Index': match['df2_record']['index'],
                            'DF2_Date': match['df2_record']['date'],
                            'DF2_Amount': match['df2_record']['amount'],
                            'DF2_Description': match['df2_record']['description'],
                            'Date_Difference': match['match_criteria'].get('date_difference_days'),
                            'Amount_Difference': match['match_criteria'].get('amount_difference')
                        }
                        all_matches.append(match_record)
                
                if all_matches:
                    matches_df = pd.DataFrame(all_matches)
                    matches_df.to_excel(writer, sheet_name='All_Matches', index=False)
                
                # Match Type Breakdown
                for match_type in ['exact', 'fuzzy', 'tolerance']:
                    type_matches = [m for m in all_matches if m['Match_Type'].lower() == match_type]
                    if type_matches:
                        type_df = pd.DataFrame(type_matches)
                        sheet_name = f'{match_type.title()}_Matches'
                        type_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Confidence Analysis
                if all_matches:
                    confidence_analysis = self._analyze_confidence_distribution(all_matches)
                    conf_df = pd.DataFrame(confidence_analysis)
                    conf_df.to_excel(writer, sheet_name='Confidence_Analysis', index=False)
            
            logger.info(f"Detailed matching report generated: {output_path}")
            return output_path
            
        except Exception as e:
            raise ReportingError(f"Failed to generate detailed matching report: {str(e)}") from e
    
    def generate_exception_report(self, 
                                exception_results: Dict[str, Any],
                                output_path: Path) -> Path:
        """Generate exception analysis Excel report."""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Exception Summary
                summary_data = []
                for data_type in exception_results['categorized_exceptions']:
                    for category, exceptions in exception_results['categorized_exceptions'][data_type].items():
                        for exception in exceptions:
                            summary_data.append({
                                'Data_Source': data_type,
                                'Category': category,
                                'Index': exception['original_index'],
                                'Date': exception['date'],
                                'Amount': exception['amount'],
                                'Description': exception['description'],
                                'Confidence': exception['category_confidence'],
                                'Classification_Time': exception['classification_timestamp']
                            })
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Exception_Summary', index=False)
                
                # Category Analysis
                if 'statistics' in exception_results:
                    category_stats = []
                    for category, count in exception_results['statistics']['category_distribution'].items():
                        category_stats.append({
                            'Category': category,
                            'Count': count,
                            'Percentage': round(count / exception_results['statistics']['total_exceptions'] * 100, 1)
                        })
                    
                    if category_stats:
                        cat_df = pd.DataFrame(category_stats)
                        cat_df.to_excel(writer, sheet_name='Category_Analysis', index=False)
                
                # Resolution Suggestions
                if 'resolution_suggestions' in exception_results:
                    suggestions = exception_results['resolution_suggestions']
                    if suggestions:
                        sugg_df = pd.DataFrame(suggestions)
                        sugg_df.to_excel(writer, sheet_name='Resolution_Suggestions', index=False)
                
                # Aging Analysis
                if 'aging_analysis' in exception_results:
                    aging_data = []
                    for source, aging_info in exception_results['aging_analysis'].items():
                        if aging_info:
                            for bucket, count in aging_info.get('age_buckets', {}).items():
                                aging_data.append({
                                    'Data_Source': source,
                                    'Age_Bucket': bucket,
                                    'Count': count
                                })
                    
                    if aging_data:
                        aging_df = pd.DataFrame(aging_data)
                        aging_df.to_excel(writer, sheet_name='Aging_Analysis', index=False)
            
            logger.info(f"Exception report generated: {output_path}")
            return output_path
            
        except Exception as e:
            raise ReportingError(f"Failed to generate exception report: {str(e)}") from e
    
    def generate_visual_dashboard(self, 
                                matching_results: Dict[str, Any],
                                exception_results: Dict[str, Any],
                                output_path: Path) -> Path:
        """Generate HTML dashboard with interactive visualizations."""
        try:
            # Create HTML dashboard
            html_content = self._create_html_dashboard(matching_results, exception_results)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Visual dashboard generated: {output_path}")
            return output_path
            
        except Exception as e:
            raise ReportingError(f"Failed to generate visual dashboard: {str(e)}") from e
    
    def generate_charts(self, 
                       matching_results: Dict[str, Any],
                       exception_results: Dict[str, Any],
                       output_dir: Path) -> Dict[str, str]:
        """Generate individual chart files."""
        chart_files = {}
        
        try:
            # Match Type Distribution Chart
            match_chart_path = self._create_match_type_chart(matching_results, output_dir / "match_distribution.png")
            chart_files['match_distribution'] = str(match_chart_path)
            
            # Confidence Score Distribution
            confidence_chart_path = self._create_confidence_chart(matching_results, output_dir / "confidence_distribution.png")
            chart_files['confidence_distribution'] = str(confidence_chart_path)
            
            # Exception Category Chart
            if exception_results.get('statistics', {}).get('category_distribution'):
                exception_chart_path = self._create_exception_chart(exception_results, output_dir / "exception_categories.png")
                chart_files['exception_categories'] = str(exception_chart_path)
            
            # Aging Analysis Chart
            if exception_results.get('aging_analysis'):
                aging_chart_path = self._create_aging_chart(exception_results, output_dir / "aging_analysis.png")
                chart_files['aging_analysis'] = str(aging_chart_path)
            
            logger.info(f"Generated {len(chart_files)} chart files")
            return chart_files
            
        except Exception as e:
            raise ReportingError(f"Failed to generate charts: {str(e)}") from e
    
    def generate_audit_trail(self, 
                           matching_results: Dict[str, Any],
                           exception_results: Dict[str, Any],
                           output_path: Path) -> Path:
        """Generate comprehensive audit trail in JSON format."""
        try:
            audit_trail = {
                'report_metadata': {
                    'generated_timestamp': datetime.now().isoformat(),
                    'report_version': '1.0.0',
                    'generator': 'SmartRecon Reporting Engine'
                },
                'input_summary': {
                    'matching_session_id': matching_results.get('session_id'),
                    'exception_session_id': exception_results.get('session_id'),
                    'total_input_records': (
                        matching_results.get('input_stats', {}).get('df1_records', 0) +
                        matching_results.get('input_stats', {}).get('df2_records', 0)
                    )
                },
                'processing_summary': {
                    'matching_processing_time': matching_results.get('processing_time'),
                    'exception_processing_time': exception_results.get('processing_time'),
                    'total_matches_found': sum(len(matches) for matches in matching_results.get('matches', {}).values()),
                    'total_exceptions_processed': exception_results.get('statistics', {}).get('total_exceptions', 0)
                },
                'quality_metrics': {
                    'match_rate_df1': matching_results.get('statistics', {}).get('match_rates', {}).get('df1_match_rate', 0),
                    'match_rate_df2': matching_results.get('statistics', {}).get('match_rates', {}).get('df2_match_rate', 0),
                    'overall_match_rate': matching_results.get('statistics', {}).get('match_rates', {}).get('overall_match_rate', 0)
                },
                'detailed_results': {
                    'matching_results': matching_results,
                    'exception_results': exception_results
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(audit_trail, f, indent=2, default=str)
            
            logger.info(f"Audit trail generated: {output_path}")
            return output_path
            
        except Exception as e:
            raise ReportingError(f"Failed to generate audit trail: {str(e)}") from e
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize report templates."""
        return {
            'executive_summary': 'executive_summary_template.xlsx',
            'detailed_matching': 'detailed_matching_template.xlsx',
            'exception_analysis': 'exception_analysis_template.xlsx'
        }
    
    def _create_summary_statistics(self, matching_results: Dict, exception_results: Dict) -> Dict[str, Any]:
        """Create summary statistics for executive report."""
        stats = matching_results.get('statistics', {})
        
        return {
            'Total Input Records (DF1)': matching_results.get('input_stats', {}).get('df1_records', 0),
            'Total Input Records (DF2)': matching_results.get('input_stats', {}).get('df2_records', 0),
            'Total Matches Found': stats.get('total_matches', 0),
            'Exact Matches': len(matching_results.get('matches', {}).get('exact', [])),
            'Fuzzy Matches': len(matching_results.get('matches', {}).get('fuzzy', [])),
            'Tolerance Matches': len(matching_results.get('matches', {}).get('tolerance', [])),
            'Total Exceptions': exception_results.get('statistics', {}).get('total_exceptions', 0),
            'DF1 Match Rate (%)': stats.get('match_rates', {}).get('df1_match_rate', 0),
            'DF2 Match Rate (%)': stats.get('match_rates', {}).get('df2_match_rate', 0),
            'Overall Match Rate (%)': stats.get('match_rates', {}).get('overall_match_rate', 0),
            'Processing Time (seconds)': matching_results.get('processing_time', 0)
        }
    
    def _create_match_analysis(self, matching_results: Dict) -> List[Dict]:
        """Create match analysis data."""
        analysis = []
        
        for match_type in ['exact', 'fuzzy', 'tolerance']:
            matches = matching_results.get('matches', {}).get(match_type, [])
            
            if matches:
                confidences = [m['confidence'] for m in matches]
                analysis.append({
                    'Match_Type': match_type.title(),
                    'Count': len(matches),
                    'Avg_Confidence': round(np.mean(confidences), 3),
                    'Min_Confidence': round(min(confidences), 3),
                    'Max_Confidence': round(max(confidences), 3)
                })
        
        return analysis
    
    def _create_exception_overview(self, exception_results: Dict) -> List[Dict]:
        """Create exception overview data."""
        overview = []
        
        if 'statistics' in exception_results:
            category_dist = exception_results['statistics'].get('category_distribution', {})
            total = exception_results['statistics'].get('total_exceptions', 0)
            
            for category, count in category_dist.items():
                overview.append({
                    'Category': category.replace('_', ' ').title(),
                    'Count': count,
                    'Percentage': round(count / total * 100, 1) if total > 0 else 0
                })
        
        return overview
    
    def _create_key_findings(self, matching_results: Dict, exception_results: Dict) -> List[List[str]]:
        """Create key findings and recommendations."""
        findings = []
        
        # Match rate analysis
        overall_match_rate = matching_results.get('statistics', {}).get('match_rates', {}).get('overall_match_rate', 0)
        
        if overall_match_rate >= 90:
            findings.append([
                'High Match Rate Achieved',
                f'Overall match rate of {overall_match_rate}% indicates excellent data quality',
                'Continue current data management practices'
            ])
        elif overall_match_rate >= 70:
            findings.append([
                'Moderate Match Rate',
                f'Overall match rate of {overall_match_rate}% suggests room for improvement',
                'Review data standardization and timing processes'
            ])
        else:
            findings.append([
                'Low Match Rate Alert',
                f'Overall match rate of {overall_match_rate}% indicates significant issues',
                'Urgent review of data sources and reconciliation processes required'
            ])
        
        # Exception analysis
        total_exceptions = exception_results.get('statistics', {}).get('total_exceptions', 0)
        
        if total_exceptions > 100:
            findings.append([
                'High Exception Volume',
                f'{total_exceptions} unmatched items require attention',
                'Implement bulk resolution strategies and process improvements'
            ])
        
        # Auto-resolvable exceptions
        auto_resolvable = exception_results.get('statistics', {}).get('auto_resolvable_count', 0)
        
        if auto_resolvable > 0:
            findings.append([
                'Auto-Resolution Opportunity',
                f'{auto_resolvable} exceptions may be auto-resolvable',
                'Implement automated resolution workflows for efficiency gains'
            ])
        
        return findings
    
    def _analyze_confidence_distribution(self, matches: List[Dict]) -> List[Dict]:
        """Analyze confidence score distribution."""
        confidences = [m['Confidence'] for m in matches]
        
        distribution = []
        buckets = [
            ('Very High (0.95-1.0)', 0.95, 1.0),
            ('High (0.85-0.95)', 0.85, 0.95),
            ('Medium (0.70-0.85)', 0.70, 0.85),
            ('Low (0.50-0.70)', 0.50, 0.70),
            ('Very Low (<0.50)', 0.0, 0.50)
        ]
        
        for bucket_name, min_val, max_val in buckets:
            count = len([c for c in confidences if min_val <= c < max_val])
            distribution.append({
                'Confidence_Range': bucket_name,
                'Count': count,
                'Percentage': round(count / len(confidences) * 100, 1) if confidences else 0
            })
        
        return distribution
    
    def _create_match_type_chart(self, matching_results: Dict, output_path: Path) -> Path:
        """Create match type distribution chart."""
        match_counts = {
            'Exact': len(matching_results.get('matches', {}).get('exact', [])),
            'Fuzzy': len(matching_results.get('matches', {}).get('fuzzy', [])),
            'Tolerance': len(matching_results.get('matches', {}).get('tolerance', []))
        }
        
        plt.figure(figsize=self.chart_config['figure_size'])
        
        # Create pie chart
        colors = self.chart_config['color_palette'][:len(match_counts)]
        wedges, texts, autotexts = plt.pie(
            match_counts.values(), 
            labels=match_counts.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        plt.title('Match Type Distribution', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _create_confidence_chart(self, matching_results: Dict, output_path: Path) -> Path:
        """Create confidence score distribution chart."""
        all_matches = []
        for match_type in ['exact', 'fuzzy', 'tolerance']:
            all_matches.extend(matching_results.get('matches', {}).get(match_type, []))
        
        if not all_matches:
            # Create empty chart
            plt.figure(figsize=self.chart_config['figure_size'])
            plt.text(0.5, 0.5, 'No matches found', ha='center', va='center', fontsize=16)
            plt.axis('off')
            plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            return output_path
        
        confidences = [m['confidence'] for m in all_matches]
        
        plt.figure(figsize=self.chart_config['figure_size'])
        
        # Create histogram
        plt.hist(confidences, bins=20, alpha=0.7, color=self.chart_config['color_palette'][0], edgecolor='black')
        plt.xlabel('Confidence Score', fontsize=12)
        plt.ylabel('Number of Matches', fontsize=12)
        plt.title('Match Confidence Score Distribution', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _create_exception_chart(self, exception_results: Dict, output_path: Path) -> Path:
        """Create exception category distribution chart."""
        category_dist = exception_results.get('statistics', {}).get('category_distribution', {})
        
        if not category_dist:
            # Create empty chart
            plt.figure(figsize=self.chart_config['figure_size'])
            plt.text(0.5, 0.5, 'No exceptions found', ha='center', va='center', fontsize=16)
            plt.axis('off')
            plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            return output_path
        
        categories = [cat.replace('_', ' ').title() for cat in category_dist.keys()]
        counts = list(category_dist.values())
        
        plt.figure(figsize=self.chart_config['figure_size'])
        
        # Create horizontal bar chart
        colors = self.chart_config['color_palette'] * (len(categories) // len(self.chart_config['color_palette']) + 1)
        bars = plt.barh(categories, counts, color=colors[:len(categories)])
        
        plt.xlabel('Number of Exceptions', fontsize=12)
        plt.title('Exception Category Distribution', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _create_aging_chart(self, exception_results: Dict, output_path: Path) -> Path:
        """Create aging analysis chart."""
        aging_data = exception_results.get('aging_analysis', {})
        
        if not aging_data:
            # Create empty chart
            plt.figure(figsize=self.chart_config['figure_size'])
            plt.text(0.5, 0.5, 'No aging data available', ha='center', va='center', fontsize=16)
            plt.axis('off')
            plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            return output_path
        
        # Combine aging buckets from both data sources
        combined_buckets = defaultdict(int)
        
        for source, aging_info in aging_data.items():
            if aging_info and 'age_buckets' in aging_info:
                for bucket, count in aging_info['age_buckets'].items():
                    combined_buckets[bucket] += count
        
        if not combined_buckets:
            # Create empty chart
            plt.figure(figsize=self.chart_config['figure_size'])
            plt.text(0.5, 0.5, 'No aging buckets data', ha='center', va='center', fontsize=16)
            plt.axis('off')
            plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            return output_path
        
        buckets = list(combined_buckets.keys())
        counts = list(combined_buckets.values())
        
        plt.figure(figsize=self.chart_config['figure_size'])
        
        # Create bar chart
        colors = self.chart_config['color_palette'] * (len(buckets) // len(self.chart_config['color_palette']) + 1)
        bars = plt.bar(buckets, counts, color=colors[:len(buckets)])
        
        plt.xlabel('Age Buckets', fontsize=12)
        plt.ylabel('Number of Exceptions', fontsize=12)
        plt.title('Exception Aging Analysis', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', 
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _create_html_dashboard(self, matching_results: Dict, exception_results: Dict) -> str:
        """Create HTML dashboard content."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SmartRecon Analytics Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .header { background-color: #2E86AB; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .metric-card { display: inline-block; background-color: #f8f9fa; padding: 15px; margin: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                .metric-value { font-size: 2em; font-weight: bold; color: #2E86AB; }
                .metric-label { font-size: 0.9em; color: #666; }
                .section { margin: 20px 0; }
                .section h2 { color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 5px; }
                table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SmartRecon Analytics Dashboard</h1>
                    <p>Generated on {timestamp}</p>
                </div>
                
                <div class="section">
                    <h2>Key Metrics</h2>
                    {metrics_html}
                </div>
                
                <div class="section">
                    <h2>Match Analysis</h2>
                    {match_analysis_html}
                </div>
                
                <div class="section">
                    <h2>Exception Summary</h2>
                    {exception_summary_html}
                </div>
            </div>
        </body>
        </html>
        """
        
        # Generate metrics HTML
        stats = matching_results.get('statistics', {})
        metrics_html = f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('total_matches', 0)}</div>
            <div class="metric-label">Total Matches</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{stats.get('match_rates', {}).get('overall_match_rate', 0)}%</div>
            <div class="metric-label">Match Rate</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{exception_results.get('statistics', {}).get('total_exceptions', 0)}</div>
            <div class="metric-label">Total Exceptions</div>
        </div>
        """
        
        # Generate match analysis HTML
        match_analysis_html = """
        <table>
            <tr><th>Match Type</th><th>Count</th><th>Percentage</th></tr>
        """
        
        total_matches = stats.get('total_matches', 0)
        for match_type in ['exact', 'fuzzy', 'tolerance']:
            count = len(matching_results.get('matches', {}).get(match_type, []))
            percentage = round(count / total_matches * 100, 1) if total_matches > 0 else 0
            match_analysis_html += f"<tr><td>{match_type.title()}</td><td>{count}</td><td>{percentage}%</td></tr>"
        
        match_analysis_html += "</table>"
        
        # Generate exception summary HTML
        exception_summary_html = """
        <table>
            <tr><th>Category</th><th>Count</th><th>Percentage</th></tr>
        """
        
        category_dist = exception_results.get('statistics', {}).get('category_distribution', {})
        total_exceptions = exception_results.get('statistics', {}).get('total_exceptions', 0)
        
        for category, count in category_dist.items():
            percentage = round(count / total_exceptions * 100, 1) if total_exceptions > 0 else 0
            exception_summary_html += f"<tr><td>{category.replace('_', ' ').title()}</td><td>{count}</td><td>{percentage}%</td></tr>"
        
        exception_summary_html += "</table>"
        
        return html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metrics_html=metrics_html,
            match_analysis_html=match_analysis_html,
            exception_summary_html=exception_summary_html
        )
