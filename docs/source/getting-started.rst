===============
Getting Started
===============

Installation
============

| **pync** should work on any system with `Python <https://www.python.org/>`_ installed (2.7 or higher).
| Using Python's pip command, you can install **pync** straight from GitHub.

.. tab:: Unix
   
   .. code-block:: sh

      pip install https://github.com/brenw0rth/pync/archive/main.zip

.. tab:: Windows

   .. code-block:: sh

      py -m pip install https://github.com/brenw0rth/pync/archive/main.zip

Running pync
============

Once installed, there are several ways to run **pync**:

* Running the **pync** command directly:

  .. code-block:: sh

     pync --help

* Running it as a module using the Python command:

  .. tab:: Unix

     .. code-block:: sh
        
        python -m pync --help

  .. tab:: Windows

     .. code-block:: sh

        py -m pync --help

* Or importing it from a Python script:

  .. code-block:: python

     # help.py
     from pync import pync
     pync('--help')

Ensure you have a working pync
==============================

Client/Server Model
-------------------

Create a server
^^^^^^^^^^^^^^^

Common Uses
===========

Transferring Data
-----------------
.. warning::
    | Please DO NOT transfer any sensitive data using the following method as the
    | connection is NOT secure.

By redirecting input and output, you can use **pync** to perform
simple file transfers.

Create a server to host a file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Talking To Servers
------------------
You can create a connection to different kinds of servers and
send messages by piping data to **pync**'s stdin stream.

Send a GET request to an HTTP server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab:: Unix

   .. code-block:: sh
        
      echo "GET / HTTP/1.0\r\n\r\n" | pync -q -1 www.example.com 80

.. tab:: Windows

   .. code-block:: sh

      echo "GET / HTTP/1.0\r\n\r\n" | py -m pync -q -1 www.example.com
      
.. tab:: Python

   .. code-block:: python
   
      # http_get.py
      import io
      from pync import pync
      
      # BytesIO turns the get request string into a file-like
      # object for the pync function.
      http_get = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('-q -1 www.example.com 80', stdin=http_get)

| Setting the -q option to a negative number tells **pync**
  not to close after sending the GET request.
| After sending the GET request, the server's response should
  be printed to the console.

Programming pync
================

Next Steps
==========
