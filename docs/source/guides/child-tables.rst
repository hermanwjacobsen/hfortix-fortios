Child Table Helpers
===================

**Simplified CRUD operations for nested configuration within singleton endpoints**

Overview
--------

Child table helpers provide a convenient API for managing nested child tables within FortiOS
singleton endpoints (endpoints without mkeys). These helpers enable granular CRUD operations
on child table entries without requiring full parent object updates.

.. note::
   Child table helpers are only generated for **router endpoints** in the CMDB category.
   This strategic focus provides maximum value (core networking functionality) with
   minimal maintenance overhead.

What are Child Tables?
----------------------

Child tables are nested configuration tables within a singleton parent endpoint. They allow
you to manage multiple sub-configurations (like BGP neighbors, OSPF areas, or RIP networks)
independently.

**Example: Router BGP Configuration**

The ``/api/v2/cmdb/router/bgp`` endpoint is a singleton (no mkey) that contains multiple
child tables:

- ``neighbor`` - BGP neighbor configurations
- ``network`` - Networks to advertise
- ``aggregate-address`` - Route aggregation rules
- ``redistribute`` - Route redistribution settings

Without child table helpers, you would need to:

1. GET the entire BGP configuration
2. Modify the nested child table array
3. PUT the entire configuration back

With child table helpers, you can directly:

.. code-block:: python

   # Add a BGP neighbor
   fgt.cmdb.router.bgp.neighbor.set(ip="10.0.0.1", remote_as=65001)
   
   # Get a specific neighbor
   neighbor = fgt.cmdb.router.bgp.neighbor.get(ip="10.0.0.1")
   
   # Delete a neighbor
   fgt.cmdb.router.bgp.neighbor.delete(ip="10.0.0.1")
   
   # List all neighbors
   neighbors = fgt.cmdb.router.bgp.neighbor.list()

Available Endpoints
-------------------

Child table helpers are available for the following router endpoints:

Router BFD
^^^^^^^^^^
- ``router.bfd.neighbor`` - BFD neighbor configurations

Router BFD6
^^^^^^^^^^^
- ``router.bfd6.neighbor`` - BFDv6 neighbor configurations

Router BGP
^^^^^^^^^^
- ``router.bgp.neighbor`` - BGP neighbors
- ``router.bgp.network`` - Networks to advertise
- ``router.bgp.aggregate_address`` - Route aggregation
- ``router.bgp.redistribute`` - Route redistribution
- ``router.bgp.confederation_peers`` - BGP confederation peers
- And 9+ more child tables

Router IS-IS
^^^^^^^^^^^^
- ``router.isis.isis_net`` - IS-IS network entities
- ``router.isis.isis_interface`` - IS-IS interfaces
- ``router.isis.summary_address`` - Route summarization
- ``router.isis.redistribute`` - Route redistribution
- And 2+ more child tables

Router Multicast
^^^^^^^^^^^^^^^^
- ``router.multicast.interface`` - Multicast interfaces
- ``router.multicast.pim_sm_global.rp_address`` - PIM-SM rendezvous points

Router Multicast6
^^^^^^^^^^^^^^^^^
- ``router.multicast6.interface`` - Multicast6 interfaces
- ``router.multicast6.pim_sm_global.rp_address`` - PIM-SM6 rendezvous points

Router OSPF
^^^^^^^^^^^
- ``router.ospf.area`` - OSPF areas
- ``router.ospf.network`` - OSPF networks
- ``router.ospf.neighbor`` - OSPF neighbors
- ``router.ospf.ospf_interface`` - OSPF interfaces
- ``router.ospf.redistribute`` - Route redistribution
- And 3+ more child tables

Router OSPF6
^^^^^^^^^^^^
- ``router.ospf6.area`` - OSPFv3 areas
- ``router.ospf6.ospf6_interface`` - OSPFv3 interfaces
- ``router.ospf6.redistribute`` - Route redistribution
- And 2+ more child tables

Router RIP
^^^^^^^^^^
- ``router.rip.neighbor`` - RIP neighbors
- ``router.rip.network`` - RIP networks
- ``router.rip.interface`` - RIP interfaces
- ``router.rip.redistribute`` - Route redistribution
- And 4+ more child tables

