===================
Client/Server Model
===================

Building a basic client/server model using
**pync** is quite simple. On one console,
create a server to listen on a specific port:

.. tab:: Unix

   .. code-block:: sh

      pync -l 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l 8000

.. tab:: Python

   .. code-block:: python

      # server.py
      from pync import pync
      pync('-l 8000')

**pync** is now listening for a connection
on port 8000. On a separate console, connect
to the server on the port being listened on:

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
