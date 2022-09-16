========================
[-e]xecuting [-c]ommands
========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

**pync** can execute a process and connect the process' stdin/stdout/stderr
to the network socket.

Any data that comes in from the network will go to the process' stdin, and
any data that comes out from the process' stdout/stderr will be sent out to the network.

There are two options that can provide this functionality, the **-e** option
and the **-c** option.

Running a Command With -e
=========================
The **-e** option takes the full pathname of a command to execute,
along with any arguments.

1. Create a local server that sends "Hello" to the first
   client that connects:

.. tab:: Unix

   .. code-block:: sh

      pync -vle "/bin/echo Hello" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vle "echo Hello" localhost 8000

.. tab:: Python

   .. code-block:: python

      import platform
      from pync import pync

      cmd = '/bin/echo Hello'
      if platform.system() == 'Windows':
          cmd = 'echo Hello'

      pync('-vle "{}" localhost 8000')

2. Connect to the Hello server to see the message:

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

Running a Command With -c
=========================
The **-c** option is the same as the **-e** option but allows
extra shell features such as pipelines and evironment variable expansion.

1. Create a local server that sends the current working directory
   to the first client that connects:

.. tab:: Unix

   .. code-block:: sh

      pync -vle "/bin/echo `pwd`" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vle "echo %cd%" localhost 8000

.. tab:: Python

   .. code-block:: python

      import platform
      from pync import pync

      cmd = '/bin/echo `pwd`'
      if platform.system() == 'Windows':
          cmd = 'echo %cd%'

      pync('-vle "{}" localhost 8000')

2. Connect to the server to receive the server's
   current working directory:

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

* :doc:`../usage/remote-command-exec`

