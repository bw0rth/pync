**********************
network daemon testing
**********************

Is the server online?
=====================

To test whether a server is accepting
connections, you can combine the **-v** and
**-z** flags together:

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

The **-z** flag tells **pync** to close the
connection immediately (zero input/output)
while the **-v** flag prints a connection
success or failure message to the console.

.. tab:: Success

   .. code-block:: sh

      Connection successful!

.. tab:: Failed

   .. code-block:: sh

      Connection failed
