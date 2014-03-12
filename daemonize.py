# #!/usr/bin/python

import fcntl
import os
import pwd
import grp
import sys
import signal
import resource
import logging
import atexit
from logging import handlers


class Daemonize(object):
    """ Daemonize object
    Object constructor expects three arguments:
    - app: contains the application name which will be sent to syslog.
    - pid: path to the pidfile.
    - action: your custom function which will be executed after daemonization.
    - keep_fds: optional list of fds which should not be closed.
    - privileged_action: action that will be executed before drop privileges if user or
                         group parameter is provided.
    - user: drop privileges to this user if provided.
    - group: drop privileges to this group if provided.
    """
    def __init__(self, app, pid, action, keep_fds=None, privileged_action=None, user=None, group=None, verbose=False):
        self.app = app
        self.pid = pid
        self.action = action
        self.keep_fds = keep_fds or []
        self.privileged_action = privileged_action or (lambda: ())
        self.user = user
        self.group = group
        # Initialize logging.
        self.logger = logging.getLogger(self.app)
        self.logger.setLevel(logging.DEBUG)
        # Display log messages only on defined handlers.
        self.logger.propagate = False
        self.verbose = verbose

    def sigterm(self, signum, frame):
        """ sigterm method
        These actions will be done after SIGTERM.
        """
        self.logger.warn("Caught signal %s. Stopping daemon." % signum)
        os.remove(self.pid)
        sys.exit(0)

    def exit(self):
        """ exit method
        Cleanup pid file at exit.
        """
        self.logger.warn("Stopping daemon.")
        os.remove(self.pid)
        sys.exit(0)

    def start(self):
        """ start method
        Main daemonization process.
        """
        # Fork, creating a new process for the child.
        process_id = os.fork()
        if process_id < 0:
            # Fork error. Exit badly.
            sys.exit(1)
        elif process_id != 0:
            # This is the parent process. Exit.
            sys.exit(0)
        # This is the child process. Continue.

        # Stop listening for signals that the parent process receives.
        # This is done by getting a new process id.
        # setpgrp() is an alternative to setsid().
        # setsid puts the process in a new parent group and detaches its controlling terminal.
        process_id = os.setsid()
        if process_id == -1:
            # Uh oh, there was a problem.
            sys.exit(1)

        # Close all file descriptors, except the ones mentioned in self.keep_fds.
        devnull = "/dev/null"
        if hasattr(os, "devnull"):
            # Python has set os.devnull on this system, use it instead as it might be different
            # than /dev/null.
            devnull = os.devnull

        for fd in range(resource.getrlimit(resource.RLIMIT_NOFILE)[0]):
            if fd not in self.keep_fds:
                try:
                    os.close(fd)
                except OSError:
                    pass

        os.open(devnull, os.O_RDWR)
        os.dup(0)
        os.dup(0)

        # Initialize syslog.
        # It will work on OS X and Linux. No FreeBSD support, guys, I don't want to import re here
        # to parse your peculiar platform string.
        if sys.platform == "darwin":
            syslog_address = "/var/run/syslog"
        else:
            syslog_address = "/dev/log"
        syslog = handlers.SysLogHandler(syslog_address)
        if self.verbose:
            syslog.setLevel(logging.DEBUG)
        else:
            syslog.setLevel(logging.INFO)
        # Try to mimic to normal syslog messages.
        formatter = logging.Formatter("%(asctime)s %(name)s: %(message)s",
                                      "%b %e %H:%M:%S")
        syslog.setFormatter(formatter)

        self.logger.addHandler(syslog)

        # Set umask to default to safe file permissions when running as a root daemon. 027 is an
        # octal number which we are typing as 0o27 for Python3 compatibility.
        os.umask(0o27)

        # Change to a known directory. If this isn't done, starting a daemon in a subdirectory that
        # needs to be deleted results in "directory busy" errors.
        os.chdir("/")

        # Execute privileged action
        priviled_action_result = self.privileged_action()

        # Change gid
        if self.group:
            try:
                gid = grp.getgrnam(self.group).gr_gid
            except KeyError:
                self.logger.error("Group {0} not found".format(self.group))
                sys.exit(1)
            try:
                os.setgid(gid)
            except OSError:
                self.logger.error("Unable to change gid.")
                sys.exit(1)

        # Change uid
        if self.user:
            try:
                uid = pwd.getpwnam(self.user).pw_uid
            except KeyError:
                self.logger.error("User {0} not found.".format(self.user))
                sys.exit(1)
            try:
                os.setuid(uid)
            except OSError:
                self.logger.error("Unable to change uid.")
                sys.exit(1)

        try:
            # Create a lockfile so that only one instance of this daemon is running at any time.
            lockfile = open(self.pid, "w")
        except IOError:
            self.logger.error("Unable to create a pidfile.")
            sys.exit(1)
        try:
            # Try to get an exclusive lock on the file. This will fail if another process has the file
            # locked.
            fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Record the process id to the lockfile. This is standard practice for daemons.
            lockfile.write("%s" % (os.getpid()))
            lockfile.flush()
        except IOError:
            self.logger.error("Unable to lock on the pidfile.")
            os.remove(self.pid)
            sys.exit(1)

        # Set custom action on SIGTERM.
        signal.signal(signal.SIGTERM, self.sigterm)
        atexit.register(self.exit)

        self.logger.warn("Starting daemon.")

        self.action(*priviled_action_result)
