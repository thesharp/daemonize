#!/usr/bin/env python

from itertools import islice, count

import daemonize

pid = "/tmp/test.pid"
logfile = "/tmp/test.log"


def main():
    daemonize.logging.debug("Counting from 0 to 4 and dying.")
    for i in islice(count(), 5):
        daemonize.logging.debug(i)

daemonize.start(main, pid, logfile, debug=True)
