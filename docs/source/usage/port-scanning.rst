=============
Port Scanning
=============

.. warning::
   | * Please be CAREFUL and RESPONSIBLE with this
       functionality.
   | * Please DO NOT scan machines without
       the owners permission first.

Sometimes it's useful to know which ports are open and what services a
target machine is running.

Scanning Multiple Ports
=======================
By passing a range and/or list of ports, we can connect
to multiple ports one after another.

Combining this with the `-v <https://pync.readthedocs.io/en/latest/options/verbose.html>`_
and `-z <https://pync.readthedocs.io/en/latest/options/zero-io.html>`_
options to turn on verbose and zero I/O mode, we can create
a simple port scanner:

.. tab:: Unix

   .. code-block:: sh

      pync -vz host.example.com 20-30 80 443

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 20-30 80 443

.. tab:: Python

   .. code-block:: python

      # scan.py
      from pync import pync
      pync('-vz host.example.com 20-30 80 443')

As you can see, you can provide a single port, a list of
ports or a range of ports to scan.
In this case, we scan port 20 to 30 (20,21,22...30), port
80 (http) and port 443 (https).

For example, if ports 22 and 25 are open, you should see
output similar to this::

   ...
   Connection to host.example.com 22 port [tcp/ssh] succeeded!
   Connection to host.example.com 25 port [tcp/smtp] succeeded!

Banner Grabbing
===============
It might also be useful to know which server software is running, and
which versions.

This can be done by setting a small timeout with the -w flag, or maybe
by issuing a well known command to the server:

.. tab:: Unix

   .. code-block:: sh
        
      echo "QUIT" | pync host.example.com 20-30

.. tab:: Windows

   .. code-block:: sh

      echo "QUIT" | py -m pync host.example.com 20-30
      
.. tab:: Python

   .. code-block:: python
   
      # banner.py
      import io
      from pync import pync

      command = io.BytesIO(b'QUIT')
      pync('host.example.com 20-30', stdin=command)

For example, if SSH was running on port 22, you might see output
similar to this::

   ...
   SSH-1.99-OpenSSH_3.6.1p2
   Protocol mismatch.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/verbose`
* :doc:`../options/zero-io`

