"""
Logging configuration for ResonanceOS
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import get_config


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        return super().format(record)


def setup_logging(
    name: str = "resonance_os",
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
    console: bool = True
) -> logging.Logger:
    """Setup logging configuration"""
    
    config = get_config()
    
    # Use provided values or defaults from config
    log_level = level or config.logging.level
    log_path = log_file or config.logging.file
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = ColoredFormatter(
        fmt=config.logging.format,
        datefmt=config.logging.date_format
    )
    
    file_formatter = logging.Formatter(
        fmt=config.logging.format,
        datefmt=config.logging.date_format
    )
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "resonance_os") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


def log_performance(func):
    """Decorator to log function performance"""
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(
                f"Function '{func.__name__}' completed in {duration:.3f}s"
            )
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.error(
                f"Function '{func.__name__}' failed after {duration:.3f}s: {str(e)}"
            )
            raise
    
    return wrapper


def log_generation_metrics(metrics: dict):
    """Log generation metrics"""
    logger = get_logger()
    
    logger.info(
        f"Generation Metrics - "
        f"Similarity: {metrics.get('similarity_score', 0):.3f}, "
        f"Drift: {metrics.get('drift_rate', 0):.3f}, "
        f"Corrections: {metrics.get('corrections_made', 0)}, "
        f"Tokens: {metrics.get('tokens_generated', 0)}"
    )


def log_profile_analysis(profile_name: str, metrics: dict):
    """Log profile analysis metrics"""
    logger = get_logger()
    
    logger.info(
        f"Profile Analysis - '{profile_name}': "
        f"Confidence: {metrics.get('confidence', 0):.3f}, "
        f"Dimensions: {metrics.get('dimensions_analyzed', 0)}, "
        f"Samples: {metrics.get('sample_count', 0)}"
    )


def log_api_request(method: str, path: str, status_code: int, duration: float):
    """Log API request metrics"""
    logger = get_logger()
    
    logger.info(
        f"API Request - {method} {path} -> {status_code} ({duration:.3f}s)"
    )


class StructuredLogger:
    """Structured logger for better parsing and analysis"""
    
    def __init__(self, name: str = "resonance_os"):
        self.logger = get_logger(name)
    
    def log_event(self, event_type: str, **kwargs):
        """Log structured event"""
        event_data = {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        self.logger.info(f"EVENT: {event_type} | {event_data}")
    
    def log_metric(self, metric_name: str, value: float, **kwargs):
        """Log metric value"""
        metric_data = {
            'metric_name': metric_name,
            'value': value,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        self.logger.info(f"METRIC: {metric_name} = {value} | {metric_data}")
    
    def log_error(self, error_type: str, error_message: str, **kwargs):
        """Log structured error"""
        error_data = {
            'error_type': error_type,
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        self.logger.error(f"ERROR: {error_type} - {error_message} | {error_data}")


# Initialize default logger
setup_logging()
