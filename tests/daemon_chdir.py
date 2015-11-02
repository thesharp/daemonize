#!/usr/bin/env python

from sys import argv

from daemonize import Daemonize

pid = argv[1]
working_dir = argv[2]
file_name = argv[3]


def main():
    with open(file_name, "w") as f:
        f.write("test")


daemon = Daemonize(app="test_app", pid=pid, action=main, chdir=working_dir)
daemon.start()
