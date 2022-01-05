import re
from unittest import TestCase

from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.util.core import get_simple_type_all_base_classes, get_cleaned_token, convert_to_xml_class_name
from musicxml.util.helprervariables import name_character


class TestHelperFunctions(MusicXmlTestCase):
    def test_get_simple_type_base_classes(self):
        assert get_simple_type_all_base_classes(self.yes_no_number_simple_type_xsd_element) == ['XSDSimpleTypeYesNo',
                                                                                                'XSDSimpleTypeDecimal']
        assert get_simple_type_all_base_classes(self.above_below_simple_type_xsd_element) == ['XSDSimpleTypeToken']

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


class TestConvertToXMLClassName(TestCase):
    def test_conversion(self):
        assert convert_to_xml_class_name('something') == 'XMLSomething'
        assert convert_to_xml_class_name('something-some-thing') == 'XMLSomethingSomeThing'
