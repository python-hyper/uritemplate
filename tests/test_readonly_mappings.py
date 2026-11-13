"""Associative values may implement Mapping without supporting mutation."""

import collections.abc
import types
import typing as t

import pytest

from uritemplate import expand
from uritemplate import variable


class ReadOnlyMapping(t.Mapping[str, variable.ScalarVariableValue]):
    def __init__(self, values: t.Mapping[str, variable.ScalarVariableValue]):
        self._values = dict(values)

    def __getitem__(self, key: str) -> variable.ScalarVariableValue:
        return self._values[key]

    def __iter__(self) -> t.Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)


@pytest.mark.parametrize("factory", [types.MappingProxyType, ReadOnlyMapping])
@pytest.mark.parametrize(
    "operator,plain,exploded",
    [
        ("", "a,one,b,two", "a=one,b=two"),
        ("+", "a,one,b,two", "a=one,b=two"),
        ("#", "#a,one,b,two", "#a=one,b=two"),
        (".", ".a,one,b,two", ".a=one.b=two"),
        ("/", "/a,one,b,two", "/a=one/b=two"),
        (";", ";v=a,one,b,two", ";a=one;b=two"),
        ("?", "?v=a,one,b,two", "?a=one&b=two"),
        ("&", "&v=a,one,b,two", "&a=one&b=two"),
    ],
)
@pytest.mark.parametrize("explode", [False, True])
def test_readonly_mapping_expands_as_associative_value(
    factory: t.Callable[
        [t.Dict[str, variable.ScalarVariableValue]],
        t.Mapping[str, variable.ScalarVariableValue],
    ],
    operator: str,
    plain: str,
    exploded: str,
    explode: bool,
) -> None:
    # Reverse insertion order also pins existing sorted-mapping behavior.
    values: t.Dict[str, variable.ScalarVariableValue] = {
        "b": "two",
        "a": "one",
    }
    mapping = factory(values)
    template = "{" + operator + "v" + ("*" if explode else "") + "}"
    assert expand(template, v=mapping) == (exploded if explode else plain)
    assert dict(mapping) == values
    assert not isinstance(mapping, collections.abc.MutableMapping)


@pytest.mark.parametrize("operator", ["", "+", "#", ".", "/", ";", "?", "&"])
@pytest.mark.parametrize("explode", [False, True])
def test_mapping_input_types_keep_identical_quoting(
    operator: str, explode: bool
) -> None:
    values: t.Dict[str, variable.ScalarVariableValue] = {
        "a b": "x/y",
        "z": "0",
    }
    template = "{" + operator + "v" + ("*" if explode else "") + "}"
    expected = expand(template, v=values)
    assert expand(template, v=types.MappingProxyType(values)) == expected
    assert expand(template, v=ReadOnlyMapping(values)) == expected


@pytest.mark.parametrize("value", ["text", ["a", "b"], [("a", "b")], 0, None])
def test_mapping_detection_does_not_reclassify_other_values(
    value: t.Any,
) -> None:
    assert not variable.dict_test(value)
