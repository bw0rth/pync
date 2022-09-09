===================
Client/Server Model
===================

**pync** can be used as a client or a server:

.. code-block:: text

   **pync** --connect--> server
   **pync** <--connect-- client
   
And once a connection has been established, any data
read from stdin gets sent to the connection and any
data received from the connection gets written to stdout:

.. code-block:: text

   stdin  --data--> **pync** --data--> connection
   stdout <--data-- **pync** <--data-- connection

To illustrate a basic client/server model, we can connect
two **pync** instances together and send messages back and
forth.

1. Create a local server to listen for incoming connections
   on port 8000:

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

2. On a separate console, connect to the server:

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

There should now be a connection between the two consoles
and anything typed in one console should display in the
other and vice-versa.

When finished, hit Ctrl+C from either console to close the
connection.

While sending messages back and forth doesn't really seem
that useful, the core concept of redirecting input and output
over the network can open up a range of other possibilities.

For instance, you can download and upload files by redirecting
input and ouput.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/listen`
