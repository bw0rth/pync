# pync
arbitrary TCP and UDP connections and listens (Netcat for Python).

Like Netcat, pync can be used for:
* Interactive client/server communication
* Remote file transfer
* Simple network chat
* Port scanning
* Relaying network data
* Executing commands over the network

## Installation
1. Install [Python](https://www.python.org/) if not already installed (version 2.7 or higher).

2. Use Python's pip command to install pync straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```

## Usage
### Using pync from the command line
To use pync from the command line, you can use the pync command.<br/>
As an example, let's create a local TCP server:
   ```sh
   pync -l localhost 8000
   ```
You can also run pync as a module with Python.<br/>
Run the following command to connect to the server:
   ```sh
   python -m pync localhost 8000
   ```
### Using pync inside a Python script
You can import pync from within your own Python scripts.<br/>
Here's an example that creates a local TCP server using the pync function:
   ```py
   from pync import pync
   with pync('-l localhost 8000') as nc:
       nc.run()
   ```
And now to connect to the server and send it a message.<br/>
Here we create a file-like object from our message string and pass it to Netcat's stdin:
   ```py
   from pync import pync, makefile
   with pync('localhost 8000') as nc:
       message = makefile('Hello, World!\n')
       nc.run(stdin=message)
   ```
