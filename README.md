# daemonize [![Build Status](https://secure.travis-ci.org/thesharp/daemonize.png)](http://travis-ci.org/thesharp/daemonize)

## Description
**daemonize** is a library for writing system daemons in Python. It has some bits from [daemonize.sourceforge.net](http://daemonize.sourceforge.net). It is distributed under MIT license.

## Dependencies
It is tested under following Python versions:

- 2.6
- 2.7
- 3.3


## Installation
You can install it from Python Package Index (PyPI):

	$ pip install daemonize

## Usage
```python
from time import sleep
from daemonize import Daemonize

pid = "/tmp/test.pid"


def main():
    while True:
        sleep(5)

daemon = Daemonize(app="test_app", pid=pid, action=main)
daemon.start()
```

## File descriptors
Daemonize object's constructor understands the optional argument **keep_fds** which contains a list of FDs which should not be closed. For example:
```python
import logging
from daemonize import Daemonize

pid = "/tmp/test.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/tmp/test.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def main():
    logger.debug("Test")

daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
```
