## Name
**pync** - arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Synopsis
```sh
pync [-hkluvz] [-e command] [-q seconds] [destination] [port]
```

## Description
Inspired by the [Black Hat Python](https://github.com/EONRaider/blackhat-python3) book,
the goal of **pync** was to create an easy to use library that
provides [Netcat](https://en.wikipedia.org/wiki/Netcat)-like functionality for Python developers.</br>

Common uses include:
* [Interactive client/server communication](https://pync.readthedocs.io/en/latest/examples/client-server.html)
* [Remote file transfer (upload/download)](https://pync.readthedocs.io/en/latest/examples/data-transfer.html)
* [Port scanning](https://pync.readthedocs.io/en/latest/examples/port-scanning.html)
* [Executing commands over the network](https://pync.readthedocs.io/en/latest/examples/executing-commands.html)

## Installation
**pync** should work on any system with  [Python](https://www.python.org/)
installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```

## Documentation
For full documentation, please visit https://pync.readthedocs.io.

## See Also
* [pync script examples](https://github.com/brenw0rth/pync/tree/main/examples)
* [Netcat man page](https://www.unix.com/man-page/Linux/1/nc/)

## TODO
* Add SSL support
* Add PTY support

## License
MIT
