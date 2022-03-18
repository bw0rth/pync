==================
Executing Commands
==================

After a connection to a client or server has been
established, you can execute a command and connect the
input/output of the command process with the connection.

1. For example, create a server that echoes a message to
   the first client that connects:

.. tab:: Unix

   .. code-block:: sh

      pync -e "echo 'Hello'" -l localhost 8000

.. tab:: Python

   .. code-block:: python

      # server.py
      from pync import pync
      pync('-e "echo \'Hello\'" -l localhost 8000')

