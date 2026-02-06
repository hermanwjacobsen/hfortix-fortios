# Router Configuration Examples

Complete examples for managing FortiOS router configurations using child table helpers.

## BGP Configuration

### Basic BGP Neighbor Setup

```python
from hfortix_fortios import FortiOS

fgt = FortiOS(host="192.168.1.99", token="your-token")

# Add BGP neighbors
fgt.cmdb.router.bgp.neighbor.set(
    ip="10.0.0.1",
    remote_as=65001,
    description="Core Router 1",
    next_hop_self="enable",
    soft_reconfiguration="enable"
)

fgt.cmdb.router.bgp.neighbor.set(
    ip="10.0.0.2",
    remote_as=65001,
    description="Core Router 2",
    route_reflector_client="enable"
)

# Verify neighbors
neighbors = fgt.cmdb.router.bgp.neighbor.list()
print(f"Configured {len(neighbors)} BGP neighbors")
```

### BGP Network Advertisement

```python
# Advertise networks via BGP
networks = [
    {"prefix": "192.168.1.0/24"},
    {"prefix": "192.168.2.0/24"},
    {"prefix": "10.0.0.0/8"},
]

for net in networks:
    fgt.cmdb.router.bgp.network.set(**net)

# List advertised networks
bgp_networks = fgt.cmdb.router.bgp.network.list()
for net in bgp_networks:
    print(f"Advertising: {net.prefix}")
```

### BGP Route Aggregation

```python
# Configure route aggregation
fgt.cmdb.router.bgp.aggregate_address.set(
    prefix="10.0.0.0/8",
    summary_only="enable",
    as_set="enable"
)

# Verify aggregation
aggregates = fgt.cmdb.router.bgp.aggregate_address.list()
for agg in aggregates:
    print(f"Aggregate: {agg.prefix}")
```

## OSPF Configuration

### OSPF Area Configuration

```python
from hfortix_fortios import FortiOS

fgt = FortiOS(host="192.168.1.99", token="your-token")

# Configure OSPF backbone area
fgt.cmdb.router.ospf.area.set(
    id="0.0.0.0",
    type="regular"
)

# Configure stub area
fgt.cmdb.router.ospf.area.set(
    id="0.0.0.1",
    type="stub",
    default_cost=10,
    stub_type="summary"
)

# Configure NSSA area
fgt.cmdb.router.ospf.area.set(
    id="0.0.0.2",
    type="nssa",
    nssa_default_information_originate="enable",
    nssa_translator_role="candidate"
)

# List all OSPF areas
areas = fgt.cmdb.router.ospf.area.list()
for area in areas:
    print(f"Area {area.id}: {area.type}")
```

### OSPF Network Configuration

```python
# Add networks to OSPF areas
fgt.cmdb.router.ospf.network.set(
    prefix="192.168.1.0/24",
    area="0.0.0.0"
)

fgt.cmdb.router.ospf.network.set(
    prefix="10.0.0.0/8",
    area="0.0.0.1"
)

# Verify networks
networks = fgt.cmdb.router.ospf.network.list()
for net in networks:
    print(f"{net.prefix} in area {net.area}")
```

### OSPF Interface Configuration

```python
# Configure OSPF on interfaces
fgt.cmdb.router.ospf.ospf_interface.set(
    name="port1",
    interface="port1",
    cost=10,
    priority=100,
    authentication="md5",
    md5_key="secretkey123"
)

fgt.cmdb.router.ospf.ospf_interface.set(
    name="port2",
    interface="port2",
    cost=20,
    network_type="point-to-point"
)

# List OSPF interfaces
interfaces = fgt.cmdb.router.ospf.ospf_interface.list()
for intf in interfaces:
    print(f"{intf.name}: cost={intf.cost}")
```

## RIP Configuration

### RIP Network Setup

```python
from hfortix_fortios import FortiOS

fgt = FortiOS(host="192.168.1.99", token="your-token")

# Add networks to RIP
networks = [
    {"prefix": "192.168.1.0/24"},
    {"prefix": "192.168.2.0/24"},
    {"prefix": "10.0.0.0/8"},
]

for net in networks:
    fgt.cmdb.router.rip.network.set(**net)

# Verify RIP networks
rip_networks = fgt.cmdb.router.rip.network.list()
print(f"RIP advertising {len(rip_networks)} networks")
```

### RIP Interface Configuration

