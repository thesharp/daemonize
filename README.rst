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
    import time
    
    import daemonize
    
    pid = "/tmp/test.pid"
    
    def main():
        print "This is it!  I will die in five seconds."
        time.sleep(5)

    daemonize.start(main, pid, debug=True)
