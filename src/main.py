"""
Main entry point for SmartRecon application.

This module provides the command-line interface and orchestrates the 
reconciliation workflow.
"""

import click
import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import Config
from .modules.data_ingestion import DataIngestion
from .modules.data_cleaning import DataCleaner
from .modules.matching_engine import MatchingEngine
from .modules.exact_matching_engine import ExactMatchingEngine
from .modules.exception_handler import ExceptionHandler
from .modules.reporting import ReportGenerator
from .modules.basic_reporting import BasicReporter
from .utils.logger import setup_logger
from .utils.exceptions import SmartReconException


@click.group()
@click.option('--config', 
              default='config/default_config.json',
              help='Configuration file path')
@click.option('--verbose', 
              is_flag=True, 
              help='Enable verbose output')
@click.option('--log-level',
              default='INFO',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
              help='Set logging level')
@click.pass_context
def main(ctx, config: str, verbose: bool, log_level: str):
    """
    SmartRecon: Intelligent Financial Reconciliation Assistant
    
    Automate financial reconciliation between GL entries and external sources.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Setup logging
    log_level_num = getattr(logging, log_level.upper())
    logger = setup_logger('smartrecon', log_level_num)
    
    # Load configuration
    try:
        ctx.obj['config'] = Config(config)
        ctx.obj['logger'] = logger
        
        if verbose:
            logger.info(f"SmartRecon v1.0.0 - Configuration loaded from: {config}")
            logger.info(f"Log level set to: {log_level}")
            
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        ctx.exit(1)


@main.command()
@click.option('--gl-file', 
              required=True,
              type=click.Path(exists=True),
              help='General Ledger data file path (CSV or Excel)')
@click.option('--bank-file',
              required=True, 
              type=click.Path(exists=True),
              help='Bank statement data file path (CSV or Excel)')
@click.option('--output-dir',
              default='output',
              help='Output directory for reconciliation results')
@click.option('--config-override',
              help='JSON string to override specific configuration values')
@click.pass_context
def reconcile(ctx, gl_file: str, bank_file: str, output_dir: str, config_override: Optional[str]):
    """
    Run the complete reconciliation process between GL and bank data.
    
    This command orchestrates the full reconciliation workflow:
    1. Data ingestion and validation
    2. Data cleaning and standardization  
    3. Transaction matching (exact and fuzzy)
    4. Exception handling and categorization
    5. Report generation and export
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    try:
        logger.info("Starting SmartRecon reconciliation process...")
        logger.info(f"GL File: {gl_file}")
        logger.info(f"Bank File: {bank_file}")
        logger.info(f"Output Directory: {output_dir}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Run reconciliation workflow
        matches, exceptions, reports = run_reconciliation_workflow(
            gl_file=gl_file,
            bank_file=bank_file,
            config=config,
            output_dir=output_dir,
            logger=logger
        )
        
        logger.info("Reconciliation process completed successfully!")
        logger.info(f"Matches found: {len(matches)}")
        logger.info(f"Exceptions identified: {len(exceptions)}")
        logger.info(f"Reports generated in: {output_dir}")
        
    except SmartReconException as e:
        logger.error(f"Reconciliation failed: {e}")
        ctx.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during reconciliation: {e}")
        ctx.exit(1)


@main.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--file-type',
              type=click.Choice(['gl', 'bank', 'auto']),
              default='auto',
              help='Specify file type for validation')
