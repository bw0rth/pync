=========================
Executing P[-Yy]thon Code
=========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

**pync** can execute python code in a separate process and connect the
process' stdin/stdout/stderr to the network socket.

Any data that comes in from the network will go to the process' stdin, and
any data that comes out from the process' stdout/stderr will be sent out to the network.

There are two options that can provide this functionality, the **-y** (lowercase y) option
and the **-Y** (uppercase Y) option.

Executing Python Code With -y
=============================
The **-y** option takes a string of python code to execute.
This option is best used when you have a simple one-liner to execute.

The following example shows how to use the **-y** option to create
a simple echo server.

1. Create a server that reads data from stdin (the network) and writes the
   same data to stdout (back to the network):

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

      pync -vq 5 -y "import sys; sys.stdout.write('Hello\n')" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vq 5 -y "import sys; sys.stdout.write('Hello\n')" localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vq 5 -y "import sys; sys.stdout.write('Hello\n')" localhost 8000')

Executing Python Files With -Y
==============================
The **-Y** option (uppercase Y) takes the full pathname of a python file
to execute.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../examples/remote-code-exec`

