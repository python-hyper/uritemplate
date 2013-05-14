#!/usr/bin/env python

import sys
import os

packages = [
    'uritemplate'
]

from distutils.core import setup

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py sdist upload")
    sys.exit()

from uritemplate import __version__

setup(
    name="uritemplate.py",
    version=__version__,
    description='URI templates',
    long_description="\n\n".join([open("README.rst").read(),
                                  open("HISTORY.rst").read()]),
    license=open('LICENSE').read(),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://uritemplate.readthedocs.org",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
