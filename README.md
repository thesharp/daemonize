# daemonize

## Description
**daemonize** is a library for writing system daemons in Python. It was forked from [daemonize.sourceforge.net](http://daemonize.sourceforge.net). It is distributed under PSF license.

## Installation
You can install it from Python Package Index (PyPI):

	$ pip install daemonize

## Usage
    #!/usr/bin/env python

    from time import sleep

    import daemonize

    pid = "/tmp/test.pid"
    logfile = "/tmp/test.log"


    def main():
        while True:
            daemonize.logging.debug("Doing some pointless job.")
            sleep(5)

    daemonize.start(main, pid, logfile, debug=True)
