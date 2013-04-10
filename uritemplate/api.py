"""

uritemplate.api
===============

This module contains the very simple API provided by uritemplate.

"""
from uritemplate.template import URITemplate


def expand(uri, *args, **kwargs):
    t = URITemplate(uri)
    return t.expand(*args, **kwargs)
