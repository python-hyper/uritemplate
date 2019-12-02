"""Module containing all exceptions for the uritemplate module."""


class TemplateException(Exception):
    """Base Exception class for all uritemplate exceptions."""

    pass


class InvalidTemplate(TemplateException):
    """Base class for template validation."""

    message = "The URI template ({0}) is invalid."

    def __init__(self, uri, *args):
        """Initialize our exception."""
        super(InvalidTemplate, self).__init__(self.message.format(uri, *args))
        self.uri = uri


class UnbalancedBraces(InvalidTemplate):
    """The template has unbalanced braces."""

    message = "The URI template ({0}) has more {1} braces than {2} braces."

    def __init__(self, uri, left_braces_count, right_braces_count):
        """Initialize our exception."""
        more, less = 'left', 'right'
        if left_braces_count < right_braces_count:
            more, less = less, more
        super(UnbalancedBraces, self).__init__(uri, more, less)
