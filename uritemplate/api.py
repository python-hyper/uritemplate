"""

uritemplate.api
===============

This module contains the very simple API provided by uritemplate.

"""
from uritemplate.template import Template


def expand(uri, *args, **kwargs):
    t = Template(uri)
    return t.expand(*args, **kwargs)
