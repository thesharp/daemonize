#!/usr/bin/env python

from os import getuid, geteuid, getgid, getegid
from sys import argv
from time import sleep

from daemonize import Daemonize

pid = argv[1]
log = argv[2]


def main():
    uids = getuid(), geteuid()
    gids = getgid(), getegid()
    with open(log, "w") as f:
        f.write(" ".join(map(str, uids + gids)))


daemon = Daemonize(app="test_app", pid=pid, action=main, user="nobody", group="nobody")
daemon.start()
