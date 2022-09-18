<h1 align="left">
  <a href="https://github.com/brenw0rth/pync"><img src="identicon.png" alt="pync" width=50></a>
  pync
</h1>

<p align="left">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
  </a>
  <a href="https://gitHub.com/brenw0rth/pync/stargazers/">
    <img src="https://badgen.net/github/stars/brenw0rth/pync">
  </a>
  <a href="https://gitHub.com/brenw0rth/pync/network/members">
    <img src="https://badgen.net/github/forks/brenw0rth/pync">
  </a>

  </br>

  <a href="https://github.com/brenw0rth/pync/actions/workflows/python-package.yml">
    <img src="https://github.com/brenw0rth/pync/actions/workflows/python-package.yml/badge.svg">
  </a>
  <a href="https://readthedocs.org/projects/pync/">
    <img src="https://readthedocs.org/projects/pync/badge/?version=latest">
  </a>

  </br>

  <a href="https://github.com/brenw0rth/pync/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/brenw0rth/pync">
  </a>
</p>

## Name
**pync** - arbitrary TCP and UDP connections and listens ([Netcat](https://en.wikipedia.org/wiki/Netcat) for Python).

## Synopsis
<details open>
<summary>Unix</summary>

```sh
pync [-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
     [-i interval] [-O length] [-P proxy_username] [-p source_port]
     [-q seconds] [-s source] [-T toskeyword] [-w timeout]
     [-X proxy_protocol] [-x proxy_address[:port]]
     [-Y pyfile] [-y pycode] [dest] [port]
```
</details>

<details>
<summary>Windows</summary>

```sh
py -m pync [-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
           [-i interval] [-O length] [-P proxy_username] [-p source_port]
           [-q seconds] [-s source] [-T toskeyword] [-w timeout]
           [-X proxy_protocol] [-x proxy_address[:port]]
           [-Y pyfile] [-y pycode] [dest] [port]
```
</details>

<details>
<summary>Python</summary>

```python
from pync import pync
args = '''[-46bCDdhklnruvz] [-c string] [-e filename] [-I length]
          [-i interval] [-O length] [-P proxy_username] [-p source_port]
          [-q seconds] [-s source] [-T toskeyword] [-w timeout]
          [-X proxy_protocol] [-x proxy_address[:port]]
          [-Y pyfile] [-y pycode] [dest] [port]'''
pync(args, stdin, stdout, stderr)
```
</details>

## Description
Inspired by the [Black Hat Python](https://github.com/EONRaider/blackhat-python3) book,
the goal of **pync** was to create an easy to use library that
provides [Netcat](https://en.wikipedia.org/wiki/Netcat)-like functionality for Python developers.</br>

Common uses include:
* simple TCP proxies
* shell-script based HTTP clients and servers
* network daemon testing
* a SOCKS or HTTP ProxyCommand for ssh(1)

## Installation
**pync** should work on any system with  [Python](https://www.python.org/)
installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from github:
<details open>
<summary>Unix</summary>

```sh
python -m pip install https://github.com/brenw0rth/pync/archive/main.zip
```
</details>

<details>
<summary>Windows</summary>

```sh
py -m pip install https://github.com/brenw0rth/pync/archive/main.zip
```
</details>

## Usage
* [Client/Server Model](https://pync.readthedocs.io/en/latest/usage/client-server.html)
* [Data Transfer](https://pync.readthedocs.io/en/latest/usage/data-transfer.html)
* [Talking to Servers](https://pync.readthedocs.io/en/latest/usage/talking-to-servers.html)
* [Port Scanning](https://pync.readthedocs.io/en/latest/usage/port-scanning.html)
* [Remote Command Execution](https://pync.readthedocs.io/en/latest/usage/remote-command-exec.html)
* [Remote Code Execution](https://pync.readthedocs.io/en/latest/usage/remote-code-exec.html)
* [pync For Developers](https://pync.readthedocs.io/en/latest/usage/pync-for-devs.html)

## Options

| Option         | Description
| :------------- | :----------
| -4             | Use IPv4 addresses only
| -6             | Use IPv6 addresses only
| -b             | Allow broadcast
| -C             | Send CRLF as line-ending
| [-c](https://pync.readthedocs.io/en/latest/options/exec.html) string | specify shell commands to exec after connect (use with caution).
| -D             | Enable the debug socket option
| -d             | Detach from stdin
| [-e](https://pync.readthedocs.io/en/latest/options/exec.html) filename | specify filename to exec after connect (use with caution).
| [-h](https://pync.readthedocs.io/en/latest/options/help.html), [--help](https://pync.readthedocs.io/en/latest/options/help.html) | show available options and exit.
| -I length      | TCP receive buffer length
| -i secs        | Delay interval for lines sent, ports scanned
| [-k](https://pync.readthedocs.io/en/latest/options/keep-server-open.html) | Keep inbound sockets open for multiple connects
| [-l](https://pync.readthedocs.io/en/latest/options/listen.html) | Listen mode, for inbound connects
| -n             | Suppress name/port resolutions
| -O length      | TCP send buffer length
| -P proxy_username | Username for proxy authentication
| -p source_port | Specify local port for remote connects
| [-q](https://pync.readthedocs.io/en/latest/options/quit-after-eof.html) seconds | quit after EOF on stdin and delay of seconds
| -r             | Randomize remote ports
| -s source      | Local source address
| -T toskeyword  | Set IP Type of Service
| [-u](https://pync.readthedocs.io/en/latest/options/udp.html) | UDP mode [default: TCP]
| [-v](https://pync.readthedocs.io/en/latest/options/verbose.html) | Verbose
| -w secs        | Timeout for connects and final net reads
| -X proxy_protocol | Proxy protocol: "4", "5" (SOCKS) or "connect"
| -x proxy_address[:port] | Specify proxy address and port
| [-Y](https://pync.readthedocs.io/en/latest/options/py-exec.html) pyfile | specify python file to exec after connect (use with caution).
| [-y](https://pync.readthedocs.io/en/latest/options/py-exec.html) pycode | specify python code to exec after connect (use with caution).
| [-z](https://pync.readthedocs.io/en/latest/options/zero-io.html) | Zero-I/O mode [used for scanning]
| dest           | The destination host name or ip to connect or bind to
| port           | The port number to connect or bind to

## API Reference
* [pync](https://pync.readthedocs.io/en/latest/api/pync.html)
* [Netcat](https://pync.readthedocs.io/en/latest/api/Netcat.html)
* [Clients](https://pync.readthedocs.io/en/latest/api/clients.html)
* [Servers](https://pync.readthedocs.io/en/latest/api/servers.html)
* [Connections](https://pync.readthedocs.io/en/latest/api/connections.html)

## Examples
| Example | Description
| :------ | :----------
| [chat.py](https://github.com/brenw0rth/pync/blob/main/examples/chat.py) | Simple chat protocol with custom username
| [upload.py](https://github.com/brenw0rth/pync/blob/main/examples/ftransfer/upload.py) | Simple file upload (use with caution).
| [download.py](https://github.com/brenw0rth/pync/blob/main/examples/ftransfer/download.py) | Simple file download (use with caution).
| [pyshell.py](https://github.com/brenw0rth/pync/blob/main/examples/pyshell.py) | Reverse or bind python interpreter shell (use with caution).
| [scan.py](https://github.com/brenw0rth/pync/blob/main/examples/scan.py) | Simple TCP connect port scanner
| [shell.py](https://github.com/brenw0rth/pync/blob/main/examples/shell.py) | Reverse or bind remote system shell (use with caution).

## See Also
* [Netcat man page](https://helpmanual.io/man1/netcat/)

## Caveats
UDP port scans will always succeed (i.e report the port as open), rendering the -uz combination of flags
relatively useless.

## License
See [LICENSE](https://github.com/brenw0rth/pync/blob/main/LICENSE)
