**********************
network daemon testing
**********************

Is the server online?
=====================

To test whether a server is accepting
connections, you can combine the **-v** and
**-z** flags together:

.. tab:: Unix

   .. code-block:: sh

      pync -vz host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 80

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vz host.example.com 80')

The **-z** flag tells **pync** to close the
connection immediately (zero input/output)
while the **-v** flag prints a connection
success or failure message to the console:

.. tab:: Success

   .. code-block:: sh

      ...
      Connection to host.example.com 80 port [tcp/http] succeeded!

.. tab:: Failure

   .. code-block:: sh

      ...
      pync: connect to host.example.com port 80 (tcp) failed: Connection refused

You can also scan multiple ports on a machine
by passing a range of port numbers. See
:doc:`../usage/port-scanning` for more.

What is the server saying?
==========================

It can also be useful to interact with a server
to test how it responds to certain requests.

1. Connect to the server:

.. tab:: Unix

   .. code-block:: sh

      pync host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      py -m pync host.example.com 80

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('host.example.com 80')

2. Once connected, send a HTTP GET request
   by typing the following and hitting enter
   a couple of times:

.. code-block:: sh

   GET / HTTP/1.1

If all goes well, the server should respond
with a HTTP 200 OK.
