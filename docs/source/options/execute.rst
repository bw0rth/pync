=====================
[-e]xecuting Commands
=====================

Using the **-e** option, you can execute a command and
connect the command processes i_o with Netcat's connection
socket.

Creating a Date/Time Server
===========================

For example, by combining the -e option with both the -l
option to [-l]isten for connections and the -k option
to [-k]eep the server open, we can create a simple
date/time server:

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

      if platform.system() == 'Windows':
          command = "echo %date%-%time%"
      else:
          command = 'date'

      pync('-kle {} localhost 8000'.format(command))

A Simple Reverse Shell
======================

To illustrate an interactive command, we can create a
simple reverse shell that lets us execute commands remotely.

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

      if platform.system() == 'Windows':
          command = 'cmd /q'
      else:
          command = "PS1='$ ' sh -i"

      pync('-e {} localhost 8000'.format(command))

There should now be a prompt on the server console that
allows you to remotely execute commands on the client machine.

