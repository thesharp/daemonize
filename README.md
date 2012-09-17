# daemonize

## Description
**daemonize** is a library for writing system daemons in Python. It has some bits from [daemonize.sourceforge.net](http://daemonize.sourceforge.net). It is distributed under MIT license.

[![Build Status](https://secure.travis-ci.org/thesharp/daemonize.png)](http://travis-ci.org/thesharp/daemonize)

## Installation
You can install it from Python Package Index (PyPI):

	$ pip install daemonize

## Usage
    from time import sleep
    from daemonize import Daemonize

    pid = "/tmp/test.pid"


    def main():
        while True:
            sleep(5)

    daemon = Daemonize(app="test_app", pid=pid, action=main)
    daemon.start()
