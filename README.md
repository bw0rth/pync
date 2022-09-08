<h1 align="center">
  <a href="https://github.com/brenw0rth/pync"><img src="identicon.png" alt="pync" width=50></a>
  pync
</h1>

<p align="center">
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
* [Talking to Servers](https://pync.readthedocs.io/en/latest/talking-to-servers.html)
* [Data Transfer](https://pync.readthedocs.io/en/latest/data-transfer.html)
* [Port Scanning](https://pync.readthedocs.io/en/latest/port-scanning.html)
* [Remote Command Execution](https://pync.readthedocs.io/en/latest/remote-command-exec.html)
* [Remote Code Execution](https://pync.readthedocs.io/en/latest/remote-code-exec.html)

## Installation
**pync** should work on any system with  [Python](https://www.python.org/)
installed (version 2.7 or higher).

Use Python's pip command to install **pync** straight from github:
<details open>
<summary>Unix</summary>

```sh
pip install https://github.com/brenw0rth/pync/archive/main.zip
```
</details>

<details>
<summary>Windows</summary>

```sh
py -m pip install https://github.com/brenw0rth/pync/archive/main.zip
```
</details>

## Documentation
https://pync.readthedocs.io
### Contents
* [Getting Started](https://pync.readthedocs.io/en/latest/getting-started.html)
* [Options](https://pync.readthedocs.io/en/latest/options/index.html)
* [Client/Server Model](https://pync.readthedocs.io/en/latest/client-server.html)
* [Data Transfer](https://pync.readthedocs.io/en/latest/data-transfer.html)
* [Talking to Servers](https://pync.readthedocs.io/en/latest/talking-to-servers.html)
* [Port Scanning](https://pync.readthedocs.io/en/latest/port-scanning.html)
* [Remote Command Execution](https://pync.readthedocs.io/en/latest/remote-command-exec.html)
* [Remote Code Execution](https://pync.readthedocs.io/en/latest/remote-code-exec.html)
* [Examples](https://pync.readthedocs.io/en/latest/examples.html)
* [API Reference](https://pync.readthedocs.io/en/latest/reference/index.html)
* [Example Scripts](https://github.com/brenw0rth/pync/tree/main/examples)

## See Also
* [Netcat man page](https://helpmanual.io/man1/netcat/)

## Caveats
UDP port scans will always succeed (i.e report the port as open), rendering the -uz combination of flags
relatively useless.

## License
See [LICENSE](https://github.com/brenw0rth/pync/blob/main/LICENSE)
