***************************************
a SOCKS or HTTP ProxyCommand for ssh(1)
***************************************

It's possible to tunnel **pync**'s traffic through a proxy
server by specifying it's address with the -x argument:

.. code-block:: sh

    pync -x proxy_addr[:proxy_port] dest port

By passing this command to the SSH ProxyCommand option,
you can create an SSH client that tunnels it's connection through
a proxy server.

For example, to create an SSH client that connects to a SOCKS v5 proxy
at address "localhost" on port 8000:

.. code-block:: sh

    ssh -o ProxyCommand="pync -X 5 -x localhost:8000 %h %p" user@host

You can also tunnel the traffic through an HTTP proxy by setting the
-X argument to "connect":

.. code-block:: sh

    ssh -o ProxyCommand="pync -X connect -x localhost:8000 %h %p" user@host
