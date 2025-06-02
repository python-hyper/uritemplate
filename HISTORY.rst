Changelog - uritemplate
=======================

4.2.0 - 2025-06-01
------------------

- Drop support for Python 3.8
- Fix bug where already url-encoded values were further escaped and
  encoded (See https://github.com/python-hyper/uritemplate/issues/99)
- Refactor ``uritemplate/variable.py`` to enable fixing the
  aforementioned bug.

4.1.1 - 2021-10-13
------------------

- Fix setup.cfg metadata to reflect lack of support for Python 2 as desired in
  4.0

4.1.0 - 2021-10-12
------------------

- Add type annotations to uritemplate and distribute them for others to use
- Update to a modern documentation theme as well

4.0.0 - 2021-10-10
------------------

- Drop support for Python 2.7, 3.4, and 3.5
- Better support number-like types as values for variables in a template

3.0.1 - 2019-12-19
------------------

- Update to Python 3.6, 3.7, and 3.8
- Drop support for Python 2.6, 3.2, and 3.3
- Ignore ``None`` in list argument expansion
- Handle a list with an empty string appropriately

3.0.0 - 2016-08-29
------------------

- Match major version number of uritemplate.py

2.0.0 - 2016-08-29
------------------

- Merge uritemplate.py into uritemplate


Changelog - uritemplate.py
==========================

3.0.2 - 2015-08-30
------------------

- Fix meta-package requirements.

3.0.1 - 2015-08-29
------------------

- Deprecate in favor of uritemplate. This package is now a metapackage that
  depends on uritemplate.

2.0.0 - 2016-08-20
------------------

- Relicense uritemplate.py as Apache 2 and BSD (See
  https://github.com/sigmavirus24/uritemplate/pull/23)

1.0.1 - 2016-08-18
------------------

- Fix some minor packaging problems.

1.0.0 - 2016-08-17
------------------

- Fix handling of Unicode values on Python 2.6 and 2.7 for urllib.quote.

- Confirm public stable API via version number.

0.3.0 - 2013-10-22
------------------

- Add ``#partial`` to partially expand templates and return new instances of
  ``URITemplate``.

0.2.0 - 2013-07-26
------------------

- Refactor the library a bit and add more tests.

- Backwards incompatible with 0.1.x if using ``URIVariable`` directly from
  ``uritemplate.template``

0.1.1 - 2013-05-19
------------------

- Add ability to get set of variable names in the current URI

- If there is no value or default given, simply return an empty string

- Fix sdist

0.1.0 - 2013-05-14
------------------

- Initial Release
