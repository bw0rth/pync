========================
Remote Code Execution
========================
.. warning::
   | Please BE CAREFUL with this functionality as it could expose your system to attackers.
   | Also, please DO NOT use this functionality for evil purposes.

The **-y** option allows you to execute a string of python code in a separate
process and have the process' stdin/stdout/stderr be connected to the network
socket.

Any data coming in from the network will go to the process' stdin and any
data coming from the process' stdout/stderr will go out to the network.

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
   
      import pync
      pync.run('-vl localhost 8000')

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
      import pync
      pync.run('-vy "import code; code.interact()" localhost 8000')

There should now be a prompt on the server console that
allows you to remotely execute python code on the client machine.

A Bind Python Shell
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
      import pync
      pync.run('-vly "import code; code.interact()" localhost 8000')

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

      import pync
      pync.run('-v localhost 8000')

There should now be a prompt on the client console that
allows you to remotely execute python code on the server machine.

A Python Exec Server
====================
Python's builtin exec function lets you execute a string of python
code in a separate namespace.

By reading data from stdin (the network), you can essentially allow
arbitrary code to be executed remotely.

1. Create a server that stays open, receiving python code to
   execute:

.. tab:: Unix

   .. code-block:: sh

      pync -vlky "import sys; exec(sys.stdin.read(), {})" localhost 8000

.. tab:: Windows

   .. code-block:: sh

      py -m pync -vlky "import sys; exec(sys.stdin.read(), {})" localhost 8000

.. tab:: Python

   .. code-block:: python

      # pyexec_server.py
      import pync
      pync.run('-vlky "import sys; exec(sys.stdin.read(), {})" localhost 8000')

We use the **-k** option here to keep the server open between connections,
serving one connection after another.

2. Connect to the exec server and send a string of python code to execute:

.. tab:: Unix

   .. code-block:: sh

      echo "import sys; sys.stdout.write('Hello\n')" | pync -vq -1 localhost 8000

.. tab:: Windows

   .. code-block:: sh

      echo "import sys; sys.stdout.write('Hello\n')" | py -m pync -vq -1 localhost 8000

.. tab:: Python

   .. code-block:: python

      import io
      import pync

      pycode = io.BytesIO(b"import sys; sys.stdout.write('Hello\n')")
      pync.run('-vq -1 localhost 8000', stdin=pycode)

After executing the above, you should be able to see the message "Hello"
printed on the client machine.

Passing a negative number to the **-q** option tells the pync client to
keep running after EOF on stdin (after sending the code to execute).
Otherwise the client would quit immediately, not giving the server any
time to respond.

You should be able to repeat step 2 (sending code to the exec server) for
as long as the server is running.

Experiment by sending different lines of code!

When finished, hit Ctrl+C on the server console to stop the server.

.. raw:: html

   <br>
   <hr>

:SEE ALSO:

* :doc:`../options/py-exec`
* :doc:`../options/listen`
* :doc:`../options/verbose`

