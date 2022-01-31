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

Basic Usage
===========
Once installed, you can run **pync** from the command-line:

.. tab:: Unix

   .. code-block:: sh

      python -m pync --help

.. tab:: Windows

   .. code-block:: sh

      py -m pync --help

Or from a Python script:

.. code-block:: python

   # help.py
   from pync import pync
   pync('--help')

