"""
Configuration management for ResonanceOS
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    url: str = Field(default="sqlite:///./resonance_os.db", env="DATABASE_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")


class APISettings(BaseSettings):
    """API server configuration"""
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    workers: int = Field(default=4, env="API_WORKERS")
    reload: bool = Field(default=False, env="API_RELOAD")
    log_level: str = Field(default="info", env="LOG_LEVEL")


class ModelSettings(BaseSettings):
    """AI model configuration"""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    huggingface_api_key: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    default_model: str = Field(default="gpt-3.5-turbo", env="DEFAULT_MODEL")
    embedding_model: str = Field(default="text-embedding-ada-002", env="EMBEDDING_MODEL")
    spacy_model: str = Field(default="en_core_web_lg", env="SPACY_MODEL")


class ResonanceSettings(BaseSettings):
    """Resonance algorithm configuration"""
    threshold: float = Field(default=0.92, env="RESONANCE_THRESHOLD")
    drift_threshold: float = Field(default=0.05, env="DRIFT_THRESHOLD")
    max_correction_attempts: int = Field(default=3, env="MAX_CORRECTION_ATTEMPTS")
    similarity_method: str = Field(default="cosine", env="SIMILARITY_METHOD")


class GenerationSettings(BaseSettings):
    """Text generation configuration"""
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    top_p: float = Field(default=0.9, env="TOP_P")
    max_tokens: int = Field(default=2048, env="MAX_TOKENS")
    batch_size: int = Field(default=32, env="BATCH_SIZE")


class PathSettings(BaseSettings):
    """File system paths"""
    data_dir: Path = Field(default=Path("data"), env="DATA_DIR")
    profiles_dir: Path = Field(default=Path("profiles"), env="PROFILES_DIR")
    cache_dir: Path = Field(default=Path(".cache"), env="CACHE_DIR")
    log_dir: Path = Field(default=Path("logs"), env="LOG_DIR")


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    file: Optional[Path] = Field(default=None, env="LOG_FILE")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        env="LOG_DATE_FORMAT"
    )


class Settings(BaseSettings):
    """Main application settings"""
    
    # Sub-settings
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    models: ModelSettings = ModelSettings()
    resonance: ResonanceSettings = ResonanceSettings()
    generation: GenerationSettings = GenerationSettings()
    paths: PathSettings = PathSettings()
    logging: LoggingSettings = LoggingSettings()
    
    # Application settings
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_config() -> Settings:
    """Get the global configuration instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
        # Ensure directories exist
        _settings.paths.data_dir.mkdir(parents=True, exist_ok=True)
        _settings.paths.profiles_dir.mkdir(parents=True, exist_ok=True)
        _settings.paths.cache_dir.mkdir(parents=True, exist_ok=True)
        _settings.paths.log_dir.mkdir(parents=True, exist_ok=True)
    return _settings


def reload_config() -> Settings:
    """Reload configuration from environment variables"""
    global _settings
    _settings = None
    return get_config()


def get_env_vars() -> Dict[str, Any]:
    """Get all relevant environment variables"""
    config = get_config()
    return {
        "OPENAI_API_KEY": "***" if config.models.openai_api_key else None,
        "HUGGINGFACE_API_KEY": "***" if config.models.huggingface_api_key else None,
        "DEFAULT_MODEL": config.models.default_model,
        "EMBEDDING_MODEL": config.models.embedding_model,
        "RESONANCE_THRESHOLD": config.resonance.threshold,
        "DRIFT_THRESHOLD": config.resonance.drift_threshold,
        "API_HOST": config.api.host,
        "API_PORT": config.api.port,
        "LOG_LEVEL": config.logging.level,
        "ENVIRONMENT": config.environment,
        "DEBUG": config.debug,
    }
