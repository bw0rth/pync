========================
Remote Command Execution
========================

Using the `-c <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option, we can execute a command and connect it's stdin/stdout/stderr
to the network socket.

For example, we could create an interactive shell
to execute commands on a remote machine.

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

A Simple Reverse Shell
======================

1. Create a server that will listen for the reverse shell connection:

.. tab:: Unix

   .. code-block:: sh
   
      pync -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -l localhost 8000

.. tab:: Python

   .. code-block:: python
   
      from pync import pync
      pync('-l localhost 8000')

2. On another console, connect back to our server and
   execute the shell:

.. tab:: Unix

   .. code-block:: sh

      pync -c "PS1='$ ' sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -c "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      # reverse_shell.py
      import platform
      from pync import pync

      command = "PS1='$ ' sh -i"
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-c {} localhost 8000'.format(command))

There should now be a prompt on the server console that
allows you to remotely execute commands on the client machine.

A Simple Bind Shell
===================

1. Create a server on port 8000 that executes the shell upon
   connection:

.. tab:: Unix

   .. code-block:: sh

      pync -c "PS1='$ ' sh -i" -l localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -c "cmd /q" -l localhost 8000

.. tab:: Python

   .. code-block:: python

      # bind_shell.py
      import platform
      from pync import pync

      command = "PS1='$ ' sh -i"
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-c {} -l localhost 8000'.format(command))

2. On another console, connect to the server to
   interact with the shell:

.. tab:: Unix

   .. code-block:: sh

      pync localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('localhost 8000')

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/execute`
* :doc:`../options/listen`