```python
# Configure RIP on interfaces
fgt.cmdb.router.rip.interface.set(
    name="port1",
    split_horizon="poisoned",
    authentication_mode="md5",
    authentication_key_string="secretkey"
)

fgt.cmdb.router.rip.interface.set(
    name="port2",
    send_version="2",
    receive_version="2"
)

# List RIP interfaces
interfaces = fgt.cmdb.router.rip.interface.list()
for intf in interfaces:
    print(f"RIP on {intf.name}")
```

### RIP Neighbor Configuration

```python
# Add static RIP neighbors
fgt.cmdb.router.rip.neighbor.set(ip="192.168.1.1")
fgt.cmdb.router.rip.neighbor.set(ip="192.168.2.1")

# Verify neighbors
neighbors = fgt.cmdb.router.rip.neighbor.list()
for neighbor in neighbors:
    print(f"RIP neighbor: {neighbor.ip}")
```

## IS-IS Configuration

### IS-IS Network Entity

```python
from hfortix_fortios import FortiOS

fgt = FortiOS(host="192.168.1.99", token="your-token")

# Configure IS-IS network entity
fgt.cmdb.router.isis.isis_net.set(
    net="49.0001.1921.6800.1001.00"
)

# Verify NET
nets = fgt.cmdb.router.isis.isis_net.list()
for net in nets:
    print(f"IS-IS NET: {net.net}")
```

### IS-IS Interface Configuration

```python
# Configure IS-IS on interfaces
fgt.cmdb.router.isis.isis_interface.set(
    name="port1",
    circuit_type="level-1-2",
    metric_l1=10,
    metric_l2=10,
    hello_interval_l1=10,
    hello_interval_l2=10
)

fgt.cmdb.router.isis.isis_interface.set(
    name="port2",
    circuit_type="level-2",
    metric_l2=20,
    priority_l2=64
)

# List IS-IS interfaces
interfaces = fgt.cmdb.router.isis.isis_interface.list()
for intf in interfaces:
    print(f"{intf.name}: {intf.circuit_type}")
```

### IS-IS Summary Addresses

```python
# Configure summary addresses
fgt.cmdb.router.isis.summary_address.set(
    prefix="192.168.0.0/16",
    level="level-2"
)

fgt.cmdb.router.isis.summary_address.set(
    prefix="10.0.0.0/8",
    level="level-1-2"
)

# Verify summaries
summaries = fgt.cmdb.router.isis.summary_address.list()
for summary in summaries:
    print(f"Summary: {summary.prefix} at {summary.level}")
```

## BFD Configuration

### BFD Neighbor Setup

```python
from hfortix_fortios import FortiOS

fgt = FortiOS(host="192.168.1.99", token="your-token")

# Configure BFD neighbors
fgt.cmdb.router.bfd.neighbor.set(
    ip="10.0.0.1",
    interface="port1"
)

fgt.cmdb.router.bfd.neighbor.set(
    ip="10.0.0.2",
    interface="port2"
)

# List BFD neighbors
neighbors = fgt.cmdb.router.bfd.neighbor.list()
for neighbor in neighbors:
    print(f"BFD neighbor: {neighbor.ip} on {neighbor.interface}")
```

### BFD6 (IPv6) Configuration

```python
# Configure BFD for IPv6
fgt.cmdb.router.bfd6.neighbor.set(
    ip6="2001:db8::1",
    interface="port1"
)

# Verify BFD6 neighbors
neighbors = fgt.cmdb.router.bfd6.neighbor.list()
for neighbor in neighbors:
    print(f"BFD6 neighbor: {neighbor.ip6}")
```

## Complete Example: Multi-Protocol Setup

### Full Router Configuration

