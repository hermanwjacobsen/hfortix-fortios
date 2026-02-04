# Firewall Policy Management

Complete guide to managing firewall policies using direct API access.

```{note}
v0.5.0 removed convenience wrappers. Use `fgt.api.cmdb.firewall.policy.*` methods instead.
```

## Overview

HFortix provides full type-safe access to FortiGate firewall policies with support for 150+ parameters and policy reordering capabilities.

## Quick Example

```python
from hfortix import FortiOS

fgt = FortiOS(host='192.168.1.99', token='token')

# Create firewall policy
policy = fgt.api.cmdb.firewall.policy.post(
    name='Allow-Web-Traffic',
    srcintf=[{"name": "port1"}],
    dstintf=[{"name": "port2"}],
    srcaddr=[{"name": "internal-network"}],
    dstaddr=[{"name": "web-server"}],
    service=[{"name": "HTTP"}, {"name": "HTTPS"}],
    action='accept',
    schedule='always',
    nat='enable'
)

# Check if policy exists
if fgt.api.cmdb.firewall.policy.exists(policyid=1):
    print("Policy exists!")

# Reorder policies (see Policy Ordering section below)
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    action='before',
    reference_policyid=50
)
```

## Policy Ordering

Firewall policies are evaluated **top-to-bottom** - the order matters! Use the `.move()` method to change policy execution order.

### Simple Moves (No Reference Needed!)

```python
# Move to top (first position)
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="top"
)

# Move to bottom (last position)
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="bottom"
)

# Move to specific position (1-based)
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position=5  # Will be the 5th policy
)
```

### Relative Moves (Reference Required)

```python
# Move policy 100 before policy 50
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="before",
    reference_policyid=50
)

# Move policy 100 after policy 75
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="after",
    reference_policyid=75
)
```

### Viewing Policy Order

```python
# Get policies in execution order
policies = fgt.api.cmdb.firewall.policy.get()

# Display execution order
for idx, policy in enumerate(policies, 1):
    print(f"Position {idx}: {policy.name} (ID: {policy.policyid})")
```

### Position Parameter Options

| Position | Description | Reference Required |
|----------|-------------|-------------------|
| `"top"` | Move to first position | No |
| `"bottom"` | Move to last position | No |
| `position=1` to `N+1` | Move to specific numbered position (1-based) | No |
| `"before"` | Move before another policy | Yes - `reference_policyid` |
| `"after"` | Move after another policy | Yes - `reference_policyid` |

```{important}
**Important Notes:**
- `.move()` changes **execution order**, not the policy ID
- The `policyid` remains the same after moving
- Integer positions use 1-based indexing (position=1 is first)
- Valid range: 1 to (current_count + 1)
- Filtering or sorting by policyid does NOT show execution order
- Always use `.get()` without filtering to see actual execution order
- Available on 561 endpoints that support the move action
```

### Availability

Check if an endpoint supports move:

```python
# Check class attribute
if fgt.api.cmdb.firewall.policy.SUPPORTS_MOVE:
    print("Move is supported!")
```

## Cloning Policies

```{warning}
The `.clone()` method has been removed due to unreliable FortiOS API support. While it works on some endpoints (like `firewall.address`), it fails on others (like `firewall.policy`) despite being in the schema.
```

### Manual Cloning Workaround

```python
# Get source policy
source = fgt.api.cmdb.firewall.policy.get(policyid=1)

# Create copy with new name
clone_data = source.model_dump(exclude={'policyid'})
clone_data['name'] = 'Copy-of-' + source.name

# Create new policy
new_policy = fgt.api.cmdb.firewall.policy.post(clone_data)
```

## Coming Soon

Detailed documentation including:
- All policy parameters
- Address and service object integration
- NAT configuration
- Security profiles
- Best practices

## Reference

For complete API documentation, see:
- [API Documentation](/fortios/api-documentation/index.rst)
