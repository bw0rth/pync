==================
Executing Commands
==================

Using the `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option, you can execute a command and have the input/output of
the command's process connected to Netcat's network socket.

Incoming network data will be fed to the processes stdin and
any output from the process will be sent back over the network.

.. note::
   With the -e option, the command will only be executed once
   the connection has been established.

Creating a Date/Time Server
===========================

1. Combining the `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
   option with the `-k <https://pync.readthedocs.io/en/latest/options/keep-server-open.html>`_
   and `-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
   options, we can create a simple date/time server:

.. tab:: Unix

   .. code-block:: sh

      pync -kle date localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -kle "echo %date%-%time%" localhost 8000

.. tab:: Python

   .. code-block:: python

      # datetime_server.py
      import platform
      from pync import pync

      command = 'date'
      if platform.system() == 'Windows':
          command = "echo %date%-%time%"

      pync('-kle {} localhost 8000'.format(command))

A Simple Reverse Shell
======================

To illustrate an interactive command, we can create
a simple reverse shell that lets us execute commands
remotely.

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

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

2. On another console, create the reverse shell to connect
   back to our server:

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

Once a connection to our server has been established,
there should be a prompt on the server console that
allows you to remotely execute commands on the client
machine.

