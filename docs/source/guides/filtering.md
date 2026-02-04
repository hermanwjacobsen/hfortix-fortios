# Filtering, Sorting, and Formatting

Complete guide to querying and filtering FortiOS API results with advanced parameters.

## Overview

HFortix supports powerful query capabilities for list operations:

- **Filtering** - Find specific objects using comparison and pattern matching operators
- **Sorting** - Order results by any field in ascending or descending order
- **Formatting** - Return only specific fields to reduce bandwidth and improve performance
- **Pagination** - Retrieve results in manageable chunks using start/count parameters

All query parameters are first-class method parameters with full IDE autocomplete and type checking support.

```{note}
Advanced filtering, sorting, and formatting features require **FortiOS 6.4.2 or later**. 
Basic filtering with `==` operator is available in all FortiOS versions.
```

## Quick Examples

```python
from hfortix import FortiOS

fgt = FortiOS(host='192.168.1.99', token='token')

# Simple exact match filter
addresses = fgt.api.cmdb.firewall.address.get(
    filter='name==web-server'
)

# Complex filter with AND operator
policies = fgt.api.cmdb.firewall.policy.get(
    filter='srcintf==port1&action==accept'
)

# Sort results descending by policy ID
policies = fgt.api.cmdb.firewall.policy.get(
    sort='policyid,dsc'
)

# Return only specific fields
addresses = fgt.api.cmdb.firewall.address.get(
    format='name|subnet|comment'
)

# Combine all parameters
policies = fgt.api.cmdb.firewall.policy.get(
    filter='action==accept&status==enable',
    sort='policyid,asc',
    format='policyid|name|srcintf|dstintf',
    start=0,
    count=50
)
```

## Filter Operators

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Exact match (case-sensitive) | `name==web-server` |
| `!=` | Not equal to | `status!=disable` |
| `=@` | Contains substring | `name=@server` |
| `!@` | Does not contain | `comment!@test` |
| `<=` | Less than or equal | `timeout<=30` |
| `<` | Less than | `sessions<100` |
| `>=` | Greater than or equal | `priority>=5` |
| `>` | Greater than | `weight>10` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `&` | Logical AND | `status==enable&action==accept` |
| `,` | Logical OR | `srcintf==port1,srcintf==port2` |

### Filter Examples

**Exact match:**
```python
# Find address object by exact name
address = fgt.api.cmdb.firewall.address.get(
    filter='name==web-server'
)

# Find enabled policies with accept action
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable&action==accept'
)
```

**Pattern matching:**
```python
# Find addresses containing "server" in name
addresses = fgt.api.cmdb.firewall.address.get(
    filter='name=@server'
)

# Find addresses NOT containing "test"
addresses = fgt.api.cmdb.firewall.address.get(
    filter='name!@test'
)

# Find addresses with comments containing "production"
addresses = fgt.api.cmdb.firewall.address.get(
    filter='comment=@production'
)
```

**Inequality filters:**
```python
# Find policies NOT disabled
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status!=disable'
)

# Find policies NOT in port1
policies = fgt.api.cmdb.firewall.policy.get(
    filter='srcintf!=port1'
)
```

**Numeric comparisons:**
```python
# Find sessions with timeout >= 3600
sessions = fgt.api.cmdb.firewall.session.get(
    filter='timeout>=3600'
)

# Find policies with priority > 5
policies = fgt.api.cmdb.firewall.policy.get(
    filter='priority>5'
)
```

**Logical AND (multiple conditions must be true):**

The library supports both syntax formats for AND filtering:

```python
# Format 1: Implicit & separator (recommended - most convenient)
# The library automatically normalizes this to FortiOS format
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable&srcintf==port1'
)

# Format 2: Explicit &filter= separator (FortiOS native format)
# Both formats produce identical results
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable&filter=srcintf==port1'
)

# More examples with implicit syntax
# Addresses in specific subnet range with specific type
addresses = fgt.api.cmdb.firewall.address.get(
    filter='subnet=@192.168&type==ipmask'
)

# Three conditions combined
policies = fgt.api.cmdb.firewall.policy.get(
    filter='action==accept&status==enable&srcintf==port1'
)

# Multiple exclusions
addresses = fgt.api.cmdb.firewall.address.get(
    filter='name=@test&name!@web&name!@ftp'
)
```

> **Note:** Both `filter='a&b'` and `filter='a&filter=b'` syntaxes are supported and produce identical results. The library automatically normalizes the filter string internally to work with FortiOS's native format.

**Logical OR (any condition can be true):**
```python
# Policies from port1 OR port2
policies = fgt.api.cmdb.firewall.policy.get(
    filter='srcintf==port1,srcintf==port2'
)

# Multiple interface matches
policies = fgt.api.cmdb.firewall.policy.get(
    filter='srcintf==wan1,srcintf==wan2,srcintf==dmz'
)
```

