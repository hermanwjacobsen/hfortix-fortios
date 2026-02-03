# Validation Examples

Examples of validation-aware code and handling validation errors.

## Handling Validation Errors

```python
from hfortix import FortiOS, ValidationError

fgt = FortiOS(host='192.168.1.99', token='token')

try:
    fgt.api.cmdb.firewall.address.post(
        name='a' * 100,  # Too long
        subnet='192.168.1.1/32'
    )
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    # Retry with valid data
    fgt.api.cmdb.firewall.address.post(
        name='valid-name',
        subnet='192.168.1.1/32'
    )
```

## Enum Validation

```python
try:
    fgt.api.cmdb.firewall.policy.post(
        name='test',
        action='invalid-action',  # Must be 'accept' or 'deny'
        srcintf=[{"name": "port1"}],
        dstintf=[{"name": "port2"}],
        srcaddr=[{"name": "all"}],
        dstaddr=[{"name": "all"}],
        service=[{"name": "ALL"}]
    )
except ValidationError as e:
    print(f"Invalid enum value: {e.message}")
```

## See Also

- [Validation Guide](/fortios/guides/validation.md)
