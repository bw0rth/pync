******************
simple TCP proxies
******************

By connecting a client and server's input and
output together, it is possible to create a
simple TCP proxy.

.. tab:: Unix

   .. code-block:: sh

      pync -l 8000 < backpipe | pync host.example.com 8001 > backpipe
