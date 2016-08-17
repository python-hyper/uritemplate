"""

uritemplate
===========

The URI templating library for humans.

See http://uritemplate.rtfd.org/ for documentation

:copyright: (c) 2013-2015 Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'uritemplate'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2013 Ian Cordasco'
__version__ = '1.0.0'
__version_info__ = tuple(int(i) for i in __version__.split('.'))

from uritemplate.api import URITemplate, expand, partial  # noqa: E402

__all__ = ('URITemplate', 'expand', 'partial')
