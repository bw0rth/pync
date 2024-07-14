=============================================
-Y: specify python file to exec after connect
=============================================

.. warning::
   | - Please BE CAREFUL not to expose your system with this functionality.
   | - Please DO NOT use this functionality for evil purposes.

**pync** can execute Python code in a separate process and connect the
process' stdin/stdout/stderr to the network socket.

Any data that comes in from the network will go to the process' stdin, and
any data that comes out from the process' stdout/stderr will be sent out to the network.

There are two options that can provide this functionality, the lowercase **-y** option
and the uppercase **-Y** option.

This section focuses on the **-Y** option to execute code from a specified file path.
To execute code from a string, see :doc:`../options/py-code-exec`.

Executing Python Files With -Y
==============================
The uppercase **-Y** option takes the full pathname of a python file
to execute.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/py-code-exec`
* :doc:`../options/quit-after-eof`
* :doc:`../options/verbose`
* :doc:`../usage/remote-code-exec`

