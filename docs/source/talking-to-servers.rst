==================
Talking To Servers
==================
You can create a connection to different kinds of servers and
send messages by piping data to **pync**'s stdin stream.

Send a GET request to an HTTP server
====================================

.. tab:: Unix

   .. code-block:: sh
        
      echo "GET / HTTP/1.0\r\n\r\n" | pync -q -1 host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      echo "GET / HTTP/1.0\r\n\r\n" | py -m pync -q -1 host.example.com 80
      
.. tab:: Python

   .. code-block:: python
   
      # http_get.py
      import io
      from pync import pync
      
      # BytesIO turns the get request string into a file-like
      # object for the pync function.
      http_get = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('-q -1 host.example.com 80', stdin=http_get)

After sending the GET request, the server's response should
be printed to the console.

.. note::
   Setting the -q option to a negative number tells **pync** not to quit after
   sending the GET request.
