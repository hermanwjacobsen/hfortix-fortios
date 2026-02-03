# Code Examples

Practical code examples for common HFortix use cases.

```{eval-rst}
.. toctree::
   :maxdepth: 1

   basic-usage
   advanced-patterns
   error-handling
   validation
```

## Overview

The Examples section provides ready-to-use code for common scenarios:

**Basic Usage**
   Simple examples covering fundamental operations like creating firewall addresses,
   policies, and querying system status.

**Advanced Patterns**
   More complex examples including bulk operations, async usage, and integration patterns.

**Error Handling**
   Examples demonstrating different error handling strategies and best practices.

**Validation**
   Examples showing validation-aware code and handling validation errors.

## Quick Examples

### Creating a Firewall Address

```python
from hfortix import FortiOS

fgt = FortiOS(host='192.168.1.99', token='token')

# Create firewall address
fgt.api.cmdb.firewall.address.post(
    name='web-server',
    subnet='192.0.2.100/32',
    comment='Production web server'
)
```

### Creating a Firewall Policy

```python
# Using direct API method
policy = fgt.api.cmdb.firewall.policy.post(
    name='Allow-Web',
    srcintf=[{"name": "port1"}],
    dstintf=[{"name": "port2"}],
    srcaddr=[{"name": "all"}],
    dstaddr=[{"name": "web-server"}],
    service=[{"name": "HTTP"}, {"name": "HTTPS"}],
    action='accept'
)
```

### Querying System Status

```python
# Get system status (use dict access - Monitor fields may not have type hints)
status = fgt.api.monitor.system.status.get()
print(f"Hostname: {status['hostname']}")
print(f"Model: {status['model']}")
```

## Downloadable Examples

All examples are available in the repository:
- `examples/` directory
- Individual example scripts
- Complete working code

## See Also

- [Quick Start Guide](//fortios/getting-started/quickstart.md)
- [User Guide](//fortios/user-guide/index.rst)
- [Topic Guides](//fortios/guides/index.rst)
