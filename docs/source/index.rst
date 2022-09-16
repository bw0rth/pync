.. |identicon| image:: ../../identicon.png
   :width: 60

********************************
|identicon| pync - documentation
********************************

Name
====
**pync** - arbitrary TCP and UDP connections and listens (Netcat for Python).

Synopsis
========
.. tab:: Unix

   .. code-block:: sh
        
      pync [-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
           [-i interval] [-O length] [-P proxy_username] [-p source_port]
           [-q seconds] [-s source] [-T toskeyword] [-w timeout]
           [-X proxy_protocol] [-x proxy_address[:port]]
           [-Y pyfile] [-y pycode] [dest] [port]

.. tab:: Windows

   .. code-block:: sh

      py -m pync [-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
                 [-i interval] [-O length] [-P proxy_username] [-p source_port]
                 [-q seconds] [-s source] [-T toskeyword] [-w timeout]
                 [-X proxy_protocol] [-x proxy_address[:port]]
                 [-Y pyfile] [-y pycode] [dest] [port]
      
.. tab:: Python

   .. code-block:: python
   
      from pync import pync
      args = '''[-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
                [-i interval] [-O length] [-P proxy_username] [-p source_port]
                [-q seconds] [-s source] [-T toskeyword] [-w timeout]
                [-X proxy_protocol] [-x proxy_address[:port]]
                [-Y pyfile] [-y pycode] [dest] [port]'''
      pync(args, stdin, stdout, stderr)

Description
===========
Inspired by the Black Hat Python book, the goal of **pync** was to create an easy to use library that provides Netcat-like functionality for Python developers.

Common uses include:

* simple TCP proxies
* shell-script based HTTP clients and servers
* network daemon testing
* a SOCKS or HTTP ProxyCommand for ssh(1)

Installation
============
**pync** should work on any system with Python installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from GitHub:

.. tab:: Unix

   .. code-block:: sh
        
      python -m pip install https://github.com/brenw0rth/pync/archive/main.zip

.. tab:: Windows

   .. code-block:: sh

      py -m pip install https://github.com/brenw0rth/pync/archive/main.zip

Options
=======

.. list-table::
   :align: left
   :widths: auto
   
   * - Option
     - Description
   * - -4
     - Use IPv4 addresses only
   * - -6
     - Use IPv6 addresses only
   * - -b
     - Allow broadcast
   * - -C
     - Send CRLF as line-ending
   * - `-c <https://pync.readthedocs.io/en/latest/options/exec.html>`_ string
     - specify shell commands to exec after connect (use with caution).
   * - -D
     - Enable the debug socket option
   * - -d
     - Detach from stdin
   * - `-e <https://pync.readthedocs.io/en/latest/options/exec.html>`_ filename
     - specify filename to exec after connect (use with caution).
   * - `-h <https://pync.readthedocs.io/en/latest/options/help.html>`_, `--help <https://pync.readthedocs.io/en/latest/options/help.html>`_
     - show this help message and exit.
   * - -I length
     - TCP receive buffer length
   * - -i secs
     - Delay interval for lines sent, ports scanned
   * - `-k <https://pync.readthedocs.io/en/latest/options/keep-server-open.html>`_
     - Keep inbound sockets open for multiple connects
   * - `-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
     - Listen mode, for inbound connects
   * - -n
     - Suppress name/port resolutions
   * - -O length
     - TCP send buffer length
   * - -P proxy_username
     - Username for proxy authentication
   * - -p source_port
     - Specify local port for remote connects
   * - `-q <https://pync.readthedocs.io/en/latest/options/quit-after-eof.html>`_ seconds
     - quit after EOF on stdin and delay of seconds
   * - -r
     - Randomize remote ports
   * - -s source
     - Local source address
   * - -T toskeyword
     - Set IP Type of Service
   * - `-u <https://pync.readthedocs.io/en/latest/options/udp.html>`_
     - UDP mode [default: TCP]
   * - `-v <https://pync.readthedocs.io/en/latest/options/verbose.html>`_
     - Verbose
   * - -w secs
     - Timeout for connects and final net reads
   * - -X proxy_protocol
     - Proxy protocol: "4", "5" (SOCKS) or "connect"
   * - -x proxy_address[:port]
     - Specify proxy address and port
   * - `-Y <https://pync.readthedocs.io/en/latest/options/py-exec.html>`_ pyfile
     - specify python file to exec after connect (use with caution).
   * - `-y <https://pync.readthedocs.io/en/latest/options/py-exec.html>`_ pycode
     - specify python code to exec after connect (use with caution).
   * - `-z <https://pync.readthedocs.io/en/latest/options/zero-io.html>`_
     - Zero-I/O mode [used for scanning]
   * - dest
     - The destination host name or ip to connect or bind to
   * - port
     - The port number to connect or bind to
     
Usage
=====
* :doc:`usage/client-server`
* :doc:`usage/data-transfer`
* :doc:`usage/talking-to-servers`
* :doc:`usage/port-scanning`
* :doc:`usage/remote-command-exec`
* :doc:`usage/remote-code-exec`
* :doc:`usage/pync-for-devs`

API
===
* :doc:`api/pync`
* :doc:`api/Netcat`
* :doc:`api/clients`
* :doc:`api/servers`
* :doc:`api/connections`

See Also
========
.. toctree::
   
   GitHub Repository <https://github.com/brenw0rth/pync>

Caveats
=======
UDP port scans will always succeed (i.e report the port as open), rendering the -uz combination of flags relatively useless.

