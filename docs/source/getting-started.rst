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
Once installed, you can run **pync** from the command-line or import it into a Python script.

.. tab:: Command

   .. tab:: Linux
      
      .. code-block:: sh

         pync --help

   .. tab:: Windows

      .. code-block:: sh

         py -m pync --help

.. tab:: Python

   .. code-block:: Python

      # help.py
      from pync import pync
      pync('--help')

