from unittest import TestCase, main
from uritemplate import URITemplate
from uritemplate.template import URIVariable


class TestURITemplate(TestCase):
    def test_no_variables_in_uri(self):
        """
        This test ensures that if there are no variables present, the
        template evaluates to itself.
        """
        uri = 'https://api.github.com/users'
        t = URITemplate(uri)
        self.assertEqual(t.expand(), uri)
        self.assertEqual(t.expand(users='foo'), uri)

    def test_all_variables_parsed(self):
        """
        This test ensures that all variables are parsed.
        """
        uris = [
            'https://api.github.com',
            'https://api.github.com/users{/user}',
            'https://api.github.com/repos{/user}{/repo}',
            'https://api.github.com/repos{/user}{/repo}/issues{/issue}'
        ]

        for i, uri in enumerate(uris):
            t = URITemplate(uri)
            self.assertEqual(len(t.variables), i)

    def test_expand(self):
        """
        This test ensures that expansion works as expected.
        """
        # Single
        t = URITemplate('https://api.github.com/users{/user}')
        expanded = 'https://api.github.com/users/sigmavirus24'
        self.assertEqual(t.expand(user='sigmavirus24'), expanded)

        # Multiple
        t = URITemplate('https://api.github.com/users{/user}{/repo}')
        expanded = 'https://api.github.com/users/sigmavirus24/github3.py'
        self.assertEqual(
            t.expand({'repo': 'github3.py'}, user='sigmavirus24'),
            expanded
        )

    def test_str(self):
        uri = 'https://api.github.com{/endpoint}'
        self.assertEqual(str(URITemplate(uri)), uri)

    def test_hash(self):
        uri = 'https://api.github.com{/endpoint}'
        self.assertEqual(hash(URITemplate(uri)), hash(uri))

    def test_level1_examples(self):
        """
        Level 1 examples from RFC 6570.
        """
        ex1 = '{var}'
        t1 = URITemplate(ex1)
        expected = value = 'value'
        self.assertEqual(str(t1.variables[0]), 'var')
        self.assertEqual(t1.expand(var=value), value)

        ex2 = '{hello}'
        t2 = URITemplate(ex2)
        value = 'Hello World!'
        expected = 'Hello%20World%21'
        self.assertEqual(str(t2.variables[0]), 'hello')
        self.assertEqual(t2.expand(hello=value), expected)


class TestURIVariable(TestCase):
    def test_level1_examples(self):
        """
        Level 1 examples from RFC 6570.
        """
        ex1 = 'var'
        value = 'value'
        expected = {ex1: value}
        v1 = URIVariable(ex1)
        self.assertEqual(v1.expand({ex1: value}), expected)

        ex2 = 'hello'
        value = 'Hello World!'
        expected = {ex2: 'Hello%20World%21'}
        v2 = URIVariable(ex2)
        self.assertEqual(v2.expand({ex2: value}), expected)


if __name__ == '__main__':
    main()
