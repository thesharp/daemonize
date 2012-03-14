#!/usr/bin/env python

# Ensure that the local library is loaded first.  Normally you don't
# want to do this.
import sys, time
sys.path.insert(0, '..')

import daemonize

def main():
    for i in range(0, 5):
        print "iteration", i
        print " (sleeping 5 seconds)"
        time.sleep(5)
    print "Goodbye!"

daemonize.start(main, debug=True)