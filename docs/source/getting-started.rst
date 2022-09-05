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

