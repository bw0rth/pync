# pync
arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Navigation
* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Options](#options)
* [Examples](#examples)
* [Module API](#module-api)
* [Website](https://brenw0rth.github.io/pync)

## Description
Inspired by the [Black Hat Python](https://github.com/EONRaider/blackhat-python3) book,
the goal of **pync** was to create an easy to use library that
provides [netcat](https://en.wikipedia.org/wiki/Netcat)-like functionality for Python developers.</br>

Though not yet as fully featured as [netcat](https://en.wikipedia.org/wiki/Netcat), it can
open TCP connections, send UDP packets, listen
on arbitrary TCP and UDP ports and even perform
a simple port scan.

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
   
## Usage
```sh
pync [OPTIONS] DEST PORT
pync [OPTIONS] -l [DEST] PORT
```
   
## Options
| Option     | Description                                     |
| :--------- | ----------------------------------------------- |
| -e CMD     | Execute a command over the network              |
| -h         | show help message and exit                      |
| -k         | Keep inbound sockets open for multiple connects |
| -l         | Listen mode, for inbound connects               |
| -q SECS    | quit after EOF on stdin and delay of SECS       |
| -u         | UDP mode. [default: TCP]                        |
| -v         | Verbose                                         |
| -z         | Zero-I/O mode [used for scanning]               |

## Examples
The following examples are command line examples.</br>
For examples of using **pync** in your own Python scripts, please
refer to the [examples folder](https://github.com/brenw0rth/pync/tree/main/examples) in the repository.

<details>
<summary>Client/server model</summary>

---
Building a basic client/server model using **pync** is quite simple.</br>
On one console, start by creating a TCP server to listen for a connection:
   ```sh
   pync -l 1234
   ```
   
On a second console/machine, create a client to connect to the server:
   ```sh
   pync localhost 1234
   ```
   
There should now be a connection and anything typed in one console
should display in the other and vice-versa.</br>
The connection may be terminated using Ctrl-C.

This may not seem very useful right now but as you'll see in later
examples, you can use this idea to transfer files and other cool stuff.

---
</details>

<details>
<summary>Data transfer</summary>

---
> :warning: WARNING</br>
> Please do not transfer any sensitive information using the
> following methods as the connections are not encrypted/secure.

Expanding upon the previous client/server example, we can easily
transfer data between connections.</br>

Start by creating a TCP server and connecting a file to
pync's standard input.</br>
This server will send the contents of the file to any client
that connects:
   ```sh
   pync -l 1234 < filename.in
   ```
   
Using another machine, connect to the server and capture output
to a new file:
   ```sh
   pync host.example.com 1234 > filename.out
   ```
   
During the file transfer, there won't be any progress indication.</br>
The connection will close automatically after the file has been transferred.

---
</details>

<details>
<summary>Talking To Servers</summary>
</details>

<details>
<summary>Port scanning</summary>
</details>

<details>
<summary>Executing commands over the network</summary>
</details>

## Module API
This section is for python developers looking to use **pync** in
their own scripts.

<details>
   <summary>pync.<b>pync</b>(<i>args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr</i>)</summary>
   
   ---
   The pync.**pync()** function is similar to running **pync** from the command line.</br>
   This function should handle all exceptions and write any errors to <i>stderr</i>.
   
   The <i>args</i> parameter should be a string representing
   the command line arguments to run.</br>
   The return value is an exit status code as an integer.

   Example:
   ```py
   from pync import pync
   status = pync('-l localhost 8000')
   ```
   
   To control input/output, you can use the <i>stdin, stdout, stderr</i>
   parameters.</br>
   These parameters can be any object that has a file-like interface.
   
   > :warning: NOTE</br>
   > **pync** expects to read bytes from stdin and writes bytes to stdout.</br>
   > So be sure to open files in binary mode to avoid errors.
   
   For example, create a TCP server that sends a file to any client
   that connects:
   ```py
   from pync import pync
   with open('file.in', 'rb') as f:
       pync('-l localhost 8000', stdin=f)
   ```
   
   And now, in a separate script, connect to the server and download the file:
   ```py
   from pync import pync
   with open('file.out', 'wb') as f:
       pync('localhost 8000', stdout=f)
   ```
   
   ---
</details>

<details>
   <summary>pync.<b>connect</b>(<i>dest, port, **kwargs</i>)</summary>
   
   ---
   pync.**connect**() is an alias for the NetcatTCPConnection.connect class method.</br>
   For use when you only need to make one connection to a server.
   
   The <i>dest</i> parameter should be a string containing either the IP address
   or the hostname of the server machine.</br>
   The <i>port</i> parameter should be an integer between 1 and 65535 inclusive
   and determines the port number the target server is listening on.</br>
   Any other keyword arguments will be passed to the NetcatTCPConnection class.
   
   Once the connection has been made, the return value will be a NetcatTCPConnection object.</br>
   
   > :warning: NOTE</br>
   > A NetcatConnection object does not close itself after use.</br>
   > So be sure to either use it's close() method or use a with statement
   > to automatically close it after use.
   
   Example:
   ```py
   import pync
   with pync.connect('localhost', 8000) as conn:
       conn.run()
   ```
   
   The previous example used the NetcatTCPConnection.run() method to simply run netcat.</br>
   For more available methods, please refer to the NetcatTCPConnection documentation.
   
   ---
</details>

<details>
   <summary>pync.<b>listen</b>(<i>dest, port, **kwargs</i>)</summary>
   
   ---
   pync.**listen**() is an alias for the NetcatTCPConnection.listen class method.</br>
   For use when you only want to serve one client.
   
   The <i>dest</i> parameter should be a string containing the interface for the
   server to listen on.</br>
   The <i>port</i> parameter should be an integer between 1 and 65535 inclusive
   and determines the port number the server should listen on.</br>
   Any other keyword arguments will be passed to the NetcatTCPConnection class.
   
   This function will block, waiting for a client to connect.</br>
   Once a client connects, the return value will be a NetcatTCPConnection object.</br>
   
   > :warning: NOTE</br>
   > A NetcatConnection object does not close itself after use.</br>
   > So be sure to either use it's close() method or use a with statement
   > to automatically close it after use.
   
   Example:
   ```py
   import pync
   with pync.listen('localhost', 8000) as conn:
       conn.run()
   ```
   
   The previous example used the NetcatTCPConnection.run() method to simply run netcat.</br>
   For more available methods, please refer to the NetcatTCPConnection documentation.
   
   ---
</details>

<details>
   <summary>pync.<b>Netcat</b>(<i>port, dest='', e=False, k=False, l=False, q=0, u=False, v=False, z=False</i>)</summary>
   
   ---
   Create a **Netcat** object.</br>
   Each parameter has it's own example below, but in short they are:
   
   ### Parameters
   | Parameter | Description                                          |
   | --------- | ---------------------------------------------------- |
   | port      | The port number to listen on or connect to           |
   | dest      | The interface to listen on or hostname to connect to |
   | e         | Execute a command over the network                   |
   | k         | Keep inbound sockets open for multiple connects      |
   | l         | Listen mode, for inbound connects                    |
   | q         | quit after EOF on stdin and delay of SECS            |
   | u         | UDP mode. [default: TCP]                             |
   | v         | Verbose                                              |
   | z         | Zero-I/O mode [used for scanning]                    |
   </br>
   
   > :warning: NOTE</br>
   > The Netcat class doesn't close itself after use.</br>
   > So be sure to use it's close() method or use the with statement
   > to automatically close Netcat after use.
   </br>
   
   There are two ways to create a **Netcat** instance.</br>
   
   1. Passing an args string to the **from_args()** class method:
   ```py
   from pync import Netcat
   with Netcat.from_args('-l localhost 8000') as nc:
       nc.run()
   ```
   
   2. Or passing keyword arguments directly to the Netcat class:
   ```py
   import pync
   with pync.Netcat(8000, 'localhost', l=True) as nc:
       nc.run()
   ```
   
   The <i>e</i> parameter should be a string containing a command
   and any arguments to run.
   
   Example:
   ```py
   import pync
   with pync.Netcat(8000, dest='localhost', l=True, e='date') as nc:
       nc.run()
   ```
   
   ---
</details>
