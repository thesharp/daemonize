import unittest
import os
import subprocess

from tempfile import mkstemp
from time import sleep


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
        pidfile = open(self.pidfile, "r")
        pid = pidfile.read()
        pidfile.close()
        self.assertEqual("%s\n" % pid, ps_pid)

    def test_pidfile_presense(self):
        sleep(10)
        self.assertTrue(os.path.isfile(self.pidfile))


class KeepFDsTest(unittest.TestCase):
    def setUp(self):
        self.pidfile = mkstemp()[1]
        self.logfile = mkstemp()[1]
        os.system("python tests/daemon_keep_fds.py %s %s" % (self.pidfile, self.logfile))
        sleep(1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        os.remove(self.logfile)
        os.remove(self.pidfile)
        sleep(.1)

    def test_keep_fds(self):
        log = open(self.logfile, "r").read()
        self.assertEqual(log, "Test\n")

if __name__ == '__main__':
    unittest.main()