```{note}
**Filter Syntax Normalization**

The library supports **4 different filter syntax formats** for AND operations, automatically normalizing them to FortiOS's native format. All formats produce identical results:

1. **Implicit & separator** (recommended - cleanest):
   ```python
   filter='name=@test&type==ipmask'
   ```

2. **Mixed implicit/explicit**:
   ```python
   filter='name=@test&filter=type==ipmask'
   ```

3. **Explicit with filter= prefix**:
   ```python
   filter='filter=name=@test&filter=type==ipmask'
   ```

4. **Prefix with implicit & separator**:
   ```python
   filter='filter=name=@test&type==ipmask'
   ```

**All 4 formats are equivalent** - use whichever feels most natural for your use case. The library automatically normalizes them internally.

**Complete example:**
```python
# All of these produce identical results:
addresses = fgt.api.cmdb.firewall.address.get(filter='name=@test&type==ipmask')
addresses = fgt.api.cmdb.firewall.address.get(filter='name=@test&filter=type==ipmask')
addresses = fgt.api.cmdb.firewall.address.get(filter='filter=name=@test&filter=type==ipmask')
addresses = fgt.api.cmdb.firewall.address.get(filter='filter=name=@test&type==ipmask')
```
```

## Sorting Results

Use the `sort` parameter to order results by any field.

**Sort syntax:**
- `field` - Sort ascending (default)
- `field,asc` - Sort ascending (explicit)
- `field,dsc` - Sort descending

**Sort examples:**
```python
# Sort by name (ascending, default)
addresses = fgt.api.cmdb.firewall.address.get(
    sort='name'
)

# Sort by policy ID descending
policies = fgt.api.cmdb.firewall.policy.get(
    sort='policyid,dsc'
)

# Sort by subnet ascending
addresses = fgt.api.cmdb.firewall.address.get(
    sort='subnet,asc'
)

# Combine with filter: enabled policies sorted by ID
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable',
    sort='policyid,asc'
)
```

## Formatting Output

Use the `format` parameter to return only specific fields. This reduces bandwidth and improves performance.

**Format syntax:**
- `field1|field2|field3` - Pipe-separated field names

**Format examples:**
```python
# Return only name and subnet
addresses = fgt.api.cmdb.firewall.address.get(
    format='name|subnet'
)

# Return minimal policy information
policies = fgt.api.cmdb.firewall.policy.get(
    format='policyid|name|action|status'
)

# Return only interface names
interfaces = fgt.api.cmdb.system.interface.get(
    format='name'
)

# Combine with filter and sort
policies = fgt.api.cmdb.firewall.policy.get(
    filter='action==accept',
    sort='policyid,dsc',
    format='policyid|name|srcintf|dstintf'
)
```

```{note}
Formatting is applied by FortiOS before returning results, reducing network transfer size.
All filtered fields are still accessible for filtering logic on the FortiOS side.
```

## Pagination

Use `start` and `count` parameters to retrieve results in chunks.

**Pagination parameters:**
- `start` - Zero-based index of first result (default: 0)
- `count` - Maximum number of results to return

```{note}
FortiOS returns all matching results by default (no implicit pagination).
Pagination is typically only needed for extremely large datasets (10,000+ objects).
```

**Pagination examples:**
```python
# Get first 50 addresses
addresses = fgt.api.cmdb.firewall.address.get(
    count=50
)

# Get next 50 addresses (51-100)
addresses = fgt.api.cmdb.firewall.address.get(
    start=50,
    count=50
)

# Get addresses 101-150
addresses = fgt.api.cmdb.firewall.address.get(
    start=100,
    count=50
)

# Combine with filtering
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable',
    start=0,
    count=25
)
```

## Complete Examples

### Example 1: Filter, Sort, and Format Addresses

```python
# Get production addresses, sorted by name, with minimal fields
addresses = fgt.api.cmdb.firewall.address.get(
    filter='comment=@production',
    sort='name,asc',
    format='name|subnet|comment'
)

for addr in addresses:
    print(f"{addr.name}: {addr.subnet}")
```

### Example 2: Find Specific Policies

```python
# Get enabled accept policies from specific interfaces
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable&action==accept&(srcintf==port1,srcintf==port2)',
    sort='policyid,asc',
    format='policyid|name|srcintf|dstintf|action'
)

for policy in policies:
    print(f"Policy {policy.policyid}: {policy.name}")
    print(f"  {policy.srcintf} -> {policy.dstintf}")
```

### Example 3: Paginated Results with All Features

```python
# Get first 25 enabled policies, sorted, with specific fields
policies = fgt.api.cmdb.firewall.policy.get(
    filter='status==enable',
    sort='policyid,dsc',
    format='policyid|name|srcintf|dstintf|action|status',
    start=0,
    count=25
)

print(f"Retrieved {len(policies)} policies")
for policy in policies:
    print(f"{policy.policyid}: {policy.name} ({policy.action})")
```

### Example 4: Search and Filter Addresses

