API Reference
=============

Complete SDK reference documentation for classes, methods, and type definitions in the HFortix-FortiOS library.

.. note::
   
   Looking for **API endpoints** (CMDB, Monitor, Log, Service)?
   See :doc:`/endpoints/index` for the complete endpoint catalog.

SDK Components
--------------

Main Client Classes
^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated
   :nosignatures:

   hfortix_fortios.FortiOS
   hfortix_fortios.AsyncFortiOS

These are the main entry points for interacting with FortiOS devices.

**FortiOS** - Synchronous client for blocking I/O operations.

**AsyncFortiOS** - Asynchronous client for concurrent operations with asyncio.

API Handlers
^^^^^^^^^^^^

The API handlers provide access to the four main API categories:

* **CMDB Handler** - Configuration management (561 endpoints)
* **Monitor Handler** - Status and statistics (490 endpoints)  
* **Log Handler** - Historical data queries (286 endpoints)
* **Service Handler** - Operations and actions (11 endpoints)

See :doc:`/endpoints/index` for complete endpoint documentation.

Configuration & Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated
   :nosignatures:

   hfortix_fortios.Config
   hfortix_fortios.AuthConfig

These classes handle client configuration and authentication settings.

Transactions & Batch Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated
   :nosignatures:

   hfortix_fortios.Transaction
   hfortix_fortios.BatchOperation

Support for atomic configuration changes and batch operations.

Error Handling
^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated
   :nosignatures:

   hfortix_fortios.FortiOSError
   hfortix_fortios.AuthenticationError
   hfortix_fortios.ValidationError
   hfortix_fortios.APIError

Exception classes for handling errors.

Type Definitions
^^^^^^^^^^^^^^^^

The library includes comprehensive type hints for all endpoints and operations.
See the individual endpoint documentation for parameter types and return types.

Advanced Features
-----------------

Observability & Debugging
^^^^^^^^^^^^^^^^^^^^^^^^^^

The SDK includes built-in observability features for monitoring API interactions:

* **Request/Response Logging** - Track all API calls
* **Performance Metrics** - Monitor API latency and throughput
* **Audit Trail** - Record configuration changes
* **Debug Mode** - Detailed diagnostic output

See :doc:`/guides/observability` for details.

FortiManager Proxy
^^^^^^^^^^^^^^^^^^

Manage multiple FortiGates through FortiManager with automatic ADOM and device routing:

.. code-block:: python

   from hfortix_fortios import FortiOS

   # Connect through FortiManager
   fgt = FortiOS.from_fortimanager(
       fmg_host="fortimanager.example.com",
       fmg_token="fmg-token",
       adom="root",
       device="FortiGate-1"
   )

See :doc:`/guides/fmg-proxy` for complete documentation.

Custom Wrappers
^^^^^^^^^^^^^^^

Build your own high-level abstractions and convenience methods:

.. code-block:: python

   from hfortix_fortios import FortiOS

   class MyFortiGate(FortiOS):
       def create_datacenter_policy(self, name, servers):
           """Custom wrapper for datacenter policies."""
           # Implementation here
           pass

See :doc:`/guides/custom-wrappers` for patterns and examples.
