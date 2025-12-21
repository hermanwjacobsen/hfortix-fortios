#!/usr/bin/env python3
"""Test firewall policy wrapper normalization"""

# Simulate the _normalize_to_name_list function
def _normalize_to_name_list(value):
    """Test the normalization function"""
    if value is None:
        return []
    
    # Already a list
    if isinstance(value, list):
        if not value:
            return []
        # If first item is a dict, assume whole list is dicts
        if isinstance(value[0], dict):
            filtered = [
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


# Test cases
print("Test 1 - String input:")
result = _normalize_to_name_list("any")
print(f"  Input: 'any'")
print(f"  Output: {result}")
print()

print("Test 2 - List of strings:")
result = _normalize_to_name_list(["any"])
print(f"  Input: ['any']")
print(f"  Output: {result}")
print()

print("Test 3 - Multiple strings:")
result = _normalize_to_name_list(["port1", "port2"])
print(f"  Input: ['port1', 'port2']")
print(f"  Output: {result}")
print()

print("Test 4 - Dict input:")
result = _normalize_to_name_list({"name": "any"})
print(f"  Input: {{'name': 'any'}}")
print(f"  Output: {result}")
print()

print("Test 5 - List of dicts:")
result = _normalize_to_name_list([{"name": "any"}])
print(f"  Input: [{{'name': 'any'}}]")
print(f"  Output: {result}")
print()

# Build a test policy data structure
policy_data = {
    "name": "Test-Policy",
    "srcintf": _normalize_to_name_list("any"),
    "dstintf": _normalize_to_name_list("any"),
    "srcaddr": _normalize_to_name_list("all"),
    "dstaddr": _normalize_to_name_list("all"),
    "service": _normalize_to_name_list("ALL"),
    "schedule": "always",
    "action": "accept",
    "status": "enable"
}

print("Complete policy data structure:")
import json
print(json.dumps(policy_data, indent=2))
