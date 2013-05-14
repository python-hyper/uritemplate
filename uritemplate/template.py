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
import collections

template_re = re.compile('{([^\}]+)}')


class URITemplate(object):

    """This parses the template and will be used to expand it.

    This is the most important object as the center of the API.

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
        return 'URITemplate(%s)' % self

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

        .. note:: Passing values by both parts, may override values in
                  ``var_dict``. For example::

                      expand('https://{var}', {'var': 'val1'}, var='val2')

                  ``val2`` will be used instead of ``val1``.

        """
        if not self.variables:
            return self.uri

        expansion = var_dict or {}
        expansion.update(kwargs)
        expanded = {}
        for v in self.variables:
            expanded.update(v.expand(expansion))

        def replace(match):
            return expanded.get(match.groups()[0], '')

        return template_re.sub(replace, self.uri)


class URIVariable(object):

    """This object validates everything inside the URITemplate object.

    It validates template expansions and will truncate length as decided by
    the template.

    Please note that just like the :class:`URITemplate <URITemplate>`, this
    object's ``__str__`` and ``__repr__`` methods do not return the same
    information. Calling ``str(var)`` will return the original variable.

    """

    operators = ('+', '#', '.', '/', ';', '?', '&', '|', '!', '@')
    reserved = ":/?#[]@!$&'()*+,;="

    def __init__(self, var):
        self.original = var
        self.operator = ''
        self.safe = ''
        self.vars = []
        self.defaults = {}
        self.parse()

        self.start = self.join_str = self.operator
        if self.operator == '+':
            self.start = ''
        if self.operator in ('+', '#', ''):
            self.join_str = ','
        if self.operator == '#':
            self.start = '#'
        if self.operator == '?':
            self.start = '?'
            self.join_str = '&'
        if self.operator == '&':
            self.start = self.join_str = '&'

        if self.operator in ('+', '#'):
            self.safe = URIVariable.reserved

    def __repr__(self):
        return 'URIVariable(%s)' % self

    def __str__(self):
        return self.original

    def parse(self):
        """Parse the variable.

        This finds the:
            - operator,
            - set of safe characters,
            - variables, and
            - defaults.

        """
        var_list = self.original
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

            explode = False
            if name.endswith('*'):
                explode = True
                name = name[:-1]

            prefix = None
            if ':' in name:
                name, prefix = tuple(name.split(':', 1))
                prefix = int(prefix)

            if default_val:
                self.defaults[name] = default_val

            self.vars.append((name, {'explode': explode, 'prefix': prefix}))

    def _query_expansion(self, name, value, explode, prefix):
        """Expansion method for the '?' and '&' operators."""
        if value is None or (len(value) == 0 and value != ""):
            return None

        tuples = is_list_of_tuples(value)

        safe = self.safe
        if isinstance(value, (list, tuple)) and not tuples:
            if explode:
                return self.join_str.join(
                    '%s=%s' % (name, quote(v, safe)) for v in value
                )
            else:
                value = ','.join(quote(v, safe) for v in value)
                return '%s=%s' % (name, value)

        if isinstance(value, (dict, collections.MutableMapping)) or tuples:
            items = value if tuples else sorted(value.items())
            if explode:
                return self.join_str.join(
                    '%s=%s' % (
                        quote(k, safe), quote(v, safe)
                    ) for k, v in items
                )
            else:
                value = ','.join(
                    '%s,%s' % (
                        quote(k, safe), quote(v, safe)
                    ) for k, v in items
                )
                return '%s=%s' % (name, value)

        if value:
            value = value[:prefix] if prefix else value
            return '%s=%s' % (name, quote(value, safe))
        return name + '='

    def _label_path_expansion(self, name, value, explode, prefix):
        """Label and path expansion method.

        Expands for operators: '/', '.'

        """
        join_str = self.join_str
        safe = self.safe

        if value is None or (len(value) == 0 and value != ''):
            return None

        tuples = is_list_of_tuples(value)

        if isinstance(value, (list, tuple)) and not tuples:
            if not explode:
                join_str = ','

            expanded = join_str.join(
                quote(v, safe) for v in value if value is not None
            )
            return expanded if expanded else None

        if isinstance(value, (dict, collections.MutableMapping)) or tuples:
            items = value if tuples else sorted(value.items())
            format_str = '%s=%s'
            if not explode:
                format_str = '%s,%s'
                join_str = ','

            expanded = join_str.join(
                format_str % (
                    quote(k, safe), quote(v, safe)
                ) for k, v in items if v is not None
            )
            return expanded if expanded else None

        value = value[:prefix] if prefix else value
        return quote(value, safe)

    def _semi_path_expansion(self, name, value, explode, prefix):
        """Expansion method for ';' operator."""
        join_str = self.join_str
        safe = self.safe

        if value is None:
            return None

        if self.operator == '?':
            join_str = '&'

        tuples = is_list_of_tuples(value)

        if isinstance(value, (list, tuple)) and not tuples:
            if explode:
                expanded = join_str.join(
                    '%s=%s' % (
                        name, quote(v, safe)
                    ) for v in value if v is not None
                )
                return expanded if expanded else None
            else:
                value = ','.join(quote(v, safe) for v in value)
                return '%s=%s' % (name, value)

        if isinstance(value, (dict, collections.MutableMapping)) or tuples:
            items = value if tuples else sorted(value.items())

            if explode:
                return join_str.join(
                    '%s=%s' % (
                        quote(k, safe), quote(v, safe)
                    ) for k, v in items if v is not None
                )
            else:
                expanded = ','.join(
                    '%s,%s' % (
                        quote(k, safe), quote(v, safe)
                    ) for k, v in items if v is not None
                )
                return '%s=%s' % (name, expanded)

        value = value[:prefix] if prefix else value
        if value:
            return '%s=%s' % (name, quote(value, safe))

        return name

    def _string_expansion(self, name, value, explode, prefix):
        if value is None:
            return None

        tuples = is_list_of_tuples(value)

        if isinstance(value, (list, tuple)) and not tuples:
            return ','.join(quote(v, self.safe) for v in value)

        if isinstance(value, (dict, collections.MutableMapping)) or tuples:
            items = value if tuples else sorted(value.items())
            if explode:
                format_str = '%s=%s'
            else:
                format_str = '%s,%s'

            return ','.join(
                format_str % (
                    quote(k, self.safe), quote(v, self.safe)
                ) for k, v in items
            )

        value = value[:prefix] if prefix else value
        return quote(value, self.safe)

    def expand(self, var_dict=None):
        """Expand the variable in question.

        Using ``var_dict`` and the previously parsed defaults, expand this
        variable and subvariables.

        """
        return_values = []

        for name, opts in self.vars:
            value = var_dict.get(name, None)
            if not value and value != '' and name in self.defaults:
                value = self.defaults[name]

            if value is None:
                continue

            expanded = None
            if self.operator in ('/', '.'):
                expansion = self._label_path_expansion
            elif self.operator in ('?', '&'):
                expansion = self._query_expansion
            elif self.operator == ';':
                expansion = self._semi_path_expansion
            else:
                expansion = self._string_expansion

            expanded = expansion(name, value, opts['explode'], opts['prefix'])

            if expanded is not None:
                return_values.append(expanded)

        if return_values:
            return {
                self.original: self.start + self.join_str.join(return_values)
            }

        return {}


def is_list_of_tuples(value):
    if not isinstance(value, (list, tuple)):
        return False

    try:
        dict(value)
    except:
        return False
    else:
        return True
