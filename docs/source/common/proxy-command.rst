***************************************
a SOCKS or HTTP ProxyCommand for ssh(1)
***************************************

You can tunnel **pync**'s traffic through
a SOCKS or HTTP proxy server by using the
-X flag to specify the protocol (default: SOCKS v5)
and -x to specify the address of the proxy server:

.. code-block:: sh

    pync [-X proto] -x addr[:port] dest port

By passing this command to the SSH ProxyCommand option,
you can create an SSH client that tunnels it's connection through
a proxy server.

For example, the following creates an SSH client that tunnels it's
traffic through a SOCKS v5 proxy server at localhost port 8000:

.. code-block:: sh

    ssh -o ProxyCommand="pync -X 5 -x localhost:8000 %h %p" user@host

You can also tunnel the traffic through an HTTP proxy by setting the
-X argument to "connect":

.. code-block:: sh

    ssh -o ProxyCommand="pync -X connect -x localhost:8000 %h %p" user@host
