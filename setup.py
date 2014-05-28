#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="daemonize",
    version="2.3.1",
    py_modules=["daemonize"],
    author="Ilya Otyutskiy",
    author_email="ilya.otyutskiy@icloud.com",
    maintainer="Ilya Otyutskiy",
    url="https://github.com/thesharp/daemonize",
    description="Library to enable your code run as a daemon process on Unix-like systems.",
    license="MIT",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: POSIX :: BSD :: FreeBSD",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.3",
                 "Topic :: Software Development"]
)
