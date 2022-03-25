=====================
[-e]xecuting Commands
=====================

Using the **-e** option, you can execute a command and
connect the command processes i_o with Netcat's connection
socket.

For example, by combining the -e option with both the -l
option to [-l]isten for connections and the -k option
to [-k]eep the server open, we can create a simple
date/time server:

.. tab:: Unix

   .. code:: sh

      pync -kle date localhost 8000

.. tab:: Python

   .. code:: python

      from pync import pync
      pync('-kle date localhost 8000')