Router RIPng
^^^^^^^^^^^^
- ``router.ripng.neighbor`` - RIPng neighbors
- ``router.ripng.network`` - RIPng networks
- ``router.ripng.interface`` - RIPng interfaces
- ``router.ripng.redistribute`` - Route redistribution
- And 5+ more child tables

Basic Operations
----------------

All child table helpers provide these core methods:

set() - Create or Update Entry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new child table entry or update an existing one.

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   # Create a BGP neighbor
   fgt.cmdb.router.bgp.neighbor.set(
       ip="10.0.0.1",
       remote_as=65001,
       description="Core Router 1",
       next_hop_self="enable"
   )
   
   # Update the neighbor (same IP, different settings)
   fgt.cmdb.router.bgp.neighbor.set(
       ip="10.0.0.1",
       remote_as=65001,
       description="Updated description"
   )

get() - Retrieve Single Entry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a specific child table entry by its mkey.

.. code-block:: python

   # Get a specific BGP neighbor
   neighbor = fgt.cmdb.router.bgp.neighbor.get(ip="10.0.0.1")
   
   print(f"Remote AS: {neighbor.remote_as}")
   print(f"Description: {neighbor.description}")

delete() - Remove Entry
^^^^^^^^^^^^^^^^^^^^^^^

Delete a child table entry.

.. code-block:: python

   # Delete a BGP neighbor
   fgt.cmdb.router.bgp.neighbor.delete(ip="10.0.0.1")

list() - Get All Entries
^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve all entries in the child table.

.. code-block:: python

   # List all BGP neighbors
   neighbors = fgt.cmdb.router.bgp.neighbor.list()
   
   for neighbor in neighbors:
       print(f"{neighbor.ip} - AS{neighbor.remote_as}")

count() - Count Entries
^^^^^^^^^^^^^^^^^^^^^^^

Get the total number of entries in the child table.

.. code-block:: python

   # Count BGP neighbors
   neighbor_count = fgt.cmdb.router.bgp.neighbor.count()
   print(f"Total neighbors: {neighbor_count}")

exists() - Check Existence
^^^^^^^^^^^^^^^^^^^^^^^^^^

Check if a specific entry exists.

.. code-block:: python

   # Check if a neighbor exists
   if fgt.cmdb.router.bgp.neighbor.exists(ip="10.0.0.1"):
       print("Neighbor exists")
   else:
       print("Neighbor not found")

Practical Examples
------------------

Example 1: BGP Neighbor Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete workflow for managing BGP neighbors:

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   # Add multiple BGP neighbors
   neighbors_config = [
       {"ip": "10.0.0.1", "remote_as": 65001, "description": "Core Router 1"},
       {"ip": "10.0.0.2", "remote_as": 65001, "description": "Core Router 2"},
       {"ip": "10.0.0.3", "remote_as": 65002, "description": "Edge Router"},
   ]
   
   for config in neighbors_config:
       fgt.cmdb.router.bgp.neighbor.set(**config)
   
   # Verify all neighbors were created
   total = fgt.cmdb.router.bgp.neighbor.count()
   print(f"Total neighbors: {total}")
   
   # List all neighbors
   neighbors = fgt.cmdb.router.bgp.neighbor.list()
   for neighbor in neighbors:
       print(f"{neighbor.ip} - AS{neighbor.remote_as} - {neighbor.description}")
   
   # Update a specific neighbor
   fgt.cmdb.router.bgp.neighbor.set(
       ip="10.0.0.1",
       remote_as=65001,
       description="Updated: Core Router 1",
       weight=100
   )
   
   # Remove a neighbor
   fgt.cmdb.router.bgp.neighbor.delete(ip="10.0.0.3")

Example 2: OSPF Area Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure OSPF areas with different types:

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   # Create backbone area
   fgt.cmdb.router.ospf.area.set(
       id="0.0.0.0",
       type="regular"
   )
   
   # Create stub area
   fgt.cmdb.router.ospf.area.set(
       id="0.0.0.1",
       type="stub",
       default_cost=10
   )
   
   # Create NSSA area
   fgt.cmdb.router.ospf.area.set(
       id="0.0.0.2",
       type="nssa",
       nssa_default_information_originate="enable"
   )
   
   # List all areas
   areas = fgt.cmdb.router.ospf.area.list()
   for area in areas:
       print(f"Area {area.id}: {area.type}")
   
   # Check if specific area exists
   if fgt.cmdb.router.ospf.area.exists(id="0.0.0.1"):
       # Get area details
       area = fgt.cmdb.router.ospf.area.get(id="0.0.0.1")
       print(f"Stub area cost: {area.default_cost}")

