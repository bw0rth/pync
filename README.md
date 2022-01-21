## Name
**pync** - arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Synopsis
**pync** [**-hkluvz**] [**-e** command] [**-q** seconds] [destination] [port]

## Description
Inspired by the [Black Hat Python](https://github.com/EONRaider/blackhat-python3) book,
the goal of **pync** was to create an easy to use library that
provides [netcat](https://en.wikipedia.org/wiki/Netcat)-like functionality for Python developers.</br>

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

There are three ways to use **pync**.
1. Running the **pync** command:</br>
   ```sh
   pync [options] [destination] [port]
   ```
2. Running it as a python module:
   ```sh
   python -m pync [options] [destination] [port]
   ```
3. Importing it into your own python code:
   ```py
   from pync import pync
   pync('[options] [destination] [port]')
   ```
   
### Client/Server model
---
1. Create a server to listen for incoming connections on port 8000:
   <details open>
   <summary>Show command</summary>

   ```sh
   pync -l localhost 8000
   ```
   </details>
   <details>
   <summary>Show python code</summary>

   ```py
   # server.py
   from pync import pync
   pync('-l localhost 8000')
   ```
   </details>
   
2. On a separate console, connect to the server:
   <details open>
   <summary>Show command</summary>
   
   ```sh
   pync localhost 8000
   ```
   </details>
   <details>
   <summary>Show python code</summary>
   
   ```py
   # client.py
   from pync import pync
   pync('localhost 8000')
   ```
   </details>
   
There should now be a connection between the two consoles and anything
typed in one console should display in the other and vice-versa.

### Data transfer
---
   
For more examples on how to use **pync** in your
own scripts, please refer to the [examples folder](https://github.com/brenw0rth/pync/tree/main/examples)
in the code repository.

## See Also
* [Website](https://brenw0rth.github.io/pync)
* [Netcat man page](https://www.unix.com/man-page/Linux/1/nc/)

## TODO
* Add SSL support
* Add PTY support
