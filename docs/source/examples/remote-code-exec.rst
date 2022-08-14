========================
Remote Code Execution
========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

The **-y** option allows you to execute a string of python code and have the
python process' stdin/stdout/stderr be connected to the network socket.

Any data coming in from the network will go to the python process' stdin and any
data coming from the python process' stdout/stderr will go out to the network.

For example, we can create an interactive python interpreter shell
to execute python code on a remote machine.

A Reverse Python Shell
======================

1. Create a local server that will listen for the reverse shell connection:

.. tab:: Unix

   .. code-block:: sh
   
      pync -vl localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vl localhost 8000

.. tab:: Python

   .. code-block:: python
   
      from pync import pync
      pync('-vl localhost 8000')

2. On another console, connect back to the server and
   execute the shell:

.. tab:: Unix

   .. code-block:: sh

      pync -vy "import code; code.interact()" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vy "import code; code.interact()" localhost 8000

.. tab:: Python

   .. code-block:: python

      # reverse_pyshell.py
      from pync import pync
      pync('-vy "import code; code.interact()" localhost 8000'

There should now be a prompt on the server console that
allows you to remotely execute python code on the client machine.

A Simple Bind Shell
===================

1. Create a server on port 8000 that executes the shell upon
   connection:

.. tab:: Unix

   .. code-block:: sh

      pync -vly "import code; code.interact()" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vly "import code; code.interact()" localhost 8000

.. tab:: Python

   .. code-block:: python

      # bind_pyshell.py
      from pync import pync
      pync('-vly "import code; code.interact()" localhost 8000'

2. On another console, connect to the server to
   interact with the shell:

.. tab:: Unix

   .. code-block:: sh

      pync -v localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -v localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-v localhost 8000')

There should now be a prompt on the client console that
allows you to remotely execute python code on the server machine.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/py-exec`
* :doc:`../options/listen`
* :doc:`../options/verbose`

