"""
===================================================================================
Application Settings Configuration
===================================================================================

This module manages all application settings using Pydantic Settings for:
- Type validation and coercion
- Environment variable loading from .env file
- Default values with validation
- Production-ready configuration management

Key Features:
-------------
1. Type Safety: All settings are validated at runtime
2. Environment Override: .env file always takes precedence
3. Default Values: Sensible defaults for all optional settings
4. Validation: Pydantic validates types and constraints automatically

Architecture:
-------------
- Uses Pydantic BaseSettings for configuration management
- Loads from .env file with override=True (critical for consistency)
- Provides global 'settings' singleton instance
- Supports environment-specific configs (dev/staging/prod)

Author: Automotive Analytics Team
Version: 2.0.0
===================================================================================
"""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# ===================================================================================
# CRITICAL: Force .env file to override system environment variables
# ===================================================================================
# Without override=True, system environment variables take precedence, which can
# lead to confusion when testing with updated keys in .env file.
# With override=True, .env always wins, ensuring predictable behavior.
load_dotenv(override=True)


class Settings(BaseSettings):
    """
    Application-wide settings with automatic validation and type coercion.
    
    This class defines all configurable settings for the application, loaded
    from environment variables or .env file. Pydantic automatically:
    - Validates types (str, int, bool, List, etc.)
    - Coerces values (e.g., "true" string -> True boolean)
    - Raises ValidationError if required fields are missing
    - Applies default values for optional fields
    
    Usage:
    ------
    >>> from config.settings import settings
    >>> print(settings.openai_api_key)  # Access any setting
    >>> print(settings.api_port)        # Returns int 8000
    
    Environment Variables:
    ----------------------
    All settings can be overridden via environment variables or .env file.
    The 'alias' parameter defines the environment variable name.
    """
    
    # ===================================================================================
    # DATABASE CONFIGURATION
    # ===================================================================================
    
    database_url: str = Field(
        ...,  # Required field (no default)
        alias="DATABASE_URL",
        description="PostgreSQL connection URL in format: postgresql://user:pass@host:port/db"
    )
    """
    PostgreSQL database connection URL.
    
    Format: postgresql://[user]:[password]@[host]:[port]/[database]
    Example: postgresql://automotive_user:password@localhost:5432/automotive_analytics
    
    Required: Yes (no default)
    Validation: Must be a valid database URL string
    """
    
    db_pool_size: int = Field(
        default=10,
        alias="DB_POOL_SIZE",
        ge=1,  # Greater than or equal to 1
        le=100,  # Less than or equal to 100
        description="Database connection pool size"
    )
    """
    Number of persistent connections to maintain in the pool.
    
    - Increase for high-concurrency applications
    - Decrease for memory-constrained environments
    - Default 10 is suitable for small to medium apps
    
    Default: 10
    Range: 1-100
    """
    
    db_max_overflow: int = Field(
        default=20,
        alias="DB_MAX_OVERFLOW",
        ge=0,
        le=100,
        description="Maximum overflow connections beyond pool_size"
    )
    """
    Additional connections allowed when pool is exhausted.
    
    - Total max connections = pool_size + max_overflow
    - Overflow connections are created on-demand and closed after use
    - Default 20 allows bursts up to 30 total connections
    
    Default: 20
    Range: 0-100
    """
    
    # ===================================================================================
    # OPENAI / LLM CONFIGURATION
    # ===================================================================================
    
    openai_api_key: str = Field(
        ...,  # Required
        alias="OPENAI_API_KEY",
        min_length=20,  # Minimum length validation
        description="OpenAI API key (sk-... or sk-proj-...)"
    )
    """
    OpenAI API key for LLM-powered features.
    
    Format:
        - Legacy: sk-... (48 chars)
        - Project: sk-proj-... (164 chars, recommended)
    
    Get your key: https://platform.openai.com/api-keys
    
    Required: Yes
    Validation: Must be at least 20 characters
    Security: Never commit this to version control
    """
    
    openai_model_primary: str = Field(
        default="gpt-4-turbo-preview",
        alias="OPENAI_MODEL_PRIMARY",
        description="Primary OpenAI model for complex tasks"
    )
    """
    Primary model used for complex analysis and generation tasks.
    
    Options:
        - gpt-4-turbo-preview: Best quality, higher cost
        - gpt-4: Stable version, high quality
        - gpt-3.5-turbo: Fast, economical
    
    Used for: Insights generation, complex reports, deep analysis
    
    Default: gpt-4-turbo-preview
    """
    
    openai_model_secondary: str = Field(
        default="gpt-3.5-turbo",
        alias="OPENAI_MODEL_SECONDARY",
        description="Secondary OpenAI model for simple tasks"
    )
    """
    Secondary model used for simpler, routine tasks.
    
    Options:
        - gpt-3.5-turbo: Recommended for most simple tasks
        - gpt-3.5-turbo-16k: For larger contexts
    
    Used for: Simple queries, data formatting, quick responses
    
    Default: gpt-3.5-turbo
    """
    
    openai_max_tokens: int = Field(
        default=4000,
        alias="OPENAI_MAX_TOKENS",
        ge=100,  # Minimum 100 tokens
        le=16000,  # Maximum 16000 tokens
        description="Maximum tokens per API request"
    )
    """
    Maximum tokens (words/pieces) allowed in API responses.
    
    - Controls response length and cost
    - 1 token ≈ 0.75 words
    - Higher = more detailed responses, higher cost
    - Lower = more concise responses, lower cost
    
    Default: 4000 (~3000 words)
    Range: 100-16000
    """
    
    # ===================================================================================
    # API SERVER CONFIGURATION
    # ===================================================================================
    
    api_host: str = Field(
        default="0.0.0.0",
        alias="API_HOST",
        description="API server host (0.0.0.0 = all interfaces)"
    )
    """
    Host address for the FastAPI server to bind to.
    
    Options:
        - 0.0.0.0: Listen on all network interfaces (production)
        - 127.0.0.1: Listen only on localhost (development)
    
    Default: 0.0.0.0
    """
    
    api_port: int = Field(
        default=8000,
        alias="API_PORT",
        ge=1024,  # Ports below 1024 require root
        le=65535,  # Maximum port number
        description="API server port number"
    )
    """
    TCP port for the FastAPI server.
    
    Default: 8000 (FastAPI convention)
    Range: 1024-65535 (non-privileged ports)
    """
    
    api_cors_origins: List[str] = Field(
        default=["http://localhost:8501"],
        alias="API_CORS_ORIGINS",
        description="Allowed CORS origins for API access"
    )
    """
    Cross-Origin Resource Sharing (CORS) allowed origins.
    
    - Controls which domains can make API requests
    - Default allows Streamlit dashboard (port 8501)
    - Add production domains for deployment
    
    Example: ["http://localhost:8501", "https://yourdomain.com"]
    
    Default: ["http://localhost:8501"]
    """
    
    # ===================================================================================
    # DASHBOARD CONFIGURATION
    # ===================================================================================
    
    dashboard_port: int = Field(
        default=8501,
        alias="DASHBOARD_PORT",
        ge=1024,
        le=65535,
        description="Streamlit dashboard port number"
    )
    """
    TCP port for the Streamlit dashboard.
    
    Default: 8501 (Streamlit default)
    Range: 1024-65535
    """
    
    # ===================================================================================
    # LOGGING CONFIGURATION
    # ===================================================================================
    
    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    """
    Logging verbosity level.
    
    Levels (from most to least verbose):
        - DEBUG: Detailed diagnostic information
        - INFO: General informational messages (default)
        - WARNING: Warning messages
        - ERROR: Error messages
        - CRITICAL: Critical errors only
    
    Development: Use DEBUG
    Production: Use INFO or WARNING
    
    Default: INFO
    """
    
    log_file: str = Field(
        default="logs/app.log",
        alias="LOG_FILE",
        description="Log file path (relative to project root)"
    )
    """
    Path to the main log file.
    
    - Logs are rotated automatically (10MB max per file)
    - Keeps 5 backup files
    - Created automatically if doesn't exist
    
    Default: logs/app.log
    """
    
    # ===================================================================================
    # VECTOR STORE CONFIGURATION
    # ===================================================================================
    
    chromadb_path: str = Field(
        default="./data/chromadb",
        alias="CHROMADB_PATH",
        description="ChromaDB vector database storage path"
    )
    """
    File system path for ChromaDB vector store persistence.
    
    - Stores vector embeddings for RAG (Retrieval-Augmented Generation)
    - Created automatically if doesn't exist
    - Can be on any filesystem path
    
    Default: ./data/chromadb
    """
    
    # ===================================================================================
    # FEATURE FLAGS
    # ===================================================================================
    
    enable_rag: bool = Field(
        default=True,
        alias="ENABLE_RAG",
        description="Enable Retrieval-Augmented Generation features"
    )
    """
    Toggle for RAG (Retrieval-Augmented Generation) features.
    
    When enabled:
        - Uses vector store for context retrieval
        - Enhances LLM responses with relevant data
        - Improves accuracy and reduces hallucinations
    
    When disabled:
        - LLM responses based only on training data
        - Faster but less context-aware
    
    Default: True
    """
    
    enable_caching: bool = Field(
        default=False,
        alias="ENABLE_CACHING",
        description="Enable response caching"
    )
    """
    Toggle for caching LLM responses.
    
    When enabled:
        - Caches identical queries
        - Reduces API costs
        - Faster responses for repeated queries
    
    When disabled:
        - Every query hits the API
        - Always fresh responses
    
    Default: False (disabled for development)
    """
    
    # ===================================================================================
    # APPLICATION METADATA
    # ===================================================================================
    
    app_name: str = Field(
        default="Automotive Analytics Pipeline",
        alias="APP_NAME",
        description="Application name for display and logging"
    )
    """
    Human-readable application name.
    
    Used in:
        - API documentation
        - Log messages
        - Dashboard headers
    
    Default: Automotive Analytics Pipeline
    """
    
    app_version: str = Field(
        default="2.0.0",
        alias="APP_VERSION",
        description="Application version (semantic versioning)"
    )
    """
    Application version number.
    
    Format: MAJOR.MINOR.PATCH (semantic versioning)
        - MAJOR: Breaking changes
        - MINOR: New features (backward compatible)
        - PATCH: Bug fixes
    
    Default: 2.0.0
    """
    
    debug: bool = Field(
        default=False,
        alias="DEBUG",
        description="Enable debug mode with verbose logging"
    )
    """
    Debug mode toggle.
    
    When enabled:
        - Verbose logging
        - SQL query logging
        - Auto-reload on code changes
        - Detailed error tracebacks
    
    Development: Set to True
    Production: Must be False
    
    Default: False
    """
    
    # ===================================================================================
    # PYDANTIC MODEL CONFIGURATION
    # ===================================================================================
    
    model_config = SettingsConfigDict(
        env_file=".env",              # Load from .env file
        env_file_encoding="utf-8",    # UTF-8 encoding
        case_sensitive=False,          # Allow case-insensitive env vars
        extra="ignore"                 # Ignore extra environment variables
    )
    """
    Pydantic Settings configuration.
    
    - env_file: Loads settings from .env file
    - env_file_encoding: Use UTF-8 for international characters
    - case_sensitive: False = DATABASE_URL == database_url
    - extra="ignore": Don't fail on unknown environment variables
    """


# ===================================================================================
# GLOBAL SETTINGS INSTANCE
# ===================================================================================

settings = Settings()
"""
Global singleton instance of Settings.

Usage throughout the application:
    from config.settings import settings
    
    # Access any setting
    api_key = settings.openai_api_key
    db_url = settings.database_url
    
This instance is created once when the module is imported and shared
across the entire application, ensuring consistent configuration.
"""

