"""
Custom logging setup with structured JSON formatting and context-aware request ID injection.

This module defines:
- A context variable (`request_id_var`) for tracking request IDs across async contexts.
- A custom logging filter (`RequestIDFilter`) to inject request IDs into log records.
- A logging configuration dictionary (`LOGGING_CONFIG`) that outputs logs in JSON format.
- Helper functions to set up logging and manage request IDs: `setup_logging`, `set_request_id`, and `get_request_id`.
"""

import logging
import logging.config
import contextvars

# Context variable for request ID
request_id_var = contextvars.ContextVar("request_id", default="-")

class RequestIDFilter(logging.Filter):
    """
    Logging filter that injects the request ID from the context variable
    into log records.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add the current request ID to the log record.

        Args:
            record (logging.LogRecord): The log record to modify.

        Returns:
            bool: Always True to allow the log record.
        """
        record.request_id = request_id_var.get()
        return True

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_logger": False,

    "formatters": {
        "json": {
            "format": (
                '{"timestamp": "%(asctime)s",'
                '"level": "%(levelname)s", '
                '"request_id": "%(request_id)s", '
                '"logger": "%(name)s", '
                '"module": "%(module)s", '
                '"function": "%(funcName)s", '
                '"line": %(lineno)d, '
                '"message": "%(message)s"}'
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },


    "filters": {
        "request_id": {
            "()": RequestIDFilter,
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO",
            "filters": ["request_id"]
        }
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO"
    },
}

# filter basically create an instance of RequestIDFilter, and assign it the name request_id.
# Then we can attach this filter to handlers or loggers.

def setup_logging():
    """
    Apply the logging configuration defined in LOGGING_CONFIG.
    """
    logging.config.dictConfig(LOGGING_CONFIG)

def set_request_id(request_id: str):
    """
    Set the request ID in the current context.

    Args:
        request_id (str): The request ID to associate with the current context.
    """
    request_id_var.set(request_id)

def get_request_id() -> str:
    """
    Get the request ID from the current context.

    Returns:
        str: The current request ID, or '-' if none is set.
    """
    return request_id_var.get()
