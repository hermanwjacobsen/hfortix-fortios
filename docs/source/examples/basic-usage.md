# Basic Usage Examples

Simple examples for getting started with HFortix.

## Connection and Authentication

### Basic Connection

```python
from hfortix import FortiOS

# Production connection with SSL verification
fgt = FortiOS(
    host='fortigate.company.com',
    token='your-api-token',
    verify=True
)

# Development connection (self-signed cert)
fgt_dev = FortiOS(
    host='192.168.1.99',
    token='your-api-token',
    verify=False
)
```

### Environment Variables

```python
import os
from dotenv import load_dotenv
from hfortix import FortiOS

load_dotenv()

fgt = FortiOS(
    host=os.getenv('FORTIGATE_HOST'),
    token=os.getenv('FORTIGATE_TOKEN'),
    verify=os.getenv('FORTIGATE_VERIFY_SSL', 'true').lower() == 'true'
)
```

## Firewall Addresses

### Create Address

```python
# Create a single host address
fgt.api.cmdb.firewall.address.post(
    name='web-server',
    subnet='192.0.2.100/32',
    comment='Production web server'
)

# Create a network address
fgt.api.cmdb.firewall.address.post(
    name='internal-network',
    subnet='10.0.0.0/8',
    comment='Internal network range'
)
```

### List Addresses

```python
# List all addresses
addresses = fgt.api.cmdb.firewall.address.get()

for addr in addresses:
    print(f"{addr['name']}: {addr.get('subnet', 'N/A')}")

# Filter addresses
web_servers = fgt.api.cmdb.firewall.address.get(
    filter='name=@server'
)
```

### Update Address

```python
# Update comment
fgt.api.cmdb.firewall.address.put(
    name='web-server',
    comment='Updated web server address'
)
```

### Delete Address

```python
# Delete address
fgt.api.cmdb.firewall.address.delete(name='web-server')
```

## Firewall Policies

### Create Policy

```python
# Simple list format (recommended) - auto-converted to dict format
policy = fgt.api.cmdb.firewall.policy.post(
    name='Allow-HTTP',
    srcintf=['port1'],           # Converted to [{'name': 'port1'}]
    dstintf=['port2'],           # Converted to [{'name': 'port2'}]
    srcaddr=['all'],             # Converted to [{'name': 'all'}]
    dstaddr=['web-server'],      # Converted to [{'name': 'web-server'}]
    service=['HTTP'],            # Converted to [{'name': 'HTTP'}]
    action='accept',
    schedule='always',
    nat='disable'
)

# Or explicit dict format (also supported)
policy = fgt.api.cmdb.firewall.policy.post(
    name='Allow-HTTP',
    srcintf=[{'name': 'port1'}],
    dstintf=[{'name': 'port2'}],
    srcaddr=[{'name': 'all'}],
    dstaddr=[{'name': 'web-server'}],
    service=[{'name': 'HTTP'}],
    action='accept'
)
```

### List Policies

```python
# List all policies
policies = fgt.api.cmdb.firewall.policy.get()

for policy in policies:
    print(f"Policy {policy['policyid']}: {policy.get('name', 'Unnamed')}")

# Filter enabled policies
enabled_policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable'
)
```

## System Operations

### Get System Status

```python
# Get system information (use dict access - Monitor fields may not have type hints)
status = fgt.api.monitor.system.status.get()

print(f"Hostname: {status['hostname']}")
print(f"Model: {status['model']}")
print(f"Model Number: {status.get('model_number', 'N/A')}")
```

### List Interfaces

```python
# List all interfaces
interfaces = fgt.api.cmdb.system.interface.get()

for iface in interfaces:
    print(f"{iface['name']}: {iface.get('ip', 'N/A')}")
```

### Get Interface Statistics

```python
# Get interface statistics
stats = fgt.api.monitor.system.interface.get()

for stat in stats:
    print(f"{stat['name']}:")
    print(f"  RX bytes: {stat.get('rx_bytes', 0)}")
    print(f"  TX bytes: {stat.get('tx_bytes', 0)}")
```

## Schedules

### Create Recurring Schedule

```python
# Business hours schedule
schedule = fgt.api.cmdb.firewall.schedule.recurring.post(
    name='business-hours',
    day='monday tuesday wednesday thursday friday',
    start='08:00',
    end='18:00'
)
```

### Create One-Time Schedule

```python
# Maintenance window
maintenance = fgt.api.cmdb.firewall.schedule.onetime.post(
    name='maintenance-jan-2026',
    start='2026-01-15 22:00',
    end='2026-01-16 02:00'
)
```

## Services

### Create Custom Service

```python
# TCP service
service = fgt.api.cmdb.firewall.service.custom.post(
    name='custom-app',
    protocol='TCP/UDP/SCTP',
    tcp_portrange='8080-8090',
    comment='Custom application'
)

# UDP service
dns_service = fgt.api.cmdb.firewall.service.custom.post(
    name='custom-dns',
    protocol='TCP/UDP/SCTP',
    udp_portrange='5353'
)
```

### Create Service Group

```python
# Group multiple services
web_services = fgt.api.cmdb.firewall.service.group.post(
    name='web-services',
    member=[{"name": "HTTP"}, {"name": "HTTPS"}, {"name": "custom-app"}]
)
```

## Complete Example

```python
from hfortix import FortiOS, APIError
import os
from dotenv import load_dotenv

def main():
    # Load environment
    load_dotenv()
    
    # Connect
    fgt = FortiOS(
        host=os.getenv('FORTIGATE_HOST'),
        token=os.getenv('FORTIGATE_TOKEN'),
        verify=False
    )
    
    try:
        # Create address
        fgt.api.cmdb.firewall.address.post(
            name='app-server',
            subnet='10.0.1.100/32',
            comment='Application server'
        )
        print("✓ Created address")
        
        # Create policy
        fgt.api.cmdb.firewall.policy.post(
            name='Allow-App-Access',
            srcintf=[{"name": "internal"}],
            dstintf=[{"name": "dmz"}],
            srcaddr=[{"name": "all"}],
            dstaddr=[{"name": "app-server"}],
            service=[{"name": "HTTPS"}],
            action='accept'
        )
        print("✓ Created policy")
        
        # Get status
        status = fgt.api.monitor.system.status.get()
        print(f"✓ Connected to {status['hostname']}")
        
    except APIError as e:
        print(f"✗ Error: {e.message}")

if __name__ == '__main__':
    main()
```

## See Also

- [Advanced Patterns](/fortios/examples/advanced-patterns.md)
- [Error Handling Examples](/fortios/examples/error-handling.md)
- [Quick Start Guide](//fortios/getting-started/quickstart.md)
