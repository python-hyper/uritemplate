from unittest import TestCase, main
from uritemplate import URITemplate


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
        uris = ['https://api.github.com',
                'https://api.github.com/users{/user}',
                'https://api.github.com/repos{/user}{/repo}',
                'https://api.github.com/repos{/user}{/repo}/issues{/issue}']

        for i, uri in enumerate(uris):
            t = URITemplate(uri)
            self.assertEqual(len(t.variables), i)


if __name__ == '__main__':
    main()
