# File: logging_config.py
# Logging Configuration

import logging
import os
from pathlib import Path

def _setup_logger(logger_name, log_file, log_format):
    """Helper function to configure a logger with the given name, file, and format."""
    try:
        # Define log directory path (using absolute path)
        log_dir = Path(__file__).parent / "log_file"
        log_path = log_dir / log_file

        # Create directory if needed
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create a logger instance
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # Avoid adding handlers if already configured
        if not logger.handlers:
            # Create handlers
            file_handler = logging.FileHandler(log_path)
            stream_handler = logging.StreamHandler()

            # Set format
            formatter = logging.Formatter(log_format)
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            # Add handlers
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        logger.info(f"Logging initialized. Logs will be saved to: {log_path}")
        return logger

    except Exception as e:
        # Fallback to console-only logging
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(log_format))
            logger.addHandler(stream_handler)
        logger.warning(f"Failed to initialize file logging: {e}. Using console logging only.")
        return logger

def setup_logging():
    """Configure logging with timestamp and level."""
    return _setup_logger(
        logger_name="eda_logger",
        log_file="eda_polluted_dataset.log",
        log_format="\n%(message)s"
    )



# Initialize loggers
logger = setup_logging()
