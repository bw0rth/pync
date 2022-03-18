=============
Port Scanning
=============

**pync** can be used to perform a simple connect scan to
see what ports and services a target machine is running.

1. To do this, use the -z flag to turn on zero i_o mode
   and -v to print connection success/failure to the
   console:

.. tab:: Unix

   .. code-block:: sh

      pync -vz host.example.com 20-30 80 443

.. tab:: Python

   .. code-block:: python

      # scan.py
      from pync import pync
      pync('-vz host.example.com 20-30 80 443')

As you can see, you can provide a single port, a list of
ports or a range of ports to scan.
In this case, we scan port 20 to 30 (20,21,22...30), port
80 (http) and port 443 (https).

You may also want to grab the server banner to check for
the version of the service running.

1. You can try this by piping a message to the server and
   hoping for a response:

.. tab:: Unix
   
   .. code-block:: sh

      echo "QUIT" | pync host.example.com 20-30

.. tab:: Python

   .. code-block:: python

      # banner.py
      import io
      from pync import pync
      # BytesIO turns our message into a file-like
      # object for the pync function.
      message = io.BytesIO(b'QUIT')
      pync('host.example.com 20-30', stdin=message)

