# -*- coding: utf-8 -*-

r"""

The documentation for :py:mod:`uritemplate.matchers`.

This module contains the logic used to take a list of ``URITemplate``\ s and
an expanded URI, and determine which template is the best match. For example,
let's say you have three templates:

- ``/resource{/id}``
- ``/resource{/id}{?attrs*}``
- ``/resource{/id}{#subsection}{?attrs*}``

And the expanded URI is: ``/resource/1?attrs=a&attrs=b&attrs=c``. You would
expect the URI to match 2 and 3. In this case it may be ambiguous which the
best match would be. A greedy match would be the third template. A non-greedy
match would be the second template.

"""


class URIMatcher(object):

    """

    The URIMatcher class contains the logic that will determine a match.

    ::

        from uri_template import URITemplate, URIMatcher

        list_of_templates = [
            URITemplate('/resource{/id}'),
            URITemplate('/resource{/id}{?attrs*}'),
            URITemplate('/resource{/id}{?attrs*}{#subsection}')
        ]

        matcher = URIMatcher(list_of_templates)

        matched = matcher.find('/resource/1?attrs=a&attrs=b&attrs=c')

    """

    def __init__(self, templates):
        """``URIMatcher(list_of_templates)``."""
        self.templates = templates

    def find(self, uri, greedy=False):
        """Find a matching template for ``uri``.

        :param str uri: The expanded URI for which we must find a match.
        :param bool greedy: Whether the match should be greedy or not.
        :returns: ``None`` if no match or ``URITemplate`` that matches the
            URI.
        :rtype: NoneType or URITemplate

        """
        pass
