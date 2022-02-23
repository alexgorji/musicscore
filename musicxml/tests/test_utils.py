import re
from unittest import TestCase

from musicxml.tests.util import MusicXmlTestCase
from musicxml.util.core import get_cleaned_token, convert_to_xml_class_name, \
    replace_key_underline_with_hyphen
from musicxml.generate_classes.utils import get_simple_type_all_base_classes
from musicxml.util.helprervariables import name_character


class TestHelperFunctions(MusicXmlTestCase):

    def test_get_cleaned_token(self):
        expected = 'Hello Alfons'
        assert get_cleaned_token('Hello\nAlfons') == expected
        assert get_cleaned_token('Hello\tAlfons') == expected
        assert get_cleaned_token('Hello\rAlfons') == expected
        assert get_cleaned_token('Hello\t  Alfons') == expected
        assert get_cleaned_token('Hello    Alfons') == expected

    def test_replace_key_underline_with_hyphen(self):
        dict_ = {'a': 1, 'b-c': 2, 'e_f': 3}
        assert replace_key_underline_with_hyphen(dict_) == {'a': 1, 'b-c': 2, 'e-f': 3}
        dict_ = {'a': 1, 'b-c': 2, 'b_c': 3}
        with self.assertRaises(KeyError):
            replace_key_underline_with_hyphen(dict_)


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


class TestConvertToXMLClassName(TestCase):
    def test_conversion(self):
        assert convert_to_xml_class_name('something') == 'XMLSomething'
        assert convert_to_xml_class_name('something-some-thing') == 'XMLSomethingSomeThing'
