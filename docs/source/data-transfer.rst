=============
Data Transfer
=============
.. warning::
    | Please DO NOT transfer any sensitive data using the following method.
    | The connection is NOT secure.

By redirecting input and output, you can use **pync** to perform
simple file transfers.

Create a server to host a file
==============================

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
     
      # pync reads and writes bytes so be sure to open
      # files in binary mode. 
      with open('file.in', 'rb') as f:
          pync('-l localhost 8000', stdin=f)
          
Connect to the server to download the file
==========================================

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

      # pync reads and writes bytes so be sure to open
      # files in binary mode. 
      with open('file.out', 'wb') as f:
          pync('localhost 8000', stdout=f)

.. note::
   | There won't be any progress indication during the file transfer.
   | The connection will automatically close after all the data has been transferred.
