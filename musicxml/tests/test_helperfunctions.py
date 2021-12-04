from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.util.helperfunctions import get_simple_format_all_base_classes


class TestHelperFunctions(MusicXmlTestCase):
    def test_get_simple_format_base_classes(self):
        assert get_simple_format_all_base_classes(self.yes_no_number_simple_type_element) == ['XMLSimpleTypeYesNo',
                                                                                          'XsDecimal']
        assert get_simple_format_all_base_classes(self.above_below_simple_type_element) == ['XMLSimpleType', 'XsToken']
