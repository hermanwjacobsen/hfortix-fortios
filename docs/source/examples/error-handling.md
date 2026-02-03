# Error Handling Examples

Practical examples of error handling strategies.

## Basic Exception Handling

```python
from hfortix import FortiOS, APIError, DuplicateEntryError, ResourceNotFoundError

fgt = FortiOS(host='192.168.1.99', token='token')

try:
    fgt.api.cmdb.firewall.address.post(
        name='test-server',
        subnet='10.0.0.1/32'
    )
except DuplicateEntryError:
    print("Address already exists, updating instead")
    fgt.api.cmdb.firewall.address.put(
        name='test-server',
        comment='Updated'
    )
except APIError as e:
    print(f"API Error: {e.message} (Code: {e.error_code})")
```

## Return Mode Error Handling

```python
# Configure client to return errors instead of raising
fgt_return = FortiOS(host='192.168.1.99', token='token', error_mode='return')

result = fgt_return.api.cmdb.firewall.policy.post(
    name='test-policy',
    srcintf=[{"name": "port1"}],
    dstintf=[{"name": "port2"}],
    srcaddr=[{"name": "all"}],
    dstaddr=[{"name": "all"}],
    service=[{"name": "ALL"}],
    action='accept'
)

if result.get('error'):
    print(f"Error creating policy: {result['error']}")
else:
    print(f"Policy created: {result}")
```

## See Also

- [Error Handling Guide](/fortios/user-guide/error-handling.md)
- [Exception Reference](/fortios/api-reference/exceptions.rst)
