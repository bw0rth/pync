============================
[-l]istening For Connections
============================

To create a server, you can use the **-l** option to listen
for incoming connections:

.. tab:: Unix

   .. code-block:: sh

      pync -l localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-l localhost 8000')

By combining the -l option with the -u option, you can
create a UDP server instead of the default TCP:

.. tab:: Unix

   .. code-block:: sh

      pync -lu localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-lu localhost 8000')

