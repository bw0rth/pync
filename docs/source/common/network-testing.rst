**********************
network daemon testing
**********************

Is the server online?
=====================

To test whether a server is accepting
connections, you can combine the **-v** and
**-z** flags together:

.. tab:: Unix

   .. code-block:: sh

      pync -vz host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vz host.example.com 80

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-vz host.example.com 80')

The **-z** flag tells **pync** to close the
connection immediately (zero input/output)
while the **-v** flag prints a connection
success or failure message to the console:

.. tab:: Success

   .. code-block:: sh

      ...
      Connection to host.example.com 80 port [tcp/http] succeeded!

.. tab:: Failure

   .. code-block:: sh

      ...
      pync: connect to host.example.com port 80 (tcp) failed: Connection refused

You can also scan multiple ports on a machine
by passing a range of port numbers. See
:doc:`../usage/port-scanning` for more.

Is the server responding?
=========================

It can also be useful to interact with a server
to test how it responds to certain requests.

For example, a web server should respond to
a HTTP GET request by sending back a HTTP
status code and the contents of the requested
web page (if it exists).

1. Connect to a web server:

.. tab:: Unix

   .. code-block:: sh

      pync host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      py -m pync host.example.com 80

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('host.example.com 80')

2. Once connected, send a GET request for the
   home page by typing the following and
   hitting enter a couple of times:

.. code-block:: sh

   GET / HTTP/1.1

If all goes well, the server should respond
with a HTTP 200 OK status along with any HTTP
headers and the contents of the requested web
page (index.html in this case):

.. code-block:: sh

   HTTP/1.1 200 OK
   Server: host.example.com
   Content-Type: text/html; charset=UTF-8
   ...

   <!doctype html>
   <html>
     <body>
       <h1>Example Web Page!</h1>
     </body>
   </html>
