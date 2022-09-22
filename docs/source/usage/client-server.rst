===================
Client/Server Model
===================

**pync** can act as a client:

.. code-block:: text

   pync [options] dest port[s]

or a server:

.. code-block:: text

   pync -l [options] [dest] port

Once a connection has been established, any
data read from stdin gets sent to the
connection and any data received from the
connection gets written to stdout:

.. code-block:: text

   stdin  --data-> connection
   stdout <-data-- connection

To illustrate a very basic client/server model,
you can connect two **pync** instances together
to send messages back and forth.

On one console, create a server to listen on a specific port:

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
on port 8000.

On a separate console, connect
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

What's next?
============

While sending messages back and forth isn't all that interesting,
this core concept of redirecting input and output opens up a range
of other possibilities:

* :doc:`data-transfer`
* :doc:`talking-to-servers`
* :doc:`port-scanning`
* :doc:`remote-command-exec`
* :doc:`remote-code-exec`

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/listen`
* `Client-server model <https://en.wikipedia.org/wiki/Client%E2%80%93server_model>`_
