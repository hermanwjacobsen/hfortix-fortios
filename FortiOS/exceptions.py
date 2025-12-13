"""
FortiOS Exceptions
Backward compatibility wrapper - imports from root fortinet_exceptions module
"""

# Import all exceptions from the root fortinet_exceptions module
from fortinet_exceptions import (
    # Base exceptions
    FortinetError,
    AuthenticationError,
    AuthorizationError,
    APIError,
    
    # Specific exceptions
    ResourceNotFoundError,
    BadRequestError,
    MethodNotAllowedError,
    RateLimitError,
    ServerError,
    DuplicateEntryError,
    EntryInUseError,
    InvalidValueError,
    PermissionDeniedError,
    
    # Helper functions
    get_error_description,
    get_http_status_description,
    raise_for_status,
    
    # Data
    HTTP_STATUS_CODES,
    FORTIOS_ERROR_CODES,
    
    # Backward compatibility aliases
    FortiOSError,
    LoginError,
)

__all__ = [
    # Base exceptions
    'FortinetError',
    'FortiOSError',
    'AuthenticationError',
    'LoginError',
    'AuthorizationError',
    'APIError',
    
    # Specific exceptions
    'ResourceNotFoundError',
    'BadRequestError',
    'MethodNotAllowedError',
    'RateLimitError',
    'ServerError',
    'DuplicateEntryError',
    'EntryInUseError',
    'InvalidValueError',
    'PermissionDeniedError',
    
    # Helper functions
    'get_error_description',
    'get_http_status_description',
    'raise_for_status',
    
    # Data
    'HTTP_STATUS_CODES',
    'FORTIOS_ERROR_CODES',
]