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

Common Uses
===========

Transferring Data
-----------------
By redirecting input and output, you can use **pync** to perform
simple file transfers.

.. warning::
    Data transferred is NOT encrypted.
    Please DO NOT transfer any sensitive data using this method.

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
   
      # file_server.py
      from pync import pync
      
      with open('file.in', 'rb') as f:
          pync('-l localhost 8000', stdin=f)
          
Connect to the server to download the file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab:: Unix

   .. code-block:: sh
        
      pync localhost 8000 > file.out

.. tab:: Windows

   .. code-block:: sh

      py -m pync localhost 8000 > file.out
      
.. tab:: Python

   .. code-block:: python
   
      # file_client.py
      from pync import pync
      
      with open('file.out', 'wb') as f:
          pync('localhost 8000', stdout=f)

Talking To Servers
------------------
This simple idea of redirecting input and output lets you
talk to all kinds of servers.

Send a GET request to a HTTP server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Programming pync
================

Next Steps
==========
