========================
[-e]xecuting [-c]ommands
========================

.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

The `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
and `-c <https://pync.readthedocs.io/en/latest/options/execute.html>`_
options both execute a process and connect the process' stdin/stdout/stderr
to the network socket.

The difference between the two is that
`-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
takes a single filename to execute whereas
`-c <https://pync.readthedocs.io/en/latest/options/execute.html>`_
can process command arguments and other shell features.

A Simple Reverse Shell (-e)
===========================

1. Create a local test server to catch the reverse shell:

.. tab:: Unix

   .. code-block:: sh

      pync -lv localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lv localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-lv localhost 8000')

2. Connect to the server and use the `-e <https://pync.readthedocs.io/en/latest/options/execute.html>`_
   option to execute a shell once the connection has been established.

.. tab:: Unix

   .. code-block:: sh

      pync -ve /bin/bash localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -ve cmd localhost 8000

.. tab:: Python

   .. code-block:: python

      import platform
      from pync import pync

      cmd = '/bin/bash'
      if platform.system() == 'Windows':
          cmd = 'cmd'

      pync('-ve {} localhost 8000'.format(cmd))

A Simple Reverse Shell (-c)
===========================

The `-c <https://pync.readthedocs.io/en/latest/options/execute.html>`_
option lets us pass arguments to give us a more customized shell.

1. Create a local test server to catch the reverse shell:

.. tab:: Unix

   .. code-block:: sh

      pync -lv localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -lv localhost 8000

.. tab:: Python

   .. code-block:: python

      from pync import pync
      pync('-lv localhost 8000')

2. Connect to the server and use the `-c <https://pync.readthedocs.io/en/latest/options/execute.html>`_
   option to execute a shell once the connection has been established.

.. tab:: Unix

   .. code-block:: sh

      pync -vc "PS1='$ ' sh -i" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vc "cmd /q" localhost 8000

.. tab:: Python

   .. code-block:: python

      import platform
      from pync import pync

      cmd = "PS1='$ ' sh -i"
      if platform.system() == 'Windows':
          cmd = 'cmd /q'

      pync('-ve {} localhost 8000'.format(cmd))

:SEE ALSO:

* :doc:`../examples/remote-command-exec`

