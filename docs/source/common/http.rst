********************************************
python-script based HTTP clients and servers
********************************************

A Simple HTTP client
====================

Retrieving the home page of a website can be as
simple as passing a GET request string to
**pync**'s stdin stream:

.. code-block:: python
   
   import pync
   pync.run('host.example.com 80', input=b'GET / HTTP/1.1\r\n\r\n')
      
.. note::
   The response will contain HTTP headers that would need filtering out using another tool.

A Simple HTTP Server
====================

1. Create a file that contains the HTTP response (index.http):

.. literalinclude:: ../../data/index.http
   :linenos:
   :language: html
   
2. Listen for connections on port 8000 and serve the index.http file:

.. code-block:: python
   
   import platform
   import pync
   
   cat = 'cat'
   if platform.system() == 'Windows':
       cat = 'type'
   
   pync.run('-vlkc "{cat} index.http" 8000'.format(cat=cat))

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/verbose`
* :doc:`../options/listen`
* :doc:`../options/keep-server-open`
* :doc:`../options/exec`
* :doc:`../usage/remote-command-exec`
