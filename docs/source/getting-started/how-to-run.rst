===============
How to Run pync
===============

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

