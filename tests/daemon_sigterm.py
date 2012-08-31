#!/usr/bin/env python

from time import sleep

import daemonize

pid = "/tmp/test.pid"
logfile = "/tmp/test.log"


def main():
    while True:
        daemonize.logging.debug("...")
        sleep(5)

daemonize.start(main, pid, logfile, debug=True)
