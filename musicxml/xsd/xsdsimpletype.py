import re
import xml.etree.ElementTree as ET
from typing import Any, Optional

from musicxml.util.core import get_cleaned_token
from musicxml.util.helprervariables import name_character, xml_name_first_character, xml_name_first_character_without_colon, \
    name_character_without_colon
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
                raise ValueError(f"{self._get_error_class()}.value '{v}' must in {self._PERMITTED}")
        elif self._PATTERN:
            restriction = self.XSD_TREE.get_restriction()
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
            restriction = self.XSD_TREE.get_restriction()
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
        restriction = self.XSD_TREE.get_restriction()
        if restriction:
            enumerations = [child for child in restriction.get_children() if
                            child.tag == 'enumeration']
            self._PERMITTED = [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def _populate_forced_permitted(self):
        union = self.XSD_TREE.get_union()
        if union and union.get_children() and union.get_children()[0].tag == 'simpleType':
            intern_simple_type = union.get_children()[0]
            enumerations = [child for child in intern_simple_type.get_restriction().get_children() if child.tag
                            == 'enumeration']
            self._FORCED_PERMITTED = [enumeration.get_attributes()['value'] for enumeration in enumerations]

    def _populate_pattern(self):
        def get_xsd_pattern(restriction_):
            if restriction_ and restriction_.get_children() and restriction_.get_children()[0].tag == 'pattern':
                return rf"{restriction.get_children()[0].get_attributes()['value']}"
            else:
                if self.__class__.__mro__[1].XSD_TREE:
                    parent_restriction = self.__class__.__mro__[1].XSD_TREE.get_restriction()
                    if parent_restriction and parent_restriction.get_children() and parent_restriction.get_children()[0].tag == 'pattern':
                        return rf"{parent_restriction.get_children()[0].get_attributes()['value']}"

        def translate_pattern(pattern_):
            if pattern_ == "[\i-[:]][\c-[:]]*":
                return rf"{xml_name_first_character_without_colon}{name_character_without_colon}*"
            pattern_ = pattern_.replace('\c', name_character)
            pattern_ = pattern_.replace('\i', xml_name_first_character)
            return pattern_

        restriction = self.XSD_TREE.get_restriction()
        pattern = get_xsd_pattern(restriction)
        if pattern:
            self._PATTERN = translate_pattern(pattern)

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
    XSD_TREE = XSDTree(ET.fromstring(
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
    XSD_TREE = XSDTree(ET.fromstring(
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
    XSD_TREE = XSDTree(ET.fromstring(
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
    XSD_TREE = XSDTree(ET.fromstring(
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
    XSD_TREE = XSDTree(ET.fromstring(
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
    XSD_TREE = XSDTree(ET.fromstring(
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

    XSD_TREE = XSDTree(ET.fromstring(
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


class XSDSimpleTypeNMTOKEN(XSDSimpleTypeToken):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="NMTOKEN" id="NMTOKEN">
    <xs:restriction base="xs:token">
        <xs:pattern value="\c+" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeName(XSDSimpleTypeToken):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="Name" id="Name">
    <xs:restriction base="xs:token">
        <xs:pattern value="\i\c*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNCName(XSDSimpleTypeName):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="NCName" id="NCName">
    <xs:restriction base="xs:Name">
        <xs:pattern value="[\i-[:]][\c-[:]]*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeID(XSDSimpleTypeNCName):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="ID" id="ID">
    <xs:restriction base="xs:NCName" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeIDREF(XSDSimpleTypeNCName):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="IDREF" id="IDREF">
    <xs:restriction base="xs:NCName" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLanguage(XSDSimpleTypeToken):
    """"""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="language" id="language">
    <xs:restriction base="xs:token">
        <xs:pattern value="([a-zA-Z]{2}|[iI]-[a-zA-Z]+|[xX]-[a-zA-Z]{1,8})(-[a-zA-Z]{1,8})*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeAboveBelow(XSDSimpleTypeToken):
    """The above-below type is used to indicate whether one element appears above or below another element."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="above-below">
    <xs:annotation>
        <xs:documentation>The above-below type is used to indicate whether one element appears above or below another element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="above" />
        <xs:enumeration value="below" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBeamLevel(XSDSimpleTypePositiveInteger):
    """The MusicXML format supports six levels of beaming, up to 1024th notes. Unlike the number-level type, the beam-level type identifies concurrent beams in a beam group. It does not distinguish overlapping beams such as grace notes within regular notes, or beams used in different voices."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="beam-level">
    <xs:annotation>
        <xs:documentation>The MusicXML format supports six levels of beaming, up to 1024th notes. Unlike the number-level type, the beam-level type identifies concurrent beams in a beam group. It does not distinguish overlapping beams such as grace notes within regular notes, or beams used in different voices.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="8" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeColor(XSDSimpleTypeToken):
    """The color type indicates the color of an element. Color may be represented as hexadecimal RGB triples, as in HTML, or as hexadecimal ARGB tuples, with the A indicating alpha of transparency. An alpha value of 00 is totally transparent; FF is totally opaque. If RGB is used, the A value is assumed to be FF.

For instance, the RGB value "#800080" represents purple. An ARGB value of "#40800080" would be a transparent purple.

As in SVG 1.1, colors are defined in terms of the sRGB color space (IEC 61966)."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="color">
    <xs:annotation>
        <xs:documentation>The color type indicates the color of an element. Color may be represented as hexadecimal RGB triples, as in HTML, or as hexadecimal ARGB tuples, with the A indicating alpha of transparency. An alpha value of 00 is totally transparent; FF is totally opaque. If RGB is used, the A value is assumed to be FF.

For instance, the RGB value "#800080" represents purple. An ARGB value of "#40800080" would be a transparent purple.

As in SVG 1.1, colors are defined in terms of the sRGB color space (IEC 61966).</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:pattern value="#[\dA-F]{6}([\dA-F][\dA-F])?" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeCommaSeparatedText(XSDSimpleTypeToken):
    """The comma-separated-text type is used to specify a comma-separated list of text elements, as is used by the font-family attribute."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="comma-separated-text">
    <xs:annotation>
        <xs:documentation>The comma-separated-text type is used to specify a comma-separated list of text elements, as is used by the font-family attribute.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:pattern value="[^,]+(, ?[^,]+)*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeCssFontSize(XSDSimpleTypeToken):
    """The css-font-size type includes the CSS font sizes used as an alternative to a numeric point size."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="css-font-size">
    <xs:annotation>
        <xs:documentation>The css-font-size type includes the CSS font sizes used as an alternative to a numeric point size.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="xx-small" />
        <xs:enumeration value="x-small" />
        <xs:enumeration value="small" />
        <xs:enumeration value="medium" />
        <xs:enumeration value="large" />
        <xs:enumeration value="x-large" />
        <xs:enumeration value="xx-large" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeDivisions(XSDSimpleTypeDecimal):
    """The divisions type is used to express values in terms of the musical divisions defined by the divisions element. It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="divisions">
    <xs:annotation>
        <xs:documentation>The divisions type is used to express values in terms of the musical divisions defined by the divisions element. It is preferred that these be integer values both for MIDI interoperability and to avoid roundoff errors.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeEnclosureShape(XSDSimpleTypeToken):
    """The enclosure-shape type describes the shape and presence / absence of an enclosure around text or symbols. A bracket enclosure is similar to a rectangle with the bottom line missing, as is common in jazz notation. An inverted-bracket enclosure is similar to a rectangle with the top line missing."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="enclosure-shape">
    <xs:annotation>
        <xs:documentation>The enclosure-shape type describes the shape and presence / absence of an enclosure around text or symbols. A bracket enclosure is similar to a rectangle with the bottom line missing, as is common in jazz notation. An inverted-bracket enclosure is similar to a rectangle with the top line missing.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="rectangle" />
        <xs:enumeration value="square" />
        <xs:enumeration value="oval" />
        <xs:enumeration value="circle" />
        <xs:enumeration value="bracket" />
        <xs:enumeration value="inverted-bracket" />
        <xs:enumeration value="triangle" />
        <xs:enumeration value="diamond" />
        <xs:enumeration value="pentagon" />
        <xs:enumeration value="hexagon" />
        <xs:enumeration value="heptagon" />
        <xs:enumeration value="octagon" />
        <xs:enumeration value="nonagon" />
        <xs:enumeration value="decagon" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFermataShape(XSDSimpleTypeString):
    """The fermata-shape type represents the shape of the fermata sign. The empty value is equivalent to the normal value."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fermata-shape">
    <xs:annotation>
        <xs:documentation>The fermata-shape type represents the shape of the fermata sign. The empty value is equivalent to the normal value.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="normal" />
        <xs:enumeration value="angled" />
        <xs:enumeration value="square" />
        <xs:enumeration value="double-angled" />
        <xs:enumeration value="double-square" />
        <xs:enumeration value="double-dot" />
        <xs:enumeration value="half-curve" />
        <xs:enumeration value="curlew" />
        <xs:enumeration value="" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFontFamily(XSDSimpleTypeCommaSeparatedText):
    """The font-family is a comma-separated list of font names. These can be specific font styles such as Maestro or Opus, or one of several generic font styles: music, engraved, handwritten, text, serif, sans-serif, handwritten, cursive, fantasy, and monospace. The music, engraved, and handwritten values refer to music fonts; the rest refer to text fonts. The fantasy style refers to decorative text such as found in older German-style printing."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font-family">
    <xs:annotation>
        <xs:documentation>The font-family is a comma-separated list of font names. These can be specific font styles such as Maestro or Opus, or one of several generic font styles: music, engraved, handwritten, text, serif, sans-serif, handwritten, cursive, fantasy, and monospace. The music, engraved, and handwritten values refer to music fonts; the rest refer to text fonts. The fantasy style refers to decorative text such as found in older German-style printing.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="comma-separated-text" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFontStyle(XSDSimpleTypeToken):
    """The font-style type represents a simplified version of the CSS font-style property."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font-style">
    <xs:annotation>
        <xs:documentation>The font-style type represents a simplified version of the CSS font-style property.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="normal" />
        <xs:enumeration value="italic" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFontWeight(XSDSimpleTypeToken):
    """The font-weight type represents a simplified version of the CSS font-weight property."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font-weight">
    <xs:annotation>
        <xs:documentation>The font-weight type represents a simplified version of the CSS font-weight property.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="normal" />
        <xs:enumeration value="bold" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLeftCenterRight(XSDSimpleTypeToken):
    """The left-center-right type is used to define horizontal alignment and text justification."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="left-center-right">
    <xs:annotation>
        <xs:documentation>The left-center-right type is used to define horizontal alignment and text justification.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="left" />
        <xs:enumeration value="center" />
        <xs:enumeration value="right" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLeftRight(XSDSimpleTypeToken):
    """The left-right type is used to indicate whether one element appears to the left or the right of another element."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="left-right">
    <xs:annotation>
        <xs:documentation>The left-right type is used to indicate whether one element appears to the left or the right of another element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="left" />
        <xs:enumeration value="right" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLineLength(XSDSimpleTypeToken):
    """The line-length type distinguishes between different line lengths for doit, falloff, plop, and scoop articulations."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-length">
    <xs:annotation>
        <xs:documentation>The line-length type distinguishes between different line lengths for doit, falloff, plop, and scoop articulations.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="short" />
        <xs:enumeration value="medium" />
        <xs:enumeration value="long" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLineShape(XSDSimpleTypeToken):
    """The line-shape type distinguishes between straight and curved lines."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-shape">
    <xs:annotation>
        <xs:documentation>The line-shape type distinguishes between straight and curved lines.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="straight" />
        <xs:enumeration value="curved" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLineType(XSDSimpleTypeToken):
    """The line-type type distinguishes between solid, dashed, dotted, and wavy lines."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-type">
    <xs:annotation>
        <xs:documentation>The line-type type distinguishes between solid, dashed, dotted, and wavy lines.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="solid" />
        <xs:enumeration value="dashed" />
        <xs:enumeration value="dotted" />
        <xs:enumeration value="wavy" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMidi16(XSDSimpleTypePositiveInteger):
    """The midi-16 type is used to express MIDI 1.0 values that range from 1 to 16."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="midi-16">
    <xs:annotation>
        <xs:documentation>The midi-16 type is used to express MIDI 1.0 values that range from 1 to 16.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="16" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMidi128(XSDSimpleTypePositiveInteger):
    """The midi-128 type is used to express MIDI 1.0 values that range from 1 to 128."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="midi-128">
    <xs:annotation>
        <xs:documentation>The midi-128 type is used to express MIDI 1.0 values that range from 1 to 128.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="128" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMidi16384(XSDSimpleTypePositiveInteger):
    """The midi-16384 type is used to express MIDI 1.0 values that range from 1 to 16,384."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="midi-16384">
    <xs:annotation>
        <xs:documentation>The midi-16384 type is used to express MIDI 1.0 values that range from 1 to 16,384.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="16384" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMute(XSDSimpleTypeString):
    """The mute type represents muting for different instruments, including brass, winds, and strings. The on and off values are used for undifferentiated mutes. The remaining values represent specific mutes."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="mute">
    <xs:annotation>
        <xs:documentation>The mute type represents muting for different instruments, including brass, winds, and strings. The on and off values are used for undifferentiated mutes. The remaining values represent specific mutes.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="on" />
        <xs:enumeration value="off" />
        <xs:enumeration value="straight" />
        <xs:enumeration value="cup" />
        <xs:enumeration value="harmon-no-stem" />
        <xs:enumeration value="harmon-stem" />
        <xs:enumeration value="bucket" />
        <xs:enumeration value="plunger" />
        <xs:enumeration value="hat" />
        <xs:enumeration value="solotone" />
        <xs:enumeration value="practice" />
        <xs:enumeration value="stop-mute" />
        <xs:enumeration value="stop-hand" />
        <xs:enumeration value="echo" />
        <xs:enumeration value="palm" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNonNegativeDecimal(XSDSimpleTypeDecimal):
    """The non-negative-decimal type specifies a non-negative decimal value."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="non-negative-decimal">
    <xs:annotation>
        <xs:documentation>The non-negative-decimal type specifies a non-negative decimal value.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal">
        <xs:minInclusive value="0" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNumberLevel(XSDSimpleTypePositiveInteger):
    """Slurs, tuplets, and many other features can be concurrent and overlap within a single musical part. The number-level entity distinguishes up to 16 concurrent objects of the same type when the objects overlap in MusicXML document order. Values greater than 6 are usually only needed for music with a large number of divisi staves in a single part, or if there are more than 6 cross-staff arpeggios in a single measure. When a number-level value is implied, the value is 1 by default.

When polyphonic parts are involved, the ordering within a MusicXML document can differ from musical score order. As an example, say we have a piano part in 4/4 where within a single measure, all the notes on the top staff are followed by all the notes on the bottom staff. In this example, each staff has a slur that starts on beat 2 and stops on beat 3, and there is a third slur that goes from beat 1 of one staff to beat 4 of the other staff.

In this situation, the two mid-measure slurs can use the same number because they do not overlap in MusicXML document order, even though they do overlap in musical score order. Within the MusicXML document, the top staff slur will both start and stop before the bottom staff slur starts and stops.

If the cross-staff slur starts in the top staff and stops in the bottom staff, it will need a separate number from the mid-measure slurs because it overlaps those slurs in MusicXML document order. However, if the cross-staff slur starts in the bottom staff and stops in the top staff, all three slurs can use the same number. None of them overlap within the MusicXML document, even though they all overlap each other in the musical score order. Within the MusicXML document, the start and stop of the top-staff slur will be followed by the stop and start of the cross-staff slur, followed by the start and stop of the bottom-staff slur.

As this example demonstrates, a reading program should be prepared to handle cases where the number-levels start and stop in an arbitrary order. Because the start and stop values refer to musical score order, a program may find the stopping point of an object earlier in the MusicXML document than it will find its starting point."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="number-level">
    <xs:annotation>
        <xs:documentation>Slurs, tuplets, and many other features can be concurrent and overlap within a single musical part. The number-level entity distinguishes up to 16 concurrent objects of the same type when the objects overlap in MusicXML document order. Values greater than 6 are usually only needed for music with a large number of divisi staves in a single part, or if there are more than 6 cross-staff arpeggios in a single measure. When a number-level value is implied, the value is 1 by default.

When polyphonic parts are involved, the ordering within a MusicXML document can differ from musical score order. As an example, say we have a piano part in 4/4 where within a single measure, all the notes on the top staff are followed by all the notes on the bottom staff. In this example, each staff has a slur that starts on beat 2 and stops on beat 3, and there is a third slur that goes from beat 1 of one staff to beat 4 of the other staff.

In this situation, the two mid-measure slurs can use the same number because they do not overlap in MusicXML document order, even though they do overlap in musical score order. Within the MusicXML document, the top staff slur will both start and stop before the bottom staff slur starts and stops.

If the cross-staff slur starts in the top staff and stops in the bottom staff, it will need a separate number from the mid-measure slurs because it overlaps those slurs in MusicXML document order. However, if the cross-staff slur starts in the bottom staff and stops in the top staff, all three slurs can use the same number. None of them overlap within the MusicXML document, even though they all overlap each other in the musical score order. Within the MusicXML document, the start and stop of the top-staff slur will be followed by the stop and start of the cross-staff slur, followed by the start and stop of the bottom-staff slur.

As this example demonstrates, a reading program should be prepared to handle cases where the number-levels start and stop in an arbitrary order. Because the start and stop values refer to musical score order, a program may find the stopping point of an object earlier in the MusicXML document than it will find its starting point.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="16" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNumberOfLines(XSDSimpleTypeNonNegativeInteger):
    """The number-of-lines type is used to specify the number of lines in text decoration attributes."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="number-of-lines">
    <xs:annotation>
        <xs:documentation>The number-of-lines type is used to specify the number of lines in text decoration attributes.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:nonNegativeInteger">
        <xs:minInclusive value="0" />
        <xs:maxInclusive value="3" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNumeralValue(XSDSimpleTypePositiveInteger):
    """The numeral-value type represents a Roman numeral or Nashville number value as a positive integer from 1 to 7."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="numeral-value">
    <xs:annotation>
        <xs:documentation>The numeral-value type represents a Roman numeral or Nashville number value as a positive integer from 1 to 7.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="7" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeOverUnder(XSDSimpleTypeToken):
    """The over-under type is used to indicate whether the tips of curved lines such as slurs and ties are overhand (tips down) or underhand (tips up)."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="over-under">
    <xs:annotation>
        <xs:documentation>The over-under type is used to indicate whether the tips of curved lines such as slurs and ties are overhand (tips down) or underhand (tips up).</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="over" />
        <xs:enumeration value="under" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePercent(XSDSimpleTypeDecimal):
    """The percent type specifies a percentage from 0 to 100."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="percent">
    <xs:annotation>
        <xs:documentation>The percent type specifies a percentage from 0 to 100.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal">
        <xs:minInclusive value="0" />
        <xs:maxInclusive value="100" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePositiveDecimal(XSDSimpleTypeDecimal):
    """The positive-decimal type specifies a positive decimal value."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="positive-decimal">
    <xs:annotation>
        <xs:documentation>The positive-decimal type specifies a positive decimal value.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal">
        <xs:minExclusive value="0" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePositiveDivisions(XSDSimpleTypeDivisions):
    """The positive-divisions type restricts divisions values to positive numbers."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="positive-divisions">
    <xs:annotation>
        <xs:documentation>The positive-divisions type restricts divisions values to positive numbers.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="divisions">
        <xs:minExclusive value="0" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeRotationDegrees(XSDSimpleTypeDecimal):
    """The rotation-degrees type specifies rotation, pan, and elevation values in degrees. Values range from -180 to 180."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="rotation-degrees">
    <xs:annotation>
        <xs:documentation>The rotation-degrees type specifies rotation, pan, and elevation values in degrees. Values range from -180 to 180.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal">
        <xs:minInclusive value="-180" />
        <xs:maxInclusive value="180" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSemiPitched(XSDSimpleTypeString):
    """The semi-pitched type represents categories of indefinite pitch for percussion instruments."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="semi-pitched">
    <xs:annotation>
        <xs:documentation>The semi-pitched type represents categories of indefinite pitch for percussion instruments.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="high" />
        <xs:enumeration value="medium-high" />
        <xs:enumeration value="medium" />
        <xs:enumeration value="medium-low" />
        <xs:enumeration value="low" />
        <xs:enumeration value="very-low" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflGlyphName(XSDSimpleTypeNMTOKEN):
    """The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-glyph-name type is used for attributes that reference a specific Standard Music Font Layout (SMuFL) character. The value is a SMuFL canonical glyph name, not a code point. For instance, the value for a standard piano pedal mark would be keyboardPedalPed, not U+E650.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:NMTOKEN" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflAccidentalGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-accidental-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) accidental character. The value is a SMuFL canonical glyph name that starts with one of the strings used at the start of glyph names for SMuFL accidentals."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-accidental-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-accidental-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) accidental character. The value is a SMuFL canonical glyph name that starts with one of the strings used at the start of glyph names for SMuFL accidentals.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="(acc|medRenFla|medRenNatura|medRenShar|kievanAccidental)(\c+)" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflCodaGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-coda-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) coda character. The value is a SMuFL canonical glyph name that starts with coda."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-coda-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-coda-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) coda character. The value is a SMuFL canonical glyph name that starts with coda.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="coda\c*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflLyricsGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-lyrics-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) lyrics elision character. The value is a SMuFL canonical glyph name that starts with lyrics."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-lyrics-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-lyrics-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) lyrics elision character. The value is a SMuFL canonical glyph name that starts with lyrics.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="lyrics\c+" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflPictogramGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-pictogram-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) percussion pictogram character. The value is a SMuFL canonical glyph name that starts with pict."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-pictogram-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-pictogram-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) percussion pictogram character. The value is a SMuFL canonical glyph name that starts with pict.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="pict\c+" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflSegnoGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-segno-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) segno character. The value is a SMuFL canonical glyph name that starts with segno."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-segno-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-segno-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) segno character. The value is a SMuFL canonical glyph name that starts with segno.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="segno\c*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSmuflWavyLineGlyphName(XSDSimpleTypeSmuflGlyphName):
    """The smufl-wavy-line-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) wavy line character. The value is a SMuFL canonical glyph name that either starts with wiggle, or begins with guitar and ends with VibratoStroke. This includes all the glyphs in the Multi-segment lines range, excluding the beam glyphs."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="smufl-wavy-line-glyph-name">
    <xs:annotation>
        <xs:documentation>The smufl-wavy-line-glyph-name type is used to reference a specific Standard Music Font Layout (SMuFL) wavy line character. The value is a SMuFL canonical glyph name that either starts with wiggle, or begins with guitar and ends with VibratoStroke. This includes all the glyphs in the Multi-segment lines range, excluding the beam glyphs.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="smufl-glyph-name">
        <xs:pattern value="(wiggle\c+)|(guitar\c*VibratoStroke)" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartNote(XSDSimpleTypeToken):
    """The start-note type describes the starting note of trills and mordents for playback, relative to the current note."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-note">
    <xs:annotation>
        <xs:documentation>The start-note type describes the starting note of trills and mordents for playback, relative to the current note.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="upper" />
        <xs:enumeration value="main" />
        <xs:enumeration value="below" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartStop(XSDSimpleTypeToken):
    """The start-stop type is used for an attribute of musical elements that can either start or stop, such as tuplets.

The values of start and stop refer to how an element appears in musical score order, not in MusicXML document order. An element with a stop attribute may precede the corresponding element with a start attribute within a MusicXML document. This is particularly common in multi-staff music. For example, the stopping point for a tuplet may appear in staff 1 before the starting point for the tuplet appears in staff 2 later in the document.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-stop">
    <xs:annotation>
        <xs:documentation>The start-stop type is used for an attribute of musical elements that can either start or stop, such as tuplets.

The values of start and stop refer to how an element appears in musical score order, not in MusicXML document order. An element with a stop attribute may precede the corresponding element with a start attribute within a MusicXML document. This is particularly common in multi-staff music. For example, the stopping point for a tuplet may appear in staff 1 before the starting point for the tuplet appears in staff 2 later in the document.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartStopContinue(XSDSimpleTypeToken):
    """The start-stop-continue type is used for an attribute of musical elements that can either start or stop, but also need to refer to an intermediate point in the symbol, as for complex slurs or for formatting of symbols across system breaks.

The values of start, stop, and continue refer to how an element appears in musical score order, not in MusicXML document order. An element with a stop attribute may precede the corresponding element with a start attribute within a MusicXML document. This is particularly common in multi-staff music. For example, the stopping point for a slur may appear in staff 1 before the starting point for the slur appears in staff 2 later in the document.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order. For example, a note that marks both the end of one slur and the start of a new slur should have the incoming slur element with a type of stop precede the outgoing slur element with a type of start."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-stop-continue">
    <xs:annotation>
        <xs:documentation>The start-stop-continue type is used for an attribute of musical elements that can either start or stop, but also need to refer to an intermediate point in the symbol, as for complex slurs or for formatting of symbols across system breaks.

The values of start, stop, and continue refer to how an element appears in musical score order, not in MusicXML document order. An element with a stop attribute may precede the corresponding element with a start attribute within a MusicXML document. This is particularly common in multi-staff music. For example, the stopping point for a slur may appear in staff 1 before the starting point for the slur appears in staff 2 later in the document.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order. For example, a note that marks both the end of one slur and the start of a new slur should have the incoming slur element with a type of stop precede the outgoing slur element with a type of start.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="continue" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartStopSingle(XSDSimpleTypeToken):
    """The start-stop-single type is used for an attribute of musical elements that can be used for either multi-note or single-note musical elements, as for groupings.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-stop-single">
    <xs:annotation>
        <xs:documentation>The start-stop-single type is used for an attribute of musical elements that can be used for either multi-note or single-note musical elements, as for groupings.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="single" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStringNumber(XSDSimpleTypePositiveInteger):
    """The string-number type indicates a string number. Strings are numbered from high to low, with 1 being the highest pitched full-length string."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="string-number">
    <xs:annotation>
        <xs:documentation>The string-number type indicates a string number. Strings are numbered from high to low, with 1 being the highest pitched full-length string.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSymbolSize(XSDSimpleTypeToken):
    """The symbol-size type is used to distinguish between full, cue sized, grace cue sized, and oversized symbols."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="symbol-size">
    <xs:annotation>
        <xs:documentation>The symbol-size type is used to distinguish between full, cue sized, grace cue sized, and oversized symbols.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="full" />
        <xs:enumeration value="cue" />
        <xs:enumeration value="grace-cue" />
        <xs:enumeration value="large" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTenths(XSDSimpleTypeDecimal):
    """The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.

Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tenths">
    <xs:annotation>
        <xs:documentation>The tenths type is a number representing tenths of interline staff space (positive or negative). Both integer and decimal values are allowed, such as 5 for a half space and 2.5 for a quarter space. Interline space is measured from the middle of a staff line.

Distances in a MusicXML file are measured in tenths of staff space. Tenths are then scaled to millimeters within the scaling element, used in the defaults element at the start of a score. Individual staves can apply a scaling factor to adjust staff size. When a MusicXML element or attribute refers to tenths, it means the global tenths defined by the scaling element, not the local tenths as adjusted by the staff-size element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTextDirection(XSDSimpleTypeToken):
    """The text-direction type is used to adjust and override the Unicode bidirectional text algorithm, similar to the Directionality data category in the W3C Internationalization Tag Set recommendation. Values are ltr (left-to-right embed), rtl (right-to-left embed), lro (left-to-right bidi-override), and rlo (right-to-left bidi-override). The default value is ltr. This type is typically used by applications that store text in left-to-right visual order rather than logical order. Such applications can use the lro value to better communicate with other applications that more fully support bidirectional text."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="text-direction">
    <xs:annotation>
        <xs:documentation>The text-direction type is used to adjust and override the Unicode bidirectional text algorithm, similar to the Directionality data category in the W3C Internationalization Tag Set recommendation. Values are ltr (left-to-right embed), rtl (right-to-left embed), lro (left-to-right bidi-override), and rlo (right-to-left bidi-override). The default value is ltr. This type is typically used by applications that store text in left-to-right visual order rather than logical order. Such applications can use the lro value to better communicate with other applications that more fully support bidirectional text.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="ltr" />
        <xs:enumeration value="rtl" />
        <xs:enumeration value="lro" />
        <xs:enumeration value="rlo" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTiedType(XSDSimpleTypeToken):
    """The tied-type type is used as an attribute of the tied element to specify where the visual representation of a tie begins and ends. A tied element which joins two notes of the same pitch can be specified with tied-type start on the first note and tied-type stop on the second note. To indicate a note should be undamped, use a single tied element with tied-type let-ring. For other ties that are visually attached to a single note, such as a tie leading into or out of a repeated section or coda, use two tied elements on the same note, one start and one stop.

In start-stop cases, ties can add more elements using a continue type. This is typically used to specify the formatting of cross-system ties.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order. For example, a note with a tie at the end of a first ending should have the tied element with a type of start precede the tied element with a type of stop."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tied-type">
    <xs:annotation>
        <xs:documentation>The tied-type type is used as an attribute of the tied element to specify where the visual representation of a tie begins and ends. A tied element which joins two notes of the same pitch can be specified with tied-type start on the first note and tied-type stop on the second note. To indicate a note should be undamped, use a single tied element with tied-type let-ring. For other ties that are visually attached to a single note, such as a tie leading into or out of a repeated section or coda, use two tied elements on the same note, one start and one stop.

In start-stop cases, ties can add more elements using a continue type. This is typically used to specify the formatting of cross-system ties.

When multiple elements with the same tag are used within the same note, their order within the MusicXML document should match the musical score order. For example, a note with a tie at the end of a first ending should have the tied element with a type of start precede the tied element with a type of stop.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="continue" />
        <xs:enumeration value="let-ring" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTimeOnly(XSDSimpleTypeToken):
    """The time-only type is used to indicate that a particular playback- or listening-related element only applies particular times through a repeated section. The value is a comma-separated list of positive integers arranged in ascending order, indicating which times through the repeated section that the element applies."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="time-only">
    <xs:annotation>
        <xs:documentation>The time-only type is used to indicate that a particular playback- or listening-related element only applies particular times through a repeated section. The value is a comma-separated list of positive integers arranged in ascending order, indicating which times through the repeated section that the element applies.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:pattern value="[1-9][0-9]*(, ?[1-9][0-9]*)*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTopBottom(XSDSimpleTypeToken):
    """The top-bottom type is used to indicate the top or bottom part of a vertical shape like non-arpeggiate."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="top-bottom">
    <xs:annotation>
        <xs:documentation>The top-bottom type is used to indicate the top or bottom part of a vertical shape like non-arpeggiate.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="top" />
        <xs:enumeration value="bottom" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTremoloType(XSDSimpleTypeToken):
    """The tremolo-type is used to distinguish double-note, single-note, and unmeasured tremolos."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tremolo-type">
    <xs:annotation>
        <xs:documentation>The tremolo-type is used to distinguish double-note, single-note, and unmeasured tremolos.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="single" />
        <xs:enumeration value="unmeasured" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTrillBeats(XSDSimpleTypeDecimal):
    """The trill-beats type specifies the beats used in a trill-sound or bend-sound attribute group. It is a decimal value with a minimum value of 2."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="trill-beats">
    <xs:annotation>
        <xs:documentation>The trill-beats type specifies the beats used in a trill-sound or bend-sound attribute group. It is a decimal value with a minimum value of 2.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal">
        <xs:minInclusive value="2" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTrillStep(XSDSimpleTypeToken):
    """The trill-step type describes the alternating note of trills and mordents for playback, relative to the current note."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="trill-step">
    <xs:annotation>
        <xs:documentation>The trill-step type describes the alternating note of trills and mordents for playback, relative to the current note.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="whole" />
        <xs:enumeration value="half" />
        <xs:enumeration value="unison" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTwoNoteTurn(XSDSimpleTypeToken):
    """The two-note-turn type describes the ending notes of trills and mordents for playback, relative to the current note."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="two-note-turn">
    <xs:annotation>
        <xs:documentation>The two-note-turn type describes the ending notes of trills and mordents for playback, relative to the current note.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="whole" />
        <xs:enumeration value="half" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeUpDown(XSDSimpleTypeToken):
    """The up-down type is used for the direction of arrows and other pointed symbols like vertical accents, indicating which way the tip is pointing."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="up-down">
    <xs:annotation>
        <xs:documentation>The up-down type is used for the direction of arrows and other pointed symbols like vertical accents, indicating which way the tip is pointing.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="up" />
        <xs:enumeration value="down" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeUprightInverted(XSDSimpleTypeToken):
    """The upright-inverted type describes the appearance of a fermata element. The value is upright if not specified."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="upright-inverted">
    <xs:annotation>
        <xs:documentation>The upright-inverted type describes the appearance of a fermata element. The value is upright if not specified.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="upright" />
        <xs:enumeration value="inverted" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeValign(XSDSimpleTypeToken):
    """The valign type is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text. If the text is on multiple lines, baseline alignment refers to the baseline of the lowest line of text. Defaults are implementation-dependent."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="valign">
    <xs:annotation>
        <xs:documentation>The valign type is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text. If the text is on multiple lines, baseline alignment refers to the baseline of the lowest line of text. Defaults are implementation-dependent.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="top" />
        <xs:enumeration value="middle" />
        <xs:enumeration value="bottom" />
        <xs:enumeration value="baseline" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeValignImage(XSDSimpleTypeToken):
    """The valign-image type is used to indicate vertical alignment for images and graphics, so it does not include a baseline value. Defaults are implementation-dependent."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="valign-image">
    <xs:annotation>
        <xs:documentation>The valign-image type is used to indicate vertical alignment for images and graphics, so it does not include a baseline value. Defaults are implementation-dependent.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="top" />
        <xs:enumeration value="middle" />
        <xs:enumeration value="bottom" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeYesNo(XSDSimpleTypeToken):
    """The yes-no type is used for boolean-like attributes. We cannot use W3C XML Schema booleans due to their restrictions on expression of boolean values."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="yes-no">
    <xs:annotation>
        <xs:documentation>The yes-no type is used for boolean-like attributes. We cannot use W3C XML Schema booleans due to their restrictions on expression of boolean values.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="yes" />
        <xs:enumeration value="no" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeYyyyMmDd(XSDSimpleTypeDate):
    """Calendar dates are represented yyyy-mm-dd format, following ISO 8601. This is a W3C XML Schema date type, but without the optional timezone data."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="yyyy-mm-dd">
    <xs:annotation>
        <xs:documentation>Calendar dates are represented yyyy-mm-dd format, following ISO 8601. This is a W3C XML Schema date type, but without the optional timezone data.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:date">
        <xs:pattern value="[^:Z]*" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeCancelLocation(XSDSimpleTypeString):
    """The cancel-location type is used to indicate where a key signature cancellation appears relative to a new key signature: to the left, to the right, or before the barline and to the left. It is left by default. For mid-measure key elements, a cancel-location of before-barline should be treated like a cancel-location of left."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="cancel-location">
    <xs:annotation>
        <xs:documentation>The cancel-location type is used to indicate where a key signature cancellation appears relative to a new key signature: to the left, to the right, or before the barline and to the left. It is left by default. For mid-measure key elements, a cancel-location of before-barline should be treated like a cancel-location of left.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="left" />
        <xs:enumeration value="right" />
        <xs:enumeration value="before-barline" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeClefSign(XSDSimpleTypeString):
    """The clef-sign type represents the different clef symbols. The jianpu sign indicates that the music that follows should be in jianpu numbered notation, just as the TAB sign indicates that the music that follows should be in tablature notation. Unlike TAB, a jianpu sign does not correspond to a visual clef notation.

The none sign is deprecated as of MusicXML 4.0. Use the clef element's print-object attribute instead. When the none sign is used, notes should be displayed as if in treble clef."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="clef-sign">
    <xs:annotation>
        <xs:documentation>The clef-sign type represents the different clef symbols. The jianpu sign indicates that the music that follows should be in jianpu numbered notation, just as the TAB sign indicates that the music that follows should be in tablature notation. Unlike TAB, a jianpu sign does not correspond to a visual clef notation.

The none sign is deprecated as of MusicXML 4.0. Use the clef element's print-object attribute instead. When the none sign is used, notes should be displayed as if in treble clef.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="G" />
        <xs:enumeration value="F" />
        <xs:enumeration value="C" />
        <xs:enumeration value="percussion" />
        <xs:enumeration value="TAB" />
        <xs:enumeration value="jianpu" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFifths(XSDSimpleTypeInteger):
    """The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name)."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fifths">
    <xs:annotation>
        <xs:documentation>The fifths type represents the number of flats or sharps in a traditional key signature. Negative numbers are used for flats and positive numbers for sharps, reflecting the key's placement within the circle of fifths (hence the type name).</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:integer" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMode(XSDSimpleTypeString):
    """The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor, dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="mode">
    <xs:annotation>
        <xs:documentation>The mode type is used to specify major/minor and other mode distinctions. Valid mode values include major, minor, dorian, phrygian, lydian, mixolydian, aeolian, ionian, locrian, and none.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeShowFrets(XSDSimpleTypeToken):
    """The show-frets type indicates whether to show tablature frets as numbers (0, 1, 2) or letters (a, b, c). The default choice is numbers."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="show-frets">
    <xs:annotation>
        <xs:documentation>The show-frets type indicates whether to show tablature frets as numbers (0, 1, 2) or letters (a, b, c). The default choice is numbers.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="numbers" />
        <xs:enumeration value="letters" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStaffLine(XSDSimpleTypePositiveInteger):
    """The staff-line type indicates the line on a given staff. Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff-line">
    <xs:annotation>
        <xs:documentation>The staff-line type indicates the line on a given staff. Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStaffLinePosition(XSDSimpleTypeInteger):
    """The staff-line-position type indicates the line position on a given staff. Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff. A staff-line-position value can extend beyond the range of the lines on the current staff."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff-line-position">
    <xs:annotation>
        <xs:documentation>The staff-line-position type indicates the line position on a given staff. Staff lines are numbered from bottom to top, with 1 being the bottom line on a staff. A staff-line-position value can extend beyond the range of the lines on the current staff.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:integer" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStaffNumber(XSDSimpleTypePositiveInteger):
    """The staff-number type indicates staff numbers within a multi-staff part. Staves are numbered from top to bottom, with 1 being the top staff on a part."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff-number">
    <xs:annotation>
        <xs:documentation>The staff-number type indicates staff numbers within a multi-staff part. Staves are numbered from top to bottom, with 1 being the top staff on a part.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStaffType(XSDSimpleTypeString):
    """The staff-type value can be ossia, editorial, cue, alternate, or regular. An ossia staff represents music that can be played instead of what appears on the regular staff. An editorial staff also represents musical alternatives, but is created by an editor rather than the composer. It can be used for suggested interpretations or alternatives from other sources. A cue staff represents music from another part. An alternate staff shares the same music as the prior staff, but displayed differently (e.g., treble and bass clef, standard notation and tablature). It is not included in playback. An alternate staff provides more information to an application reading a file than encoding the same music in separate parts, so its use is preferred in this situation if feasible. A regular staff is the standard default staff-type."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff-type">
    <xs:annotation>
        <xs:documentation>The staff-type value can be ossia, editorial, cue, alternate, or regular. An ossia staff represents music that can be played instead of what appears on the regular staff. An editorial staff also represents musical alternatives, but is created by an editor rather than the composer. It can be used for suggested interpretations or alternatives from other sources. A cue staff represents music from another part. An alternate staff shares the same music as the prior staff, but displayed differently (e.g., treble and bass clef, standard notation and tablature). It is not included in playback. An alternate staff provides more information to an application reading a file than encoding the same music in separate parts, so its use is preferred in this situation if feasible. A regular staff is the standard default staff-type.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="ossia" />
        <xs:enumeration value="editorial" />
        <xs:enumeration value="cue" />
        <xs:enumeration value="alternate" />
        <xs:enumeration value="regular" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTimeRelation(XSDSimpleTypeString):
    """The time-relation type indicates the symbol used to represent the interchangeable aspect of dual time signatures."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="time-relation">
    <xs:annotation>
        <xs:documentation>The time-relation type indicates the symbol used to represent the interchangeable aspect of dual time signatures.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="parentheses" />
        <xs:enumeration value="bracket" />
        <xs:enumeration value="equals" />
        <xs:enumeration value="slash" />
        <xs:enumeration value="space" />
        <xs:enumeration value="hyphen" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTimeSeparator(XSDSimpleTypeToken):
    """The time-separator type indicates how to display the arrangement between the beats and beat-type values in a time signature. The default value is none. The horizontal, diagonal, and vertical values represent horizontal, diagonal lower-left to upper-right, and vertical lines respectively. For these values, the beats and beat-type values are arranged on either side of the separator line. The none value represents no separator with the beats and beat-type arranged vertically. The adjacent value represents no separator with the beats and beat-type arranged horizontally."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="time-separator">
    <xs:annotation>
        <xs:documentation>The time-separator type indicates how to display the arrangement between the beats and beat-type values in a time signature. The default value is none. The horizontal, diagonal, and vertical values represent horizontal, diagonal lower-left to upper-right, and vertical lines respectively. For these values, the beats and beat-type values are arranged on either side of the separator line. The none value represents no separator with the beats and beat-type arranged vertically. The adjacent value represents no separator with the beats and beat-type arranged horizontally.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="none" />
        <xs:enumeration value="horizontal" />
        <xs:enumeration value="diagonal" />
        <xs:enumeration value="vertical" />
        <xs:enumeration value="adjacent" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTimeSymbol(XSDSimpleTypeToken):
    """The time-symbol type indicates how to display a time signature. The normal value is the usual fractional display, and is the implied symbol type if none is specified. Other options are the common and cut time symbols, as well as a single number with an implied denominator. The note symbol indicates that the beat-type should be represented with the corresponding downstem note rather than a number. The dotted-note symbol indicates that the beat-type should be represented with a dotted downstem note that corresponds to three times the beat-type value, and a numerator that is one third the beats value."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="time-symbol">
    <xs:annotation>
        <xs:documentation>The time-symbol type indicates how to display a time signature. The normal value is the usual fractional display, and is the implied symbol type if none is specified. Other options are the common and cut time symbols, as well as a single number with an implied denominator. The note symbol indicates that the beat-type should be represented with the corresponding downstem note rather than a number. The dotted-note symbol indicates that the beat-type should be represented with a dotted downstem note that corresponds to three times the beat-type value, and a numerator that is one third the beats value.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="common" />
        <xs:enumeration value="cut" />
        <xs:enumeration value="single-number" />
        <xs:enumeration value="note" />
        <xs:enumeration value="dotted-note" />
        <xs:enumeration value="normal" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBackwardForward(XSDSimpleTypeToken):
    """The backward-forward type is used to specify repeat directions. The start of the repeat has a forward direction while the end of the repeat has a backward direction."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="backward-forward">
    <xs:annotation>
        <xs:documentation>The backward-forward type is used to specify repeat directions. The start of the repeat has a forward direction while the end of the repeat has a backward direction.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="backward" />
        <xs:enumeration value="forward" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBarStyle(XSDSimpleTypeString):
    """The bar-style type represents barline style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy, heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd and 4th lines), and none."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="bar-style">
    <xs:annotation>
        <xs:documentation>The bar-style type represents barline style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy, heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd and 4th lines), and none.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="regular" />
        <xs:enumeration value="dotted" />
        <xs:enumeration value="dashed" />
        <xs:enumeration value="heavy" />
        <xs:enumeration value="light-light" />
        <xs:enumeration value="light-heavy" />
        <xs:enumeration value="heavy-light" />
        <xs:enumeration value="heavy-heavy" />
        <xs:enumeration value="tick" />
        <xs:enumeration value="short" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeEndingNumber(XSDSimpleTypeToken):
    """The ending-number type is used to specify either a comma-separated list of positive integers without leading zeros, or a string of zero or more spaces. It is used for the number attribute of the ending element. The zero or more spaces version is used when software knows that an ending is present, but cannot determine the type of the ending."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="ending-number">
    <xs:annotation>
        <xs:documentation>The ending-number type is used to specify either a comma-separated list of positive integers without leading zeros, or a string of zero or more spaces. It is used for the number attribute of the ending element. The zero or more spaces version is used when software knows that an ending is present, but cannot determine the type of the ending.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:pattern value="([ ]*)|([1-9][0-9]*(, ?[1-9][0-9]*)*)" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeRightLeftMiddle(XSDSimpleTypeToken):
    """The right-left-middle type is used to specify barline location."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="right-left-middle">
    <xs:annotation>
        <xs:documentation>The right-left-middle type is used to specify barline location.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="right" />
        <xs:enumeration value="left" />
        <xs:enumeration value="middle" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartStopDiscontinue(XSDSimpleTypeToken):
    """The start-stop-discontinue type is used to specify ending types. Typically, the start type is associated with the left barline of the first measure in an ending. The stop and discontinue types are associated with the right barline of the last measure in an ending. Stop is used when the ending mark concludes with a downward jog, as is typical for first endings. Discontinue is used when there is no downward jog, as is typical for second endings that do not conclude a piece."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-stop-discontinue">
    <xs:annotation>
        <xs:documentation>The start-stop-discontinue type is used to specify ending types. Typically, the start type is associated with the left barline of the first measure in an ending. The stop and discontinue types are associated with the right barline of the last measure in an ending. Stop is used when the ending mark concludes with a downward jog, as is typical for first endings. Discontinue is used when there is no downward jog, as is typical for second endings that do not conclude a piece.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="discontinue" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeWinged(XSDSimpleTypeToken):
    """The winged attribute indicates whether the repeat has winged extensions that appear above and below the barline. The straight and curved values represent single wings, while the double-straight and double-curved values represent double wings. The none value indicates no wings and is the default."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="winged">
    <xs:annotation>
        <xs:documentation>The winged attribute indicates whether the repeat has winged extensions that appear above and below the barline. The straight and curved values represent single wings, while the double-straight and double-curved values represent double wings. The none value indicates no wings and is the default.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="none" />
        <xs:enumeration value="straight" />
        <xs:enumeration value="curved" />
        <xs:enumeration value="double-straight" />
        <xs:enumeration value="double-curved" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeAccordionMiddle(XSDSimpleTypePositiveInteger):
    """The accordion-middle type may have values of 1, 2, or 3, corresponding to having 1 to 3 dots in the middle section of the accordion registration symbol. This type is not used if no dots are present."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="accordion-middle">
    <xs:annotation>
        <xs:documentation>The accordion-middle type may have values of 1, 2, or 3, corresponding to having 1 to 3 dots in the middle section of the accordion registration symbol. This type is not used if no dots are present.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:positiveInteger">
        <xs:minInclusive value="1" />
        <xs:maxInclusive value="3" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBeaterValue(XSDSimpleTypeString):
    """The beater-value type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram. The finger and hammer values are in addition to Stone's list."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="beater-value">
    <xs:annotation>
        <xs:documentation>The beater-value type represents pictograms for beaters, mallets, and sticks that do not have different materials represented in the pictogram. The finger and hammer values are in addition to Stone's list.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="bow" />
        <xs:enumeration value="chime hammer" />
        <xs:enumeration value="coin" />
        <xs:enumeration value="drum stick" />
        <xs:enumeration value="finger" />
        <xs:enumeration value="fingernail" />
        <xs:enumeration value="fist" />
        <xs:enumeration value="guiro scraper" />
        <xs:enumeration value="hammer" />
        <xs:enumeration value="hand" />
        <xs:enumeration value="jazz stick" />
        <xs:enumeration value="knitting needle" />
        <xs:enumeration value="metal hammer" />
        <xs:enumeration value="slide brush on gong" />
        <xs:enumeration value="snare stick" />
        <xs:enumeration value="spoon mallet" />
        <xs:enumeration value="superball" />
        <xs:enumeration value="triangle beater" />
        <xs:enumeration value="triangle beater plain" />
        <xs:enumeration value="wire brush" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeDegreeSymbolValue(XSDSimpleTypeToken):
    """The degree-symbol-value type indicates which symbol should be used in specifying a degree."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="degree-symbol-value">
    <xs:annotation>
        <xs:documentation>The degree-symbol-value type indicates which symbol should be used in specifying a degree.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="major" />
        <xs:enumeration value="minor" />
        <xs:enumeration value="augmented" />
        <xs:enumeration value="diminished" />
        <xs:enumeration value="half-diminished" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeDegreeTypeValue(XSDSimpleTypeString):
    """The degree-type-value type indicates whether the current degree element is an addition, alteration, or subtraction to the kind of the current chord in the harmony element."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="degree-type-value">
    <xs:annotation>
        <xs:documentation>The degree-type-value type indicates whether the current degree element is an addition, alteration, or subtraction to the kind of the current chord in the harmony element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="add" />
        <xs:enumeration value="alter" />
        <xs:enumeration value="subtract" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeEffectValue(XSDSimpleTypeString):
    """The effect-value type represents pictograms for sound effect percussion instruments. The cannon, lotus flute, and megaphone values are in addition to Stone's list."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="effect-value">
    <xs:annotation>
        <xs:documentation>The effect-value type represents pictograms for sound effect percussion instruments. The cannon, lotus flute, and megaphone values are in addition to Stone's list.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="anvil" />
        <xs:enumeration value="auto horn" />
        <xs:enumeration value="bird whistle" />
        <xs:enumeration value="cannon" />
        <xs:enumeration value="duck call" />
        <xs:enumeration value="gun shot" />
        <xs:enumeration value="klaxon horn" />
        <xs:enumeration value="lions roar" />
        <xs:enumeration value="lotus flute" />
        <xs:enumeration value="megaphone" />
        <xs:enumeration value="police whistle" />
        <xs:enumeration value="siren" />
        <xs:enumeration value="slide whistle" />
        <xs:enumeration value="thunder sheet" />
        <xs:enumeration value="wind machine" />
        <xs:enumeration value="wind whistle" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeGlassValue(XSDSimpleTypeString):
    """The glass-value type represents pictograms for glass percussion instruments."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="glass-value">
    <xs:annotation>
        <xs:documentation>The glass-value type represents pictograms for glass percussion instruments.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="glass harmonica" />
        <xs:enumeration value="glass harp" />
        <xs:enumeration value="wind chimes" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHarmonyArrangement(XSDSimpleTypeToken):
    """The harmony-arrangement type indicates how stacked chords and bass notes are displayed within a harmony element. The vertical value specifies that the second element appears below the first. The horizontal value specifies that the second element appears to the right of the first. The diagonal value specifies that the second element appears both below and to the right of the first."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="harmony-arrangement">
    <xs:annotation>
        <xs:documentation>The harmony-arrangement type indicates how stacked chords and bass notes are displayed within a harmony element. The vertical value specifies that the second element appears below the first. The horizontal value specifies that the second element appears to the right of the first. The diagonal value specifies that the second element appears both below and to the right of the first.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="vertical" />
        <xs:enumeration value="horizontal" />
        <xs:enumeration value="diagonal" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHarmonyType(XSDSimpleTypeToken):
    """The harmony-type type differentiates different types of harmonies when alternate harmonies are possible. Explicit harmonies have all note present in the music; implied have some notes missing but implied; alternate represents alternate analyses."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="harmony-type">
    <xs:annotation>
        <xs:documentation>The harmony-type type differentiates different types of harmonies when alternate harmonies are possible. Explicit harmonies have all note present in the music; implied have some notes missing but implied; alternate represents alternate analyses.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="explicit" />
        <xs:enumeration value="implied" />
        <xs:enumeration value="alternate" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeKindValue(XSDSimpleTypeString):
    """A kind-value indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points. Values include:

Triads:
    major (major third, perfect fifth)
    minor (minor third, perfect fifth)
    augmented (major third, augmented fifth)
    diminished (minor third, diminished fifth)
Sevenths:
    dominant (major triad, minor seventh)
    major-seventh (major triad, major seventh)
    minor-seventh (minor triad, minor seventh)
    diminished-seventh (diminished triad, diminished seventh)
    augmented-seventh (augmented triad, minor seventh)
    half-diminished (diminished triad, minor seventh)
    major-minor (minor triad, major seventh)
Sixths:
    major-sixth (major triad, added sixth)
    minor-sixth (minor triad, added sixth)
Ninths:
    dominant-ninth (dominant-seventh, major ninth)
    major-ninth (major-seventh, major ninth)
    minor-ninth (minor-seventh, major ninth)
11ths (usually as the basis for alteration):
    dominant-11th (dominant-ninth, perfect 11th)
    major-11th (major-ninth, perfect 11th)
    minor-11th (minor-ninth, perfect 11th)
13ths (usually as the basis for alteration):
    dominant-13th (dominant-11th, major 13th)
    major-13th (major-11th, major 13th)
    minor-13th (minor-11th, major 13th)
Suspended:
    suspended-second (major second, perfect fifth)
    suspended-fourth (perfect fourth, perfect fifth)
Functional sixths:
    Neapolitan
    Italian
    French
    German
Other:
    pedal (pedal-point bass)
    power (perfect fifth)
    Tristan

The "other" kind is used when the harmony is entirely composed of add elements.

The "none" kind is used to explicitly encode absence of chords or functional harmony. In this case, the root, numeral, or function element has no meaning. When using the root or numeral element, the root-step or numeral-step text attribute should be set to the empty string to keep the root or numeral from being displayed."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="kind-value">
    <xs:annotation>
        <xs:documentation>A kind-value indicates the type of chord. Degree elements can then add, subtract, or alter from these starting points. Values include:

Triads:
    major (major third, perfect fifth)
    minor (minor third, perfect fifth)
    augmented (major third, augmented fifth)
    diminished (minor third, diminished fifth)
Sevenths:
    dominant (major triad, minor seventh)
    major-seventh (major triad, major seventh)
    minor-seventh (minor triad, minor seventh)
    diminished-seventh (diminished triad, diminished seventh)
    augmented-seventh (augmented triad, minor seventh)
    half-diminished (diminished triad, minor seventh)
    major-minor (minor triad, major seventh)
Sixths:
    major-sixth (major triad, added sixth)
    minor-sixth (minor triad, added sixth)
Ninths:
    dominant-ninth (dominant-seventh, major ninth)
    major-ninth (major-seventh, major ninth)
    minor-ninth (minor-seventh, major ninth)
11ths (usually as the basis for alteration):
    dominant-11th (dominant-ninth, perfect 11th)
    major-11th (major-ninth, perfect 11th)
    minor-11th (minor-ninth, perfect 11th)
13ths (usually as the basis for alteration):
    dominant-13th (dominant-11th, major 13th)
    major-13th (major-11th, major 13th)
    minor-13th (minor-11th, major 13th)
Suspended:
    suspended-second (major second, perfect fifth)
    suspended-fourth (perfect fourth, perfect fifth)
Functional sixths:
    Neapolitan
    Italian
    French
    German
Other:
    pedal (pedal-point bass)
    power (perfect fifth)
    Tristan

The "other" kind is used when the harmony is entirely composed of add elements.

The "none" kind is used to explicitly encode absence of chords or functional harmony. In this case, the root, numeral, or function element has no meaning. When using the root or numeral element, the root-step or numeral-step text attribute should be set to the empty string to keep the root or numeral from being displayed.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="major" />
        <xs:enumeration value="minor" />
        <xs:enumeration value="augmented" />
        <xs:enumeration value="diminished" />
        <xs:enumeration value="dominant" />
        <xs:enumeration value="major-seventh" />
        <xs:enumeration value="minor-seventh" />
        <xs:enumeration value="diminished-seventh" />
        <xs:enumeration value="augmented-seventh" />
        <xs:enumeration value="half-diminished" />
        <xs:enumeration value="major-minor" />
        <xs:enumeration value="major-sixth" />
        <xs:enumeration value="minor-sixth" />
        <xs:enumeration value="dominant-ninth" />
        <xs:enumeration value="major-ninth" />
        <xs:enumeration value="minor-ninth" />
        <xs:enumeration value="dominant-11th" />
        <xs:enumeration value="major-11th" />
        <xs:enumeration value="minor-11th" />
        <xs:enumeration value="dominant-13th" />
        <xs:enumeration value="major-13th" />
        <xs:enumeration value="minor-13th" />
        <xs:enumeration value="suspended-second" />
        <xs:enumeration value="suspended-fourth" />
        <xs:enumeration value="Neapolitan" />
        <xs:enumeration value="Italian" />
        <xs:enumeration value="French" />
        <xs:enumeration value="German" />
        <xs:enumeration value="pedal" />
        <xs:enumeration value="power" />
        <xs:enumeration value="Tristan" />
        <xs:enumeration value="other" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLineEnd(XSDSimpleTypeToken):
    """The line-end type specifies if there is a jog up or down (or both), an arrow, or nothing at the start or end of a bracket."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-end">
    <xs:annotation>
        <xs:documentation>The line-end type specifies if there is a jog up or down (or both), an arrow, or nothing at the start or end of a bracket.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="up" />
        <xs:enumeration value="down" />
        <xs:enumeration value="both" />
        <xs:enumeration value="arrow" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMeasureNumberingValue(XSDSimpleTypeToken):
    """The measure-numbering-value type describes how measure numbers are displayed on this part: no numbers, numbers every measure, or numbers every system."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="measure-numbering-value">
    <xs:annotation>
        <xs:documentation>The measure-numbering-value type describes how measure numbers are displayed on this part: no numbers, numbers every measure, or numbers every system.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="none" />
        <xs:enumeration value="measure" />
        <xs:enumeration value="system" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMembraneValue(XSDSimpleTypeString):
    """The membrane-value type represents pictograms for membrane percussion instruments."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="membrane-value">
    <xs:annotation>
        <xs:documentation>The membrane-value type represents pictograms for membrane percussion instruments.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="bass drum" />
        <xs:enumeration value="bass drum on side" />
        <xs:enumeration value="bongos" />
        <xs:enumeration value="Chinese tomtom" />
        <xs:enumeration value="conga drum" />
        <xs:enumeration value="cuica" />
        <xs:enumeration value="goblet drum" />
        <xs:enumeration value="Indo-American tomtom" />
        <xs:enumeration value="Japanese tomtom" />
        <xs:enumeration value="military drum" />
        <xs:enumeration value="snare drum" />
        <xs:enumeration value="snare drum snares off" />
        <xs:enumeration value="tabla" />
        <xs:enumeration value="tambourine" />
        <xs:enumeration value="tenor drum" />
        <xs:enumeration value="timbales" />
        <xs:enumeration value="tomtom" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMetalValue(XSDSimpleTypeString):
    """The metal-value type represents pictograms for metal percussion instruments. The hi-hat value refers to a pictogram like Stone's high-hat cymbals but without the long vertical line at the bottom."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="metal-value">
    <xs:annotation>
        <xs:documentation>The metal-value type represents pictograms for metal percussion instruments. The hi-hat value refers to a pictogram like Stone's high-hat cymbals but without the long vertical line at the bottom.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="agogo" />
        <xs:enumeration value="almglocken" />
        <xs:enumeration value="bell" />
        <xs:enumeration value="bell plate" />
        <xs:enumeration value="bell tree" />
        <xs:enumeration value="brake drum" />
        <xs:enumeration value="cencerro" />
        <xs:enumeration value="chain rattle" />
        <xs:enumeration value="Chinese cymbal" />
        <xs:enumeration value="cowbell" />
        <xs:enumeration value="crash cymbals" />
        <xs:enumeration value="crotale" />
        <xs:enumeration value="cymbal tongs" />
        <xs:enumeration value="domed gong" />
        <xs:enumeration value="finger cymbals" />
        <xs:enumeration value="flexatone" />
        <xs:enumeration value="gong" />
        <xs:enumeration value="hi-hat" />
        <xs:enumeration value="high-hat cymbals" />
        <xs:enumeration value="handbell" />
        <xs:enumeration value="jaw harp" />
        <xs:enumeration value="jingle bells" />
        <xs:enumeration value="musical saw" />
        <xs:enumeration value="shell bells" />
        <xs:enumeration value="sistrum" />
        <xs:enumeration value="sizzle cymbal" />
        <xs:enumeration value="sleigh bells" />
        <xs:enumeration value="suspended cymbal" />
        <xs:enumeration value="tam tam" />
        <xs:enumeration value="tam tam with beater" />
        <xs:enumeration value="triangle" />
        <xs:enumeration value="Vietnamese hat" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMilliseconds(XSDSimpleTypeNonNegativeInteger):
    """The milliseconds type represents an integral number of milliseconds."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="milliseconds">
    <xs:annotation>
        <xs:documentation>The milliseconds type represents an integral number of milliseconds.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:nonNegativeInteger" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNumeralMode(XSDSimpleTypeString):
    """The numeral-mode type specifies the mode similar to the mode type, but with a restricted set of values. The different minor values are used to interpret numeral-root values of 6 and 7 when present in a minor key. The harmonic minor value sharpens the 7 and the melodic minor value sharpens both 6 and 7. If a minor mode is used without qualification, either in the mode or numeral-mode elements, natural minor is used."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="numeral-mode">
    <xs:annotation>
        <xs:documentation>The numeral-mode type specifies the mode similar to the mode type, but with a restricted set of values. The different minor values are used to interpret numeral-root values of 6 and 7 when present in a minor key. The harmonic minor value sharpens the 7 and the melodic minor value sharpens both 6 and 7. If a minor mode is used without qualification, either in the mode or numeral-mode elements, natural minor is used.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="major" />
        <xs:enumeration value="minor" />
        <xs:enumeration value="natural minor" />
        <xs:enumeration value="melodic minor" />
        <xs:enumeration value="harmonic minor" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeOnOff(XSDSimpleTypeToken):
    """The on-off type is used for notation elements such as string mutes."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="on-off">
    <xs:annotation>
        <xs:documentation>The on-off type is used for notation elements such as string mutes.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="on" />
        <xs:enumeration value="off" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePedalType(XSDSimpleTypeToken):
    """The pedal-type simple type is used to distinguish types of pedal directions. The start value indicates the start of a damper pedal, while the sostenuto value indicates the start of a sostenuto pedal. The other values can be used with either the damper or sostenuto pedal. The soft pedal is not included here because there is no special symbol or graphic used for it beyond what can be specified with words and bracket elements.

The change, continue, discontinue, and resume types are used when the line attribute is yes. The change type indicates a pedal lift and retake indicated with an inverted V marking. The continue type allows more precise formatting across system breaks and for more complex pedaling lines. The discontinue type indicates the end of a pedal line that does not include the explicit lift represented by the stop type. The resume type indicates the start of a pedal line that does not include the downstroke represented by the start type. It can be used when a line resumes after being discontinued, or to start a pedal line that is preceded by a text or symbol representation of the pedal."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="pedal-type">
    <xs:annotation>
        <xs:documentation>The pedal-type simple type is used to distinguish types of pedal directions. The start value indicates the start of a damper pedal, while the sostenuto value indicates the start of a sostenuto pedal. The other values can be used with either the damper or sostenuto pedal. The soft pedal is not included here because there is no special symbol or graphic used for it beyond what can be specified with words and bracket elements.

The change, continue, discontinue, and resume types are used when the line attribute is yes. The change type indicates a pedal lift and retake indicated with an inverted V marking. The continue type allows more precise formatting across system breaks and for more complex pedaling lines. The discontinue type indicates the end of a pedal line that does not include the explicit lift represented by the stop type. The resume type indicates the start of a pedal line that does not include the downstroke represented by the start type. It can be used when a line resumes after being discontinued, or to start a pedal line that is preceded by a text or symbol representation of the pedal.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="sostenuto" />
        <xs:enumeration value="change" />
        <xs:enumeration value="continue" />
        <xs:enumeration value="discontinue" />
        <xs:enumeration value="resume" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePitchedValue(XSDSimpleTypeString):
    """The pitched-value type represents pictograms for pitched percussion instruments. The chimes and tubular chimes values distinguish the single-line and double-line versions of the pictogram."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="pitched-value">
    <xs:annotation>
        <xs:documentation>The pitched-value type represents pictograms for pitched percussion instruments. The chimes and tubular chimes values distinguish the single-line and double-line versions of the pictogram.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="celesta" />
        <xs:enumeration value="chimes" />
        <xs:enumeration value="glockenspiel" />
        <xs:enumeration value="lithophone" />
        <xs:enumeration value="mallet" />
        <xs:enumeration value="marimba" />
        <xs:enumeration value="steel drums" />
        <xs:enumeration value="tubaphone" />
        <xs:enumeration value="tubular chimes" />
        <xs:enumeration value="vibraphone" />
        <xs:enumeration value="xylophone" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypePrincipalVoiceSymbol(XSDSimpleTypeString):
    """The principal-voice-symbol type represents the type of symbol used to indicate a principal or secondary voice. The "plain" value represents a plain square bracket. The value of "none" is used for analysis markup when the principal-voice element does not have a corresponding appearance in the score."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="principal-voice-symbol">
    <xs:annotation>
        <xs:documentation>The principal-voice-symbol type represents the type of symbol used to indicate a principal or secondary voice. The "plain" value represents a plain square bracket. The value of "none" is used for analysis markup when the principal-voice element does not have a corresponding appearance in the score.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="Hauptstimme" />
        <xs:enumeration value="Nebenstimme" />
        <xs:enumeration value="plain" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStaffDivideSymbol(XSDSimpleTypeToken):
    """The staff-divide-symbol type is used for staff division symbols. The down, up, and up-down values correspond to SMuFL code points U+E00B, U+E00C, and U+E00D respectively."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff-divide-symbol">
    <xs:annotation>
        <xs:documentation>The staff-divide-symbol type is used for staff division symbols. The down, up, and up-down values correspond to SMuFL code points U+E00B, U+E00C, and U+E00D respectively.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="down" />
        <xs:enumeration value="up" />
        <xs:enumeration value="up-down" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStartStopChangeContinue(XSDSimpleTypeToken):
    """The start-stop-change-continue type is used to distinguish types of pedal directions."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="start-stop-change-continue">
    <xs:annotation>
        <xs:documentation>The start-stop-change-continue type is used to distinguish types of pedal directions.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="start" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="change" />
        <xs:enumeration value="continue" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSyncType(XSDSimpleTypeToken):
    """The sync-type type specifies the style that a score following application should use to synchronize an accompaniment with a performer. The none type indicates no synchronization to the performer. The tempo type indicates synchronization based on the performer tempo rather than individual events in the score. The event type indicates synchronization by following the performance of individual events in the score rather than the performer tempo. The mostly-tempo and mostly-event types combine these two approaches, with mostly-tempo giving more weight to tempo and mostly-event giving more weight to performed events. The always-event type provides the strictest synchronization by not being forgiving of missing performed events."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="sync-type">
    <xs:annotation>
        <xs:documentation>The sync-type type specifies the style that a score following application should use to synchronize an accompaniment with a performer. The none type indicates no synchronization to the performer. The tempo type indicates synchronization based on the performer tempo rather than individual events in the score. The event type indicates synchronization by following the performance of individual events in the score rather than the performer tempo. The mostly-tempo and mostly-event types combine these two approaches, with mostly-tempo giving more weight to tempo and mostly-event giving more weight to performed events. The always-event type provides the strictest synchronization by not being forgiving of missing performed events.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="none" />
        <xs:enumeration value="tempo" />
        <xs:enumeration value="mostly-tempo" />
        <xs:enumeration value="mostly-event" />
        <xs:enumeration value="event" />
        <xs:enumeration value="always-event" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSystemRelationNumber(XSDSimpleTypeString):
    """The system-relation-number type distinguishes measure numbers that are associated with a system rather than the particular part where the element appears. A value of only-top or only-bottom indicates that the number should appear only on the top or bottom part of the current system, respectively. A value of also-top or also-bottom indicates that the number should appear on both the current part and the top or bottom part of the current system, respectively. If these values appear in a score, when parts are created the number should only appear once in this part, not twice. A value of none indicates that the number is associated only with the current part, not with the system."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="system-relation-number">
    <xs:annotation>
        <xs:documentation>The system-relation-number type distinguishes measure numbers that are associated with a system rather than the particular part where the element appears. A value of only-top or only-bottom indicates that the number should appear only on the top or bottom part of the current system, respectively. A value of also-top or also-bottom indicates that the number should appear on both the current part and the top or bottom part of the current system, respectively. If these values appear in a score, when parts are created the number should only appear once in this part, not twice. A value of none indicates that the number is associated only with the current part, not with the system.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="only-top" />
        <xs:enumeration value="only-bottom" />
        <xs:enumeration value="also-top" />
        <xs:enumeration value="also-bottom" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSystemRelation(XSDSimpleTypeSystemRelationNumber):
    """The system-relation type distinguishes elements that are associated with a system rather than the particular part where the element appears. A value of only-top indicates that the element should appear only on the top part of the current system. A value of also-top indicates that the element should appear on both the current part and the top part of the current system. If this value appears in a score, when parts are created the element should only appear once in this part, not twice. A value of none indicates that the element is associated only with the current part, not with the system."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="system-relation">
    <xs:annotation>
        <xs:documentation>The system-relation type distinguishes elements that are associated with a system rather than the particular part where the element appears. A value of only-top indicates that the element should appear only on the top part of the current system. A value of also-top indicates that the element should appear on both the current part and the top part of the current system. If this value appears in a score, when parts are created the element should only appear once in this part, not twice. A value of none indicates that the element is associated only with the current part, not with the system.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="system-relation-number">
        <xs:enumeration value="only-top" />
        <xs:enumeration value="also-top" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTipDirection(XSDSimpleTypeString):
    """The tip-direction type represents the direction in which the tip of a stick or beater points, using Unicode arrow terminology."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tip-direction">
    <xs:annotation>
        <xs:documentation>The tip-direction type represents the direction in which the tip of a stick or beater points, using Unicode arrow terminology.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="up" />
        <xs:enumeration value="down" />
        <xs:enumeration value="left" />
        <xs:enumeration value="right" />
        <xs:enumeration value="northwest" />
        <xs:enumeration value="northeast" />
        <xs:enumeration value="southeast" />
        <xs:enumeration value="southwest" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStickLocation(XSDSimpleTypeString):
    """The stick-location type represents pictograms for the location of sticks, beaters, or mallets on cymbals, gongs, drums, and other instruments."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="stick-location">
    <xs:annotation>
        <xs:documentation>The stick-location type represents pictograms for the location of sticks, beaters, or mallets on cymbals, gongs, drums, and other instruments.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="center" />
        <xs:enumeration value="rim" />
        <xs:enumeration value="cymbal bell" />
        <xs:enumeration value="cymbal edge" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStickMaterial(XSDSimpleTypeString):
    """The stick-material type represents the material being displayed in a stick pictogram."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="stick-material">
    <xs:annotation>
        <xs:documentation>The stick-material type represents the material being displayed in a stick pictogram.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="soft" />
        <xs:enumeration value="medium" />
        <xs:enumeration value="hard" />
        <xs:enumeration value="shaded" />
        <xs:enumeration value="x" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStickType(XSDSimpleTypeString):
    """The stick-type type represents the shape of pictograms where the material in the stick, mallet, or beater is represented in the pictogram."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="stick-type">
    <xs:annotation>
        <xs:documentation>The stick-type type represents the shape of pictograms where the material in the stick, mallet, or beater is represented in the pictogram.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="bass drum" />
        <xs:enumeration value="double bass drum" />
        <xs:enumeration value="glockenspiel" />
        <xs:enumeration value="gum" />
        <xs:enumeration value="hammer" />
        <xs:enumeration value="superball" />
        <xs:enumeration value="timpani" />
        <xs:enumeration value="wound" />
        <xs:enumeration value="xylophone" />
        <xs:enumeration value="yarn" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeUpDownStopContinue(XSDSimpleTypeToken):
    """The up-down-stop-continue type is used for octave-shift elements, indicating the direction of the shift from their true pitched values because of printing difficulty."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="up-down-stop-continue">
    <xs:annotation>
        <xs:documentation>The up-down-stop-continue type is used for octave-shift elements, indicating the direction of the shift from their true pitched values because of printing difficulty.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="up" />
        <xs:enumeration value="down" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="continue" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeWedgeType(XSDSimpleTypeToken):
    """The wedge type is crescendo for the start of a wedge that is closed at the left side, diminuendo for the start of a wedge that is closed on the right side, and stop for the end of a wedge. The continue type is used for formatting wedges over a system break, or for other situations where a single wedge is divided into multiple segments."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="wedge-type">
    <xs:annotation>
        <xs:documentation>The wedge type is crescendo for the start of a wedge that is closed at the left side, diminuendo for the start of a wedge that is closed on the right side, and stop for the end of a wedge. The continue type is used for formatting wedges over a system break, or for other situations where a single wedge is divided into multiple segments.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="crescendo" />
        <xs:enumeration value="diminuendo" />
        <xs:enumeration value="stop" />
        <xs:enumeration value="continue" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeWoodValue(XSDSimpleTypeString):
    """The wood-value type represents pictograms for wood percussion instruments. The maraca and maracas values distinguish the one- and two-maraca versions of the pictogram."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="wood-value">
    <xs:annotation>
        <xs:documentation>The wood-value type represents pictograms for wood percussion instruments. The maraca and maracas values distinguish the one- and two-maraca versions of the pictogram.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="bamboo scraper" />
        <xs:enumeration value="board clapper" />
        <xs:enumeration value="cabasa" />
        <xs:enumeration value="castanets" />
        <xs:enumeration value="castanets with handle" />
        <xs:enumeration value="claves" />
        <xs:enumeration value="football rattle" />
        <xs:enumeration value="guiro" />
        <xs:enumeration value="log drum" />
        <xs:enumeration value="maraca" />
        <xs:enumeration value="maracas" />
        <xs:enumeration value="quijada" />
        <xs:enumeration value="rainstick" />
        <xs:enumeration value="ratchet" />
        <xs:enumeration value="reco-reco" />
        <xs:enumeration value="sandpaper blocks" />
        <xs:enumeration value="slit drum" />
        <xs:enumeration value="temple block" />
        <xs:enumeration value="vibraslap" />
        <xs:enumeration value="whip" />
        <xs:enumeration value="wood block" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeDistanceType(XSDSimpleTypeToken):
    """The distance-type defines what type of distance is being defined in a distance element. Values include beam and hyphen. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="distance-type">
    <xs:annotation>
        <xs:documentation>The distance-type defines what type of distance is being defined in a distance element. Values include beam and hyphen. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeGlyphType(XSDSimpleTypeToken):
    """The glyph-type defines what type of glyph is being defined in a glyph element. Values include quarter-rest, g-clef-ottava-bassa, c-clef, f-clef, percussion-clef, octave-shift-up-8, octave-shift-down-8, octave-shift-continue-8, octave-shift-down-15, octave-shift-up-15, octave-shift-continue-15, octave-shift-down-22, octave-shift-up-22, and octave-shift-continue-22. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.

A quarter-rest type specifies the glyph to use when a note has a rest element and a type value of quarter. The c-clef, f-clef, and percussion-clef types specify the glyph to use when a clef sign element value is C, F, or percussion respectively. The g-clef-ottava-bassa type specifies the glyph to use when a clef sign element value is G and the clef-octave-change element value is -1. The octave-shift types specify the glyph to use when an octave-shift type attribute value is up, down, or continue and the octave-shift size attribute value is 8, 15, or 22."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="glyph-type">
    <xs:annotation>
        <xs:documentation>The glyph-type defines what type of glyph is being defined in a glyph element. Values include quarter-rest, g-clef-ottava-bassa, c-clef, f-clef, percussion-clef, octave-shift-up-8, octave-shift-down-8, octave-shift-continue-8, octave-shift-down-15, octave-shift-up-15, octave-shift-continue-15, octave-shift-down-22, octave-shift-up-22, and octave-shift-continue-22. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.

A quarter-rest type specifies the glyph to use when a note has a rest element and a type value of quarter. The c-clef, f-clef, and percussion-clef types specify the glyph to use when a clef sign element value is C, F, or percussion respectively. The g-clef-ottava-bassa type specifies the glyph to use when a clef sign element value is G and the clef-octave-change element value is -1. The octave-shift types specify the glyph to use when an octave-shift type attribute value is up, down, or continue and the octave-shift size attribute value is 8, 15, or 22.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeLineWidthType(XSDSimpleTypeToken):
    """The line-width-type defines what type of line is being defined in a line-width element. Values include beam, bracket, dashes, enclosure, ending, extend, heavy barline, leger, light barline, octave shift, pedal, slur middle, slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="line-width-type">
    <xs:annotation>
        <xs:documentation>The line-width-type defines what type of line is being defined in a line-width element. Values include beam, bracket, dashes, enclosure, ending, extend, heavy barline, leger, light barline, octave shift, pedal, slur middle, slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge. This is left as a string so that other application-specific types can be defined, but it is made a separate type so that it can be redefined more strictly.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMarginType(XSDSimpleTypeToken):
    """The margin-type type specifies whether margins apply to even page, odd pages, or both."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="margin-type">
    <xs:annotation>
        <xs:documentation>The margin-type type specifies whether margins apply to even page, odd pages, or both.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="odd" />
        <xs:enumeration value="even" />
        <xs:enumeration value="both" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMillimeters(XSDSimpleTypeDecimal):
    """The millimeters type is a number representing millimeters. This is used in the scaling element to provide a default scaling from tenths to physical units."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="millimeters">
    <xs:annotation>
        <xs:documentation>The millimeters type is a number representing millimeters. This is used in the scaling element to provide a default scaling from tenths to physical units.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNoteSizeType(XSDSimpleTypeToken):
    """The note-size-type type indicates the type of note being defined by a note-size element. The grace-cue type is used for notes of grace-cue size. The grace type is used for notes of cue size that include a grace element. The cue type is used for all other notes with cue size, whether defined explicitly or implicitly via a cue element. The large type is used for notes of large size."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="note-size-type">
    <xs:annotation>
        <xs:documentation>The note-size-type type indicates the type of note being defined by a note-size element. The grace-cue type is used for notes of grace-cue size. The grace type is used for notes of cue size that include a grace element. The cue type is used for all other notes with cue size, whether defined explicitly or implicitly via a cue element. The large type is used for notes of large size.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="cue" />
        <xs:enumeration value="grace" />
        <xs:enumeration value="grace-cue" />
        <xs:enumeration value="large" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeAccidentalValue(XSDSimpleTypeString):
    """The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="accidental-value">
    <xs:annotation>
        <xs:documentation>The accidental-value type represents notated accidentals supported by MusicXML. In the MusicXML 2.0 DTD this was a string with values that could be included. The XSD strengthens the data typing to an enumerated list. The quarter- and three-quarters- accidentals are Tartini-style quarter-tone accidentals. The -down and -up accidentals are quarter-tone accidentals that include arrows pointing down or up. The slash- accidentals are used in Turkish classical music. The numbered sharp and flat accidentals are superscripted versions of the accidental signs, used in Turkish folk music. The sori and koron accidentals are microtonal sharp and flat accidentals used in Iranian and Persian music. The other accidental covers accidentals other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL accidental. The smufl attribute may be used with any accidental value to help specify the appearance of symbols that share the same MusicXML semantics.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="sharp" />
        <xs:enumeration value="natural" />
        <xs:enumeration value="flat" />
        <xs:enumeration value="double-sharp" />
        <xs:enumeration value="sharp-sharp" />
        <xs:enumeration value="flat-flat" />
        <xs:enumeration value="natural-sharp" />
        <xs:enumeration value="natural-flat" />
        <xs:enumeration value="quarter-flat" />
        <xs:enumeration value="quarter-sharp" />
        <xs:enumeration value="three-quarters-flat" />
        <xs:enumeration value="three-quarters-sharp" />
        <xs:enumeration value="sharp-down" />
        <xs:enumeration value="sharp-up" />
        <xs:enumeration value="natural-down" />
        <xs:enumeration value="natural-up" />
        <xs:enumeration value="flat-down" />
        <xs:enumeration value="flat-up" />
        <xs:enumeration value="double-sharp-down" />
        <xs:enumeration value="double-sharp-up" />
        <xs:enumeration value="flat-flat-down" />
        <xs:enumeration value="flat-flat-up" />
        <xs:enumeration value="arrow-down" />
        <xs:enumeration value="arrow-up" />
        <xs:enumeration value="triple-sharp" />
        <xs:enumeration value="triple-flat" />
        <xs:enumeration value="slash-quarter-sharp" />
        <xs:enumeration value="slash-sharp" />
        <xs:enumeration value="slash-flat" />
        <xs:enumeration value="double-slash-flat" />
        <xs:enumeration value="sharp-1" />
        <xs:enumeration value="sharp-2" />
        <xs:enumeration value="sharp-3" />
        <xs:enumeration value="sharp-5" />
        <xs:enumeration value="flat-1" />
        <xs:enumeration value="flat-2" />
        <xs:enumeration value="flat-3" />
        <xs:enumeration value="flat-4" />
        <xs:enumeration value="sori" />
        <xs:enumeration value="koron" />
        <xs:enumeration value="other" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeArrowDirection(XSDSimpleTypeString):
    """The arrow-direction type represents the direction in which an arrow points, using Unicode arrow terminology."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="arrow-direction">
    <xs:annotation>
        <xs:documentation>The arrow-direction type represents the direction in which an arrow points, using Unicode arrow terminology.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="left" />
        <xs:enumeration value="up" />
        <xs:enumeration value="right" />
        <xs:enumeration value="down" />
        <xs:enumeration value="northwest" />
        <xs:enumeration value="northeast" />
        <xs:enumeration value="southeast" />
        <xs:enumeration value="southwest" />
        <xs:enumeration value="left right" />
        <xs:enumeration value="up down" />
        <xs:enumeration value="northwest southeast" />
        <xs:enumeration value="northeast southwest" />
        <xs:enumeration value="other" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeArrowStyle(XSDSimpleTypeString):
    """The arrow-style type represents the style of an arrow, using Unicode arrow terminology. Filled and hollow arrows indicate polygonal single arrows. Paired arrows are duplicate single arrows in the same direction. Combined arrows apply to double direction arrows like left right, indicating that an arrow in one direction should be combined with an arrow in the other direction."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="arrow-style">
    <xs:annotation>
        <xs:documentation>The arrow-style type represents the style of an arrow, using Unicode arrow terminology. Filled and hollow arrows indicate polygonal single arrows. Paired arrows are duplicate single arrows in the same direction. Combined arrows apply to double direction arrows like left right, indicating that an arrow in one direction should be combined with an arrow in the other direction.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="single" />
        <xs:enumeration value="double" />
        <xs:enumeration value="filled" />
        <xs:enumeration value="hollow" />
        <xs:enumeration value="paired" />
        <xs:enumeration value="combined" />
        <xs:enumeration value="other" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBeamValue(XSDSimpleTypeString):
    """The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="beam-value">
    <xs:annotation>
        <xs:documentation>The beam-value type represents the type of beam associated with each of 8 beam levels (up to 1024th notes) available for each note.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="begin" />
        <xs:enumeration value="continue" />
        <xs:enumeration value="end" />
        <xs:enumeration value="forward hook" />
        <xs:enumeration value="backward hook" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBendShape(XSDSimpleTypeString):
    """The bend-shape type distinguishes between the angled bend symbols commonly used in standard notation and the curved bend symbols commonly used in both tablature and standard notation."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="bend-shape">
    <xs:annotation>
        <xs:documentation>The bend-shape type distinguishes between the angled bend symbols commonly used in standard notation and the curved bend symbols commonly used in both tablature and standard notation.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="angled" />
        <xs:enumeration value="curved" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeBreathMarkValue(XSDSimpleTypeString):
    """The breath-mark-value type represents the symbol used for a breath mark."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="breath-mark-value">
    <xs:annotation>
        <xs:documentation>The breath-mark-value type represents the symbol used for a breath mark.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="" />
        <xs:enumeration value="comma" />
        <xs:enumeration value="tick" />
        <xs:enumeration value="upbow" />
        <xs:enumeration value="salzedo" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeCaesuraValue(XSDSimpleTypeString):
    """The caesura-value type represents the shape of the caesura sign."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="caesura-value">
    <xs:annotation>
        <xs:documentation>The caesura-value type represents the shape of the caesura sign.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="normal" />
        <xs:enumeration value="thick" />
        <xs:enumeration value="short" />
        <xs:enumeration value="curved" />
        <xs:enumeration value="single" />
        <xs:enumeration value="" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeCircularArrow(XSDSimpleTypeString):
    """The circular-arrow type represents the direction in which a circular arrow points, using Unicode arrow terminology."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="circular-arrow">
    <xs:annotation>
        <xs:documentation>The circular-arrow type represents the direction in which a circular arrow points, using Unicode arrow terminology.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="clockwise" />
        <xs:enumeration value="anticlockwise" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFan(XSDSimpleTypeToken):
    """The fan type represents the type of beam fanning present on a note, used to represent accelerandos and ritardandos."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fan">
    <xs:annotation>
        <xs:documentation>The fan type represents the type of beam fanning present on a note, used to represent accelerandos and ritardandos.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="accel" />
        <xs:enumeration value="rit" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHandbellValue(XSDSimpleTypeString):
    """The handbell-value type represents the type of handbell technique being notated."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="handbell-value">
    <xs:annotation>
        <xs:documentation>The handbell-value type represents the type of handbell technique being notated.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="belltree" />
        <xs:enumeration value="damp" />
        <xs:enumeration value="echo" />
        <xs:enumeration value="gyro" />
        <xs:enumeration value="hand martellato" />
        <xs:enumeration value="mallet lift" />
        <xs:enumeration value="mallet table" />
        <xs:enumeration value="martellato" />
        <xs:enumeration value="martellato lift" />
        <xs:enumeration value="muted martellato" />
        <xs:enumeration value="pluck lift" />
        <xs:enumeration value="swing" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHarmonClosedLocation(XSDSimpleTypeString):
    """The harmon-closed-location type indicates which portion of the symbol is filled in when the corresponding harmon-closed-value is half."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="harmon-closed-location">
    <xs:annotation>
        <xs:documentation>The harmon-closed-location type indicates which portion of the symbol is filled in when the corresponding harmon-closed-value is half.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="right" />
        <xs:enumeration value="bottom" />
        <xs:enumeration value="left" />
        <xs:enumeration value="top" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHarmonClosedValue(XSDSimpleTypeString):
    """The harmon-closed-value type represents whether the harmon mute is closed, open, or half-open."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="harmon-closed-value">
    <xs:annotation>
        <xs:documentation>The harmon-closed-value type represents whether the harmon mute is closed, open, or half-open.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="yes" />
        <xs:enumeration value="no" />
        <xs:enumeration value="half" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHoleClosedLocation(XSDSimpleTypeString):
    """The hole-closed-location type indicates which portion of the hole is filled in when the corresponding hole-closed-value is half."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="hole-closed-location">
    <xs:annotation>
        <xs:documentation>The hole-closed-location type indicates which portion of the hole is filled in when the corresponding hole-closed-value is half.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="right" />
        <xs:enumeration value="bottom" />
        <xs:enumeration value="left" />
        <xs:enumeration value="top" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeHoleClosedValue(XSDSimpleTypeString):
    """The hole-closed-value type represents whether the hole is closed, open, or half-open."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="hole-closed-value">
    <xs:annotation>
        <xs:documentation>The hole-closed-value type represents whether the hole is closed, open, or half-open.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="yes" />
        <xs:enumeration value="no" />
        <xs:enumeration value="half" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNoteTypeValue(XSDSimpleTypeString):
    """The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest)."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="note-type-value">
    <xs:annotation>
        <xs:documentation>The note-type-value type is used for the MusicXML type element and represents the graphic note type, from 1024th (shortest) to maxima (longest).</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="1024th" />
        <xs:enumeration value="512th" />
        <xs:enumeration value="256th" />
        <xs:enumeration value="128th" />
        <xs:enumeration value="64th" />
        <xs:enumeration value="32nd" />
        <xs:enumeration value="16th" />
        <xs:enumeration value="eighth" />
        <xs:enumeration value="quarter" />
        <xs:enumeration value="half" />
        <xs:enumeration value="whole" />
        <xs:enumeration value="breve" />
        <xs:enumeration value="long" />
        <xs:enumeration value="maxima" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeNoteheadValue(XSDSimpleTypeString):
    """The notehead-value type indicates shapes other than the open and closed ovals associated with note durations. 

The values do, re, mi, fa, fa up, so, la, and ti correspond to Aikin's 7-shape system.  The fa up shape is typically used with upstems; the fa shape is typically used with downstems or no stems.

The arrow shapes differ from triangle and inverted triangle by being centered on the stem. Slashed and back slashed notes include both the normal notehead and a slash. The triangle shape has the tip of the triangle pointing up; the inverted triangle shape has the tip of the triangle pointing down. The left triangle shape is a right triangle with the hypotenuse facing up and to the left.

The other notehead covers noteheads other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL notehead. The smufl attribute may be used with any notehead value to help specify the appearance of symbols that share the same MusicXML semantics. Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="notehead-value">
    <xs:annotation>
        <xs:documentation>
The notehead-value type indicates shapes other than the open and closed ovals associated with note durations. 

The values do, re, mi, fa, fa up, so, la, and ti correspond to Aikin's 7-shape system.  The fa up shape is typically used with upstems; the fa shape is typically used with downstems or no stems.

The arrow shapes differ from triangle and inverted triangle by being centered on the stem. Slashed and back slashed notes include both the normal notehead and a slash. The triangle shape has the tip of the triangle pointing up; the inverted triangle shape has the tip of the triangle pointing down. The left triangle shape is a right triangle with the hypotenuse facing up and to the left.

The other notehead covers noteheads other than those listed here. It is usually used in combination with the smufl attribute to specify a particular SMuFL notehead. The smufl attribute may be used with any notehead value to help specify the appearance of symbols that share the same MusicXML semantics. Noteheads in the SMuFL Note name noteheads and Note name noteheads supplement ranges (U+E150–U+E1AF and U+EEE0–U+EEFF) should not use the smufl attribute or the "other" value, but instead use the notehead-text element.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="slash" />
        <xs:enumeration value="triangle" />
        <xs:enumeration value="diamond" />
        <xs:enumeration value="square" />
        <xs:enumeration value="cross" />
        <xs:enumeration value="x" />
        <xs:enumeration value="circle-x" />
        <xs:enumeration value="inverted triangle" />
        <xs:enumeration value="arrow down" />
        <xs:enumeration value="arrow up" />
        <xs:enumeration value="circled" />
        <xs:enumeration value="slashed" />
        <xs:enumeration value="back slashed" />
        <xs:enumeration value="normal" />
        <xs:enumeration value="cluster" />
        <xs:enumeration value="circle dot" />
        <xs:enumeration value="left triangle" />
        <xs:enumeration value="rectangle" />
        <xs:enumeration value="none" />
        <xs:enumeration value="do" />
        <xs:enumeration value="re" />
        <xs:enumeration value="mi" />
        <xs:enumeration value="fa" />
        <xs:enumeration value="fa up" />
        <xs:enumeration value="so" />
        <xs:enumeration value="la" />
        <xs:enumeration value="ti" />
        <xs:enumeration value="other" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeOctave(XSDSimpleTypeInteger):
    """Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="octave">
    <xs:annotation>
        <xs:documentation>Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:integer">
        <xs:minInclusive value="0" />
        <xs:maxInclusive value="9" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSemitones(XSDSimpleTypeDecimal):
    """The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="semitones">
    <xs:annotation>
        <xs:documentation>The semitones type is a number representing semitones, used for chromatic alteration. A value of -1 corresponds to a flat and a value of 1 to a sharp. Decimal values like 0.5 (quarter tone sharp) are used for microtones.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:decimal" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeShowTuplet(XSDSimpleTypeToken):
    """The show-tuplet type indicates whether to show a part of a tuplet relating to the tuplet-actual element, both the tuplet-actual and tuplet-normal elements, or neither."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="show-tuplet">
    <xs:annotation>
        <xs:documentation>The show-tuplet type indicates whether to show a part of a tuplet relating to the tuplet-actual element, both the tuplet-actual and tuplet-normal elements, or neither.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:enumeration value="actual" />
        <xs:enumeration value="both" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStemValue(XSDSimpleTypeString):
    """The stem-value type represents the notated stem direction."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="stem-value">
    <xs:annotation>
        <xs:documentation>The stem-value type represents the notated stem direction.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="down" />
        <xs:enumeration value="up" />
        <xs:enumeration value="double" />
        <xs:enumeration value="none" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeStep(XSDSimpleTypeString):
    """The step type represents a step of the diatonic scale, represented using the English letters A through G."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="step">
    <xs:annotation>
        <xs:documentation>The step type represents a step of the diatonic scale, represented using the English letters A through G.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="A" />
        <xs:enumeration value="B" />
        <xs:enumeration value="C" />
        <xs:enumeration value="D" />
        <xs:enumeration value="E" />
        <xs:enumeration value="F" />
        <xs:enumeration value="G" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSyllabic(XSDSimpleTypeString):
    """Lyric hyphenation is indicated by the syllabic type. The single, begin, end, and middle values represent single-syllable words, word-beginning syllables, word-ending syllables, and mid-word syllables, respectively."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="syllabic">
    <xs:annotation>
        <xs:documentation>Lyric hyphenation is indicated by the syllabic type. The single, begin, end, and middle values represent single-syllable words, word-beginning syllables, word-ending syllables, and mid-word syllables, respectively.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="single" />
        <xs:enumeration value="begin" />
        <xs:enumeration value="end" />
        <xs:enumeration value="middle" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTapHand(XSDSimpleTypeString):
    """The tap-hand type represents the symbol to use for a tap element. The left and right values refer to the SMuFL guitarLeftHandTapping and guitarRightHandTapping glyphs respectively."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tap-hand">
    <xs:annotation>
        <xs:documentation>The tap-hand type represents the symbol to use for a tap element. The left and right values refer to the SMuFL guitarLeftHandTapping and guitarRightHandTapping glyphs respectively.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="left" />
        <xs:enumeration value="right" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeTremoloMarks(XSDSimpleTypeInteger):
    """The number of tremolo marks is represented by a number from 0 to 8: the same as beam-level with 0 added."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tremolo-marks">
    <xs:annotation>
        <xs:documentation>The number of tremolo marks is represented by a number from 0 to 8: the same as beam-level with 0 added.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:integer">
        <xs:minInclusive value="0" />
        <xs:maxInclusive value="8" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeGroupBarlineValue(XSDSimpleTypeString):
    """The group-barline-value type indicates if the group should have common barlines."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="group-barline-value">
    <xs:annotation>
        <xs:documentation>The group-barline-value type indicates if the group should have common barlines.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="yes" />
        <xs:enumeration value="no" />
        <xs:enumeration value="Mensurstrich" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeGroupSymbolValue(XSDSimpleTypeString):
    """The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="group-symbol-value">
    <xs:annotation>
        <xs:documentation>The group-symbol-value type indicates how the symbol for a group or multi-staff part is indicated in the score.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:string">
        <xs:enumeration value="none" />
        <xs:enumeration value="brace" />
        <xs:enumeration value="line" />
        <xs:enumeration value="bracket" />
        <xs:enumeration value="square" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeMeasureText(XSDSimpleTypeToken):
    """The measure-text type is used for the text attribute of measure elements. It has at least one character. The implicit attribute of the measure element should be set to "yes" rather than setting the text attribute to an empty string."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="measure-text">
    <xs:annotation>
        <xs:documentation>The measure-text type is used for the text attribute of measure elements. It has at least one character. The implicit attribute of the measure element should be set to "yes" rather than setting the text attribute to an empty string.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="xs:token">
        <xs:minLength value="1" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeSwingTypeValue(XSDSimpleTypeNoteTypeValue):
    """The swing-type-value type specifies the note type, either eighth or 16th, to which the ratio defined in the swing element is applied."""
    
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="swing-type-value">
    <xs:annotation>
        <xs:documentation>The swing-type-value type specifies the note type, either eighth or 16th, to which the ratio defined in the swing element is applied.</xs:documentation>
    </xs:annotation>
    <xs:restriction base="note-type-value">
        <xs:enumeration value="16th" />
        <xs:enumeration value="eighth" />
    </xs:restriction>
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeFontSize(XSDSimpleType):
    _UNION = [XSDSimpleTypeCssFontSize, XSDSimpleTypeDecimal]
    """The font-size can be one of the CSS font sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric point size."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font-size">
    <xs:annotation>
        <xs:documentation>The font-size can be one of the CSS font sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric point size.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:decimal css-font-size" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeYesNoNumber(XSDSimpleType):
    _UNION = [XSDSimpleTypeYesNo, XSDSimpleTypeDecimal]
    """The yes-no-number type is used for attributes that can be either boolean or numeric values."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="yes-no-number">
    <xs:annotation>
        <xs:documentation>The yes-no-number type is used for attributes that can be either boolean or numeric values.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="yes-no xs:decimal" />
</xs:simpleType>
"""
                                     ))

class XSDSimpleTypePositiveIntegerOrEmpty(XSDSimpleTypePositiveInteger):
    """The positive-integer-or-empty values can be either a positive integer or an empty string."""
    _FORCED_PERMITTED = ['']
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="positive-integer-or-empty">
    <xs:annotation>
        <xs:documentation>The positive-integer-or-empty values can be either a positive integer or an empty string.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:positiveInteger">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:enumeration value="" />
            </xs:restriction>
        </xs:simpleType>
    </xs:union>
</xs:simpleType>
"""
                                     ))

    def __init__(self, value='', *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class XSDSimpleTypeNumberOrNormal(XSDSimpleTypeDecimal):
    """The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height and letter-spacing attributes."""
    _FORCED_PERMITTED = ['normal']
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="number-or-normal">
    <xs:annotation>
        <xs:documentation>The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height and letter-spacing attributes.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:decimal">
        <xs:simpleType>
            <xs:restriction base="xs:token">
                <xs:enumeration value="normal" />
            </xs:restriction>
        </xs:simpleType>
    </xs:union>
</xs:simpleType>
"""
                                     ))

__all__=['XSDSimpleType', 'XSDSimpleTypeInteger', 'XSDSimpleTypeNonNegativeInteger', 'XSDSimpleTypePositiveInteger', 'XSDSimpleTypeDecimal', 'XSDSimpleTypeString', 'XSDSimpleTypeToken', 'XSDSimpleTypeDate', 'XSDSimpleTypeNumberOrNormal', 'XSDSimpleTypePositiveIntegerOrEmpty', 'XSDSimpleTypeFontSize', 'XSDSimpleTypeYesNoNumber', 'XSDSimpleTypeNMTOKEN', 'XSDSimpleTypeName', 'XSDSimpleTypeNCName', 'XSDSimpleTypeID', 'XSDSimpleTypeIDREF', 'XSDSimpleTypeLanguage', 'XSDSimpleTypeAboveBelow', 'XSDSimpleTypeBeamLevel', 'XSDSimpleTypeColor', 'XSDSimpleTypeCommaSeparatedText', 'XSDSimpleTypeCssFontSize', 'XSDSimpleTypeDivisions', 'XSDSimpleTypeEnclosureShape', 'XSDSimpleTypeFermataShape', 'XSDSimpleTypeFontFamily', 'XSDSimpleTypeFontStyle', 'XSDSimpleTypeFontWeight', 'XSDSimpleTypeLeftCenterRight', 'XSDSimpleTypeLeftRight', 'XSDSimpleTypeLineLength', 'XSDSimpleTypeLineShape', 'XSDSimpleTypeLineType', 'XSDSimpleTypeMidi16', 'XSDSimpleTypeMidi128', 'XSDSimpleTypeMidi16384', 'XSDSimpleTypeMute', 'XSDSimpleTypeNonNegativeDecimal', 'XSDSimpleTypeNumberLevel', 'XSDSimpleTypeNumberOfLines', 'XSDSimpleTypeNumeralValue', 'XSDSimpleTypeOverUnder', 'XSDSimpleTypePercent', 'XSDSimpleTypePositiveDecimal', 'XSDSimpleTypePositiveDivisions', 'XSDSimpleTypeRotationDegrees', 'XSDSimpleTypeSemiPitched', 'XSDSimpleTypeSmuflGlyphName', 'XSDSimpleTypeSmuflAccidentalGlyphName', 'XSDSimpleTypeSmuflCodaGlyphName', 'XSDSimpleTypeSmuflLyricsGlyphName', 'XSDSimpleTypeSmuflPictogramGlyphName', 'XSDSimpleTypeSmuflSegnoGlyphName', 'XSDSimpleTypeSmuflWavyLineGlyphName', 'XSDSimpleTypeStartNote', 'XSDSimpleTypeStartStop', 'XSDSimpleTypeStartStopContinue', 'XSDSimpleTypeStartStopSingle', 'XSDSimpleTypeStringNumber', 'XSDSimpleTypeSymbolSize', 'XSDSimpleTypeTenths', 'XSDSimpleTypeTextDirection', 'XSDSimpleTypeTiedType', 'XSDSimpleTypeTimeOnly', 'XSDSimpleTypeTopBottom', 'XSDSimpleTypeTremoloType', 'XSDSimpleTypeTrillBeats', 'XSDSimpleTypeTrillStep', 'XSDSimpleTypeTwoNoteTurn', 'XSDSimpleTypeUpDown', 'XSDSimpleTypeUprightInverted', 'XSDSimpleTypeValign', 'XSDSimpleTypeValignImage', 'XSDSimpleTypeYesNo', 'XSDSimpleTypeYyyyMmDd', 'XSDSimpleTypeCancelLocation', 'XSDSimpleTypeClefSign', 'XSDSimpleTypeFifths', 'XSDSimpleTypeMode', 'XSDSimpleTypeShowFrets', 'XSDSimpleTypeStaffLine', 'XSDSimpleTypeStaffLinePosition', 'XSDSimpleTypeStaffNumber', 'XSDSimpleTypeStaffType', 'XSDSimpleTypeTimeRelation', 'XSDSimpleTypeTimeSeparator', 'XSDSimpleTypeTimeSymbol', 'XSDSimpleTypeBackwardForward', 'XSDSimpleTypeBarStyle', 'XSDSimpleTypeEndingNumber', 'XSDSimpleTypeRightLeftMiddle', 'XSDSimpleTypeStartStopDiscontinue', 'XSDSimpleTypeWinged', 'XSDSimpleTypeAccordionMiddle', 'XSDSimpleTypeBeaterValue', 'XSDSimpleTypeDegreeSymbolValue', 'XSDSimpleTypeDegreeTypeValue', 'XSDSimpleTypeEffectValue', 'XSDSimpleTypeGlassValue', 'XSDSimpleTypeHarmonyArrangement', 'XSDSimpleTypeHarmonyType', 'XSDSimpleTypeKindValue', 'XSDSimpleTypeLineEnd', 'XSDSimpleTypeMeasureNumberingValue', 'XSDSimpleTypeMembraneValue', 'XSDSimpleTypeMetalValue', 'XSDSimpleTypeMilliseconds', 'XSDSimpleTypeNumeralMode', 'XSDSimpleTypeOnOff', 'XSDSimpleTypePedalType', 'XSDSimpleTypePitchedValue', 'XSDSimpleTypePrincipalVoiceSymbol', 'XSDSimpleTypeStaffDivideSymbol', 'XSDSimpleTypeStartStopChangeContinue', 'XSDSimpleTypeSyncType', 'XSDSimpleTypeSystemRelationNumber', 'XSDSimpleTypeSystemRelation', 'XSDSimpleTypeTipDirection', 'XSDSimpleTypeStickLocation', 'XSDSimpleTypeStickMaterial', 'XSDSimpleTypeStickType', 'XSDSimpleTypeUpDownStopContinue', 'XSDSimpleTypeWedgeType', 'XSDSimpleTypeWoodValue', 'XSDSimpleTypeDistanceType', 'XSDSimpleTypeGlyphType', 'XSDSimpleTypeLineWidthType', 'XSDSimpleTypeMarginType', 'XSDSimpleTypeMillimeters', 'XSDSimpleTypeNoteSizeType', 'XSDSimpleTypeAccidentalValue', 'XSDSimpleTypeArrowDirection', 'XSDSimpleTypeArrowStyle', 'XSDSimpleTypeBeamValue', 'XSDSimpleTypeBendShape', 'XSDSimpleTypeBreathMarkValue', 'XSDSimpleTypeCaesuraValue', 'XSDSimpleTypeCircularArrow', 'XSDSimpleTypeFan', 'XSDSimpleTypeHandbellValue', 'XSDSimpleTypeHarmonClosedLocation', 'XSDSimpleTypeHarmonClosedValue', 'XSDSimpleTypeHoleClosedLocation', 'XSDSimpleTypeHoleClosedValue', 'XSDSimpleTypeNoteTypeValue', 'XSDSimpleTypeNoteheadValue', 'XSDSimpleTypeOctave', 'XSDSimpleTypeSemitones', 'XSDSimpleTypeShowTuplet', 'XSDSimpleTypeStemValue', 'XSDSimpleTypeStep', 'XSDSimpleTypeSyllabic', 'XSDSimpleTypeTapHand', 'XSDSimpleTypeTremoloMarks', 'XSDSimpleTypeGroupBarlineValue', 'XSDSimpleTypeGroupSymbolValue', 'XSDSimpleTypeMeasureText', 'XSDSimpleTypeSwingTypeValue']
