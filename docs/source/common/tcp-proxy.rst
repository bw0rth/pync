******************
simple TCP proxies
******************

By redirecting input and output through pipes,
it's possible to create a simple TCP proxy
server.

.. tab:: Unix

   .. code-block:: sh

      pync -l 8000 < backpipe | pync host.example.com 8001 > backpipe
