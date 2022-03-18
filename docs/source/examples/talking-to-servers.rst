==================
Talking to Servers
==================

Sometimes it can be useful to interact with servers
by hand for troubleshooting or to verify a servers
response to certain commands.

1. For example, we can pipe a get request to a web server
   to retrieve the home page:

.. tab:: Linux

   .. code-block:: sh

      printf "GET / HTTP/1.0\r\n\r\n" | pync host.example.com 80

.. tab:: Python

   .. code-block:: python

      # get.py
      import io
      from pync import pync
      # BytesIO turns our request into a file-like
      # object for the pync function.
      request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('host.example.com 80', stdin=request)

