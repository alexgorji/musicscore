import re
import xml.etree.ElementTree as ET
from typing import Any, Optional

from musicxml.util.core import get_cleaned_token
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement


class XSDSimpleType(XSDTreeElement):
    """
    Parent Class for all SimpleType classes
    """
    _TYPES: list[type] = []
    _UNION: list[Any] = []
    _FORCED_PERMITTED: list[str] = []
    _PERMITTED: list[str] = []
    _PATTERN: Optional[str] = None

    def __init__(self, value: Any, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        if not self._PERMITTED:
            self._populate_permitted()
        if not self._FORCED_PERMITTED:
            self._populate_forced_permitted()
        if self._UNION:
            self._TYPES = []
            for t_ in self._UNION:
                self._TYPES.extend(t_._TYPES)
        self._populate_pattern()
        self._value = None
        self.value = value

    def _check_value(self, v):
        if self._UNION:
            errors = []
            for t_ in self._UNION:
                try:
                    t_(v)
                    return
                except TypeError:
                    pass
                except ValueError as err:
                    errors.append(err.args[0])
            raise ValueError(self._get_error_class(), errors)

        elif v in self._FORCED_PERMITTED:
            return
        if self._PERMITTED:
            if v not in self._PERMITTED:
                raise ValueError(f"{self._get_error_class()}.value '{v}' must be in {self._PERMITTED}")
        elif self._PATTERN:
            restriction = self.get_xsd_tree().get_restriction()
            if restriction:
                if restriction.get_attributes()['base'] == 'xs:date':
                    XSDSimpleTypeDate(v)
                elif restriction.get_attributes()['base'] == 'xs:token':
                    v = XSDSimpleTypeToken(v).value
                elif restriction.get_attributes()['base'] == 'xs:smufl-glyph-name':
                    XSDSimpleTypeSmuflGlyphName(v)
            if re.compile(self._PATTERN).fullmatch(v) is None:
                raise ValueError(
                    f"{self._get_error_class()}.value '{v}' must match the following pattern: {self._PATTERN}")
        else:
            restriction = self.get_xsd_tree().get_restriction()
            if restriction:
                restriction_children = restriction.get_children()
                for child in restriction_children:
                    if child.tag == 'minLength' and len(v) < int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self._get_error_class()}.value '{v}' must have a length >= 1")
                    if child.tag == 'minExclusive' and v <= int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self._get_error_class()}.value '{v}' must be greater than"
                            f" '{child.get_attributes()['value']}'")
                    if child.tag == 'minInclusive' and v < int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self._get_error_class()}.value '{v}' must be greater than or equal to"
                            f" '{child.get_attributes()['value']}'")
                    if child.tag == 'maxInclusive' and v > int(child.get_attributes()['value']):
                        raise ValueError(
                            f"{self._get_error_class()}.value '{v}' must be less than or equal to"
                            f" '{child.get_attributes()['value']}'")

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
            message = f"{self._get_error_class()}'s value '{value}' can only be of types {[type_.__name__ for type_ in self._TYPES]} not {type(value).__name__}."
            if self._PERMITTED:
                message += f" {self._get_error_class()}.value must in {self._PERMITTED}"
            if self._FORCED_PERMITTED:
                message += f" {self._get_error_class()}.value can also be {self._FORCED_PERMITTED}"
            raise TypeError(message)

    def _get_error_class(self):
        if self.parent:
            return self.parent.__class__.__name__
        else:
            return self.__class__.__name__

    def _populate_permitted(self):
        self._PERMITTED = self.get_xsd_tree().get_permitted()

    def _populate_forced_permitted(self):
        union = self.get_xsd_tree().get_union()
        if union and union.get_children() and union.get_children()[0].tag == 'simpleType':
            intern_simple_type = union.get_children()[0]
            enumerations = [child for child in intern_simple_type.get_restriction().get_children() if child.tag
                            == 'enumeration']
            self._FORCED_PERMITTED = [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def _populate_pattern(self):
        pattern = self.get_xsd_tree().get_pattern(self.__class__.__mro__[1].get_xsd_tree())
        if pattern:
            self._PATTERN = pattern

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._check_value_type(v)
        if v not in self._FORCED_PERMITTED:
            self._check_value(v)
        self._value = v

    def __repr__(self):
        return str(self.value)


class XSDSimpleTypeInteger(XSDSimpleType):
    _TYPES = [int]
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypeInteger, type(self)).value.fset(self, v)


class XSDSimpleTypeNonNegativeInteger(XSDSimpleTypeInteger):
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypeNonNegativeInteger, type(self)).value.fset(self, v)
        if v < 0:
            raise ValueError(f'value {v} must be non negative.')


class XSDSimpleTypePositiveInteger(XSDSimpleTypeInteger):
    _TYPES = [int]
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypePositiveInteger, type(self)).value.fset(self, v)
        try:
            if v <= 0:
                raise ValueError(f'value {v} must be greater than 0.')
        except TypeError:
            # Important because of XSDSimpleTypePositiveIntegerOrEmpty
            pass


class XSDSimpleTypeDecimal(XSDSimpleType):
    _TYPES = [float, int]
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypeDecimal, type(self)).value.fset(self, v)


class XSDSimpleTypeString(XSDSimpleType):
    _TYPES = [str]
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypeString, type(self)).value.fset(self, v)


class XSDSimpleTypeToken(XSDSimpleTypeString):
    _XSD_TREE = XSDTree(ET.fromstring(
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
        super(XSDSimpleTypeToken, type(self)).value.fset(self, v)
        v = get_cleaned_token(v)
        self._value = v


class XSDSimpleTypeDate(XSDSimpleTypeString):
    # [-]CCYY-MM-DD[Z|(+|-)hh:mm]
    # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s07.html

    _XSD_TREE = XSDTree(ET.fromstring(
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

# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_simple_types.py
# -----------------------------------------------------
