# Reordering Objects with .move()

Learn how to reorder FortiOS configuration objects using the `.move()` method.

## Overview

The `.move()` method allows you to change the execution order of configuration objects. This is critical for:

- **Firewall Policies**: Evaluated top-to-bottom, first match wins
- **Route Policies**: Order determines routing decisions
- **NAT Policies**: First matching rule is applied
- **Other Sequential Objects**: 561 endpoints support reordering

```{important}
**Order Matters!** 
- FortiOS evaluates many object types sequentially from top to bottom
- The `.move()` method changes **execution order**, not object IDs
- Object identifiers (policyid, id, seq-num, etc.) remain unchanged
```

## Position Parameter

The `position` parameter supports multiple ways to specify where to move an object:

| Position Type | Example | Description | Reference Required? |
|--------------|---------|-------------|-------------------|
| **String: "before"** | `position="before"` | Move before another object | Yes - `reference_policyid` |
| **String: "after"** | `position="after"` | Move after another object | Yes - `reference_policyid` |
| **String: "top"** | `position="top"` | Move to first position | No - auto-determined |
| **String: "bottom"** | `position="bottom"` | Move to last position | No - auto-determined |
| **Integer: 1-based** | `position=5` | Move to specific position | No - calculated automatically |

## Basic Usage

### Move to Top (Simplest!)

```python
from hfortix import FortiOS

fgt = FortiOS(host='192.168.1.99', token='token')

# Move to first position - no reference needed!
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="top"
)
# Result: FortiOS(status=success, http=200, mkey=100, vdom=root)
```

### Move to Bottom

```python
# Move to last position - no reference needed!
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="bottom"
)
```

### Move to Specific Position (New!)

```python
# Move to 5th position using 1-based indexing
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position=5  # Will be the 5th policy in execution order
)

# Move to first position (equivalent to position="top")
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position=1
)
```

### Move Before Another Object

```python
# Move policy 100 to execute before policy 50
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="before",
    reference_policyid=50
)
```

### Move After Another Object

```python
# Move policy 100 to execute after policy 75
result = fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="after",
    reference_policyid=75
)
```

## Common Patterns

### Viewing Execution Order

```python
# Get all policies in their current execution order
policies = fgt.api.cmdb.firewall.policy.get()

print("Policy Execution Order:")
for idx, policy in enumerate(policies, 1):
    print(f"  Position {idx}: {policy.name} (ID: {policy.policyid})")
```

**Output Example:**
```
Policy Execution Order:
  Position 1: Block-Malicious-IPs (ID: 5)
  Position 2: Allow-Web-Traffic (ID: 100)
  Position 3: Allow-Internal (ID: 50)
  Position 4: Deny-All (ID: 1)
```

## Advanced Examples

### Organize Policies by Priority

```python
# Move all security policies to the top
security_policies = fgt.api.cmdb.firewall.policy.get(filter='name=@Security')

for idx, policy in enumerate(security_policies, 1):
    # Use numbered position for precise placement
    fgt.api.cmdb.firewall.policy.move(
        policyid=policy.policyid,
        position=idx  # Position 1, 2, 3, etc.
    )
```

### Insert Policy at Specific Position

```python
# Insert new policy at position 5
new_policy_id = 100

fgt.api.cmdb.firewall.policy.move(
    policyid=new_policy_id,
    position=5  # Simple! No need to fetch current policies
)
```

### Reorder Multiple Policies

```python
# Define desired order by policyid
desired_order = [10, 20, 5, 15, 30]

# Reorder to match desired sequence using numbered positions
for target_position, policyid in enumerate(desired_order, 1):
    fgt.api.cmdb.firewall.policy.move(
        policyid=policyid,
        position=target_position  # 1, 2, 3, 4, 5
    )
```

### Move Policy Relative to Current Position

```python
# Get current order
policies = fgt.api.cmdb.firewall.policy.get()
policy_ids = [p.policyid for p in policies]

# Find current position of policy 100
current_pos = policy_ids.index(100) + 1  # Convert to 1-based

# Move up 2 positions
new_position = max(1, current_pos - 2)
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position=new_position
)
```

### Swap Two Policies

```python
# Swap positions of policies 100 and 200
policies = fgt.api.cmdb.firewall.policy.get()
policy_ids = [p.policyid for p in policies]

pos_100 = policy_ids.index(100) + 1
pos_200 = policy_ids.index(200) + 1

# Move 100 to where 200 was
fgt.api.cmdb.firewall.policy.move(policyid=100, position=pos_200)

# Move 200 to where 100 was
fgt.api.cmdb.firewall.policy.move(policyid=200, position=pos_100)
```

## Supported Endpoints

