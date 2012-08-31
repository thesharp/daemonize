import unittest
import os
import subprocess
from time import sleep


class CounterTest(unittest.TestCase):
    def setUp(self):
        self.logfile = "/tmp/test.log"
        self.pidfile = "/tmp/test.pid"
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)
        os.system("python tests/daemon_counter.py")
        sleep(.1)

    def tearDown(self):
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)
        if os.path.isfile(self.pidfile):
            os.remove(self.pidfile)

    def test_counter_logfile(self):
        self.assertTrue(os.path.isfile(self.logfile))

    def test_counter_logfile_length(self):
        log = open(self.logfile, "r")
        self.assertEqual(len(log.readlines()), 7)
        log.close()

    def test_counter_logfile_last_line(self):
        log = open(self.logfile, "r")
        self.assertEqual(log.readlines()[6].split()[4], "4")
        log.close()


class DaemonizeTest(unittest.TestCase):
    def setUp(self):
        self.logfile = "/tmp/test.log"
        self.pidfile = "/tmp/test.pid"
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)
        os.system("python tests/daemon_sigterm.py")
        sleep(.1)

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)

    def test_is_working(self):
        proc = subprocess.Popen("ps ax | awk '{print $1}' | grep `cat %s`" \
                                % self.pidfile, shell=True,
                                stdout=subprocess.PIPE)
        ps_pid = proc.communicate()[0]
        pidfile = open(self.pidfile, "r")
        pid = pidfile.read()
        pidfile.close()
        self.assertEqual("%s\n" % pid, ps_pid)

    def test_pidfile_presense(self):
        self.assertTrue(os.path.isfile(self.pidfile))


class SIGTERMTest(unittest.TestCase):
    def setUp(self):
        self.logfile = "/tmp/test.log"
        self.pidfile = "/tmp/test.pid"
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)
        os.system("python tests/daemon_sigterm.py")
        sleep(.1)

    def test_sigterm(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)
        self.assertFalse(os.path.isfile(self.pidfile))

    def tearDown(self):
        os.system("kill `cat %s`" % self.pidfile)
        sleep(.1)
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)

if __name__ == '__main__':
    unittest.main()
