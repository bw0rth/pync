*******************************************
shell-script based HTTP clients and servers
*******************************************

A Simple HTTP client
====================

.. tab:: Unix

   .. code-block:: sh
      
      printf "GET / HTTP/1.1\r\n\r\n" | pync host.example.com 80

.. tab:: Python

   .. code-block:: python
   
      import io
      from pync import pync
      
      req = io.BytesIO(b'GET / HTTP/1.1\r\n\r\n')
      pync('host.example.com 80', stdin=req)

A Simple HTTP Server
====================
