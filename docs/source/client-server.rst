*******************
Client/Server Model
*******************
**pync** can act as a client or a server.

Creating a server
=================

.. tab:: Unix

   .. code-block:: sh
        
      pync -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l localhost 8000
      
.. tab:: Python

   .. code-block:: python
   
      # server.py
      from pync import pync
      pync('-l localhost 8000')

Creating a client
=================

.. tab:: Unix

   .. code-block:: sh
        
      pync localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync localhost 8000
      
.. tab:: Python

   .. code-block:: python
   
      # client.py
      from pync import pync
      pync('localhost 8000')

Once a connection has been established, anything
typed on one console will be concatenated to the other,
and vice-versa.

When finished, hit Ctrl-C on either console to close
the connection.

