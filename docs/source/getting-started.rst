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

Client/Server Model
===================
**pync** can act as a client or a server.

Create a server to listen for a connection
------------------------------------------

.. tab:: Unix

   .. code-block:: sh
        
      pync -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l localhost 8000
      
.. tab:: Python

   .. code-block:: python
   
      # server.py
      from pync import pync
      pync('-l localhost 8000')

Create a client to connect to the server
----------------------------------------

.. tab:: Unix

   .. code-block:: sh
        
      pync localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync localhost 8000
      
.. tab:: Python

   .. code-block:: python
   
      # client.py
      from pync import pync
      pync('localhost 8000')

Once a connection has been established, anything
typed on one console will be concatenated to the other,
and vice-versa.

When finished, hit Ctrl-C on either console to close
the connection.

Common Uses
===========

Transferring Data
-----------------
.. warning::
    | Please DO NOT transfer any sensitive data using the following method.
    | The connection is NOT secure.

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
        
      echo "GET / HTTP/1.0\r\n\r\n" | pync -q -1 host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      echo "GET / HTTP/1.0\r\n\r\n" | py -m pync -q -1 host.example.com 80
      
.. tab:: Python

   .. code-block:: python
   
      # http_get.py
      import io
      from pync import pync
      
      # BytesIO turns the get request string into a file-like
      # object for the pync function.
      http_get = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('-q -1 host.example.com 80', stdin=http_get)

After sending the GET request, the server's response should
be printed to the console.

.. note::
   Setting the -q option to a negative number tells **pync** not to quit after
   sending the GET request.

Port Scanning
-------------
Sometimes it's useful to know which ports are open and what services a
target machine is running.

Scan a list of ports on a target machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combining the -v and -z flags, you can scan a list of ports to reveal
the ones that are accepting connections:

.. tab:: Unix

   .. code-block:: sh
        
      pync -vz host.example.com 20-30

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 20-30
      
.. tab:: Python

   .. code-block:: python
   
      # scan.py
      from pync import pync
      pync('-vz host.example.com 20-30')

For example, if ports 22 and 25 are open, you should see
output similar to this::

   ...
   Connection to host.example.com 22 port [tcp/ssh] succeeded!
   Connection to host.example.com 25 port [tcp/smtp] succeeded!

Get the version of software a port is running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It might also be useful to know which server software is running, and
which versions.

This can be done by setting a small timeout with the -w flag, or maybe
by issuing a well known command to the server:

.. tab:: Unix

   .. code-block:: sh
        
      echo "QUIT" | pync host.example.com 20-30

.. tab:: Windows

   .. code-block:: sh

      echo "QUIT" | py -m pync host.example.com 20-30
      
.. tab:: Python

   .. code-block:: python
   
      # banner.py
      import io
      from pync import pync

      command = io.BytesIO(b'QUIT')
      pync('host.example.com 20-30', stdin=command)

For example, if SSH was running on port 22, you might see output
similar to this::

   ...
   SSH-1.99-OpenSSH_3.6.1p2
   Protocol mismatch.

pync For Python Developers
==========================
There are two main objects of interest when using
**pync** in your own Python scripts: the **pync** function
and the Netcat class.

Running the pync function
-------------------------
Running the **pync** function is similar to running **pync** from the
command-line. It will run a given string of arguments and return an
integer exit status value once finished.

| The **pync** function also takes a few more keyword arguments: stdin,
  stdout and stderr.
| By default, these arguments point to the console for input and output.

You can pass your own file-like objects to these keyword arguments
to control where the data gets read from and written to.

Send a GET request to an HTTP server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # pync_http_get.py
   import io
   import sys

   from pync import pync

   # io.BytesIO turns the GET request bytes string into a file-like
   # object for the pync function.
   request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')

   # pync reads and writes bytes, so be sure to open files in
   # binary mode.
   with open('http.response', 'wb') as response:
       status = pync('-q -1 host.example.com 80', stdin=request, stdout=response)

   sys.exit(status)

This example sends a GET request string to a web server and saves
the response to a file.

Creating a Netcat instance
--------------------------
Under the hood, the **pync** function creates a custom Netcat class
and handles any exceptions that may occur, printing them to stderr.

If you would like more control over exception handling or maybe you'd
like to customize your own Netcat, you can use the Netcat class.

Send a GET request to an HTTP server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # netcat_http_get.py
   import io
   from pync import Netcat

   # io.BytesIO turns the GET request byte string into a file-like
   # object for the Netcat class.
   request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')

   # Netcat reads and writes bytes so be sure to open files in
   # binary mode.
   response = open('http.response', 'wb')
   nc = Netcat('host.example.com', 80,
       q=-1,
       stdin=request,
       stdout=response,
   )

   try:
       nc.readwrite()
   finally:
       response.close()
       nc.close()

As before when using the **pync** function, this sends a GET request
to a web server and saves the response to a file.

Next Steps
==========
It is recommended to have a look at the Options and Examples sections.

If you're a developer looking for more information on how to use
**pync** in your own scripts, take a look at the API Reference or
the Example Scripts.

