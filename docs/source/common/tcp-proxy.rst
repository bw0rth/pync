******************
simple TCP proxies
******************

By connecting a client and server's input and
output together, it is possible to create a
simple TCP proxy.

.. tab:: Unix

   1. Create a named pipe by using the mkfifo command:
   
   .. code-block:: sh

      mkfifo backpipe
      
   2. Create a server on port 8000 and feed it's output into
      a connection to the destination host on port 80 while
      using the backpipe to feed the host connection's output back
      to the server's input stream:

   .. code-block:: sh

      pync -l 8000 < backpipe | pync host.example.com 80 > backpipe

.. tab:: Python

   .. code-block:: python
      :linenos:
      
      # proxy.py
      import pync
      
      
      def main():
          server = pync.Netcat(port=8000,
              l=True,
              stdin=pync.PIPE,
              stdout=pync.PIPE,
          )
          server.start_process(daemon=True)

          client = pync.Netcat('host.example.com', 80,
              stdin=server.stdout,
              stdout=server.stdin,
          )
          client.run()
              
              
      if __name__ == '__main__':
          main()
          
This would create a proxy server on port 8000 that
will forward any request made to it to the destination
server (host.example.com in this case).

To test this out, connect to the proxy server on port
8000 and send a HTTP GET request:

.. tab:: Unix

   .. code-block:: sh
   
      echo "GET / HTTP/1.1\r\n\r\n" | pync localhost 8000
      
.. tab:: Python

   .. code-block:: python
      :linenos:
      
      # http_get.py
      from io import BytesIO
      from pync import pync
      
      http_get = BytesIO(b'GET / HTTP/1.1\r\n\r\n')
      pync('localhost 8000', stdin=http_get)
