==========================
[-k]eeping the Server Open
==========================

By default, **pync**'s TCP server will accept one client before
closing the server's socket.

By using the `-k <https://pync.readthedocs.io/en/latest/options/keep-server-open.html>`_
option, you can keep the server open to serve multiple clients
one after another.

Creating a Date/Time Server
===========================

1. Combining `-k <https://pync.readthedocs.io/en/latest/options/keep-server-open.html>`_
   with the `-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
   and `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
   options, we can create a simple date/time server that stays
   open between connections:

.. tab:: Unix

   .. code-block:: sh

      pync -kle date localhost 8000

.. tab:: Windows

   .. code-block:: sh
   
      py -m pync -kle "time /t && date /t" localhost 8000

.. tab:: Python

   .. code-block:: python
      
      # datetime_server.py
      import platform
      from pync import pync

      command = 'date'
      if platform.system() == 'Windows':
          command = 'time /t && date /t'

      pync('-kle {} localhost 8000'.format(command))

2. To test this, connect to the server on a separate console:

.. tab:: Unix

   .. code-block:: sh

      pync localhost 8000

.. tab:: Windows

   .. code-block:: sh
   
      py -m pync localhost 8000

.. tab:: Python

   .. code-block:: python
      
      from pync import pync
      pync('localhost 8000')

Because we set the `-k <https://pync.readthedocs.io/en/latest/options/keep-server-open.html>`_
option on the server, we should be able to keep connecting
to it to get the current time and date.

When you're finished, hit Ctrl+C on the server console to close the server.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`execute`
* :doc:`listen`

