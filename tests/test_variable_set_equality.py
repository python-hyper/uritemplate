import typing as t
import unittest

from uritemplate import URITemplate
from uritemplate import variables
from uritemplate.orderedset import OrderedSet


class TestVariableSetEquality(unittest.TestCase):
    def test_builtin_set_equality(self) -> None:
        cases = [
            ("", set(), True),
            ("{a}", {"a"}, True),
            ("{a,b}", {"a", "b"}, True),
            ("{a}", {"a", "b"}, False),
            ("{a,b}", {"a"}, False),
            ("{a,b}", {"a", "c"}, False),
            ("{a}", {"b"}, False),
            ("", {"a"}, False),
            ("{a}", set(), False),
        ]
        for uri, names, expected in cases:
            for operand in (names, frozenset(names)):
                with self.subTest(uri=uri, names=operand):
                    result = variables(uri)
                    self.assertEqual(result == operand, expected)
                    self.assertEqual(operand == result, expected)
                    self.assertEqual(result != operand, not expected)
                    self.assertEqual(
                        URITemplate(uri).variable_names == operand, expected
                    )

    def test_ordered_comparison_keeps_order(self) -> None:
        self.assertEqual(variables("{a,b}"), OrderedSet(["a", "b"]))
        self.assertNotEqual(variables("{a,b}"), OrderedSet(["b", "a"]))
        self.assertEqual(variables(""), OrderedSet())

    def test_iterable_comparison(self) -> None:
        for names, expected in [
            (["a", "a"], True),
            (["a", "b"], False),
            ([], False),
        ]:
            operands: t.List[t.Iterable[str]] = [
                names,
                tuple(names),
                iter(names),
            ]
            for operand in operands:
                with self.subTest(names=names, operand=type(operand)):
                    self.assertEqual(variables("{a}") == operand, expected)
