"""Module containing all the validation logic for uritemplate."""
from uritemplate import exceptions as exc


class Validator(object):
    """Provide configurable validation of URITemplate objects.

    .. versionadded:: 3.1.0

    .. code-block::

        from uritemplate import URITemplate, Validator


    """

    def __init__(self):
        """Initialize our validator."""
        self.enforcing_unbalanced_braces = True

    def allow_unbalanced_braces(self):
        """Allow a template to have unbalanced braces.

        .. versionadded:: 3.1.0

        Returns the validator instance.
        """
        self.enforcing_unbalanced_braces = False
        return self

    def force_balanced_braces(self):
        """Force a template to have balanced braces.

        .. versionadded:: 3.1.0

        Returns the validator instance.
        """
        self.enforcing_unbalanced_braces = True
        return self

    def validate(self, template):
        """Validate that a template meets the parameters.

        .. versionadded:: 3.1.0

        :raises: uritemplate.exceptions.InvalidTemplate
        :raises: uritemplate.exceptions.UnbalancedBraces
        """
        if self.enforcing_unbalanced_braces:
            _enforce_balanced_braces(template)


def _enforce_balanced_braces(template):
    uri = template.uri
    left_braces = uri.count('{')
    right_braces = uri.count('}')
    if left_braces != right_braces:
        raise exc.UnbalancedBraces(uri, left_braces, right_braces)
