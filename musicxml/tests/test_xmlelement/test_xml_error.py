from unittest import TestCase

from musicxml.xmlelement.xmlelement import *


class TestXMLElementError(TestCase):
    def test_simple_type_wrong_type(self):
        with self.assertRaises(TypeError) as err:
            XMLVoice()
        assert err.exception.args[0] == "XMLVoice's value 'None' can only be of types ['str'] not NoneType."

    def test_simple_type_wrong_type_with_enumeration(self):
        with self.assertRaises(TypeError) as err:
            XMLStep()
        assert err.exception.args[
                   0] == "XMLStep's value 'None' can only be of types ['str'] not NoneType. XMLStep.value must in ['A', 'B', 'C', 'D', 'E', 'F', 'G']"

    def test_simple_type_value_error_enumeration(self):
        with self.assertRaises(ValueError) as err:
            XMLFermata('something')
        assert err.exception.args[
                   0] == "XMLFermata: XSDSimpleTypeFermataShape.value 'something' must in ['normal', 'angled', 'square', 'double-angled', 'double-square', 'double-dot', 'half-curve', 'curlew', '']"

    def test_simple_type_value_error_restriction_min_exclusive(self):
        with self.assertRaises(ValueError) as err:
            XMLDivisions(-1)
        assert err.exception.args[0] == "XMLDivisions.value '-1' must be greater than '0'"

    def test_simple_type_value_error_restriction_min_inclusive(self):
        with self.assertRaises(ValueError) as err:
            XMLStaffSize(-1)
        assert err.exception.args[0] == "XMLStaffSize: XSDSimpleTypeNonNegativeDecimal.value '-1' must be greater than or equal to '0'"

    def test_simple_type_value_error_restriction_max_inclusive(self):
        with self.assertRaises(ValueError) as err:
            XMLPan(190)
        assert err.exception.args[0] == "XMLPan.value '190' must be less than or equal to '180'"

    def test_simple_type_attribute_value_err_pattern(self):
        w = XMLTie(type='start')
        with self.assertRaises(ValueError) as err:
            w.time_only = 'bla'
        assert err.exception.args[0] == "XSDSimpleTypeTimeOnly.value 'bla' must match the following pattern: [1-9][0-9]*(, ?[1-9][0-9]*)*"

    def test_simple_type_value_error_union(self):
        fs = XMLSymbol('bal')
        with self.assertRaises(TypeError) as err:
            fs.letter_spacing = 'not normal'
        assert err.exception.args[
                   0] == "XSDSimpleTypeNumberOrNormal's value 'not normal' can only be of types ['float', 'int'] not str. XSDSimpleTypeNumberOrNormal.value can also be ['normal']"
