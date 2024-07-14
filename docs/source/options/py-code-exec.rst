=============================================
-y: specify python code to exec after connect
=============================================

.. warning::
   | - Please BE CAREFUL not to expose your system with this functionality.
   | - Please DO NOT use this functionality for evil purposes.

**pync** can execute Python code in a separate process and connect the
process' stdin/stdout/stderr to the network socket.

Any data that comes in from the network will go to the process' stdin, and
any data that comes out from the process' stdout/stderr will be sent out to the network.

There are two options that can provide this functionality, the lowercase **-y** option
and the uppercase **-Y** option.

This section focuses on the **-y** option to execute code given as a string.
To execute code from a specified file path, see :doc:`../options/py-file-exec`.

Executing Python Code With -y
=============================
The lowercase **-y** option takes a string of python code to execute.
This option is best used when you have a simple one-liner to execute.

For example, you can create a simple echo server by reading data from
stdin (the network) and writing that same data back to stdout (the network):

.. tab:: Unix

   .. code-block:: sh

      pync -vly "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vly "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000

.. tab:: Python

   .. code-block:: python

      import pync
      pync.run('-vly "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000')

To test this server, connect to it and send it a message:

.. tab:: Unix

   .. code-block:: sh

      echo Hello | pync -vq -1 localhost 8000

.. tab:: Windows

   .. code-block:: sh

      echo Hello | py -m pync -vq -1 localhost 8000

.. tab:: Python

   .. code-block:: python

      import io
      import pync

      hello = io.BytesIO(b'Hello\n')
      pync.run('-vq -1 localhost 8000', stdin=hello)

After receiving the message, the echo server should send it back
to the client which then would display on the client console.

Here, we pass a negative number to the **-q** option to ensure pync
doesn't quit immediately after EOF on stdin (after sending the "Hello" message).
Otherwise, there's a chance the client would quit before receiving
the message back from the echo server.

.. note::
   You could just as well use the builtin print and input functions
   for this but because print and input (raw_input on python 2) are
   different on python 2 and python 3 I just decided using the
   sys module would be better since it works on both versions of
   python.

Executing Python Files With -Y
==============================
The uppercase **-Y** option takes the full pathname of a python file
to execute.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/py-file-exec`
* :doc:`../options/quit-after-eof`
* :doc:`../options/verbose`
* :doc:`../usage/remote-code-exec`

