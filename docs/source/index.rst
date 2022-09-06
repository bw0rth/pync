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
Inspired by the Black Hat Python book, the goal of pync was to create an easy to use library that provides Netcat-like functionality for Python developers.

Common uses include:

* Interactive client/server communication
* Remote data transfer (upload/download)
* Port scanning (simple connect scan)
* Remote command execution (reverse/bind shell)
* Remote code execution (Python)

Contents
========
.. toctree::
   :maxdepth: 2

   getting-started
   options/index
   client-server
   data-transfer
   talking-to-servers
   port-scanning
   remote-command-exec
   remote-code-exec
   examples/index
   pync-for-devs
   reference/index

See Also
========
.. toctree::
   
   GitHub Repository <https://github.com/brenw0rth/pync>

Caveats
=======
UDP port scans will always succeed (i.e report the port as open), rendering the -uz combination of flags relatively useless.

