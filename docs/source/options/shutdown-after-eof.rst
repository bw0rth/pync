=====================
Shutdow[-N] After EOF
=====================

The **-N** option allows you to tell the other end of the
connection that you have no more data to send after
EOF (End Of File) has been reached on stdin.

Sometimes, a server may require this behaviour to work properly.

An example would be when you're transferring file data and want
to tell the other end of the connection when you have
sent all the data.

1. Create a server to host a file to download:

.. tab:: Unix

   .. code-block:: sh

      pync -lN localhost 8000 < file.in

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lN localhost 8000 < file.in

.. tab:: Python

   .. code-block:: python

      from pync import pync
      # Be sure to open files in binary mode
      # when passing them to pync.
      with open('file.in', 'rb') as f:
          pync('-lN localhost 8000', stdin=f)

2. Connect to the server to download the file data:

.. tab:: Unix

   .. code-block:: sh

      pync localhost 8000 > file.out

.. tab:: Windows

   .. code-block:: sh
   
      py -m pync localhost 8000 > file.out

.. tab:: Python
   
   .. code-block:: python

      from pync import pync
      # Be sure to open files in binary mode
      # when passing them to pync.
      with open('file.out', 'wb') as f:
          pync('localhost 8000', stdout=f)

Without the server using the **-N** option to tell the client
that it has sent all the file data, the connection would
stay alive until the user manually closes it with Ctrl+C.

In the previous example, it's important to note that the server
tells the client that it has no more data to send, and based
on that information, the client then closes the connection.

