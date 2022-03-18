===================
Client/Server Model
===================

To illustrate a basic client/server model, we can connect
two pync instances together and send messages back and
forth.

1. Create a local server to listen for incoming connections
   on port 8000:

.. tab:: Command

   .. code-block:: sh

      pync -l localhost 8000

.. tab:: Python

   .. code-block:: python

      # server.py
      from pync import pync
      pync('-l localhost 8000')

2. On a separate console, connect to the server:

.. tab:: Command

   .. code-block:: sh

      pync localhost 8000

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

