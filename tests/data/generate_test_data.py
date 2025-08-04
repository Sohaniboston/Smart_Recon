#!/usr/bin/env python3
"""
Test data generation for SmartRecon testing.

Creates various test datasets for comprehensive testing:
- Clean data for basic testing
- Corrupted data for error handling tests
- Large datasets for performance testing
- Edge case datasets

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json


def create_basic_test_data():
    """Create basic test datasets for GL and Bank data."""
    
    # Basic GL data
    gl_data = {
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
        'Amount': [1000.00, -50.25, 750.50, 2000.00, -25.00],
        'Description': ['Customer payment A', 'Bank service charge', 'Customer deposit B', 
                      'Large customer payment', 'Monthly fee'],
        'Reference': ['PAY001', 'SVC001', 'DEP001', 'PAY002', 'FEE001'],
        'Account': ['12345'] * 5
    }
    
    # Basic Bank data (some matching records)
    bank_data = {
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-06', '2025-01-07'],
        'Amount': [1000.00, -50.25, 750.50, 500.00, -30.00],
        'Description': ['Payment from customer A', 'Service charge', 'Deposit B', 
                      'Different payment', 'Other fee'],
        'Reference': ['PAY001', 'SVC001', 'DEP001', 'PAY003', 'FEE002'],
        'Account': ['67890'] * 5
    }
    
    return pd.DataFrame(gl_data), pd.DataFrame(bank_data)


def create_fuzzy_matching_test_data():
    """Create test data specifically for fuzzy matching scenarios."""
    
    # GL data with variations
    gl_data = {
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04'],
        'Amount': [105.50, 75.00, 250.25, 999.99],
        'Description': ['Payment received from client ABC Corp', 
                      'Bank service charge fee',
                      'Customer deposit transfer',
                      'Wire transfer payment'],
        'Reference': ['PAY001', 'SVC002', 'DEP003', 'WIRE004']
    }
    
    # Bank data with similar but not exact descriptions
    bank_data = {
        'Date': ['2025-01-01', '2025-01-03', '2025-01-04', '2025-01-05'],
        'Amount': [105.00, 75.50, 250.00, 1000.00],
        'Description': ['Payment from ABC Corp client', 
                      'Service charge bank fee',
                      'Deposit transfer customer',
                      'Electronic wire payment'],
        'Reference': ['PAY-001', 'SVC-002', 'DEP-003', 'WIRE-004']
    }
    
    return pd.DataFrame(gl_data), pd.DataFrame(bank_data)


def create_corrupted_test_data():
    """Create test data with various data quality issues."""
    
    # Data with missing values, wrong formats, etc.
    corrupted_data = {
        'Date': ['2025-01-01', 'invalid_date', '2025-01-03', None, '01/05/2025'],
        'Amount': ['100.50', 'invalid_amount', '', None, '$250.75'],
        'Description': ['Valid description', '', '   Whitespace   ', None, 'Normal desc'],
        'Reference': ['REF001', '', 'REF003', None, 'REF005'],
        'Account': ['12345', '12345', '', None, '67890']
    }
    
    return pd.DataFrame(corrupted_data)


def create_large_test_dataset(num_records=1000):
    """Create large test dataset for performance testing."""
    
    np.random.seed(42)  # For reproducible results
    
    # Generate dates
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_records)]
    
    # Generate amounts
    amounts = np.random.uniform(-1000, 5000, num_records)
    amounts = np.round(amounts, 2)
    
    # Generate descriptions
    desc_templates = [
        'Payment from customer {}',
        'Deposit transaction {}',
        'Wire transfer {}',
        'Service charge {}',
        'ATM withdrawal {}',
        'Check payment {}',
        'Online transfer {}',
        'Card payment {}'
    ]
    
    descriptions = [
        np.random.choice(desc_templates).format(i) 
        for i in range(num_records)
    ]
    
    # Generate references
    references = [f'REF{i:06d}' for i in range(num_records)]
    
    # GL data
    gl_data = {
        'Date': [d.strftime('%Y-%m-%d') for d in dates],
        'Amount': amounts,
        'Description': descriptions,
        'Reference': references,
        'Account': ['GL' + str(np.random.randint(10000, 99999)) for _ in range(num_records)]
    }
    
    # Bank data (with some matching records and some not)
    # Create 70% matching records, 30% unique
    matching_count = int(num_records * 0.7)
    
    bank_dates = dates[:matching_count] + [
        start_date + timedelta(days=np.random.randint(0, 365)) 
        for _ in range(num_records - matching_count)
    ]
    
    bank_amounts = list(amounts[:matching_count]) + list(
        np.round(np.random.uniform(-1000, 5000, num_records - matching_count), 2)
    )
    
    bank_descriptions = descriptions[:matching_count] + [
        f'Bank transaction {i}' for i in range(num_records - matching_count)
    ]
    
    bank_references = references[:matching_count] + [
        f'BNK{i:06d}' for i in range(num_records - matching_count)
    ]
    
    bank_data = {
        'Date': [d.strftime('%Y-%m-%d') for d in bank_dates],
        'Amount': bank_amounts,
        'Description': bank_descriptions,
        'Reference': bank_references,
        'Account': ['BNK' + str(np.random.randint(10000, 99999)) for _ in range(num_records)]
    }
    
    return pd.DataFrame(gl_data), pd.DataFrame(bank_data)


def create_edge_case_test_data():
    """Create test data for edge cases."""
    
    # Edge cases: zero amounts, very large amounts, duplicate data, etc.
    edge_data = {
        'Date': ['2025-01-01', '2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04'],
        'Amount': [0.00, 0.00, 999999999.99, -999999999.99, 0.01],
        'Description': ['Zero amount transaction', 'Duplicate zero amount', 
                      'Very large positive amount', 'Very large negative amount',
                      'Very small amount'],
        'Reference': ['ZERO001', 'ZERO001', 'LARGE001', 'LARGE002', 'SMALL001'],
        'Account': ['12345'] * 5
    }
    
    return pd.DataFrame(edge_data)


def save_test_datasets(output_dir):
    """Save all test datasets to files."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Basic test data
    gl_basic, bank_basic = create_basic_test_data()
    gl_basic.to_csv(os.path.join(output_dir, 'gl_basic.csv'), index=False)
    bank_basic.to_csv(os.path.join(output_dir, 'bank_basic.csv'), index=False)
    
    # Excel versions
    gl_basic.to_excel(os.path.join(output_dir, 'gl_basic.xlsx'), index=False)
    bank_basic.to_excel(os.path.join(output_dir, 'bank_basic.xlsx'), index=False)
    
    # Fuzzy matching test data
    gl_fuzzy, bank_fuzzy = create_fuzzy_matching_test_data()
    gl_fuzzy.to_csv(os.path.join(output_dir, 'gl_fuzzy.csv'), index=False)
    bank_fuzzy.to_csv(os.path.join(output_dir, 'bank_fuzzy.csv'), index=False)
    
    # Corrupted data
    corrupted = create_corrupted_test_data()
    corrupted.to_csv(os.path.join(output_dir, 'corrupted_data.csv'), index=False)
    
    # Large datasets
    gl_large, bank_large = create_large_test_dataset(1000)
    gl_large.to_csv(os.path.join(output_dir, 'gl_large.csv'), index=False)
    bank_large.to_csv(os.path.join(output_dir, 'bank_large.csv'), index=False)
    
    # Edge cases
    edge_data = create_edge_case_test_data()
    edge_data.to_csv(os.path.join(output_dir, 'edge_cases.csv'), index=False)
    
    # Create metadata file
    metadata = {
        'created_date': datetime.now().isoformat(),
        'datasets': {
            'basic': {
                'gl_records': len(gl_basic),
                'bank_records': len(bank_basic),
                'description': 'Basic test data with exact matches'
            },
            'fuzzy': {
                'gl_records': len(gl_fuzzy),
                'bank_records': len(bank_fuzzy),
                'description': 'Test data for fuzzy matching scenarios'
            },
            'corrupted': {
                'records': len(corrupted),
                'description': 'Data with quality issues for error handling tests'
            },
            'large': {
                'gl_records': len(gl_large),
                'bank_records': len(bank_large),
                'description': 'Large dataset for performance testing'
            },
            'edge_cases': {
                'records': len(edge_data),
                'description': 'Edge cases and extreme values'
            }
        }
    }
    
    with open(os.path.join(output_dir, 'test_data_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Test datasets created in: {output_dir}")
    print(f"Generated {len(metadata['datasets'])} different test datasets")
    return metadata


if __name__ == '__main__':
    # Create test data in the tests/data directory
    current_dir = os.path.dirname(__file__)
    test_data_dir = os.path.join(current_dir, '..', 'data')
    
    metadata = save_test_datasets(test_data_dir)
    
    print("\nTest Data Summary:")
    for dataset_name, info in metadata['datasets'].items():
        print(f"  {dataset_name}: {info['description']}")
        if 'gl_records' in info:
            print(f"    GL records: {info['gl_records']}, Bank records: {info['bank_records']}")
        else:
            print(f"    Records: {info['records']}")
