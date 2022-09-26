******************
simple TCP proxies
******************

By connecting a client and server's input and
output together, it is possible to create a
simple TCP proxy.

.. tab:: Unix

   On Unix, this can be done by creating a named
   pipe:

   .. code-block:: sh

      mkfifo backpipe

   And then passing it as the server's input
   and the client's output.

   .. code-block:: sh

      pync -l 8000 < backpipe | pync host.example.com 8001 > backpipe
