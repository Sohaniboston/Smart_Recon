"""
Custom exceptions for SmartRecon application.

This module defines all custom exception classes used throughout the application
for specific error handling and debugging.
"""


class SmartReconException(Exception):
    """Base exception class for all SmartRecon-specific exceptions."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception with message and optional details.
        
        Args:
            message: Human-readable error message
            details: Additional error context and details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class DataIngestionError(SmartReconException):
    """Raised when data ingestion operations fail."""
    pass


class DataValidationError(SmartReconException):
    """Raised when data validation fails."""
    pass


class DataCleaningError(SmartReconException):
    """Raised when data cleaning operations fail."""
    pass


class MatchingError(SmartReconException):
    """Raised when transaction matching operations fail."""
    pass


class ExceptionHandlingError(SmartReconException):
    """Raised when exception processing fails."""
    pass


class ReportingError(SmartReconException):
    """Raised when report generation fails."""
    pass


class ConfigurationError(SmartReconException):
    """Raised when configuration loading or validation fails."""
    pass


class FileProcessingError(SmartReconException):
    """Raised when file processing operations fail."""
    pass


class DataMappingError(SmartReconException):
    """Raised when data mapping operations fail."""
    pass
