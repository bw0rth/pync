=====================================
-l: Listen mode, for inbound connects
=====================================

To create a TCP server, you can use the
`-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
option to listen for incoming connections:

.. tab:: Unix

   .. code-block:: sh

      pync -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-l localhost 8000')

If instead you want a UDP server, combine the
`-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_ and
`-u <https://pync.readthedocs.io/en/latest/options/udp.html>`_ options:

.. tab:: Unix

   .. code-block:: sh

      pync -lu localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lu localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-lu localhost 8000')

.. raw:: html
   
   <br>
   <hr>

:SEE ALSO:

* :doc:`keep-server-open`
* :doc:`udp`