The `.move()` method is available on **561 endpoints** across FortiOS. Common examples:

### Firewall
- `firewall.policy` - Security policies
- `firewall.local-in-policy` - Local-in policies
- `firewall.proxy-policy` - Proxy policies
- `firewall.central-snat-map` - Central SNAT mapping

### Router
- `router.policy` - Route policies (IPv4)
- `router.policy6` - Route policies (IPv6)
- `router.static` - Static routes
- `router.static6` - Static routes (IPv6)

### NAT
- `firewall.ippool` - IP pools
- `firewall.vip` - Virtual IPs

### Check Availability

```python
# Check if endpoint supports move
if fgt.api.cmdb.firewall.policy.SUPPORTS_MOVE:
    print("Move is supported!")
    
# All 561 endpoints expose this attribute
print(f"Move supported: {fgt.api.cmdb.router.policy.SUPPORTS_MOVE}")
```

## Important Notes

```{warning}
**Common Mistakes:**

1. **Don't sort by ID to view order**
   ```python
   # ❌ WRONG - This shows policies sorted by ID, not execution order
   policies = sorted(fgt.api.cmdb.firewall.policy.get(), key=lambda p: p.policyid)
   
   # ✅ CORRECT - This shows actual execution order
   policies = fgt.api.cmdb.firewall.policy.get()
   ```

2. **IDs don't change after move**
   ```python
   # policyid 100 stays 100 even after moving to position 1
   # Only the POSITION changes, not the identifier
   ```

3. **Filtering affects what you see**
   ```python
   # ❌ WRONG - Filtered results don't show full execution order
   web_policies = fgt.api.cmdb.firewall.policy.get(filter='name=@web')
   
   # ✅ CORRECT - Get all policies to see complete order
   all_policies = fgt.api.cmdb.firewall.policy.get()
   ```

4. **Position validation**
   ```python
   # Position must be >= 1 (1-based indexing)
   fgt.api.cmdb.firewall.policy.move(policyid=100, position=0)  # ❌ ValueError
   
   # Position must be <= (total_count + 1)
   # If there are 10 policies, valid range is 1-11
   fgt.api.cmdb.firewall.policy.move(policyid=100, position=50)  # ❌ ValueError
   ```
```

## Position Parameter Reference

### String Positions

| Value | Behavior | Reference Required | Example |
|-------|----------|-------------------|---------|
| `"before"` | Move before specified object | ✅ Yes | `position="before", reference_policyid=50` |
| `"after"` | Move after specified object | ✅ Yes | `position="after", reference_policyid=75` |
| `"top"` | Move to first position | ❌ No | `position="top"` |
| `"bottom"` | Move to last position | ❌ No | `position="bottom"` |

### Integer Positions (1-based)

| Value | Behavior | Valid Range |
|-------|----------|-------------|
| `1` | Move to first position (same as "top") | Always valid |
| `2` to `N` | Move to specific position | Must be ≤ current count |
| `N+1` | Move to last position (same as "bottom") | Must be = count + 1 |

**Examples:**
```python
# If there are 10 policies currently:
position=1    # ✅ Move to first position
position=5    # ✅ Move to 5th position
position=10   # ✅ Move to 10th position (last)
position=11   # ✅ Move after all (new last position)
position=12   # ❌ ValueError: out of range
position=0    # ❌ ValueError: must be >= 1
```

## Virtual Domains (VDOMs)

When using VDOMs, specify the target domain:

```python
# Move policy in specific VDOM
fgt.api.cmdb.firewall.policy.move(
    policyid=100,
    position="before",
    reference_policyid=50,
    vdom='customer1'
)

# Move across all VDOMs (admin access required)
for vdom in ['customer1', 'customer2', 'customer3']:
    fgt.api.cmdb.firewall.policy.move(
        policyid=100,
        position="top",
        vdom=vdom
    )
```

## Error Handling

```python
try:
    result = fgt.api.cmdb.firewall.policy.move(
        policyid=100,
        action='before',
        reference_policyid=50
    )
    print(f"Success: {result.status}")
except Exception as e:
    if '404' in str(e):
        print("Policy not found - check policyid")
    elif '424' in str(e):
        print("Invalid reference_policyid")
    else:
        print(f"Move failed: {e}")
```

## Performance Considerations

- Move operations are typically fast (<100ms)
- No configuration backup is triggered
- Changes are immediate (no commit required)
- Safe to use in automation scripts
- Can be used in loops for bulk reordering

## See Also

- [Firewall Policy Management](firewall-policies.md) - Complete policy guide
- [API Documentation](/fortios/api-documentation/index.rst) - Full API reference
- [Filtering](filtering.md) - Query and filter objects
