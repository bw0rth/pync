**********************
network daemon testing
**********************

Is the server online?
=====================

To test whether a server is accepting
connections, you can use the -z flag to turn
zero input/output mode on:

.. tab:: Unix

   .. code-block:: sh

      pync -vz host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 80

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vz host.example.com 80')
