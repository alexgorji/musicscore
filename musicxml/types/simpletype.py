import re

from musicxml.util.helperfunctions import get_simple_format_all_base_classes, find_all_xsd_children, get_cleaned_token
from musicxml.util.helprervariables import name_character
from musicxml.xmlelement import MusicXMLElement, XSDTree
import xml.etree.ElementTree as ET


class XMLSimpleType(MusicXMLElement):
    """
    Parent Class for all SimpleType classes
    """
    _TYPES = []
    _FORCED_PERMITTED = []
    _PERMITTED = []
    _PATTERN = None

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self._PERMITTED:
            self._populate_permitted()
        if not self._FORCED_PERMITTED:
            self._populate_forced_permitted()
        self._populate_pattern()
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._check_value_type(v)
        if v not in self._FORCED_PERMITTED:
            self._check_value(v)
        self._value = v

    def _check_value(self, v):
        if v in self._FORCED_PERMITTED:
            return
        if self._PERMITTED:
            if v not in self._PERMITTED:
                raise ValueError(f'{self.__class__.__name__}.value {v} must in {self.__class__._PERMITTED}')
        elif self._PATTERN:
            restriction = self.XML_ET_ELEMENT.get_restriction()
            if restriction:
                if restriction.get_attributes()['base'] == 'xs:date':
                    XMLSimpleTypeDate(v)
                elif restriction.get_attributes()['base'] == 'xs:token':
                    v = XMLSimpleTypeToken(v).value
                elif restriction.get_attributes()['base'] == 'xs:smufl-glyph-name':
                    XMLSimpleTypeSmuflGlypyName(v)
            if re.compile(self._PATTERN).fullmatch(v) is None:
                raise ValueError(
                    f'{self.__class__.__name__}.value {v} must match the following pattern: {self._PATTERN}')
        else:
            restriction = self.XML_ET_ELEMENT.get_restriction()
            if restriction:
                restriction_children = restriction.get_children()
                for child in restriction_children:
                    if child.tag == 'minLength' and len(v) < int(child.get_attributes()['value']):
                        raise ValueError(
                            f'{self.__class__.__name__}.value {v} must have a length >= 1')
                    if child.tag == 'minExclusive' and v <= int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self.__class__.__name__}.value {v} must be greater than"
                            f" {child.get_attributes()['value']}")
                    if child.tag == 'minInclusive' and v < int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self.__class__.__name__}.value {v} must be greater than or equal to"
                            f" {child.get_attributes()['value']}")
                    if child.tag == 'maxInclusive' and v > int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self.__class__.__name__}.value {v} must be less than or equal to"
                            f" {child.get_attributes()['value']}")

    def _check_value_type(self, value):
        if value in self._FORCED_PERMITTED:
            return
        if isinstance(self._TYPES, str):
            raise TypeError
        if self._TYPES == str or not hasattr(self._TYPES, '__iter__'):
            raise TypeError

        if True in [isinstance(value, type_) for type_ in self._TYPES]:
            pass
        else:
            raise TypeError(f"value {value} can only be of types {[type_.__name__ for type_ in self._TYPES]} "
                            f"not {type(value).__name__}.")

    def _populate_permitted(self):
        restriction = self.XML_ET_ELEMENT.get_restriction()
        if restriction:
            enumerations = [child for child in restriction.get_children() if
                            child.tag == 'enumeration']
            self._PERMITTED = [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def _populate_forced_permitted(self):
        union = self.XML_ET_ELEMENT.get_union()
        if union and union.get_children and union.get_children()[0].tag == 'simpleType':
            intern_simple_type = union.get_children()[0]
            enumerations = [child for child in intern_simple_type.get_restriction().get_children() if child.tag
                            == 'enumeration']
            self._FORCED_PERMITTED = [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def _populate_pattern(self):
        restriction = self.XML_ET_ELEMENT.get_restriction()
        if restriction and restriction.get_children and restriction.get_children()[0].tag == 'pattern':
            pattern = rf"{restriction.get_children()[0].get_attributes()['value']}"
            pattern = pattern.replace('\c', name_character)
            self._PATTERN = pattern

    def __repr__(self):
        return str(self.value)


class XMLSimpleTypeInteger(XMLSimpleType):
    _TYPES = [int]
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
        self._check_value_type(v)
        super(XMLSimpleTypeInteger, type(self)).value.fset(self, v)


class XMLSimpleTypeNonNegativeInteger(XMLSimpleTypeInteger):
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
    _TYPES = [int]
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
        try:
            if v <= 0:
                raise ValueError(f'value {v} must be greater than 0.')
        except TypeError:
            # Important because of XMLSimpleTypePositiveIntegerOrEmpty
            pass


class XMLSimpleTypeDecimal(XMLSimpleType):
    _TYPES = [float, int]
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
        self._check_value_type(v)
        super(XMLSimpleTypeDecimal, type(self)).value.fset(self, v)


class XMLSimpleTypeString(XMLSimpleType):
    _TYPES = [str]
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
        self._check_value_type(v)
        super(XMLSimpleTypeString, type(self)).value.fset(self, v)


class XMLSimpleTypeToken(XMLSimpleTypeString):
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
    XML_ET_ELEMENT = XSDTree(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="NMTOKEN" id="NMTOKEN">
            <xs:restriction base="xs:token">
                <xs:pattern value="\c+"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    _PATTERN = rf"({name_character})+"


class XMLSimpleTypeDate(XMLSimpleTypeString):
    # [-]CCYY-MM-DD[Z|(+|-)hh:mm]
    # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s07.html

    XML_ET_ELEMENT = XSDTree(ET.fromstring(
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
    xml_element_tree_element = XSDTree(simple_type)
    class_name = xml_element_tree_element.class_name
    base_classes = f"({', '.join(get_simple_format_all_base_classes(xml_element_tree_element))}, )"
    attributes = """
    {
    '__doc__': xml_element_tree_element.get_doc(), 
    'XML_ET_ELEMENT':xml_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
