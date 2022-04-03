==========================
[-k]eeping the Server Open
==========================

By default, **pync**'s TCP server will accept one client before
closing the server's socket.

By using the **-k** option, you can keep the server open
to serve multiple clients one after another.

For example, combining with the `-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
option and `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option, we can create a simple date/time server that stays
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

