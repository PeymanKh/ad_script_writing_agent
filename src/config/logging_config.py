"""
Simple logging configuration for GCP Cloud Run deployment.
Integrates with the main application configuration.
"""
import yaml
import logging
import logging.config
from pathlib import Path

# DON'T import config at module level


class LoggingConfig:
    """Simple logging configuration manager for Cloud Run"""

    def __init__(self):
        self.config_path = Path(__file__).parent / "logging_config.yaml"

    def setup_logging(self, config_obj) -> None:
        """Initialize logging from YAML configuration"""
        try:
            # Load YAML configuration
            with open(self.config_path, 'r', encoding='utf-8') as f:
                logging_config = yaml.safe_load(f)

            # Apply environment-specific log level from your main config
            self._apply_log_level(logging_config, config_obj)

            # Configure logging
            logging.config.dictConfig(logging_config)

            # Test logging works
            logger = logging.getLogger(__name__)
            logger.info(
                "Logging configured successfully",
                extra={
                    "app_name": config_obj.app_name,
                    "environment": config_obj.environment,
                    "log_level": config_obj.log_level.value
                }
            )

        except Exception as e:
            # Fallback to basic logging if YAML fails
            self._setup_fallback_logging(config_obj)
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to load logging config: {e}")
            logger.info("Using fallback logging")

    def _apply_log_level(self, logging_config: dict, config_obj) -> None:
        """Apply log level from main configuration"""
        log_level = config_obj.log_level.value

        # Update root logger level
        logging_config['root']['level'] = log_level

        # Update app logger level
        if 'src' in logging_config['loggers']:
            logging_config['loggers']['src']['level'] = log_level

    def _setup_fallback_logging(self, config_obj) -> None:
        """Simple fallback if YAML config fails"""
        logging.basicConfig(
            level=getattr(logging, config_obj.log_level.value),
            format=config_obj.log_format,
            handlers=[logging.StreamHandler()]
        )

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance"""
        return logging.getLogger(name)


# Global instance
_logging_config = LoggingConfig()


def setup_logging(config_obj) -> None:
    """Initialize application logging"""
    _logging_config.setup_logging(config_obj)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name"""
    return _logging_config.get_logger(name)


# Export public interface
__all__ = ['setup_logging', 'get_logger']
