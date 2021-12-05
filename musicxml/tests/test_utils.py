import re
from unittest import TestCase

from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.util.helperfunctions import get_simple_format_all_base_classes, check_value_type, get_cleaned_token
from musicxml.util.helprervariables import name_character


class TestHelperFunctions(MusicXmlTestCase):
    def test_get_simple_format_base_classes(self):
        assert get_simple_format_all_base_classes(self.yes_no_number_simple_type_element) == ['XMLSimpleTypeYesNo',
                                                                                              'XMLSimpleTypeDecimal']
        assert get_simple_format_all_base_classes(self.above_below_simple_type_element) == ['XMLSimpleTypeToken']

    def test_check_types(self):
        with self.assertRaises(TypeError):
            try:
                check_value_type(1, [str, float])
            except TypeError as err:
                assert str(err) == "value 1 can only be of types ['str', 'float'] not int."
                raise err

        with self.assertRaises(TypeError):
            try:
                check_value_type(1, [str])
            except TypeError as err:
                assert str(err) == "value 1 can only be of types ['str'] not int."
                raise err

            # assert err == "value 1 can only be of types ['str'] not int."

        check_value_type(1, [int, float])
        check_value_type(1, [int])
        check_value_type(1.3, [int, float])
        check_value_type("hello", [str])

    def test_get_cleaned_token(self):
        expected = 'Hello Alfons'
        assert get_cleaned_token('Hello\nAlfons') == expected
        assert get_cleaned_token('Hello\tAlfons') == expected
        assert get_cleaned_token('Hello\rAlfons') == expected
        assert get_cleaned_token('Hello\t  Alfons') == expected
        assert get_cleaned_token('Hello    Alfons') == expected


class TestHelperVariables(TestCase):
    def test_name_character(self):
        pattern = rf"({name_character})+"
        p = re.compile(pattern)
        assert p.fullmatch('HeL1lo') is not None
        assert p.fullmatch('HeL1lo@') is None
        assert p.fullmatch('HeL1 lo') is None
        assert p.fullmatch('HeL1.o') is not None
        assert p.fullmatch('HeL1:._-o') is not None
        assert p.fullmatch('ÖÜöüäÄ:._-o') is not None
        assert p.fullmatch('&:._-o') is None
