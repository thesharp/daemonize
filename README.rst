daemonize
========================


.. image:: https://readthedocs.org/projects/daemonize/badge/?version=latest
    :target: http://daemonize.readthedocs.org/en/latest/?badge=latest
    :alt: Latest version

.. image:: https://img.shields.io/travis/thesharp/daemonize.svg
    :target: http://travis-ci.org/thesharp/daemonize
    :alt: Travis CI

.. image:: https://img.shields.io/pypi/dm/daemonize.svg
    :target: https://pypi.python.org/pypi/daemonize
    :alt: PyPI montly downloads

.. image:: https://img.shields.io/pypi/v/daemonize.svg
    :target: https://pypi.python.org/pypi/daemonize
    :alt: PyPI last version available

.. image:: https://img.shields.io/pypi/l/daemonize.svg
    :target: https://pypi.python.org/pypi/daemonize
    :alt: PyPI license


**daemonize** is a library for writing system daemons in Python. It is
distributed under MIT license. Latest version can be downloaded from
`PyPI <https://pypi.python.org/pypi/daemonize>`__. Full documentation can
be found at
`ReadTheDocs <http://daemonize.readthedocs.org/en/latest/?badge=latest>`__.

Dependencies
------------

It is tested under following Python versions:

-  2.6
-  2.7
-  3.3
-  3.4
-  3.5

Installation
------------

You can install it from Python Package Index (PyPI):

::

    $ pip install daemonize

Usage
-----

.. code-block:: python

    from time import sleep
    from daemonize import Daemonize

    pid = "/tmp/test.pid"


    def main():
        while True:
            sleep(5)

    daemon = Daemonize(app="test_app", pid=pid, action=main)
    daemon.start()

File descriptors
----------------

Daemonize object's constructor understands the optional argument
**keep\_fds** which contains a list of FDs which should not be closed.
For example:

.. code-block:: python

    import logging
    from daemonize import Daemonize

    pid = "/tmp/test.pid"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("/tmp/test.log", "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]


    def main():
        logger.debug("Test")

    daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=keep_fds)
    daemon.start()