Example 3: RIP Network Advertisement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add networks to RIP for advertisement:

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   # Add networks to advertise via RIP
   networks = [
       {"prefix": "192.168.1.0/24"},
       {"prefix": "192.168.2.0/24"},
       {"prefix": "10.0.0.0/8"},
   ]
   
   for network in networks:
       fgt.cmdb.router.rip.network.set(**network)
   
   # Verify networks
   rip_networks = fgt.cmdb.router.rip.network.list()
   print(f"Advertising {len(rip_networks)} networks:")
   for net in rip_networks:
       print(f"  - {net.prefix}")
   
   # Remove a network
   fgt.cmdb.router.rip.network.delete(prefix="10.0.0.0/8")

Example 4: IS-IS Interface Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure IS-IS on interfaces:

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   # Configure IS-IS on interfaces
   interfaces = [
       {
           "name": "port1",
           "circuit_type": "level-1-2",
           "metric_l1": 10,
           "metric_l2": 10
       },
       {
           "name": "port2",
           "circuit_type": "level-2",
           "metric_l2": 20
       },
   ]
   
   for intf in interfaces:
       fgt.cmdb.router.isis.isis_interface.set(**intf)
   
   # List configured interfaces
   isis_intfs = fgt.cmdb.router.isis.isis_interface.list()
   for intf in isis_intfs:
       print(f"{intf.name}: {intf.circuit_type}")

Best Practices
--------------

Use Specific Field Updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When updating entries, only specify fields you want to change:

.. code-block:: python

   # Good: Only update description
   fgt.cmdb.router.bgp.neighbor.set(
       ip="10.0.0.1",
       description="New description"
   )
   
   # Avoid: Setting all fields every time
   neighbor = fgt.cmdb.router.bgp.neighbor.get(ip="10.0.0.1")
   neighbor.description = "New description"
   fgt.cmdb.router.bgp.neighbor.set(**neighbor.to_dict())

Check Existence Before Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prevent errors by checking if entries exist:

.. code-block:: python

   # Check before deleting
   if fgt.cmdb.router.bgp.neighbor.exists(ip="10.0.0.1"):
       fgt.cmdb.router.bgp.neighbor.delete(ip="10.0.0.1")
       print("Neighbor deleted")
   else:
       print("Neighbor doesn't exist")

Handle Required Fields
^^^^^^^^^^^^^^^^^^^^^^

Always provide required fields (typically the mkey field):

.. code-block:: python

   # Required: IP address for BGP neighbor
   fgt.cmdb.router.bgp.neighbor.set(
       ip="10.0.0.1",  # Required mkey
       remote_as=65001  # Required field
   )

Use Count for Validation
^^^^^^^^^^^^^^^^^^^^^^^^

Verify operations completed successfully:

.. code-block:: python

   initial_count = fgt.cmdb.router.bgp.neighbor.count()
   
   # Add new neighbor
   fgt.cmdb.router.bgp.neighbor.set(ip="10.0.0.1", remote_as=65001)
   
   # Verify
   new_count = fgt.cmdb.router.bgp.neighbor.count()
   assert new_count == initial_count + 1, "Neighbor not added"

Error Handling
--------------

Common Errors
^^^^^^^^^^^^^

**Missing Required Fields**

.. code-block:: python

   try:
       fgt.cmdb.router.bgp.neighbor.set(ip="10.0.0.1")
   except Exception as e:
       # Error -56: Empty values not allowed (missing remote_as)
       print(f"Error: {e}")

**Invalid Field Values**

.. code-block:: python

   try:
       fgt.cmdb.router.bgp.neighbor.set(
           ip="10.0.0.1",
           remote_as="invalid"  # Should be integer
       )
   except Exception as e:
       # Error -651: Input value is invalid
       print(f"Error: {e}")

**Entry Not Found**

.. code-block:: python

   try:
       neighbor = fgt.cmdb.router.bgp.neighbor.get(ip="999.999.999.999")
   except Exception as e:
       # 404 Not Found
       print(f"Error: {e}")

