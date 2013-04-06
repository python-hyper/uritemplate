uritemplate
===========

Simple python library to deal with `URI Templates`_. When complete the API 
should look something like::

    from uritemplate import Template, expand

    t = Template('https://api.github.com/users/sigmavirus24/gists{/gist_id}')
    print(t.expand(gist_id=123456))
    # => https://api.github.com/users/sigmavirus24/gists/123456

    # or
    print(expand(
        'https://api.github.com/users/sigmavirus24/gists{/gist_id}',
        gist_id=123456
    ))

    # And possibly
    t = Template('https://api.github.com/users/sigmavirus24/gists{/gist_id}')
    t.gist_id = 123456
    print(t.expand())

.. _URI Templates: http://tools.ietf.org/html/rfc6570
