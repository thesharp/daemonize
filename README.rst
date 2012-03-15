daemonize
=========

Description
-----------
``daemonize`` is a library for writing system daemons in Python. It was forked from daemonize.sourceforge.net.

Installation
------------
You can install it from Python Package Index (PyPI) using ``$ pip install daemonize``

Usage
-----
    #!/usr/bin/python

    import time
    
    import daemonize
    
    pid = "/tmp/test.pid"
    logfile = "/tmp/test.log"
    
    def main():
        while True:
            daemonize.logging.debug("Doing some pointless job.")
            time.sleep(5)

    daemonize.start(main, pid, logfile, debug=True)
