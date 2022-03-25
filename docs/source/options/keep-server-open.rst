==========================
[-k]eeping the Server Open
==========================

By default, pync's TCP server will accept one client before
closing the server's socket.

By using the **-k** option, you can keep the server open
to serve multiple clients one after another.

For example, combining with the -l option and -e option,
we can create a simple date/time server that stays
open between connections:

.. tab:: Unix

   .. code-block:: sh

      pync -kle date localhost 8000

.. tab:: Python

   .. code-block:: python
      
      from pync import pync
      pync('-kle date localhost 8000')

