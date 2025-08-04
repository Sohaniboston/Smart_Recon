#!/usr/bin/env python3
"""
Unit tests for Configuration module.

Tests cover:
- Configuration loading
- Parameter validation
- Default values
- Configuration updates
- Error handling

Author: SmartRecon Development Team
Date: 2025-07-28
"""

import unittest
import json
import os
import tempfile
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.config import Config
from src.utils.exceptions import ConfigurationError


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample configuration data
        self.sample_config = {
            "data_ingestion": {
                "supported_formats": ["csv", "xlsx"],
                "encoding_detection": True,
                "max_file_size_mb": 100
            },
            "data_cleaning": {
                "missing_value_strategy": "drop",
                "duplicate_handling": "remove",
                "date_formats": ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
            },
            "matching": {
                "exact_matching": {
                    "amount_tolerance": 0.01,
                    "date_tolerance_days": 0
                },
                "fuzzy_matching": {
                    "auto_match_threshold": 85,
                    "potential_match_threshold": 60,
                    "similarity_algorithms": ["ratio", "partial_ratio"]
                }
            },
            "reporting": {
                "default_format": "excel",
                "include_charts": True
            }
        }
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_config_file(self, filename: str, config_data: dict = None):
        """Create a test configuration file."""
        if config_data is None:
            config_data = self.sample_config
        
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return filepath
    
    def test_default_config_loading(self):
        """Test loading default configuration."""
        config = Config()
        
        # Should load without errors
        self.assertIsInstance(config.data_ingestion, dict)
        self.assertIsInstance(config.data_cleaning, dict)
        self.assertIsInstance(config.matching, dict)
        self.assertIsInstance(config.reporting, dict)
    
    def test_custom_config_file_loading(self):
        """Test loading custom configuration file."""
        config_file = self.create_test_config_file('custom_config.json')
        
        config = Config(config_file)
        
        # Should load custom configuration
        self.assertEqual(config.data_ingestion['max_file_size_mb'], 100)
        self.assertEqual(config.data_cleaning['missing_value_strategy'], 'drop')
        self.assertEqual(config.matching['exact_matching']['amount_tolerance'], 0.01)
    
    def test_nonexistent_config_file(self):
        """Test handling of non-existent configuration file."""
        with self.assertRaises(ConfigurationError):
            Config('/nonexistent/config.json')
    
    def test_invalid_json_config(self):
        """Test handling of invalid JSON configuration."""
        invalid_config_file = os.path.join(self.temp_dir, 'invalid.json')
        with open(invalid_config_file, 'w') as f:
            f.write('{ invalid json content }')
        
        with self.assertRaises(ConfigurationError):
            Config(invalid_config_file)
    
    def test_get_parameter_success(self):
        """Test successful parameter retrieval."""
        config = Config()
        
        # Test nested parameter access
        amount_tolerance = config.get_parameter('matching.exact_matching.amount_tolerance')
        self.assertIsInstance(amount_tolerance, (int, float))
        
        # Test top-level parameter access
        data_ingestion = config.get_parameter('data_ingestion')
        self.assertIsInstance(data_ingestion, dict)
    
    def test_get_parameter_with_default(self):
        """Test parameter retrieval with default value."""
        config = Config()
        
        # Non-existent parameter should return default
        value = config.get_parameter('non.existent.parameter', default='default_value')
        self.assertEqual(value, 'default_value')
        
        # Existing parameter should return actual value
        value = config.get_parameter('data_ingestion.supported_formats', default=[])
        self.assertIsInstance(value, list)
        self.assertGreater(len(value), 0)
    
    def test_get_parameter_invalid_path(self):
        """Test parameter retrieval with invalid path."""
        config = Config()
        
        with self.assertRaises(ConfigurationError):
            config.get_parameter('non.existent.parameter')
    
    def test_set_parameter_success(self):
        """Test successful parameter setting."""
        config = Config()
        
        # Set new parameter value
        config.set_parameter('matching.exact_matching.amount_tolerance', 0.05)
        
        # Verify it was set
        value = config.get_parameter('matching.exact_matching.amount_tolerance')
        self.assertEqual(value, 0.05)
    
    def test_set_parameter_new_path(self):
        """Test setting parameter with new path."""
        config = Config()
        
        # Set parameter in new section
        config.set_parameter('new_section.new_parameter', 'test_value')
        
        # Verify it was set
        value = config.get_parameter('new_section.new_parameter')
        self.assertEqual(value, 'test_value')
    
    def test_validate_configuration(self):
        """Test configuration validation."""
        config_file = self.create_test_config_file('valid_config.json')
        config = Config(config_file)
        
        # Should validate without errors
        is_valid = config.validate_configuration()
        self.assertTrue(is_valid)
    
    def test_validate_invalid_configuration(self):
        """Test validation of invalid configuration."""
        invalid_config = {
            "data_ingestion": {
                "max_file_size_mb": "invalid_number"  # Should be numeric
            },
            "matching": {
                "exact_matching": {
                    "amount_tolerance": -1  # Should be positive
                }
            }
        }
        
        config_file = self.create_test_config_file('invalid_config.json', invalid_config)
        
        with self.assertRaises(ConfigurationError):
            Config(config_file)
    
    def test_update_configuration(self):
        """Test configuration updates."""
        config = Config()
        
        # Update configuration with new values
        updates = {
            'matching': {
                'exact_matching': {
                    'amount_tolerance': 0.02
                }
            }
        }
        
        config.update_configuration(updates)
        
        # Verify update
        value = config.get_parameter('matching.exact_matching.amount_tolerance')
        self.assertEqual(value, 0.02)
    
    def test_save_configuration(self):
        """Test saving configuration to file."""
        config = Config()
        
        # Modify configuration
        config.set_parameter('matching.exact_matching.amount_tolerance', 0.03)
        
        # Save to file
        save_path = os.path.join(self.temp_dir, 'saved_config.json')
        config.save_configuration(save_path)
        
        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(save_path))
        
        with open(save_path, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['matching']['exact_matching']['amount_tolerance'], 0.03)
    
    def test_load_configuration_from_dict(self):
        """Test loading configuration from dictionary."""
        config = Config()
        
        # Load new configuration from dict
        new_config = {
            'matching': {
                'fuzzy_matching': {
                    'auto_match_threshold': 90
                }
            }
        }
        
        config.load_configuration_from_dict(new_config)
        
        # Verify configuration was loaded
        value = config.get_parameter('matching.fuzzy_matching.auto_match_threshold')
        self.assertEqual(value, 90)
    
    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        config = Config()
        
        # Modify configuration
        config.set_parameter('matching.exact_matching.amount_tolerance', 0.05)
        
        # Reset to defaults
        config.reset_to_defaults()
        
        # Should be back to default value
        default_tolerance = config.get_parameter('matching.exact_matching.amount_tolerance')
        self.assertNotEqual(default_tolerance, 0.05)
    
    def test_get_column_mappings(self):
        """Test getting column mappings."""
        config = Config()
        
        gl_mappings = config.get_column_mappings('gl')
        bank_mappings = config.get_column_mappings('bank')
        
        self.assertIsInstance(gl_mappings, dict)
        self.assertIsInstance(bank_mappings, dict)
        
        # Should have standard column mappings
        self.assertIn('date_column', gl_mappings)
        self.assertIn('amount_column', gl_mappings)
        self.assertIn('description_column', gl_mappings)
    
    def test_get_matching_parameters(self):
        """Test getting matching parameters."""
        config = Config()
        
        exact_params = config.get_matching_parameters('exact')
        fuzzy_params = config.get_matching_parameters('fuzzy')
        
        self.assertIsInstance(exact_params, dict)
        self.assertIsInstance(fuzzy_params, dict)
        
        # Should have expected parameters
        self.assertIn('amount_tolerance', exact_params)
        self.assertIn('auto_match_threshold', fuzzy_params)
    
    def test_environment_variable_override(self):
        """Test configuration override from environment variables."""
        # Set environment variable
        os.environ['SMARTRECON_AMOUNT_TOLERANCE'] = '0.10'
        
        try:
            config = Config()
            
            # Should use environment variable value
            if hasattr(config, 'load_from_environment'):
                config.load_from_environment()
                tolerance = config.get_parameter('matching.exact_matching.amount_tolerance')
                self.assertEqual(tolerance, 0.10)
        finally:
            # Clean up environment variable
            if 'SMARTRECON_AMOUNT_TOLERANCE' in os.environ:
                del os.environ['SMARTRECON_AMOUNT_TOLERANCE']
    
    def test_configuration_schema_validation(self):
        """Test configuration against schema."""
        config = Config()
        
        # Should have all required sections
        required_sections = ['data_ingestion', 'data_cleaning', 'matching', 'reporting']
        
        for section in required_sections:
            self.assertTrue(hasattr(config, section))
            self.assertIsInstance(getattr(config, section), dict)
    
    def test_thread_safety(self):
        """Test configuration access in multi-threaded environment."""
        import threading
        import time
        
        config = Config()
        results = []
        
        def access_config():
            for i in range(10):
                value = config.get_parameter('matching.exact_matching.amount_tolerance')
                results.append(value)
                time.sleep(0.001)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=access_config)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All results should be the same (configuration should be thread-safe)
        self.assertTrue(all(result == results[0] for result in results))


class TestConfigurationEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for Configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_deeply_nested_parameter_access(self):
        """Test accessing deeply nested parameters."""
        config = Config()
        
        # Create deeply nested structure
        config.set_parameter('level1.level2.level3.level4.parameter', 'deep_value')
        
        # Should be able to access it
        value = config.get_parameter('level1.level2.level3.level4.parameter')
        self.assertEqual(value, 'deep_value')
    
    def test_parameter_path_with_special_characters(self):
        """Test parameter paths with special characters."""
        config = Config()
        
        # This should handle special characters gracefully
        with self.assertRaises(ConfigurationError):
            config.get_parameter('invalid..path')
        
        with self.assertRaises(ConfigurationError):
            config.get_parameter('.invalid.path')
        
        with self.assertRaises(ConfigurationError):
            config.get_parameter('invalid.path.')
    
    def test_large_configuration_file(self):
        """Test handling of large configuration files."""
        # Create large configuration
        large_config = {}
        
        # Add many sections with many parameters
        for section in range(100):
            large_config[f'section_{section}'] = {}
            for param in range(100):
                large_config[f'section_{section}'][f'param_{param}'] = f'value_{param}'
        
        config_file = os.path.join(self.temp_dir, 'large_config.json')
        with open(config_file, 'w') as f:
            json.dump(large_config, f)
        
        # Should handle large configuration
        config = Config(config_file)
        
        # Should be able to access parameters
        value = config.get_parameter('section_50.param_50')
        self.assertEqual(value, 'value_50')
    
    def test_circular_reference_prevention(self):
        """Test prevention of circular references in configuration."""
        config = Config()
        
        # This would create a circular reference in a more complex system
        # Our simple dict-based approach shouldn't have this issue
        config.set_parameter('section1.ref', 'section2.value')
        config.set_parameter('section2.value', 'some_value')
        
        # Should work without infinite recursion
        value = config.get_parameter('section1.ref')
        self.assertEqual(value, 'section2.value')


if __name__ == '__main__':
    unittest.main()
