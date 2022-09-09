==================
Talking to Servers
==================

Sometimes it can be useful to interact with servers
by hand for troubleshooting or to verify a servers
response to certain commands.

Talking to a web server
-----------------------
You can send a GET request to a web server to receive the home page.

.. tab:: Unix

   .. code-block:: sh

      printf "GET / HTTP/1.0\r\n\r\n" | pync host.example.com 80

.. tab:: Windows

   On Windows, it isn't as easy as just piping the GET request string to **pync**.

   First, create a text file (http_get.txt) containing the following:

   .. literalinclude:: ../data/http_get.txt
      :linenos:

   | That's the GET request followed by a blank line.
   | The blank line tells the web server that you're done
     sending the request.

   Once you've created the http_get.txt file, you can then pipe
   it into **pync**'s stdin stream to receive the web page:

   .. code-block:: sh

      py -m pync -C host.example.com 80 < http_get.txt

   Web servers typically expect header fields to be terminated with a
   carriage return (CR) and line feed (LF) character sequence (\\r\\n).

   Without the -C flag, the data sent over the network would look like this:

   .. code-block:: text

      GET / HTTP/1.0\n\n

   The -C flag tells **pync** to replace all LF (\\n) characters
   with a CRLF sequence (\\r\\n) so the data would look like this:

   .. code-block:: text

      GET / HTTP/1.0\r\n\r\n

   So that's a GET request terminated with a CRLF sequence:

   .. code-block:: text

      GET / HTTP/1.0\r\n

   Followed by a blank line terminated with a CRLF sequence:

   .. code-block:: text

      \r\n

   As mentioned earlier, that blank line is to tell the web server
   that you're done sending the request and are now ready to
   receive the response.

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

