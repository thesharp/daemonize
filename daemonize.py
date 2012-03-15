#!/usr/bin/python
# Copyright 2007 Jerry Seutter yello (*a*t*) thegeeks.net
# Copyright 2012 Ilya A. Otyutskiy <sharp@thesharp.ru>

from functools import partial

import fcntl
import os
import sys
import time
import signal
import resource
import logging


def sigterm(pid, signum, frame):
    logging.info("Caught signal %d. Stopping daemon." % signum)
    os.remove(pid)
    sys.exit(0)


def start(fun_to_start, pid, logfile=None, debug=False):
    # Fork, creating a new process for the child.
    process_id = os.fork()
    if process_id < 0:
        # Fork error.  Exit badly.
        sys.exit(1)
    elif process_id != 0:
        # This is the parent process.  Exit.
        sys.exit(0)
    # This is the child process.  Continue.

    # Stop listening for signals that the parent process receives.
    # This is done by getting a new process id.
    # setpgrp() is an alternative to setsid().
    # setsid puts the process in a new parent group and detaches its
    # controlling terminal.
    process_id = os.setsid()
    if process_id == -1:
        # Uh oh, there was a problem.
        sys.exit(1)

    # Close file descriptors
    devnull = "/dev/null"
    if hasattr(os, "devnull"):
        # Python has set os.devnull on this system, use it instead
        # as it might be different than /dev/null.
        devnull = os.devnull

    null_descriptor = open(devnull, "rw")
    for fd in range(resource.getrlimit(resource.RLIMIT_NOFILE)[0]):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open(devnull, os.O_RDWR)
    os.dup(0)
    os.dup(0)

    # Set umask to default to safe file permissions when running
    # as a root daemon.  027 is an octal number.
    os.umask(027)

    # Change to a known directory.  If this isn't done, starting
    # a daemon in a subdirectory that needs to be deleted results
    # in "directory busy" errors.
    # On some systems, running with chdir("/") is not allowed,
    # so this should be settable by the user of this library.
    os.chdir("/")

    # Create a lockfile so that only one instance of this daemon
    # is running at any time.
    lockfile = open(pid, "w")
    # Try to get an exclusive lock on the file.  This will fail
    # if another process has the file locked.
    fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)

    # Record the process id to the lockfile.  This is standard
    # practice for daemons.
    lockfile.write("%s" % (os.getpid()))
    lockfile.flush()

    # Set custom action on SIGTERM.
    signal.signal(signal.SIGTERM, partial(sigterm, pid))

    # Initializing logger.
    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", \
                        datefmt="%b %d %H:%M:%S", level=loglevel, \
                        filename=logfile)
    logging.info("Starting daemon.")

    fun_to_start()