Robust Error Handling Pattern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from hfortix_fortios import FortiOS
   from hfortix_core.exceptions import APIError
   
   fgt = FortiOS(host="192.168.1.99", token="your-token")
   
   def add_bgp_neighbor(ip, remote_as, **kwargs):
       """Safely add a BGP neighbor with error handling."""
       try:
           # Check if already exists
           if fgt.cmdb.router.bgp.neighbor.exists(ip=ip):
               print(f"Neighbor {ip} already exists, updating...")
           
           # Set neighbor
           fgt.cmdb.router.bgp.neighbor.set(
               ip=ip,
               remote_as=remote_as,
               **kwargs
           )
           
           # Verify
           if fgt.cmdb.router.bgp.neighbor.exists(ip=ip):
               print(f"Successfully configured neighbor {ip}")
               return True
           else:
               print(f"Failed to configure neighbor {ip}")
               return False
               
       except APIError as e:
           print(f"API Error: {e}")
           return False
       except Exception as e:
           print(f"Unexpected error: {e}")
           return False
   
   # Use the function
   add_bgp_neighbor("10.0.0.1", 65001, description="Core Router")

Limitations
-----------

Router-Only Scope
^^^^^^^^^^^^^^^^^

Child table helpers are only generated for router endpoints. Other endpoint categories
(system, firewall, etc.) were intentionally excluded to maintain a focused, high-value
feature set with minimal maintenance overhead.

**Available**: ``router/*`` endpoints (10 endpoints)

**Not Available**: ``system/*``, ``firewall/*``, ``user/*``, etc.

**Rationale**: Router endpoints provide core networking functionality with the highest
test success rate (93%) and clear use cases for granular child table management.

Single-Entry Limitations
^^^^^^^^^^^^^^^^^^^^^^^^^

Some child tables only support a single entry due to FortiOS limitations:

.. code-block:: python

   # Some child tables only allow one entry
   fgt.cmdb.router.rip.offset_list.set(id=1, offset=10)
   
   # Adding a second entry may fail with Error -61
   fgt.cmdb.router.rip.offset_list.set(id=2, offset=20)  # May fail

Always check the child table count before adding multiple entries.

Pre-Created Entries
^^^^^^^^^^^^^^^^^^^

Some child tables have pre-created entries that cannot be deleted (e.g., ``redistribute``
entries). Use the modify pattern instead:

.. code-block:: python

   # Get existing redistribute entry
   entry = fgt.cmdb.router.bgp.redistribute.get(name="connected")
   
   # Modify and update
   fgt.cmdb.router.bgp.redistribute.set(
       name="connected",
       status="enable",
       route_map="my-route-map"
   )

API Reference
-------------

Child table helpers are accessed via the endpoint path:

.. code-block:: python

   # Pattern: fgt.cmdb.{category}.{endpoint}.{child_table}.{method}()
   fgt.cmdb.router.bgp.neighbor.set(ip="10.0.0.1", remote_as=65001)

All helpers implement these methods:

.. py:method:: set(**kwargs)
   
   Create or update a child table entry.
   
   :param kwargs: Field values including the mkey field
   :return: API response object
   :raises APIError: If the operation fails

.. py:method:: get(**mkey)
   
   Retrieve a specific child table entry.
   
   :param mkey: The mkey value (e.g., ip="10.0.0.1")
   :return: Child table entry object
   :raises APIError: If entry not found

.. py:method:: delete(**mkey)
   
   Delete a child table entry.
   
   :param mkey: The mkey value
   :return: API response object
   :raises APIError: If deletion fails

.. py:method:: list()
   
   Get all entries in the child table.
   
   :return: List of child table entry objects

.. py:method:: count()
   
   Count total entries in the child table.
   
   :return: Integer count

.. py:method:: exists(**mkey)
   
   Check if an entry exists.
   
   :param mkey: The mkey value
   :return: Boolean (True if exists, False otherwise)

See Also
--------

- :doc:`/examples/router-bgp` - Complete BGP configuration examples
- :doc:`/examples/router-ospf` - OSPF configuration examples
- :doc:`/api-reference/cmdb/router` - Router endpoint API reference
- :doc:`/guides/validation` - Input validation and error handling
