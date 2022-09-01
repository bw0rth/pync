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

Interacting With Servers
------------------------

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
      
      http_get = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('-q -1 www.example.com 80', stdin=http_get)
      
Programming pync
================