```python
from hfortix_fortios import FortiOS

def configure_router(host, token):
    """Complete router configuration with BGP, OSPF, and BFD."""
    
    fgt = FortiOS(host=host, token=token)
    
    print("Configuring BGP...")
    # BGP neighbors
    bgp_neighbors = [
        {"ip": "10.0.0.1", "remote_as": 65001, "description": "Core-1"},
        {"ip": "10.0.0.2", "remote_as": 65001, "description": "Core-2"},
    ]
    for neighbor in bgp_neighbors:
        fgt.cmdb.router.bgp.neighbor.set(**neighbor)
    
    # BGP networks
    bgp_networks = [
        {"prefix": "192.168.1.0/24"},
        {"prefix": "192.168.2.0/24"},
    ]
    for network in bgp_networks:
        fgt.cmdb.router.bgp.network.set(**network)
    
    print("Configuring OSPF...")
    # OSPF areas
    fgt.cmdb.router.ospf.area.set(id="0.0.0.0", type="regular")
    fgt.cmdb.router.ospf.area.set(id="0.0.0.1", type="stub", default_cost=10)
    
    # OSPF networks
    ospf_networks = [
        {"prefix": "192.168.1.0/24", "area": "0.0.0.0"},
        {"prefix": "192.168.2.0/24", "area": "0.0.0.1"},
    ]
    for network in ospf_networks:
        fgt.cmdb.router.ospf.network.set(**network)
    
    print("Configuring BFD...")
    # BFD neighbors
    bfd_neighbors = [
        {"ip": "10.0.0.1", "interface": "port1"},
        {"ip": "10.0.0.2", "interface": "port2"},
    ]
    for neighbor in bfd_neighbors:
        fgt.cmdb.router.bfd.neighbor.set(**neighbor)
    
    # Verify configuration
    print("\nConfiguration Summary:")
    print(f"  BGP neighbors: {fgt.cmdb.router.bgp.neighbor.count()}")
    print(f"  BGP networks: {fgt.cmdb.router.bgp.network.count()}")
    print(f"  OSPF areas: {fgt.cmdb.router.ospf.area.count()}")
    print(f"  OSPF networks: {fgt.cmdb.router.ospf.network.count()}")
    print(f"  BFD neighbors: {fgt.cmdb.router.bfd.neighbor.count()}")

# Run configuration
configure_router("192.168.1.99", "your-token")
```

## Error Handling Examples

### Robust Configuration Function

```python
from hfortix_fortios import FortiOS
from hfortix_core.exceptions import APIError

def add_bgp_neighbor_safe(fgt, ip, remote_as, **kwargs):
    """Safely add BGP neighbor with comprehensive error handling."""
    
    try:
        # Check if neighbor exists
        if fgt.cmdb.router.bgp.neighbor.exists(ip=ip):
            print(f"Neighbor {ip} exists, updating...")
        else:
            print(f"Adding new neighbor {ip}...")
        
        # Set neighbor configuration
        fgt.cmdb.router.bgp.neighbor.set(
            ip=ip,
            remote_as=remote_as,
            **kwargs
        )
        
        # Verify operation
        neighbor = fgt.cmdb.router.bgp.neighbor.get(ip=ip)
        if neighbor.remote_as == remote_as:
            print(f"✓ Successfully configured neighbor {ip}")
            return True
        else:
            print(f"✗ Configuration mismatch for {ip}")
            return False
            
    except APIError as e:
        print(f"✗ API Error for {ip}: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error for {ip}: {e}")
        return False

# Usage
fgt = FortiOS(host="192.168.1.99", token="your-token")
add_bgp_neighbor_safe(fgt, "10.0.0.1", 65001, description="Core Router")
```

### Batch Configuration with Validation

```python
from hfortix_fortios import FortiOS

def batch_configure_ospf_areas(fgt, areas_config):
    """Configure multiple OSPF areas with validation."""
    
    success_count = 0
    fail_count = 0
    
    for area_cfg in areas_config:
        area_id = area_cfg["id"]
        try:
            fgt.cmdb.router.ospf.area.set(**area_cfg)
            
            # Verify
            if fgt.cmdb.router.ospf.area.exists(id=area_id):
                print(f"✓ Area {area_id} configured")
                success_count += 1
            else:
                print(f"✗ Area {area_id} verification failed")
                fail_count += 1
                
        except Exception as e:
            print(f"✗ Failed to configure area {area_id}: {e}")
            fail_count += 1
    
    print(f"\nResults: {success_count} success, {fail_count} failed")
    return success_count, fail_count

# Usage
fgt = FortiOS(host="192.168.1.99", token="your-token")

areas = [
    {"id": "0.0.0.0", "type": "regular"},
    {"id": "0.0.0.1", "type": "stub", "default_cost": 10},
    {"id": "0.0.0.2", "type": "nssa"},
]

batch_configure_ospf_areas(fgt, areas)
```

## See Also

- [Child Table Helpers Guide](../guides/child-tables.rst) - Complete reference
- [API Reference - Router](../api-reference/cmdb/router.rst) - Detailed API documentation
- [Error Handling](error-handling.md) - Error handling patterns
