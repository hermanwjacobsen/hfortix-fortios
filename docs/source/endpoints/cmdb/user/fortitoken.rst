Fortitoken
==========

Configuration endpoint for user/fortitoken.

Python Attribute
----------------

.. code-block:: python

   fgt.api.cmdb.user.fortitoken

Available Methods
-----------------

- ``get()`` - GET operation
- ``post()`` - POST operation
- ``put()`` - PUT operation
- ``delete()`` - DELETE operation

Examples
--------

.. code-block:: python

   from hfortix_fortios import FortiOS
   
   fgt = FortiOS(host='192.168.1.99', token='your-token')

   # List all items
   items = fgt.api.cmdb.user.fortitoken.get()


   # Create new item
   result = fgt.api.cmdb.user.fortitoken.post(
       nkey='value',  # optional
       serial_number='value',  # optional
       status='value',  # optional
   )

   # Update existing item
   result = fgt.api.cmdb.user.fortitoken.put(
       serial_number='updated-value',
       status='updated-value',
       seed='updated-value',
       comments='updated-value',
   )

   # Delete item
   result = fgt.api.cmdb.user.fortitoken.delete()


Method Reference
----------------

``get()``
^^^^^^^^^

.. code-block:: python

   get(
       serial_number=None,
       payload_dict=None,
       attr=None,
       skip_to_datasource=None,
       acs=None,
       search=None,
       vdom=None,
       raw_json=False,
       **kwargs
   )

Select a specific entry from a CLI table.


``post()``
^^^^^^^^^^

.. code-block:: python

   post(
       payload_dict=None,
       nkey=None,
       serial_number=None,
       status=None,
       seed=None,
       comments=None,
       license=None,
       activation_code=None,
       activation_expire=None,
       reg_id=None,
       os_ver=None,
       vdom=None,
       raw_json=False,
       **kwargs
   )

Create object(s) in this table.


``put()``
^^^^^^^^^

.. code-block:: python

   put(
       serial_number=None,
       payload_dict=None,
       before=None,
       after=None,
       status=None,
       seed=None,
       comments=None,
       license=None,
       activation_code=None,
       activation_expire=None,
       reg_id=None,
       os_ver=None,
       vdom=None,
       raw_json=False,
       **kwargs
   )

Update this specific resource.


``delete()``
^^^^^^^^^^^^

.. code-block:: python

   delete(
       serial_number=None,
       payload_dict=None,
       vdom=None,
       raw_json=False,
       **kwargs
   )

Delete this specific resource.

