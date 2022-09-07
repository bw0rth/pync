==================
Talking to Servers
==================

Sometimes it can be useful to interact with servers
by hand for troubleshooting or to verify a servers
response to certain commands.

Talking to a web server
-----------------------
For example, we can pipe a GET request to a web server
to retrieve the home page:

.. tab:: Unix

   .. code-block:: sh

      echo "GET / HTTP/1.0\r\n\r\n" | pync -q -1 host.example.com 80

.. tab:: Windows

   .. code-block:: sh

      echo "GET / HTTP/1.0\r\n\r\n" | py -m pync -q -1 host.example.com 80

.. tab:: Python

   .. code-block:: python

      # http_get.py
      import io
      from pync import pync
      # BytesIO turns our request into a file-like
      # object for the pync function.
      request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
      pync('-q -1 host.example.com 80', stdin=request)

Talking to an SMTP server
-------------------------
| You could also submit emails to Simple Mail Transfer Protocol (SMTP) servers.
| Suppose you have a text file (email_template.txt)::

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

| SMTP requires lines to be terminated with a carriage return (CR)
  line feed (LF) sequence (\r\n).
| The -C flag tells **pync** to replace all LF characters (\n) with CRLF characters instead (\r\n).

