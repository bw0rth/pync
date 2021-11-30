# pync
arbitrary TCP and UDP connections and listens ([Netcat](https://manpages.debian.org/testing/netcat-openbsd/nc.1.en.html) for Python).

Like Netcat, pync can be used for:
* Interactive client/server communication
* Remote file transfer (upload/download)
* Network chat
* Port scanning
* Relaying/proxying network data
* Executing commands over the network

## Installation
1. Install [Python](https://www.python.org/) if not already installed (version 2.7 or higher).

2. Use Python's pip command to install pync straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```

## Basic Usage
### Using pync from the command line
To use pync from the command line, you can use the pync command.<br/>
Run pync with the "-l" option to listen for incoming connections:
   ```sh
   pync -l localhost 8000
   ```
You can also run pync as a module with Python.<br/>
Run the following command in a separate terminal window to connect to the server:
   ```sh
   python -m pync localhost 8000
   ```
To list all available options for the pync command, use the "-h" option:
   ```sh
   pync -h
   ```
### Using pync inside a Python script
You can import pync into your own Python scripts too.<br/>
Here's an example that creates a local TCP server using the pync function:
   ```py
   # server.py
   from pync import pync
   with pync('-l localhost 8000') as nc:
       nc.run()
   ```
In a separate script, we can use the same pync function to connect to the server:
   ```py
   # client.py
   from pync import pync
   with pync('localhost 8000') as nc:
       nc.run()
   ```
