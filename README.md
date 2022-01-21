## Name
**pync** - arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Synopsis
```sh
pync [-hkluvz] [-e command] [-q seconds] [destination] [port]
```

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
1. Running the **pync** command:
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
   
For examples on how to use **pync** in your
own scripts, please refer to the [examples folder](https://github.com/brenw0rth/pync/tree/main/examples)
in the code repository.
   
### Client/Server Model
---
1. Create a local server to listen for incoming connections on port 8000:
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

### Data Transfer
---
To build on the previous example, we can transfer file data from one machine
to another.

> :warning: WARNING:</br>
> Please do not transfer any sensitive data using this method as the connection
> is not secure.

1. Create a server to host the file:
   <details open>
   <summary>Show command</summary>
   
   ```sh
   pync -l 8000 < file.in
   ```
   </details>
   <details>
   <summary>Show python code</summary>
   
   ```py
   # server.py
   from pync import pync
   # NOTE:
   # pync reads bytes and writes bytes
   # so be sure to open files in binary
   # mode to avoid any errors.
   with open('file.in', 'rb') as f:
       pync('-l 8000', stdin=f)
   ```
   </details>
   
2. On a separate console, connect to the server to download the file:
   <details open>
   <summary>Show command</summary>
   
   ```sh
   pync localhost 8000 > file.out
   ```
   </details>
   <details>
   <summary>Show python code</summary>
   
   ```py
   # client.py
   from pync import pync
   # NOTE:
   # pync reads bytes and writes bytes
   # so be sure to open files in binary
   # mode to avoid any errors.
   with open('file.out', 'wb') as f:
       pync('localhost 8000', stdout=f)
   ```
   </details>
   
During the file transfer, there won't be any progress indication.</br>
The connection will close automatically after the file has been transferred.

### Port Scanning
---
**pync** can be used to perform a simple connect scan to see what ports and
services a target machine is running.

To do this, use the -z flag to turn on zero I/O mode and -v to print
connection success/failure to the console:
<details open>
   <summary>Show command</summary>
   
   ```sh
   pync -zv host.example.com 20-30 80 443
   ```
   </details>
   <details>
   <summary>Show python code</summary>
   
   ```py
   # scan.py
   from pync import pync
   pync('-zv host.example.com 20-30 80 443')
   ```
   </details>
   
As you can see, you can provide a single port, a list of ports
or a range of ports to scan.</br>
In this case, we scan port 20 to 30 (20,21,22...30), port 80 (http)
and port 443 (https).

## See Also
* [Website](https://brenw0rth.github.io/pync)
* [Netcat man page](https://www.unix.com/man-page/Linux/1/nc/)

## TODO
* Add SSL support
* Add PTY support
