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
* [Interactive client/server communication](#talking-to-servers)
* [Remote file transfer (upload/download)](#data-transfer)
* [Port scanning](#port-scanning)
* [Executing commands over the network](#executing-commands)

See the [Examples](#examples) section below for more.

## Documentation
For full documentation, please visit https://pync.readthedocs.io.

## Installation
**pync** should work on any system with  [Python](https://www.python.org/)
installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```
   
## Options
### -h
show help message and exit.

### -k
Keeps the server open between connections.</br>
This option is only valid with the **-l** option.

### -l
Create a server to listen for incoming connections.

### -u
Use UDP for transport instead of TCP.

### -v
Print status messages to stderr.

### -z
Connect then close immediately.</br>
Useful for port scanning when combined with
the **-v** option.

### -e *command*
Execute a command after a connection has been
established.</br>
Input/output will be connected with the newly
created process.

### -q *seconds*
Quit after end of file on stdin with a delay
of <b><i>seconds</i></b>.

## Examples

There are several ways to run **pync**.
* Running the **pync** command:
   ```sh
   pync [options] [destination] [port]
   ```
* Running it as a python module:
   ```sh
   python -m pync [options] [destination] [port]
   ```
* Importing it into your own python code:
   ```py
   from pync import pync
   pync('[options] [destination] [port]')
   ```
   
For examples on how to use **pync** in your
own scripts, please refer to the [examples folder](https://github.com/brenw0rth/pync/tree/main/examples)
in the code repository.
   
### Client/Server Model
---
To illustrate a basic client/server model, we can connect two **pync** instances
together and send messages back and forth.

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

When finished, hit <kbd>Ctrl</kbd><kbd>C</kbd> from either console to close the connection.

### Data Transfer
---
> :warning: WARNING:</br>
> Please DO NOT transfer any sensitive data using this method as the connection
> is not secure.

To build on the previous example, we can transfer file data from one machine
to another.

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

### Talking to Servers
---
Sometimes it can be useful to interact with servers by hand for troubleshooting
or to verify a servers response to certain commands.

1. For example, we can pipe a get request to a web server to retrieve the home page:
   <details open>
   <summary>Show command</summary>
   
   ```sh
   printf "GET / HTTP/1.0\r\n\r\n" | pync host.example.com 80
   ```
   </details>
   <details>
   <summary>Show python code</summary>
   
   ```py
   # get.py
   import io
   from pync import pync
   # BytesIO turns our request into a file-like
   # object for the pync function.
   request = io.BytesIO(b'GET / HTTP/1.0\r\n\r\n')
   pync('host.example.com 80', stdin=request)
   ```
   </details>

### Port Scanning
---
> :warning: WARNING:</br>
> Please DO NOT scan machines without permission.</br>
> Whether it is illegal or not, it is considered rude
> and can be seen as suspicious behaviour.</br>
> It is recommended to setup your own servers or use Nmap's scanme
> domain for testing.

**pync** can be used to perform a simple connect scan to see what ports and
services a target machine is running.

1. To do this, use the -z flag to turn on zero I/O mode and -v to print
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

You may also want to grab the server banner to check for the version
of the service running.</br>

1. You can try this by piping a message to the server and hoping for a response:
   <details open>
   <summary>Show command</summary>

   ```sh
   echo "QUIT" | pync host.example.com 20-30
   ```
   </details>
   <details>
   <summary>Show python code</summary>

   ```py
   # banner.py
   import io
   from pync import pync
   # BytesIO turns our message into a file-like
   # object for the pync function.
   message = io.BytesIO(b'QUIT')
   pync('host.example.com 20-30', stdin=message)
   ```
   </details>

### Executing Commands
---
After a connection to a client or server has been
established, you can execute a command and connect
the input/output of the command process with
the connection.

1. For example, create a server that echoes a message
to the first client that connects:
   <details open>
   <summary>Show command</summary>

   ```sh
   pync -e "echo 'Hello'" -l localhost 8000
   ```
   </details>
   <details>
   <summary>Show python code</summary>

   ```py
   # server.py
   from pync import pync
   pync('-e "echo \'Hello\'" -l localhost 8000')
   ```
   </details>

## See Also
* [pync documentation](https://pync.rtfd.io)
* [Netcat man page](https://www.unix.com/man-page/Linux/1/nc/)

## TODO
* Add SSL support
* Add PTY support
