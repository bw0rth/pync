=============
Data Transfer
=============

To build on the previous client/server example, we can
transfer file data from one machine to another.

1. Create a server to host the file:

.. tab:: Unix

   .. code-block:: sh

      pync -l localhost 8000 < file.in

.. tab:: Windows

   .. code-block:: sh
      
      py -m pync -l localhost 8000 < file.in

.. tab:: Python

   .. code-block:: python

      # server.py
      from pync import pync

      # Be sure to open files in binary mode
      # for the pync function.
      with open('file.in', 'rb') as f:
          pync('-l localhost 8000', stdin=f)

2. On a separate console, connect to the server to
   download the file:

.. tab:: Unix

   .. code-block:: sh

      pync localhost 8000 > file.out

.. tab:: Windows

   .. code-block:: sh

      py -m pync localhost 8000 > file.out

.. tab:: Python

   .. code-block:: python

      # client.py
      from pync import pync

      # Be sure to open files in binary mode
      # for the pync function.
      with open('file.out', 'wb') as f:
          pync('localhost 8000', stdout=f)

During the file transfer, there won't be any progress
indication. The connection will close automatically after
the file has been transferred.

