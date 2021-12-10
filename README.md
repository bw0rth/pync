# pync
arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Contents
* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Options](#options)
* [Examples](#examples)
* [Module API](#module-api)

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
1. Install [Python](https://www.python.org/) if not already installed (version 2.7 or higher).

2. Use Python's pip command to install pync straight from github:
   ```sh
   pip install https://github.com/brenw0rth/pync/archive/main.zip
   ```
   
## Usage
```sh
pync [OPTIONS] DEST PORT
pync [OPTIONS] -l [DEST] PORT
```
   
## Options
| Option     | Default | Description                               |
| :--------- | ------- | :---------------------------------------- |
| -e CMD     | n/a     | Execute a command over the network        |
| -h         | n/a     | show help message and exit                |
| -l         | False   | Listen mode, for inbound connects         |
| -q SECS    | 0       | quit after EOF on stdin and delay of SECS |
| -u         | False   | UDP mode. [default: TCP]                  |
| -v         | False   | Verbose                                   |
| -z         | False   | Zero-I/O mode [used for scanning]         |

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
<summary>Port scanning</summary>
</details>

<details>
<summary>Relaying network data</summary>
</details>

<details>
<summary>Executing commands over the network</summary>
</details>

<details>
<summary>Simple network chat</summary>
</details>

<details>
<summary>Creating a reverse/bind backdoor shell</summary>
</details>

## Module API
...
