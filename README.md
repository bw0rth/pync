## Name
**pync** - arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Synopsis
**pync** [**-hkluvz**] [**-e** command] [**-q** seconds] [destination] [port]

## Description
Inspired by the [Black Hat Python](https://github.com/EONRaider/blackhat-python3) book,
the goal of **pync** was to create an easy to use library that
provides [netcat](https://en.wikipedia.org/wiki/Netcat)-like functionality for Python developers.</br>

Though not yet as fully featured as [netcat](https://en.wikipedia.org/wiki/Netcat), it can
open TCP connections, send UDP packets, listen
on arbitrary TCP and UDP ports and more.

Common uses include:
* Interactive client/server communication
* Remote file transfer (upload/download)
* Port scanning
* Network chat
* Relaying/proxying network data
* Executing commands over the network

For practical examples, see the [Examples](#examples) section below.

## Installation
**pync** should work on any system with  [Python](https://www.python.org/)
installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```
   
## Options
...

## Examples

<details>
<summary>Using pync from the command line</summary>

---
Simply use the **pync** command to run **pync** from the command line:
   ```sh
   pync example.com 80
   ```

---
</details>

<details>
<summary>Using pync from a python script</summary>

---
For examples on how to use **pync** in your
own scripts, please refer to the [examples folder](https://github.com/brenw0rth/pync/tree/main/examples)
in the code repository.

---
</details>

## See Also
* [Website](https://brenw0rth.github.io/pync)
* [Netcat man page](https://www.unix.com/man-page/Linux/1/nc/)

## TODO
* Add SSL support
* Add PTY support
