"""

uritemplate.template
====================

This module contains the essential inner workings of uritemplate.

What treasures await you:

- URITemplate class
- URIVariable class

"""
try:
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

import re

template_re = re.compile('{([^\}]+)}')


class URITemplate(object):
    """The :class:`URITemplate <URITemplate>` object is the central object to
    uritemplate. This parses the template and will be used to expand it.

    Example::

        from uritemplate import URITemplate
        import requests


        t = URITemplate(
            'https://api.github.com/users/sigmavirus24/gists{/gist_id}'
        )
        uri = t.expand(gist_id=123456)
        resp = requests.get(uri)
        for gist in resp.json():
            print(gist['html_url'])

    """
    def __init__(self, uri):
        self.uri = uri
        self.var_list = [
            URIVariable(m.groups()[0]) for m in template_re.finditer(self.uri)
        ]

    def __repr__(self):
        return 'URITemplate({0})'.format(self.uri)

    def expand(self, *args, **kwargs):
        pass


class URIVariable(object):
    """The :class:`URIVariable <URIVariable>` object validates everything
    underneath the Template object. It validates template expansions and will
    truncate length as decided by the template.
    """

    operators = ('+', '#', '.', '/', ';', '?', '&', '|', '!', '@')
    reserved = ":/?#[]@!$&'()*+,;="

    def __init__(self, var):
        self.original = var
        self.operator = None
        self.safe = '/'
        #self.parse()

    def __repr__(self):
        return 'URIVariable({0})'.format(self.original)

    def parse(self):
        if self.original[0] in URIVariable.operators:
            self.operator = self.orig[0]

        if self.operator in URIVariable.operators[:2]:
            self.safe = URIVariable.reserved
            var_list = self.original[1:].split(',')
        else:
            var_list = self.original.split(',')

        for var in var_list:
            pass

    def substitute(self, *args, **kwargs):
        args = [quote(a, self.safe) for a in args]
        kwargs = dict((k, quote(v)) for k, v in kwargs.items())
