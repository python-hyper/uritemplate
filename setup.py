from setuptools import setup

from uritemplate import __version__

packages = [
    'uritemplate'
]

with open("README.rst") as file:
    readme = file.read()

with open("HISTORY.rst") as file:
    history = file.read()

setup(
    name="uritemplate",
    version=__version__,
    description='URI templates',
    long_description="\n\n".join([readme, history]),
    license="BSD 3-Clause License or Apache License, Version 2.0",
    author="Ian Stapleton Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://uritemplate.readthedocs.org",
    packages=packages,
    package_data={'': ['LICENSE', 'LICENSE.APACHE', 'LICENSE.BSD',
                       'AUTHORS.rst']},
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
