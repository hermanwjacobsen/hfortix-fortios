"""
Helpers module for firewall API endpoints.

Provides shared helper functions to eliminate code duplication
across different firewall resource types (policy, address, addrgrp, etc.).

Includes functions for:
- Payload building
- List normalization
- Validation (future)
- Data cleaning (future)
"""

from .policy_helpers import (
    build_policy_payload,
    build_policy_payload_normalized,
    normalize_to_name_list,
)

__all__ = [
    "build_policy_payload",
    "build_policy_payload_normalized",
    "normalize_to_name_list",
]
