==========
[-v]erbose
==========

| The :doc:`-v <verbose>` option will print status messages to stderr when running **pync**.
| This can be useful to see feedback as to whether a connection to a server was successful or not.

Example
=======

1. Create a test TCP server:

.. tab:: Unix

   .. code-block:: sh

      pync -lv localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lv localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-lv localhost 8000')

