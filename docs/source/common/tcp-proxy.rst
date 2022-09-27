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

   And then using it to connect the client's
   output to the server's input:

   .. code-block:: sh

      pync -l 8000 < backpipe | pync host.example.com 8001 > backpipe
