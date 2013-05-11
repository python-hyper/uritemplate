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

    Please note::

        str(t)
        # 'https://api.github.com/users/sigmavirus24/gists{/gistid}'
        repr(t)  # is equivalent to
        # URITemplate(str(t))
        # Where str(t) is interpreted as the URI string.

    Also, ``URITemplates`` are hashable so they can be used as keys in
    dictionaries.

    """
    def __init__(self, uri):
        self.uri = uri
        self.variables = [
            URIVariable(m.groups()[0]) for m in template_re.finditer(self.uri)
        ]

    def __repr__(self):
        return 'URITemplate({0})'.format(self)

    def __str__(self):
        return self.uri

    def __hash__(self):
        return hash(self.uri)

    def expand(self, var_dict=None, **kwargs):
        """Expand the template with the given parameters.

        :param dict var_dict: Optional dictionary with variables and values
        :param kwargs: Alternative way to pass arguments
        :returns: str

        Example::

            t = URITemplate('https://api.github.com{/end}')
            t.expand({'end': 'users'})
            t.expand(end='gists')

        .. note:: Passing values by both parts, will override values in
                  ``var_dict``.
        """
        if not self.variables:
            return self.uri

        expansion = var_dict or {}
        expansion.update(kwargs)
        return ''


class URIVariable(object):
    """The :class:`URIVariable <URIVariable>` object validates everything
    underneath the Template object. It validates template expansions and will
    truncate length as decided by the template.

    Please note that just like the :class:`URITemplate <URITemplate>`, this
    object's ``__str__`` and ``__repr__`` methods do not return the same
    information. Calling ``str(var)`` will return the original variable.
    """

    operators = ('+', '#', '.', '/', ';', '?', '&', '|', '!', '@')
    reserved = ":/?#[]@!$&'()*+,;="

    def __init__(self, var):
        self.original = var
        self.operator = None
        self.safe = '/'
        self.vars = []
        self.defaults = {}
        self.parse()

    def __repr__(self):
        return 'URIVariable({0})'.format(self)

    def __str__(self):
        return self.original

    def parse(self):
        """Parse the variable: find the operator, the set of safe characters,
        all the variables and the defaults.
        """
        if self.original[0] in URIVariable.operators:
            self.operator = self.original[0]
            var_list = self.original[1:]

        if self.operator in URIVariable.operators[:2]:
            self.safe = URIVariable.reserved

        var_list = var_list.split(',')

        for var in var_list:
            default_val = None
            name = var
            if '=' in var:
                name, default_val = tuple(var.split('=', 1))

            explode = True if name.endswith('*') else False

            prefix = None
            if ':' in name:
                name, prefix = tuple(name.split(':', 1))
                prefix = int(prefix)

            if default_val:
                self.defaults[name] = default_val

            self.vars.append((name, {'explode': explode, 'prefix': prefix}))

    def expand(self, var_dict=None):
        """Expand the variable in question using ``var_dict`` and the
        parsed defaults.
        """
        var_dict = dict((k, quote(v)) for k, v in var_dict.items())
