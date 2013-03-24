#!/usr/bin/env python

import logging
from sys import argv

from daemonize import Daemonize

pid = argv[1]
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(argv[2], "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def main():
    logger.debug("Test")

daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
