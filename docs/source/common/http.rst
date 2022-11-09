*******************************************
shell-script based HTTP clients and servers
*******************************************

A Simple HTTP client
====================

Retrieving the home page of a website can be as
simple as passing a GET request string to
**pync**'s stdin stream:

.. tab:: Unix

   .. code-block:: sh
      
      printf "GET / HTTP/1.1\r\n\r\n" | pync host.example.com 80

.. tab:: Python

   .. code-block:: python
   
      import io
      from pync import pync
      
      req = io.BytesIO(b'GET / HTTP/1.1\r\n\r\n')
      pync('host.example.com 80', stdin=req)
      
.. note::
   The response will contain HTTP headers that would need filtering out using another tool.

A Simple HTTP Server
====================

1. Create the HTML index page to serve (index.html):

.. literalinclude:: ../../data/index.html
   :linenos:
   :language: html
   
2. Create the server:
   
.. tab::Unix

   .. code-block:: sh
   
      pync -vlkc "cat index.html" 8000
