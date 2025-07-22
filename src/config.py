"""
Configuration management for SmartRecon application.

This module handles loading, validation, and management of application
configuration from JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import jsonschema
from jsonschema import validate

try:
    from .utils.exceptions import SmartReconException
except ImportError:
    # Fallback for direct execution
    from utils.exceptions import SmartReconException


class ConfigurationError(SmartReconException):
    """Raised when configuration loading or validation fails."""
    pass


class Config:
    """
    Configuration manager for SmartRecon application.
    
    Handles loading configuration from JSON files, validation against schema,
    and providing access to configuration values throughout the application.
    """
    
    def __init__(self, config_path: str = "config/default_config.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration JSON file
            
        Note:
            Configuration is loaded lazily on first access to avoid import-time issues
        """
        self.config_path = config_path
        self._config_data = None
        self._loaded = False
    
    def _ensure_loaded(self):
        """Ensure configuration is loaded (lazy loading)."""
        if not self._loaded:
            self._config_data = {}
            self._load_config()
            self._validate_config()
            self._loaded = True
    
    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            if not os.path.exists(self.config_path):
                raise ConfigurationError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
                
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    def _validate_config(self):
        """Validate configuration against schema."""
        schema = self._get_config_schema()
        try:
            validate(instance=self._config_data, schema=schema)
        except jsonschema.ValidationError as e:
            raise ConfigurationError(f"Configuration validation failed: {e.message}")
    
    def _get_config_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for configuration validation.
        
        Returns:
            Configuration validation schema
        """
        return {
            "type": "object",
            "properties": {
                "data_ingestion": {
                    "type": "object",
                    "properties": {
                        "encoding": {"type": "string"},
                        "required_columns": {
                            "type": "object",
                            "properties": {
                                "gl": {"type": "array", "items": {"type": "string"}},
                                "bank": {"type": "array", "items": {"type": "string"}}
                            }
                        },
                        "column_mapping": {"type": "object"}
                    }
                },
                "data_cleaning": {
                    "type": "object",
                    "properties": {
                        "date_formats": {"type": "array", "items": {"type": "string"}},
                        "amount_precision": {"type": "integer"},
                        "text_normalization": {"type": "object"}
                    }
                },
                "matching": {
                    "type": "object",
                    "properties": {
                        "exact_match_tolerance": {"type": "number"},
                        "fuzzy_match_threshold": {"type": "number"},
                        "date_tolerance_days": {"type": "integer"}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "formats": {"type": "array", "items": {"type": "string"}},
                        "include_charts": {"type": "boolean"}
                    }
                },
                "logging": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "string"},
                        "format": {"type": "string"},
                        "file_path": {"type": "string"}
                    }
                }
            },
            "required": ["data_ingestion", "matching", "output"]
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key path.
        
        Args:
            key: Configuration key path (e.g., 'matching.exact_match_tolerance')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        self._ensure_loaded()
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_data_ingestion_config(self) -> Dict[str, Any]:
        """Get data ingestion configuration section."""
        return self.get('data_ingestion', {})
    
    def get_data_cleaning_config(self) -> Dict[str, Any]:
        """Get data cleaning configuration section."""
        return self.get('data_cleaning', {})
    
    def get_matching_config(self) -> Dict[str, Any]:
        """Get matching configuration section."""
        return self.get('matching', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration section."""
        return self.get('output', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration section."""
        return self.get('logging', {})
    
    def update(self, key: str, value: Any):
        """
        Update configuration value.
        
        Args:
            key: Configuration key path
            value: New value to set
        """
        self._ensure_loaded()
        keys = key.split('.')
        config = self._config_data
        
        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save(self, output_path: Optional[str] = None):
        """
        Save current configuration to file.
        
        Args:
            output_path: Path to save configuration (defaults to original path)
        """
        self._ensure_loaded()
        save_path = output_path or self.config_path
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        self._ensure_loaded()
        return self._config_data.copy()
    
    def __str__(self) -> str:
        """String representation of configuration."""
        self._ensure_loaded()
        return f"Config(path='{self.config_path}', sections={list(self._config_data.keys())})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return self.__str__()
