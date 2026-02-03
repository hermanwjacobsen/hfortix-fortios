Status
======

Configuration endpoint for user/fortitoken_cloud.

Python Attribute
----------------

.. code-block:: python

   fgt.api.monitor.user.fortitoken_cloud

Available Methods
-----------------

- ``get()`` - GET operation

Examples
--------

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host='192.168.1.99', token='your-token')

   # List all items
   items = fgt.api.monitor.user.fortitoken_cloud.get()



Method Reference
----------------

``get()``
^^^^^^^^^

.. code-block:: python

   get(
       payload_dict=None,
       raw_json=False,
       **kwargs
   )

Retrieve FortiToken Cloud service status.

