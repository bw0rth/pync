===================
Client/Server Model
===================
The basic idea of **pync** is to create a
connection to a client or server then,
once connected, redirect any data from
stdin to the connection while, at
the same time, redirecting any data
from the connection to stdout:

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

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/listen`

