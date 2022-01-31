===============
Getting Started
===============

Installation
============
| **pync** should work on any system with `Python <https://www.python.org/>`_ installed (2.7 or higher).
| Using `Python <https://www.python.org/>`_'s pip command, you can install **pync** straight from github.

.. tab:: Linux
   
   .. code-block:: sh

      pip install https://github.com/brenw0rth/pync/archive/main.zip

.. tab:: Windows

   .. code-block:: sh

      py -m pip install https://github.com/brenw0rth/pync/archive/main.zip

Basic Usage
===========
Once installed, there are three ways to run **pync**.

1. Running the **pync** command directly:

   .. code-block:: sh

      pync --help

2. Running **pync** as a module with the Python command:

   .. tab:: Linux

      .. code-block:: sh

         python -m pync --help

   .. tab:: Windows

      .. code-block:: sh

         py -m pync --help

3. Or importing **pync** from a Python script:

   .. code-block:: python

      # help.py
      from pync import pync
      pync('--help')

