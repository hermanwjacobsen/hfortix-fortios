"""
Shared utilities for building firewall policy payloads.

This module eliminates code duplication between policy.py (API layer)
and firewallPolicy.py (convenience wrapper) by providing shared logic
for converting Python parameter names to FortiOS API field names.
"""

from typing import Any, Dict, List, Union


def normalize_to_name_list(
    value: Union[str, List[str], Dict[str, str], List[Dict[str, str]], None],
) -> List[Dict[str, str]]:
    """
    Normalize various input formats to FortiOS API format: [{'name': 'value'}, ...]

    Args:
        value: Can be:
            - String: 'port1' → [{'name': 'port1'}]
            - List of strings: ['port1', 'port2'] → [{'name': 'port1'}, {'name': 'port2'}]
            - Dict: {'name': 'port1'} → [{'name': 'port1'}]
            - List of dicts: [{'name': 'port1'}, {'name': 'port2'}] → unchanged
            - None: []

    Returns:
        List of dicts in FortiOS format
    """
    if value is None:
        return []

    # Already a list
    if isinstance(value, list):
        if not value:
            return []
        # If first item is a dict, assume whole list is dicts
        if isinstance(value[0], dict):
            # Filter out empty dicts that sometimes appear in API responses
            filtered: list[dict[str, Any]] = [
                item
                for item in value
                if isinstance(item, dict) and item and "name" in item
            ]
            return filtered
        # List of strings
        return [{"name": str(item)} for item in value]

    # Single dict
    if isinstance(value, dict):
        return [value] if value and "name" in value else []

    # Single string
    return [{"name": str(value)}]


def build_policy_payload(**params: Any) -> dict[str, Any]:
    """
    Build a policy payload dictionary from keyword arguments (API layer - no normalization).
    
    Converts Python snake_case parameter names to FortiOS kebab-case API keys
    and filters out None values. Does NOT normalize list fields - caller is responsible
    for providing data in the correct FortiOS format.
    
    This is used by policy.py (API layer) which accepts data as-is.
    
    Args:
        **params: All policy parameters (e.g., srcintf=..., dstintf=...)
        
    Returns:
        Dictionary with FortiOS API-compatible keys and non-None values
        
    Example:
        >>> build_policy_payload(
        ...     srcintf=[{'name': 'port1'}],  # Already in FortiOS format
        ...     dstintf=[{'name': 'port2'}],
        ...     action='accept'
        ... )
        {
            'srcintf': [{'name': 'port1'}],
            'dstintf': [{'name': 'port2'}],
            'action': 'accept'
        }
    """
    payload: dict[str, Any] = {}
    
    for param_name, value in params.items():
        if value is None:
            continue
        
        # Convert snake_case to kebab-case for FortiOS API
        api_key = param_name.replace("_", "-")
        payload[api_key] = value
    
    return payload


def build_policy_payload_normalized(**params: Any) -> dict[str, Any]:
    """
    Build a policy payload with automatic normalization (convenience wrapper layer).
    
    Converts Python snake_case parameter names to FortiOS kebab-case API keys,
    filters out None values, AND normalizes list fields to FortiOS format.
    
    This is used by firewallPolicy.py (convenience wrapper) to accept flexible inputs
    like strings or lists and automatically convert them to FortiOS format.
    
    Args:
        **params: All policy parameters (e.g., srcintf=..., dstintf=...)
        
    Returns:
        Dictionary with FortiOS API-compatible keys and normalized values
        
    Example:
        >>> build_policy_payload_normalized(
        ...     srcintf='port1',  # String gets normalized to [{'name': 'port1'}]
        ...     dstintf=['port2'],  # List gets normalized to [{'name': 'port2'}]
        ...     src_vendor_mac=['vendor1'],  # Gets normalized to [{'name': 'vendor1'}]
        ...     action='accept'  # Simple strings pass through
        ... )
        {
            'srcintf': [{'name': 'port1'}],
            'dstintf': [{'name': 'port2'}],
            'src-vendor-mac': [{'name': 'vendor1'}],
            'action': 'accept'
        }
    """
    # List of parameter names that should be normalized to [{'name': 'value'}] format
    LIST_PARAMS = {
        'srcintf', 'dstintf', 'srcaddr', 'dstaddr', 'service',
        'srcaddr6', 'dstaddr6',
        'internet_service_name', 'internet_service_group', 
        'internet_service_custom', 'internet_service_custom_group',
        'network_service_dynamic', 'internet_service_fortiguard',
        'internet_service_src_name', 'internet_service_src_group',
        'internet_service_src_custom', 'internet_service_src_custom_group',
        'network_service_src_dynamic', 'internet_service_src_fortiguard',
        'internet_service6_name', 'internet_service6_group',
        'internet_service6_custom', 'internet_service6_custom_group',
        'internet_service6_fortiguard',
        'internet_service6_src_name', 'internet_service6_src_group',
        'internet_service6_src_custom', 'internet_service6_src_custom_group',
        'internet_service6_src_fortiguard',
        'rtp_addr', 'ztna_ems_tag', 'ztna_ems_tag_secondary', 'ztna_geo_tag',
        'src_vendor_mac', 'poolname', 'poolname6', 'pcp_poolname',
        'users', 'groups', 'fsso_groups', 'ntlm_enabled_browsers',
        'custom_log_fields', 'sgt',
    }
    
    payload: dict[str, Any] = {}
    
    for param_name, value in params.items():
        if value is None:
            continue
        
        # Convert snake_case to kebab-case for FortiOS API
        api_key = param_name.replace("_", "-")
        
        # Normalize list parameters to FortiOS format
        if param_name in LIST_PARAMS:
            normalized = normalize_to_name_list(value)
            # Only add if normalization resulted in non-empty list
            if normalized:
                payload[api_key] = normalized
        else:
            payload[api_key] = value
    
    return payload
