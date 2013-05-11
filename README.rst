uritemplate
===========

Simple python library to deal with `URI Templates`_. When complete the API 
should look something like::

    from uritemplate import URITemplate, expand

    gist_uri = 'https://api.github.com/users/sigmavirus24/gists{/gist_id}'
    t = URITemplate(gist_uri)
    print(t.expand(gist_id=123456))
    # => https://api.github.com/users/sigmavirus24/gists/123456

    # or
    print(expand(gist_uri, gist_id=123456))

    # also
    t.expand({'gist_id': 123456})
    expand(gist_uri, {'gist_id': 123456})

.. _URI Templates: http://tools.ietf.org/html/rfc6570
