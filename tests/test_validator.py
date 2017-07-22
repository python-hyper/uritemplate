"""Tests for the uritemplate.Validator class."""
import uritemplate
from uritemplate import exceptions

import pytest


@pytest.mark.parametrize('template', [
    'https://github.com{/user}',
    'https://github.com/sigmavirus24{/repository}',
    '{foo}',
    '?{bar}',
    'https://example.com',
])
def test_valid_uris(template):
    """Verify we don't raise an exception."""
    urit = uritemplate.URITemplate(template)
    uritemplate.Validator().validate(urit)


@pytest.mark.parametrize('template', [
    'https://github.com{/user',
    'https://github.com/sigmavirus24/repository}',
    '{foo}}',
    '?{{bar}',
])
def test_invalid_uris(template):
    """Verify we catch invalid URITemplates."""
    urit = uritemplate.URITemplate(template)
    with pytest.raises(exceptions.InvalidTemplate):
        uritemplate.Validator().validate(urit)


@pytest.mark.parametrize('template', [
    'https://github.com{/user',
    'https://github.com/sigmavirus24/repository}',
    '{foo}}',
    '?{{bar}',
])
def test_allow_invalid_uris(template):
    """Verify we allow invalid URITemplates."""
    urit = uritemplate.URITemplate(template)
    uritemplate.Validator().allow_unbalanced_braces().validate(urit)
