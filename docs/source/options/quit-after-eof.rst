================================================
-q: quit after EOF on stdin and delay of seconds
================================================

| By default, :doc:`-q <quit-after-eof>` is set to 0 to tell **pync** to quit immediately after reaching EOF (End Of File) on stdin.
| If you want to have it wait after EOF, set :doc:`-q <quit-after-eof>` to the number of seconds you want to wait.
| Or if you would like to wait forever until the connection closes, set :doc:`-q <quit-after-eof>` to a negative number.

An Example
==========

1. Create a test TCP server:

.. tab:: Unix

   .. code-block:: sh

      pync -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-l localhost 8000')

2. Connect to the server with :doc:`-q <quit-after-eof>` set to
   5 seconds.
   This will pipe the message "Hello, World!" into **pync**'s
   stdin, then after EOF has been reached on the message,
   it will wait 5 seconds before closing:

.. tab:: Unix

   .. code-block:: sh

      echo "Hello, World!" | pync -q 5 localhost 8000

.. tab:: Windows

   .. code-block:: sh

      echo Hello, World! | py -m pync -q 5 localhost 8000

.. tab:: Python

   .. code-block:: python

      import io
      from pync import pync

      # io.BytesIO turns our message into a file-like
      # object for the pync function.
      message = io.BytesIO(b'Hello, World!')
      pync('-q 5 localhost 8000', stdin=message)

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`listen`

