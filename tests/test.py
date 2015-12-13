import unittest
import os
import pwd
import grp
import subprocess

from tempfile import mkstemp
from time import sleep
from os.path import split

NOBODY_UID = pwd.getpwnam("nobody").pw_uid
if os.path.exists("/etc/debian_version"):
    NOBODY_GID = grp.getgrnam("nogroup").gr_gid
else:
    NOBODY_GID = grp.getgrnam("nobody").gr_gid


class DaemonizeTest(unittest.TestCase):
    def setUp(self):
        self.pidfile = mkstemp()[1]
        os.system("python tests/daemon_sigterm.py %s" % self.pidfile)
        sleep(.1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)

    def test_is_working(self):
        sleep(10)
        proc = subprocess.Popen("ps ax | awk '{print $1}' | grep `cat %s`" % self.pidfile,
                                shell=True, stdout=subprocess.PIPE)
        ps_pid = proc.communicate()[0].decode()
        with open(self.pidfile, "r") as pidfile:
            pid = pidfile.read()
        self.assertEqual("%s\n" % pid, ps_pid)

    def test_pidfile_presense(self):
        sleep(10)
        self.assertTrue(os.path.isfile(self.pidfile))


class LockingTest(unittest.TestCase):
    def setUp(self):
        self.pidfile = mkstemp()[1]
        print("First daemonize process started")
        os.system("python tests/daemon_sigterm.py %s" % self.pidfile)
        sleep(.1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)

    def test_locking(self):
        sleep(10)
        print("Attempting to start second daemonize process")
        proc = subprocess.call(["python", "tests/daemon_sigterm.py", self.pidfile])
        self.assertEqual(proc, 1)


class KeepFDsTest(unittest.TestCase):
    def setUp(self):
        self.pidfile = mkstemp()[1]
        self.logfile = mkstemp()[1]
        os.system("python tests/daemon_keep_fds.py %s %s" % (self.pidfile, self.logfile))
        sleep(1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        os.remove(self.logfile)
        sleep(.1)

    def test_keep_fds(self):
        log = open(self.logfile, "r").read()
        self.assertEqual(log, "Test\n")


class UidGidTest(unittest.TestCase):
    def setUp(self):
        self.expected = " ".join(map(str, [NOBODY_UID] * 2 + [NOBODY_GID] * 2))
        self.pidfile = mkstemp()[1]
        self.logfile = mkstemp()[1]

    def tearDown(self):
        os.remove(self.logfile)

    def test_uid_gid(self):
        # Skip test if user is not root
        if os.getuid() != 0:
            return True

        os.chown(self.logfile, NOBODY_UID, NOBODY_GID)

        os.system("python tests/daemon_uid_gid.py %s %s" % (self.pidfile, self.logfile))
        sleep(.1)

        with open(self.logfile, "r") as f:
            self.assertEqual(f.read(), self.expected)
        self.assertEqual(not os.access(self.pidfile, os.F_OK))

    def test_uid_gid_action(self):
        # Skip test if user is not root
        if os.getuid() != 0:
            return True

        os.chown(self.pidfile, NOBODY_UID, NOBODY_GID)

        os.system("python tests/daemon_uid_gid_action.py %s %s" % (self.pidfile, self.logfile))
        sleep(.1)

        with open(self.logfile, "r") as f:
            self.assertEqual(f.read(), self.expected)


class PrivilegedActionTest(unittest.TestCase):
    def setUp(self):
        self.correct_log = """Privileged action.
Starting daemon.
Action.
Stopping daemon.
"""
        self.pidfile = mkstemp()[1]
        self.logfile = mkstemp()[1]
        os.system("python tests/daemon_privileged_action.py %s %s" % (self.pidfile, self.logfile))
        sleep(.1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)

    def test_privileged_action(self):
        sleep(5)
        with open(self.logfile, "r") as contents:
            self.assertEqual(contents.read(), self.correct_log)


class ChdirTest(unittest.TestCase):
    def setUp(self):
        self.pidfile = mkstemp()[1]
        self.target = mkstemp()[1]
        base, file = split(self.target)

        os.system("python tests/daemon_chdir.py %s %s %s" % (self.pidfile, base, file))
        sleep(1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)

    def test_keep_fds(self):
        log = open(self.target, "r").read()
        self.assertEqual(log, "test")

if __name__ == '__main__':
    unittest.main()
