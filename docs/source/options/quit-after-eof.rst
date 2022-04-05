=================
[-q]uit After EOF
=================

The **-q** option allows us to quit the readwrite loop after reaching
EOF on stdin.

By default, **pync**'s -q option is set to -1 which tells it to carry
on writing network data to stdout until the connection closes.

Setting the **-q** option to a positive number tells **pync** to
quit the readwrite loop after the number of seconds has elapsed.

1. Setup a local test server on port 8000:

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

2. Connect to the server on another console and send a message
   with **-q** set to 5 seconds:

.. tab:: Unix

   .. code-block:: sh

      echo "Hello" | pync -q 5 localhost 8000

.. tab:: Windows

   .. code-block:: sh

      echo Hello | py -m pync -q 5 localhost 8000

.. tab:: Python

   .. code-block:: python
      
      import io
      from pync import pync

      # io.BytesIO turns our bytes string into a file-like
      # object for the pync function.
      msg = io.BytesIO(b'Hello')
      pync('-q 5 localhost 8000', stdin=msg)

After the connection has been established, the client will
send the message "Hello" and after EOF (End Of File) has
been reached on the message, the connection will then close
5 seconds after.

