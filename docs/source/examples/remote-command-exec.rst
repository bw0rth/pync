========================
Remote Command Execution
========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

The **-e** option allows you to execute a process and have that process' stdin/stdout/stderr
be connected to the network socket.

Any data coming in from the network will go to the process' stdin and any
data coming from the process' stdout/stderr with go out to the network.

For example, we can create an interactive shell
to execute commands on a remote machine.

A Simple Reverse Shell
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

      pync -ve "/bin/sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -ve "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      # reverse_shell.py
      import platform
      from pync import pync

      command = '/bin/sh -i'
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-ve "{}" localhost 8000'.format(command))

There should now be a prompt on the server console that
allows you to remotely execute commands on the client machine.

A Simple Bind Shell
===================

1. Create a server on port 8000 that executes the shell upon
   connection:

.. tab:: Unix

   .. code-block:: sh

      pync -vle "/bin/sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vle "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      # bind_shell.py
      import platform
      from pync import pync

      command = '/bin/sh -i'
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-vle "{}" localhost 8000'.format(command))

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

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/execute`
* :doc:`../options/listen`
* :doc:`../options/verbose`

