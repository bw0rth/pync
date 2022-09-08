==================
Talking to Servers
==================

Sometimes it can be useful to interact with servers
by hand for troubleshooting or to verify a servers
response to certain commands.

Talking to a web server
-----------------------
| You can send a GET request to a web server to receive the home page.
| The GET request will look like this:

.. code-block:: text

   GET / HTTP/1.0\r\n\r\n

| But just sending this won't complete the request.
| The web server will typically wait until a sequence of carriage return
  (\r) line feed (\n) characters before sending a response:

.. code-block:: text

   \r\n\r\n

.. tab:: Unix

   .. code-block:: sh

      printf "GET / HTTP/1.0\r\n\r\n" | pync host.example.com 80

.. tab:: Windows

   On Windows' cmd.exe, it isn't as easy as just piping the request string.

   First, create a text file (http_get.txt) containing the following:

   .. literalinclude:: ../data/http_get.txt
      :linenos:

   So that's the line "GET / HTTP/1.0" followed by a blank line.

   .. note::

      That blank line is important. It tells the server that you're done
      sending the request and are now ready to receive the response.
      Without it, the connection would likely hang indefinitely and you wouldn't
      receive the response from the server.

   Once you've created the http_get.txt file, you can then pipe
   it into **pync**'s stdin stream:

   .. code-block:: sh

      py -m pync host.example.com 80 < http_get.txt

.. tab:: Python

   .. code-block:: python

      # http_get.py
      import io
      from pync import pync
      # BytesIO turns our request into a file-like
      # object for the pync function.
      request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('host.example.com 80', stdin=request)

Talking to a mail server
-------------------------
| You could also submit emails to Simple Mail Transfer Protocol (SMTP) servers.
| Suppose you have a text file (email_template.txt):

.. literalinclude:: ../data/email_template.txt
   :language: text
   :linenos:

You could then send this template to the server like so:

.. tab:: Unix

   .. code-block:: sh

      pync -C smtp.example.com 25 < email_template.txt

.. tab:: Windows

   .. code-block:: sh

      py -m pync -C smtp.example.com 25 < email_template.txt

.. tab:: Python

   .. code-block:: python

      # smtp.py
      from pync import pync
      with open('email_template.txt', 'rb') as f:
          pync('-C smtp.example.com 25', stdin=f)

| SMTP typically requires lines to be terminated with a carriage return (CR)
  line feed (LF) sequence (\\r\\n).
| The -C flag tells **pync** to replace all LF characters (\\n) with CRLF characters instead (\\r\\n).

