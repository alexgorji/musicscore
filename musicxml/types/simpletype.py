import re

from musicxml.util.helperfunctions import get_simple_format_all_base_classes, find_all_xsd_children, check_value_type, \
    get_cleaned_token
from musicxml.util.helprervariables import name_character
from musicxml.xmlelement import MusicXMLElement, XMLElementTreeElement
import xml.etree.ElementTree as ET


class XMLSimpleType(MusicXMLElement):
    """
    Parent Class for all SimpleType classes
    """
    _PERMITTED = None
    _PATTERN = None

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._PERMITTED and self._PATTERN:
            raise ValueError('Both _PERMITTED and _PATTERN are set.')
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if self._PERMITTED:
            if v not in self._PERMITTED:
                raise ValueError(f'{self.__class__.__name__}.value {v} must in {self._PERMITTED}')
        if self._PATTERN:
            if re.compile(self._PATTERN).fullmatch(v) is None:
                raise ValueError(
                    f'{self.__class__.__name__}.value {v} must match the following pattern: {self._PATTERN}')
        self._value = v

    def __repr__(self):
        return str(self.value)


class XMLSimpleTypeInteger(XMLSimpleType):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="integer" id="integer">
            <xs:restriction base="xs:decimal">
                <xs:fractionDigits value="0" fixed="true"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        check_value_type(v, [int])
        super(XMLSimpleTypeInteger, type(self)).value.fset(self, v)


class XMLSimpleTypeNonNegativeInteger(XMLSimpleTypeInteger):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="nonNegativeInteger" id="nonNegativeInteger">
            <xs:restriction base="xs:integer">
                <xs:minInclusive value="0"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        super(XMLSimpleTypeNonNegativeInteger, type(self)).value.fset(self, v)
        if v < 0:
            raise ValueError(f'value {v} must be non negative.')


class XMLSimpleTypePositiveInteger(XMLSimpleTypeInteger):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="positiveInteger" id="positiveInteger">
            <xs:restriction base="xs:nonNegativeInteger">
                <xs:minInclusive value="1"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        super(XMLSimpleTypePositiveInteger, type(self)).value.fset(self, v)
        if v <= 0:
            raise ValueError(f'value {v} must be greater than 0.')


class XMLSimpleTypeDecimal(XMLSimpleType):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="decimal" id="decimal">
            <xs:restriction base="xs:anySimpleType">
                <xs:whiteSpace value="collapse" fixed="true"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        check_value_type(v, [int, float])
        super(XMLSimpleTypeDecimal, type(self)).value.fset(self, v)


class XMLSimpleTypeString(XMLSimpleType):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="string" id="string">
            <xs:restriction base="xs:anySimpleType">
                <xs:whiteSpace value="preserve"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        check_value_type(v, [str])
        super(XMLSimpleTypeString, type(self)).value.fset(self, v)


class XMLSimpleTypeToken(XMLSimpleTypeString):
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="token" id="token">
            <xs:restriction base="xs:normalizedString">
                <xs:whiteSpace value="collapse"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, v):
        super(XMLSimpleTypeToken, type(self)).value.fset(self, v)
        v = get_cleaned_token(v)
        self._value = v


class XMLSimpleTypeNMTOKEN(XMLSimpleTypeToken):
    """
    Name Token supports at the moment only:
    [A-Z] | [a-z] | [À-Ö] | [Ø-ö] | [ø-ÿ]
    [0-9]
    '.' | '-' | '_' | ':'
    """
    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="NMTOKEN" id="NMTOKEN">
            <xs:restriction base="xs:token">
                <xs:pattern value="\c+"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    _PATTERN = rf"({name_character})+"


class XMLSimpleTypeDate(XMLSimpleType):
    # [-]CCYY-MM-DD[Z|(+|-)hh:mm]
    # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s07.html

    XML_ET_ELEMENT = XMLElementTreeElement(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="date" id="date">
            <xs:restriction base="xs:anySimpleType">
                <xs:whiteSpace value="collapse" fixed="true"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))
    _PATTERN = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])(Z|[+-](?:2[0-3]|[01][0-9]):[' \
               r'0-5][0-9])?$'


for simple_type in find_all_xsd_children(tag='simpleType'):
    xml_element_tree_element = XMLElementTreeElement(simple_type)
    class_name = xml_element_tree_element.class_name
    base_classes = f"({', '.join(get_simple_format_all_base_classes(xml_element_tree_element))}, )"
    attributes = """
    {
    '__doc__': xml_element_tree_element.get_doc(), 
    'XML_ET_ELEMENT':xml_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
