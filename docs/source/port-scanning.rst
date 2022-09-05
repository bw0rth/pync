=============
Port Scanning
=============
Sometimes it's useful to know which ports are open and what services a
target machine is running.

Scan a list of ports on a target machine
========================================
Combining the -v and -z flags, you can scan a list of ports to reveal
the ones that are accepting connections:

.. tab:: Unix

   .. code-block:: sh
        
      pync -vz host.example.com 20-30

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 20-30
      
.. tab:: Python

   .. code-block:: python
   
      # scan.py
      from pync import pync
      pync('-vz host.example.com 20-30')

For example, if ports 22 and 25 are open, you should see
output similar to this::

   ...
   Connection to host.example.com 22 port [tcp/ssh] succeeded!
   Connection to host.example.com 25 port [tcp/smtp] succeeded!

Get the version of software a port is running
=============================================
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
