========================
Executing P[-y]thon Code
========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

**pync** can execute python code and connect the python process' stdin/stdout/stderr
to the network socket.

Any data that comes in from the network will go to the process' stdin, and
any data that comes out from the process' stdout/stderr will be sent out to the network.

There are two options that can provide this functionality, the **-y** (lowercase y) option
and the **-Y** (capital Y) option.
The **-y** option takes a string of python code to execute
while **-Y** takes the full path of a python script to execute.

A Simple Echo Server
====================

1. Create a server that echoes data back to the first client
   that connects:

.. tab:: Unix

   .. code-block:: sh

      pync -vly "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vly "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vle "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000')

2. Connect to the echo server and send a message:

.. tab:: Unix

   .. code-block:: sh

      pync -vq 5 -y "import sys; sys.stdout.write('Echo...\n')" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vq 5 -y "import sys; sys.stdout.write('Echo...\n')" localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vq 5 -y "import sys; sys.stdout.write('Echo...\n')" localhost 8000')

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../examples/remote-code-exec`

