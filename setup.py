#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = "daemonize",
    version = "1.1",
    packages = ['daemonize'],
    author = "Ilya A. Otyutskiy",
    author_email = "sharp@thesharp.ru",
    maintainer = "Ilya A. Otyutskiy",
    url = "https://github.com/thesharp/daemonize",
    description = "Library to enable your code run as a daemon process "
                  "on Unix-like systems.",
    license = "PSF"
)
