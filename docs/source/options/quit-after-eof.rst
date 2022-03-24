=================
[-q]uit After EOF
=================

The **-q** option allows us to quit the readwrite loop after reaching
EOF on stdin.

By default, **pync**'s -q option is set to -1 which tells it to carry
on writing network data to stdout until the connection closes.

Setting the **-q** option to a positive number tells **pync** to
quit the readwrite loop after the number of seconds has elapsed.

