==================
Talking to Servers
==================

Sometimes it can be useful to interact with servers
by hand for troubleshooting or to verify a servers
response to certain commands.

Talking to a web server
-----------------------
You can send a GET request to a web server to receive the home page:

.. tab:: Unix

   .. code-block:: sh

      printf "GET / HTTP/1.0\r\n\r\n" | pync host.example.com 80

.. tab:: Windows

   On Windows' cmd.exe, it isn't as easy as just piping the request string.

   First, create a text file containing the GET request (http_get.txt):

   .. literalinclude:: ../data/http_get.txt
      :language: text
      :linenos:

   So that's the line "GET / HTTP/1.0" followed by a blank line.

   .. note::

      That blank line is important. It tells the server that you're done
      sending the request and are now ready to receive the response.
      Without it, the connection would hang indefinitely and you wouldn't
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

.. code-block:: text
   :linenos:

   HELO host.example.com
   MAIL FROM: <user@host.example.com>
   RCPT TO: <user2@host.example.com>
   DATA
   From: A tester <user@host.example.com>
   To: <user2@host.example.com>
   Date: date
   Subject: a test message

   Body of email.
   .
   QUIT

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

