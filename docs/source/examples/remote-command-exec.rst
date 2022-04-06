========================
Remote Command Execution
========================

Using the `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option, we can execute a shell command and have it's i_o
(input/output) connect to Netcat's network socket.

Using this idea, we can execute commands on a remote
system.

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

2. On another console, create the reverse shell to connect back
   to our server:

.. tab:: Unix

   .. code-block:: sh

      pync -e "PS1='$ ' sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -e "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      # reverse_shell.py
      import platform
      from pync import pync

      command = "PS1='$ ' sh -i"
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-e {} localhost 8000'.format(command))

There should now be a prompt on the server console that
allows you to remotely execute commands on the client machine.

A Simple Bind Shell
===================

1. Create a server on port 8000 that executes the shell upon
   connection:

.. tab:: Unix

   .. code-block:: sh

      pync -le "PS1='$ ' sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -le "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      # bind_shell.py
      import platform
      from pync import pync

      command = "PS1='$ ' sh -i"
      if platform.system() == 'Windows':
          command = 'cmd /q'

      pync('-le {} localhost 8000'.format(command))

2. On another console, connect to the bind shell server:

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

