=========================
[-u]ser Datagram Protocol
=========================

| By default, **pync** uses TCP (Transmission Control Protocol) for transport.
| Using the :doc:`-u <udp>` option, you can set the transport to UDP (User Datagram Protocol) instead.

A Client/Server Example
=======================

1. Create a test UDP server:

.. tab:: Unix

   .. code-block:: sh
      
      pync -lu localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lu localhost 8000

.. tab:: Python

   .. code-block:: python

      # server.py
      from pync import pync
      pync('-lu localhost 8000')

2. On a separate console, connect to the server:

.. tab:: Unix

   .. code-block:: sh
      
      pync -u localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -u localhost 8000

.. tab:: Python

   .. code-block:: python

      # client.py
      from pync import pync
      pync('-u localhost 8000')

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`listen`

