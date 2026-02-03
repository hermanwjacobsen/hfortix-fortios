API Endpoints
=============

Complete catalog of all **1,348 FortiOS API endpoints** organized by API type.
Each endpoint provides standard HTTP methods (``.get()``, ``.post()``, ``.put()``, ``.delete()``) for direct API access.

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 📝 CMDB API (561 endpoints)
        :link: cmdb/index
        :link-type: doc

        **Configuration Management Database**
        
        Create, read, update, and delete FortiOS configuration objects including firewall policies, addresses, VPNs, routing, and system settings.

    .. grid-item-card:: 📊 Monitor API (490 endpoints)
        :link: monitor/index
        :link-type: doc

        **Status & Statistics**
        
        Real-time monitoring and statistics - system status, active sessions, routing tables, VPN tunnels, WiFi clients, and performance metrics.

    .. grid-item-card:: 📜 Log API (286 endpoints)
        :link: log/index
        :link-type: doc

        **Historical Data**
        
        Query historical logs and events - traffic logs, security events, system logs, UTM activity, and application logs.

    .. grid-item-card:: ⚙️ Service API (11 endpoints)
        :link: service/index
        :link-type: doc

        **Operations & Actions**
        
        System operations and administrative tasks - backups, restores, reboots, firmware updates, and maintenance.

Quick Navigation
----------------

.. toctree::
   :maxdepth: 1
   :caption: API Categories

   cmdb/index
   monitor/index
   log/index
   service/index

API Overview
------------

CMDB API - Configuration Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Configuration Management Database (CMDB)** API provides access to all FortiOS configuration settings with **561 endpoints** across categories:

* **Firewall**: Addresses, policies, services, VIPs, NAT, schedules
* **System**: Global settings, interfaces, routing, admin users, HA
* **VPN**: IPsec tunnels, SSL VPN, certificates, authentication
* **Wireless**: WiFi controllers, access points, SSIDs, profiles
* **Security Profiles**: IPS, antivirus, web filtering, application control, DLP
* **Network Services**: Routing (static, BGP, OSPF), DNS, DHCP, NTP
* **User Authentication**: LDAP, RADIUS, local users, SSO
* **Switch Controller**: Managed switches, VLANs, port policies
* **And much more...**

See :doc:`cmdb/index` for the complete list of CMDB endpoints.

Monitor API - Status & Statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Monitor** API provides real-time status information and statistics with **490 endpoints**:

* **System**: Status, resources, CPU/memory usage, disk space
* **Firewall**: Active sessions, policy counters, NAT translations
* **Router**: Routing tables, BGP neighbors, OSPF status
* **VPN**: Tunnel status, IPsec/SSL connections, certificates
* **WiFi**: Connected clients, AP status, signal strength
* **UTM**: IPS statistics, AV activity, web filter logs
* **Network**: Interface statistics, ARP tables, DHCP leases
* **Diagnostics**: Debug flows, packet capture, connectivity tests

See :doc:`monitor/index` for the complete list of Monitor endpoints.

Log API - Historical Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

The **Log** API provides access to historical logs and events with **286 endpoints**:

* **Traffic Logs**: Connection logs, bandwidth usage
* **Security Events**: IPS alerts, AV detections, intrusion attempts
* **System Logs**: Admin actions, configuration changes
* **UTM Logs**: Web filter, application control, email filter
* **Event Logs**: System events, HA events, VPN events
* **Query Capabilities**: Filtering, sorting, time ranges

See :doc:`log/index` for log query capabilities and endpoint details.

Service API - Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

The **Service** API provides operational commands with **11 endpoints**:

* **Backup/Restore**: Configuration backups, system restore
* **System Control**: Reboot, shutdown, factory reset
* **Updates**: Firmware updates, signature updates
* **Diagnostics**: System diagnostics, troubleshooting tools
* **Maintenance**: Log rotation, database cleanup

See :doc:`service/index` for operational endpoint details.

Usage Examples
--------------

**CMDB - Create Firewall Address:**

.. code-block:: python

    fgt.api.cmdb.firewall.address.post(
        name="web-server",
        subnet="10.0.1.100/32",
        comment="Production web server"
    )

**Monitor - Get System Status:**

.. code-block:: python

    status = fgt.api.monitor.system.status.get()
    print(f"Hostname: {status['hostname']}, Version: {status['version']}")

**Log - Query Traffic Logs:**

.. code-block:: python

    logs = fgt.api.log.memory.traffic.forward.get(
        rows=100,
        filter="dstip==10.0.1.100"
    )

**Service - Backup Configuration:**

.. code-block:: python

    backup = fgt.api.service.system.config.backup()
