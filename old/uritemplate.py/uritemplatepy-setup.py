from setuptools import setup

setup(
    name="uritemplate.py",
    version="3.0.2",
    description="URI templates",
    long_description="\n\n".join(
        [open("README.rst").read(), open("HISTORY.rst").read()]
    ),
    license="BSD 3-Clause License or Apache License, Version 2.0",
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://uritemplate.readthedocs.org",
    install_requires=["uritemplate>=2.0"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