@click.pass_context
def validate(ctx, filepath: str, file_type: str):
    """
    Validate data file format and structure.
    
    Checks if the specified file meets SmartRecon requirements for
    data format, required columns, and data quality.
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    try:
        logger.info(f"Validating file: {filepath}")
        
        # Initialize data ingestion module
        ingestion = DataIngestion(config)
        
        # Perform validation
        validation_result = ingestion.validate_file(filepath)
        
        if validation_result['is_valid']:
            logger.info("✅ File validation successful!")
            logger.info(f"File type: {validation_result['file_type']}")
            logger.info(f"File size: {validation_result['file_size']} bytes")
            
            if validation_result['warnings']:
                logger.warning("Validation warnings:")
                for warning in validation_result['warnings']:
                    logger.warning(f"  - {warning}")
        else:
            logger.error("❌ File validation failed!")
            for error in validation_result['errors']:
                logger.error(f"  - {error}")
                
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        ctx.exit(1)


@main.command()
@click.pass_context
def version(ctx):
    """Display SmartRecon version information."""
    logger = ctx.obj['logger']
    logger.info("SmartRecon v1.0.0")
    logger.info("Intelligent Financial Reconciliation Assistant")


@main.command()
@click.argument('gl_file', type=click.Path(exists=True))
@click.argument('bank_file', type=click.Path(exists=True))
@click.option('--output-dir',
              default='output',
              help='Output directory for results')
@click.option('--strategies',
              multiple=True,
              type=click.Choice(['reference_exact', 'amount_date_exact', 'amount_date_desc', 'composite_key', 'amount_tolerance']),
              help='Exact matching strategies to use (can specify multiple)')
@click.option('--amount-tolerance',
              default=0.01,
              type=float,
              help='Amount tolerance for exact matching')
@click.option('--export-format',
              default='excel',
              type=click.Choice(['excel', 'csv', 'both']),
              help='Export format for results')
@click.pass_context
def exact_match(ctx, gl_file: str, bank_file: str, output_dir: str, 
                strategies: tuple, amount_tolerance: float, export_format: str):
    """
    Perform exact matching reconciliation between GL and bank files.
    
    This command uses high-performance exact matching algorithms to reconcile
    financial transactions with multiple matching strategies.
    
    GL_FILE: Path to General Ledger data file
    BANK_FILE: Path to Bank statement data file
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    try:
        logger.info("Starting exact matching reconciliation")
        logger.info(f"GL file: {gl_file}")
        logger.info(f"Bank file: {bank_file}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Load and validate data files
        logger.info("Loading data files...")
        
        # Initialize data ingestion
        ingestion = DataIngestion(config)
        
        # Load GL data
        gl_result = ingestion.load_file(gl_file, file_type='gl')
        gl_data = gl_result['data']
        logger.info(f"Loaded {len(gl_data)} GL records")
        
        # Load bank data
        bank_result = ingestion.load_file(bank_file, file_type='bank')
        bank_data = bank_result['data']
        logger.info(f"Loaded {len(bank_data)} bank records")
        
        # Step 2: Clean and prepare data
        logger.info("Cleaning and preparing data...")
        
        cleaner = DataCleaner(config)
        gl_cleaned = cleaner.clean_data(gl_data)['cleaned_data']
        bank_cleaned = cleaner.clean_data(bank_data)['cleaned_data']
        
        # Step 3: Configure exact matching engine
        exact_engine = ExactMatchingEngine(config)
        
        # Update configuration with CLI parameters
        if amount_tolerance != 0.01:
            exact_engine.params['amount_tolerance'] = amount_tolerance
        
        # Step 4: Perform exact matching reconciliation
        logger.info("Performing exact matching reconciliation...")
        
        # Use specified strategies or default
        match_strategies = list(strategies) if strategies else None
        
        reconciliation_results = exact_engine.reconcile_exact_matches(
            gl_cleaned, bank_cleaned, match_strategies
        )
        
        # Step 5: Generate reports and export results
        logger.info("Generating reports...")
        
        # Generate summary report
        stats = reconciliation_results['match_statistics']
        performance = reconciliation_results['performance_metrics']
        
        logger.info("=== EXACT MATCHING RECONCILIATION RESULTS ===")
        logger.info(f"Total Exact Matches: {stats['total_exact_matches']}")
        logger.info(f"GL Match Rate: {stats['gl_match_rate']:.1f}%")
        logger.info(f"Bank Match Rate: {stats['bank_match_rate']:.1f}%")
        logger.info(f"Overall Match Rate: {stats['overall_match_rate']:.1f}%")
        logger.info(f"Processing Time: {performance['total_processing_time']:.2f} seconds")
        logger.info(f"Records/Second: {performance['records_per_second']:.0f}")
        
        # Strategy breakdown
        logger.info("\n=== STRATEGY BREAKDOWN ===")
        for strategy, count in stats['strategy_breakdown'].items():
            logger.info(f"{strategy}: {count} matches")
        
        # Confidence distribution
        logger.info("\n=== CONFIDENCE DISTRIBUTION ===")
        conf_dist = stats['confidence_distribution']
        for level, count in conf_dist.items():
            logger.info(f"{level.title()}: {count} matches")
        
        # Export results
        logger.info("\n=== EXPORTING RESULTS ===")
        
        # Export matches
        matches_df = exact_engine.export_matches_to_dataframe()
        if not matches_df.empty:
            if export_format in ['excel', 'both']:
                matches_excel_path = os.path.join(output_dir, 'exact_matches.xlsx')
                matches_df.to_excel(matches_excel_path, index=False)
                logger.info(f"Exact matches exported to: {matches_excel_path}")
            
            if export_format in ['csv', 'both']:
                matches_csv_path = os.path.join(output_dir, 'exact_matches.csv')
                matches_df.to_csv(matches_csv_path, index=False)
                logger.info(f"Exact matches exported to: {matches_csv_path}")
        
        # Export unmatched records
        unmatched = exact_engine.get_unmatched_records()
        
        if not unmatched['gl'].empty:
            if export_format in ['excel', 'both']:
                gl_unmatched_path = os.path.join(output_dir, 'unmatched_gl.xlsx')
                unmatched['gl'].to_excel(gl_unmatched_path, index=False)
                logger.info(f"Unmatched GL records exported to: {gl_unmatched_path}")
            
            if export_format in ['csv', 'both']:
                gl_unmatched_path = os.path.join(output_dir, 'unmatched_gl.csv')
                unmatched['gl'].to_csv(gl_unmatched_path, index=False)
                logger.info(f"Unmatched GL records exported to: {gl_unmatched_path}")
        
        if not unmatched['bank'].empty:
            if export_format in ['excel', 'both']:
                bank_unmatched_path = os.path.join(output_dir, 'unmatched_bank.xlsx')
                unmatched['bank'].to_excel(bank_unmatched_path, index=False)
                logger.info(f"Unmatched bank records exported to: {bank_unmatched_path}")
            
            if export_format in ['csv', 'both']:
                bank_unmatched_path = os.path.join(output_dir, 'unmatched_bank.csv')
                unmatched['bank'].to_csv(bank_unmatched_path, index=False)
                logger.info(f"Unmatched bank records exported to: {bank_unmatched_path}")
        
        # Export reconciliation summary
        import json
        summary_path = os.path.join(output_dir, 'reconciliation_summary.json')
        with open(summary_path, 'w') as f:
            # Create JSON-serializable summary
            summary = {
                'session_id': reconciliation_results['session_id'],
                'gl_count': reconciliation_results['gl_count'],
                'bank_count': reconciliation_results['bank_count'],
                'strategies_used': reconciliation_results['strategies_used'],
                'match_statistics': stats,
                'performance_metrics': {
                    'total_processing_time': performance['total_processing_time'],
                    'records_per_second': performance['records_per_second'],
                    'matches_per_second': performance['matches_per_second']
                },
                'validation_results': reconciliation_results['validation_results']
            }
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Reconciliation summary exported to: {summary_path}")
        
        logger.info("\n✅ Exact matching reconciliation completed successfully!")
        
        # Display final summary
        unmatched_gl_count = len(unmatched['gl'])
        unmatched_bank_count = len(unmatched['bank'])
        
        if unmatched_gl_count > 0 or unmatched_bank_count > 0:
            logger.info(f"\n⚠️  {unmatched_gl_count} GL records and {unmatched_bank_count} bank records remain unmatched")
            logger.info("Consider using fuzzy matching or manual review for remaining items")
        
    except Exception as e:
        logger.error(f"Exact matching reconciliation failed: {e}")
        ctx.exit(1)


def run_reconciliation_workflow(gl_file: str, bank_file: str, config: Config, 
                               output_dir: str, logger) -> tuple:
    """
    Execute the complete reconciliation workflow.
    
    Args:
        gl_file: Path to GL data file
        bank_file: Path to bank data file  
        config: Configuration object
        output_dir: Output directory path
        logger: Logger instance
        
    Returns:
        Tuple of (matching_results, exception_results, report_files)
    """
    try:
        # Initialize modules
        ingestion = DataIngestion(config)
        cleaner = DataCleaner(config)
        matcher = MatchingEngine(config)
        exception_handler = ExceptionHandler(config)
        reporter = ReportGenerator(config)
        
        # Phase 1: Data Ingestion
        logger.info("Phase 1: Data Ingestion")
        logger.info("Loading GL data...")
        gl_data = ingestion.load_file(gl_file, file_type='gl')
        logger.info(f"Loaded {len(gl_data)} GL records")
        
        logger.info("Loading bank data...")
        bank_data = ingestion.load_file(bank_file, file_type='bank')
        logger.info(f"Loaded {len(bank_data)} bank records")
        
        # Phase 2: Data Cleaning
        logger.info("Phase 2: Data Cleaning and Standardization")
        gl_clean = cleaner.clean_data(gl_data, data_type='gl')
        logger.info(f"Cleaned GL data: {len(gl_clean)} records")
        
        bank_clean = cleaner.clean_data(bank_data, data_type='bank')
        logger.info(f"Cleaned bank data: {len(bank_clean)} records")
        
        # Phase 3: Matching
        logger.info("Phase 3: Transaction Matching")
        matching_results = matcher.run_matching(gl_clean, bank_clean, 'gl', 'bank')
        
        total_matches = sum(len(matches) for matches in matching_results['matches'].values())
        logger.info(f"Matching complete: {total_matches} matches found")
        
        # Phase 4: Exception Handling
        logger.info("Phase 4: Exception Processing")
        exception_results = exception_handler.process_exceptions(
            matching_results['unmatched']['df1'],
            matching_results['unmatched']['df2'],
            'gl',
            'bank'
        )
        
        total_exceptions = exception_results['statistics']['total_exceptions']
        logger.info(f"Exception processing complete: {total_exceptions} exceptions categorized")
        
        # Phase 5: Reporting
        logger.info("Phase 5: Report Generation")
        report_files = reporter.generate_all_reports(
            matching_results,
            exception_results,
            output_dir
        )
        
        logger.info(f"Reports generated: {len(report_files)} files created")
        
        return matching_results, exception_results, report_files
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        raise


@main.command()
@click.argument('data_files', nargs=-1, type=click.Path(exists=True))
@click.option('--output-dir',
              default='reports',
              help='Output directory for reports')
@click.option('--report-type',
              default='ingestion',
              type=click.Choice(['ingestion', 'quality', 'summary']),
              help='Type of basic report to generate')
@click.option('--include-charts',
              is_flag=True,
              default=True,
              help='Include charts and visualizations')
@click.option('--export-format',
              default='all',
              type=click.Choice(['excel', 'html', 'csv', 'all']),
              help='Export format for reports')
@click.pass_context
def basic_report(ctx, data_files: tuple, output_dir: str, report_type: str, 
                include_charts: bool, export_format: str):
    """
    Generate basic reports for data ingestion and quality analysis.
    
    This command creates simple, focused reports for data analysis and quality assessment.
    
    DATA_FILES: One or more data files to analyze and report on
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    try:
        if not data_files:
            logger.error("No data files provided. Please specify at least one file.")
            ctx.exit(1)
        
        logger.info(f"Generating {report_type} report for {len(data_files)} files")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        ingestion = DataIngestion(config)
        basic_reporter = BasicReporter(config)
        
        # Update reporter configuration
        if export_format != 'all':
            basic_reporter.params['excel_export'] = export_format in ['excel', 'all']
            basic_reporter.params['html_export'] = export_format in ['html', 'all']
            basic_reporter.params['csv_export'] = export_format in ['csv', 'all']
        
        basic_reporter.params['include_charts'] = include_charts
        
        if report_type == 'ingestion':
            # Generate data ingestion report
            logger.info("Processing files for ingestion report...")
            
            ingestion_results = []
            for file_path in data_files:
                logger.info(f"Processing file: {file_path}")
                try:
                    # Detect file type
                    file_type = 'auto'
                    if 'gl' in str(file_path).lower():
                        file_type = 'gl'
                    elif 'bank' in str(file_path).lower():
                        file_type = 'bank'
                    
                    # Load and analyze file
                    result = ingestion.load_file(file_path, file_type=file_type)
                    ingestion_results.append(result)
                    
                    logger.info(f"✅ Processed {result['processing_stats']['rows_loaded']} rows from {os.path.basename(file_path)}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to process {file_path}: {e}")
                    # Add error result
                    ingestion_results.append({
                        'file_info': {'name': os.path.basename(file_path)},
                        'processing_stats': {'rows_loaded': 0, 'columns_loaded': 0, 'processing_time_seconds': 0},
                        'data_quality': {'overall_score': 0},
                        'warnings': [],
                        'errors': [str(e)]
                    })
            
            # Generate ingestion report
            report_result = basic_reporter.generate_ingestion_report(ingestion_results, output_dir)
            
            # Display summary
            report_data = report_result['report_data']
            stats = report_data['overall_statistics']
            
            logger.info("\n=== DATA INGESTION REPORT SUMMARY ===")
            logger.info(f"Files Processed: {stats['total_files_processed']}")
            logger.info(f"Total Rows Loaded: {stats['total_rows_loaded']:,}")
            logger.info(f"Average Quality Score: {stats['average_data_quality_score']:.2f}")
            logger.info(f"Warnings: {stats['total_warnings']}")
            logger.info(f"Errors: {stats['total_errors']}")
            
            # Quality summary
            if report_data.get('data_quality_summary'):
                quality = report_data['data_quality_summary']
                logger.info(f"\n=== DATA QUALITY SUMMARY ===")
                logger.info(f"Highest Quality Score: {quality['highest_quality_score']:.2f}")
                logger.info(f"Lowest Quality Score: {quality['lowest_quality_score']:.2f}")
                logger.info(f"Files Above Threshold (0.8): {quality['files_above_threshold']}")
                logger.info(f"Files Needing Attention: {quality['files_needing_attention']}")
            
        elif report_type == 'quality':
            # Generate focused data quality report
            logger.info("Generating data quality assessment...")
            
            quality_results = []
            for file_path in data_files:
                logger.info(f"Analyzing quality for: {file_path}")
                try:
                    result = ingestion.load_file(file_path, file_type='auto')
                    quality_results.append(result)
                except Exception as e:
                    logger.error(f"Failed to analyze {file_path}: {e}")
            
            if quality_results:
                report_result = basic_reporter.generate_ingestion_report(quality_results, output_dir)
                logger.info("✅ Data quality report generated successfully")
            else:
                logger.error("No files could be processed for quality analysis")
                ctx.exit(1)
        
        elif report_type == 'summary':
            # Generate high-level summary report
            logger.info("Generating summary report...")
            
            summary_data = []
            total_rows = 0
            total_files = 0
            
            for file_path in data_files:
                try:
                    # Quick validation without full loading
                    validation = ingestion.validate_file(file_path)
                    if validation['is_valid']:
                        total_files += 1
                        # For summary, just get basic info
                        summary_data.append({
                            'file_name': os.path.basename(file_path),
                            'file_type': validation.get('file_type', 'unknown'),
                            'file_size': validation.get('file_size', 0),
                            'estimated_rows': validation.get('row_count', 0) * 100,  # Estimate from sample
                            'columns': validation.get('column_count', 0)
                        })
                        total_rows += validation.get('row_count', 0) * 100
                    
                except Exception as e:
                    logger.warning(f"Could not summarize {file_path}: {e}")
            
            # Create simple summary output
            summary_file = os.path.join(output_dir, 'file_summary.txt')
            with open(summary_file, 'w') as f:
                f.write("SmartRecon File Summary Report\n")
                f.write("=" * 40 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Total Files: {total_files}\n")
                f.write(f"Estimated Total Rows: {total_rows:,}\n\n")
                f.write("File Details:\n")
                f.write("-" * 40 + "\n")
                
                for item in summary_data:
                    f.write(f"File: {item['file_name']}\n")
                    f.write(f"  Type: {item['file_type']}\n")
                    f.write(f"  Size: {item['file_size']:,} bytes\n")
                    f.write(f"  Columns: {item['columns']}\n")
                    f.write(f"  Est. Rows: {item['estimated_rows']:,}\n\n")
            
            logger.info(f"Summary report saved to: {summary_file}")
        
        # Display output files
        if 'report_result' in locals() and report_result.get('output_files'):
            logger.info(f"\n=== OUTPUT FILES ===")
            for file_path in report_result['output_files']:
                logger.info(f"📄 {file_path}")
        
        logger.info(f"\n✅ Basic {report_type} report completed successfully!")
        logger.info(f"📁 Reports saved to: {output_dir}")
        
    except Exception as e:
        logger.error(f"Basic reporting failed: {e}")
        ctx.exit(1)


if __name__ == '__main__':
    main()
