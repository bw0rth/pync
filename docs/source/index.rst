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
...

Options
=======

.. list-table::
   :align: left
   
   * - Option
     - Description
   * - -4
     - Use IPv4 addresses only
   * - -6
     - Use IPv6 addresses only

Contents
========
.. toctree::
   :maxdepth: 2

   options/index
   getting-started
   client-server
   data-transfer
   talking-to-servers
   port-scanning
   remote-command-exec
   remote-code-exec
   examples
   pync-for-devs
   reference/index

See Also
========
.. toctree::
   
   GitHub Repository <https://github.com/brenw0rth/pync>

Caveats
=======
UDP port scans will always succeed (i.e report the port as open), rendering the -uz combination of flags relatively useless.

