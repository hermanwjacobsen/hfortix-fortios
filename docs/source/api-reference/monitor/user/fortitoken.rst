Activate
========

Configuration endpoint for user/fortitoken.

Python Attribute
----------------

.. code-block:: python

   fgt.api.monitor.user.fortitoken

Available Methods
-----------------

- ``post()`` - POST operation

Examples
--------

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host='192.168.1.99', token='your-token')

   # Create new item
   result = fgt.api.monitor.user.fortitoken.post(
       tokens='value',  # optional
   )


Method Reference
----------------

``post()``
^^^^^^^^^^

.. code-block:: python

   post(
       tokens=None,
       payload_dict=None,
       raw_json=False,
       **kwargs
   )

Activate a set of FortiTokens by serial number.

