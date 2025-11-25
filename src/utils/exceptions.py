"""Custom exception classes."""


class AnalyticsPipelineException(Exception):
    """Base exception for analytics pipeline."""

    pass


class DatabaseError(AnalyticsPipelineException):
    """Database-related errors."""

    pass


class DataValidationError(AnalyticsPipelineException):
    """Data validation errors."""

    pass


class LLMServiceError(AnalyticsPipelineException):
    """LLM service errors."""

    pass


class APIError(AnalyticsPipelineException):
    """API-related errors."""

    pass


class ConfigurationError(AnalyticsPipelineException):
    """Configuration errors."""

    pass