```python
# Find all addresses in 192.168.x.x range, excluding test addresses
addresses = fgt.api.cmdb.firewall.address.get(
    filter='subnet=@192.168&comment!@test',
    sort='subnet,asc',
    format='name|subnet|comment'
)

for addr in addresses:
    print(f"{addr.name}: {addr.subnet}")
    if hasattr(addr, 'comment'):
        print(f"  Comment: {addr.comment}")
```

## Best Practices

### Performance Optimization

1. **Use format parameter** - Return only needed fields to reduce bandwidth
   ```python
   # Good - only retrieve needed fields
   policies = fgt.api.cmdb.firewall.policy.get(
       format='policyid|name|status'
   )
   
   # Avoid - retrieves all fields (larger payload)
   policies = fgt.api.cmdb.firewall.policy.get()
   ```

2. **Filter on FortiOS side** - Let FortiOS filter before returning results
   ```python
   # Good - FortiOS filters, returns only matches
   addresses = fgt.api.cmdb.firewall.address.get(
       filter='comment=@production'
   )
   
   # Avoid - retrieves all, filters in Python
   all_addresses = fgt.api.cmdb.firewall.address.get()
   prod_addresses = [a for a in all_addresses if 'production' in a.comment]
   ```

3. **Use pagination for large datasets** - Don't retrieve 10,000+ objects at once
   ```python
   # Good - retrieve in chunks
   for page in range(0, 10000, 100):
       batch = fgt.api.cmdb.firewall.address.get(start=page, count=100)
       process_batch(batch)
   ```

### Filter Efficiency

1. **Specific filters are faster** - Use exact matches when possible
   ```python
   # Fast - exact match
   address = fgt.api.cmdb.firewall.address.get(filter='name==web-server')
   
   # Slower - pattern matching
   addresses = fgt.api.cmdb.firewall.address.get(filter='name=@server')
   ```

2. **Combine filters efficiently** - Put most restrictive filters first
   ```python
   # Better - restrictive filter first
   policies = fgt.api.cmdb.firewall.policy.get(
       filter='policyid==100&status==enable'
   )
   
   # Less efficient - broad filter first
   policies = fgt.api.cmdb.firewall.policy.get(
       filter='status==enable&policyid==100'
   )
   ```

### Code Clarity

1. **Use descriptive filter strings** - Make intent clear
   ```python
   # Clear intent
   enabled_accept_policies = fgt.api.cmdb.firewall.policy.get(
       filter='status==enable&action==accept'
   )
   ```

2. **Break complex filters into variables** - Improve readability
   ```python
   # Complex filter as variable
   production_filter = 'comment=@production&status==enable&name!@test'
   
   addresses = fgt.api.cmdb.firewall.address.get(
       filter=production_filter,
       sort='name,asc',
       format='name|subnet|comment'
   )
   ```

## Version Compatibility

| Feature | FortiOS Version | Notes |
|---------|----------------|-------|
| Basic filtering (`==`) | All versions | Always available |
| Advanced operators | 6.4.2+ | `!=`, `=@`, `!@`, `<=`, `<`, `>=`, `>` |
| Sorting (`sort`) | 6.4.2+ | All fields supported |
| Formatting (`format`) | 6.4.2+ | Reduces bandwidth |
| Pagination | All versions | `start` and `count` always supported |

```{warning}
Using advanced operators on FortiOS < 6.4.2 may result in API errors or unexpected behavior.
Check your FortiOS version before using advanced filtering features.
```

## Troubleshooting

### No Results Returned

**Problem:** Filter returns empty list when objects exist

**Solutions:**
1. Check filter syntax - operators are case-sensitive
   ```python
   # Wrong
   filter='name=web-server'  # Missing second =
   
   # Correct
   filter='name==web-server'
   ```

2. Verify field names match FortiOS schema
   ```python
   # Check object structure first
   address = fgt.api.cmdb.firewall.address.get(name='test')
   print(vars(address))  # See all available fields
   ```

3. Check for case-sensitivity in exact matches
   ```python
   # Case-sensitive exact match
   filter='name==Web-Server'  # Won't match 'web-server'
   
   # Use contains for case-insensitive
   filter='name=@server'  # Matches 'web-server', 'Web-Server', etc.
   ```

### Format Parameter Not Working

**Problem:** All fields returned despite using `format` parameter

**Cause:** FortiOS < 6.4.2 or unsupported endpoint

**Solution:**
1. Check FortiOS version
2. Verify endpoint supports formatting
3. Filter in Python if needed:
   ```python
   all_data = fgt.api.cmdb.firewall.address.get()
   filtered = [{'name': a.name, 'subnet': a.subnet} for a in all_data]
   ```

## See Also

- [API Request Inspection](api-request-inspection.rst) - Debug filter parameters
- [Performance Guide](performance.md) - Optimize query performance
- [Firewall Policies](firewall-policies.md) - Policy-specific filtering examples
