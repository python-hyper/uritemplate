uritemplate
===========

Release v\ |version|.

Examples
--------

This first example shows how simple the API can be when using for a one-off 
item in a script or elsewhere.

.. code-block:: python

    from requests import get
    from uritemplate import expand

    uri = 'https://api.github.com{/user}'

    user = get(expand(uri, user='sigmavirus24')).json()

This second example shows how using the class will save you time for template 
parsing and object creation. Making the template once means the URI is parsed 
once which decreases the number of :class:`URITemplate 
<uritemplate.URITemplate>` objects created and usage of the ``re`` module.  
This means that as soon as the file is parsed, the ``User.github_url`` and 
``Repository.github_url`` variables are made once and only once. They're then 
usable in every instance of those classes.

.. code-block:: python

    from uritemplate import URITemplate

    class User(object):
        github_url = URITemplate('https://api.github.com{/user}')
        def __init__(self, name):
            self.uri = self.github_url.expand({'user': name})
            self.name = name

    class Repository(object):
        github_url = URITemplate('https://api.github.com{/user}{/repo}')
        def __init__(self, name):
            self.uri = self.github_url.expand(
                dict(zip(['user', 'repo'], name.split('/')))
            )
            self.name = name

API
---

.. module:: uritemplate

.. autofunction:: uritemplate.expand

.. autofunction:: uritemplate.partial

.. autoclass:: uritemplate.URITemplate
    :members:

Implementation Details
----------------------

Classes, their methods, and functions in this section are not part of the API 
and as such are not meant to be used by users of ``uritemplate.py``. These are 
documented here purely for reference as they are inadvertently exposed via the 
public API.

For example::

    t = URITemplate('https://api.github.com/users{/user}')
    t.variables
    # => [URIVariable(/user)]

Users can interact with :class:`URIVariable` objects as they see fit, but 
their API may change and are not guaranteed to be consistent across versions.  
Code relying on methods defined on :class:`URIVariable` and other classes, 
methods, and functions in this section may break in future releases.

.. autoclass:: uritemplate.template.URIVariable
    :members: expand
