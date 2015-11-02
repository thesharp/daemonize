#!/usr/bin/python

import re
import ast

from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('daemonize.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name="daemonize",
    version=version,
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
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Software Development"]
)
