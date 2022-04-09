=====================
[-e]xecuting Commands
=====================

Using the `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option, you can execute commands over Netcat's connection.

Hello World
===========

1. By combining `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
   with the `-l <https://pync.readthedocs.io/en/latest/options/listen.html>`_
   option, we can create a server that will echo "Hello, World!" to the
   first client that connects:

.. tab:: Unix

   .. code-block:: sh

      pync -le 'echo "Hello, World!"' localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -le "echo Hello, World!" localhost 8000

.. tab:: Python

   .. code-block:: python

      import platform
      from pync import pync

      message = '"Hello, World!"'
      if platform.system() == 'Windows':
          message = 'Hello, World!'

      pync('-le \'echo {}\' localhost 8000'.format(message))

2. Test this by connecting to the server:

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
   <br>

.. toctree::
   :caption: See Also

   ../examples/remote-command-exec

