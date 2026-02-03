# Advanced Patterns

Advanced usage patterns and techniques.

```{note}
Coming soon: Advanced examples including bulk operations, async patterns,
complex filtering, and integration strategies.
```

## Async Operations

```python
import asyncio
from hfortix import FortiOS

async def get_all_data(fgt):
    # Concurrent API calls
    addresses, policies, status = await asyncio.gather(
        fgt.api.cmdb.firewall.address.list_async(),
        fgt.api.cmdb.firewall.policy.list_async(),
        fgt.api.monitor.system.status.get_async()
    )
    return addresses, policies, status

fgt = FortiOS(host='192.168.1.99', token='token')
results = asyncio.run(get_all_data(fgt))
```

## Bulk Operations

```python
# Create multiple addresses
addresses_to_create = [
    {'name': f'server-{i}', 'subnet': f'10.0.1.{i}/32'}
    for i in range(1, 11)
]

for addr in addresses_to_create:
    fgt.api.cmdb.firewall.address.post(**addr)
```

## See Also

- [Basic Usage](/fortios/examples/basic-usage.md)
- [Async Guide](//fortios/user-guide/async-usage.md)
