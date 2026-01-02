"""
HFortix FortiOS - Python SDK for FortiGate

Provides comprehensive API client for FortiOS with:
- Full CRUD operations
- Firewall policy management
- Schedule, service, and shaper configuration
- Async support
"""

from __future__ import annotations

import logging
import sys
from typing import Literal

from .client import FortiOS

__version__ = "0.4.0"
__all__ = ["FortiOS", "configure_logging"]


def configure_logging(
    level: str | int = "INFO",
    format: Literal["json", "text"] = "text",
    handler: logging.Handler | None = None,
    use_color: bool = False,
) -> None:
    """
    Configure logging for HFortix library
    
    Provides a convenient way to set up structured logging for all
    HFortix loggers. Useful for enterprise observability with log
    aggregation systems (ELK, Splunk, CloudWatch).
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) or numeric value
        format: Output format - "json" for structured logs or "text" for human-readable
        handler: Custom logging handler (optional, default: StreamHandler to stdout)
        use_color: Use ANSI color codes in text format (default: False)
    
    Examples:
        Basic text logging:
        
        >>> from hfortix_fortios import configure_logging, FortiOS
        >>> configure_logging(level="INFO", format="text")
        >>> fgt = FortiOS("192.168.1.99", token="token")
        
        Structured JSON logging for ELK/Splunk:
        
        >>> configure_logging(level="INFO", format="json")
        >>> # All logs now output as JSON
        
        Debug logging with colors:
        
        >>> configure_logging(level="DEBUG", format="text", use_color=True)
        >>> # Debug logs with ANSI colors
        
        Custom handler:
        
        >>> import logging
        >>> file_handler = logging.FileHandler("/var/log/hfortix.log")
        >>> configure_logging(level="INFO", format="json", handler=file_handler)
    
    Note:
        This configures all loggers under the "hfortix" namespace:
        - hfortix.http (HTTP client operations)
        - hfortix.audit (Audit logging)
        - hfortix.core (Core utilities)
    """
    # Import formatters
    from hfortix_core.logging import StructuredFormatter, TextFormatter
    
    # Get root hfortix logger
    logger = logging.getLogger("hfortix")
    
    # Convert level string to logging constant
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create handler if not provided
    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
    
    # Set formatter based on format type
    if format == "json":
        formatter = StructuredFormatter()
    else:
        formatter = TextFormatter(use_color=use_color)
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False
    
    # Log configuration
    logger.debug(
        f"Logging configured: level={logging.getLevelName(level)}, format={format}",
        extra={"format": format, "level": logging.getLevelName(level)},
    )
