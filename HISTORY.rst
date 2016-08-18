Changelog
=========

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
