import re

from musicxml.util.core import get_simple_type_all_base_classes, find_all_xsd_children, get_cleaned_token
from musicxml.util.helprervariables import name_character
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
import xml.etree.ElementTree as ET
from typing import Union, Any, Optional, cast


class XSDSimpleType(XSDTreeElement):
    """
    Parent Class for all SimpleType classes
    """
    _TYPES: list[type] = []
    _FORCED_PERMITTED: list[str] = []
    _PERMITTED: list[str] = []
    _PATTERN: Optional[str] = None

    def __init__(self, value: Any, *args, **kwargs):
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
                raise ValueError(f'{self.__class__.__name__}.value {v} must in {self._PERMITTED}')
        elif self._PATTERN:
            restriction = self.XSD_TREE.get_restriction()
            if restriction:
                if restriction.get_attributes()['base'] == 'xs:date':
                    XSDSimpleTypeDate(v)
                elif restriction.get_attributes()['base'] == 'xs:token':
                    v = XSDSimpleTypeToken(v).value
                elif restriction.get_attributes()['base'] == 'xs:smufl-glyph-name':
                    XSDSimpleTypeSmuflGlypyName(v)
            if re.compile(self._PATTERN).fullmatch(v) is None:
                raise ValueError(
                    f'{self.__class__.__name__}.value {v} must match the following pattern: {self._PATTERN}')
        else:
            restriction = self.XSD_TREE.get_restriction()
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
            raise TypeError(f"{self.__class__.__name__}'s value {value} can only be of types {[type_.__name__ for type_ in self._TYPES]} "
                            f"not {type(value).__name__}.")

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
        restriction = self.XSD_TREE.get_restriction()
        if restriction and restriction.get_children() and restriction.get_children()[0].tag == 'pattern':
            pattern = rf"{restriction.get_children()[0].get_attributes()['value']}"
            pattern = pattern.replace('\c', name_character)
            self._PATTERN = pattern

    def __repr__(self):
        return str(self.value)

    @classmethod
    def value_is_required(cls):
        return True


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


class XSDSimpleTypeNMTOKEN(XSDSimpleTypeToken):
    """
    Name Token supports at the moment only:
    [A-Z] | [a-z] | [À-Ö] | [Ø-ö] | [ø-ÿ]
    [0-9]
    '.' | '-' | '_' | ':'
    """
    XSD_TREE = XSDTree(ET.fromstring(
        """
        <xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="NMTOKEN" id="NMTOKEN">
            <xs:restriction base="xs:token">
                <xs:pattern value="\c+"/>
            </xs:restriction>
        </xs:simpleType>
        """
    ))

    _PATTERN = rf"({name_character})+"


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


xml_simple_type_class_names = ['XSDSimpleTypeInteger', 'XSDSimpleTypeNonNegativeInteger', 'XSDSimpleTypePositiveInteger',
                               'XSDSimpleTypeDecimal',
                               'XSDSimpleTypeString', 'XSDSimpleTypeString', 'XSDSimpleTypeToken', 'XSDSimpleTypeNMTOKEN',
                               'XSDSimpleTypeDate', ]
"""
Creating all XSDSimpleType classes
"""
for simple_type in find_all_xsd_children(tag='simpleType', root='1'):
    xsd_tree = XSDTree(simple_type)
    class_name = xsd_tree.xsd_element_class_name
    print('class_name', class_name)
    base_classes = f"({', '.join(get_simple_type_all_base_classes(xsd_tree))}, )"
    print('base_classes', base_classes)
    attributes = """
    {
    '__doc__': xsd_tree.get_doc(), 
    'XSD_TREE': xsd_tree
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_simple_type_class_names.append(class_name)

for simple_type in find_all_xsd_children(tag='simpleType', root='2'):
    xsd_tree = XSDTree(simple_type)
    class_name = xsd_tree.xsd_element_class_name
    base_classes = f"({', '.join(get_simple_type_all_base_classes(xsd_tree))}, )"
    attributes = """
    {
    '__doc__': xsd_tree.get_doc(),
    'XSD_TREE': xsd_tree
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xml_simple_type_class_names.append(class_name)

# __all__ = xml_simple_type_class_names
__all__ = ['XSDSimpleTypeInteger', 'XSDSimpleTypeNonNegativeInteger',
           'XSDSimpleTypePositiveInteger', 'XSDSimpleTypeDecimal',
           'XSDSimpleTypeString', 'XSDSimpleTypeString', 'XSDSimpleTypeToken',
           'XSDSimpleTypeNMTOKEN', 'XSDSimpleTypeDate', 'XSDSimpleTypeAboveBelow',
           'XSDSimpleTypeBeamLevel', 'XSDSimpleTypeColor', 'XSDSimpleTypeCommaSeparatedText',
           'XSDSimpleTypeCssFontSize', 'XSDSimpleTypeDivisions',
           'XSDSimpleTypeEnclosureShape', 'XSDSimpleTypeFermataShape',
           'XSDSimpleTypeFontFamily', 'XSDSimpleTypeFontSize', 'XSDSimpleTypeFontStyle',
           'XSDSimpleTypeFontWeight', 'XSDSimpleTypeLeftCenterRight',
           'XSDSimpleTypeLeftRight', 'XSDSimpleTypeLineLength', 'XSDSimpleTypeLineShape',
           'XSDSimpleTypeLineType', 'XSDSimpleTypeMidi16', 'XSDSimpleTypeMidi128',
           'XSDSimpleTypeMidi16384', 'XSDSimpleTypeMute', 'XSDSimpleTypeNonNegativeDecimal',
           'XSDSimpleTypeNumberLevel', 'XSDSimpleTypeNumberOfLines',
           'XSDSimpleTypeNumberOrNormal', 'XSDSimpleTypeNumeralValue',
           'XSDSimpleTypeOverUnder', 'XSDSimpleTypePercent', 'XSDSimpleTypePositiveDecimal',
           'XSDSimpleTypePositiveDivisions', 'XSDSimpleTypePositiveIntegerOrEmpty',
           'XSDSimpleTypeRotationDegrees', 'XSDSimpleTypeSemiPitched',
           'XSDSimpleTypeSmuflGlyphName', 'XSDSimpleTypeSmuflAccidentalGlyphName',
           'XSDSimpleTypeSmuflCodaGlyphName', 'XSDSimpleTypeSmuflLyricsGlyphName',
           'XSDSimpleTypeSmuflPictogramGlyphName', 'XSDSimpleTypeSmuflSegnoGlyphName',
           'XSDSimpleTypeSmuflWavyLineGlyphName', 'XSDSimpleTypeStartNote',
           'XSDSimpleTypeStartStop', 'XSDSimpleTypeStartStopContinue',
           'XSDSimpleTypeStartStopSingle', 'XSDSimpleTypeStringNumber',
           'XSDSimpleTypeSymbolSize', 'XSDSimpleTypeTenths', 'XSDSimpleTypeTextDirection',
           'XSDSimpleTypeTiedType', 'XSDSimpleTypeTimeOnly', 'XSDSimpleTypeTopBottom',
           'XSDSimpleTypeTremoloType', 'XSDSimpleTypeTrillBeats', 'XSDSimpleTypeTrillStep',
           'XSDSimpleTypeTwoNoteTurn', 'XSDSimpleTypeUpDown', 'XSDSimpleTypeUprightInverted',
           'XSDSimpleTypeValign', 'XSDSimpleTypeValignImage', 'XSDSimpleTypeYesNo',
           'XSDSimpleTypeYesNoNumber', 'XSDSimpleTypeYyyyMmDd',
           'XSDSimpleTypeCancelLocation', 'XSDSimpleTypeClefSign', 'XSDSimpleTypeFifths',
           'XSDSimpleTypeMode', 'XSDSimpleTypeShowFrets', 'XSDSimpleTypeStaffLine',
           'XSDSimpleTypeStaffLinePosition', 'XSDSimpleTypeStaffNumber',
           'XSDSimpleTypeStaffType', 'XSDSimpleTypeTimeRelation',
           'XSDSimpleTypeTimeSeparator', 'XSDSimpleTypeTimeSymbol',
           'XSDSimpleTypeBackwardForward', 'XSDSimpleTypeBarStyle',
           'XSDSimpleTypeEndingNumber', 'XSDSimpleTypeRightLeftMiddle',
           'XSDSimpleTypeStartStopDiscontinue', 'XSDSimpleTypeWinged',
           'XSDSimpleTypeAccordionMiddle', 'XSDSimpleTypeBeaterValue',
           'XSDSimpleTypeDegreeSymbolValue', 'XSDSimpleTypeDegreeTypeValue',
           'XSDSimpleTypeEffectValue', 'XSDSimpleTypeGlassValue',
           'XSDSimpleTypeHarmonyArrangement', 'XSDSimpleTypeHarmonyType',
           'XSDSimpleTypeKindValue', 'XSDSimpleTypeLineEnd',
           'XSDSimpleTypeMeasureNumberingValue', 'XSDSimpleTypeMembraneValue',
           'XSDSimpleTypeMetalValue', 'XSDSimpleTypeMilliseconds',
           'XSDSimpleTypeNumeralMode', 'XSDSimpleTypeOnOff', 'XSDSimpleTypePedalType',
           'XSDSimpleTypePitchedValue', 'XSDSimpleTypePrincipalVoiceSymbol',
           'XSDSimpleTypeStaffDivideSymbol', 'XSDSimpleTypeStartStopChangeContinue',
           'XSDSimpleTypeSyncType', 'XSDSimpleTypeSystemRelationNumber',
           'XSDSimpleTypeSystemRelation', 'XSDSimpleTypeTipDirection',
           'XSDSimpleTypeStickLocation', 'XSDSimpleTypeStickMaterial',
           'XSDSimpleTypeStickType', 'XSDSimpleTypeUpDownStopContinue',
           'XSDSimpleTypeWedgeType', 'XSDSimpleTypeWoodValue', 'XSDSimpleTypeDistanceType',
           'XSDSimpleTypeGlyphType', 'XSDSimpleTypeLineWidthType', 'XSDSimpleTypeMarginType',
           'XSDSimpleTypeMillimeters', 'XSDSimpleTypeNoteSizeType',
           'XSDSimpleTypeAccidentalValue', 'XSDSimpleTypeArrowDirection',
           'XSDSimpleTypeArrowStyle', 'XSDSimpleTypeBeamValue', 'XSDSimpleTypeBendShape',
           'XSDSimpleTypeBreathMarkValue', 'XSDSimpleTypeCaesuraValue',
           'XSDSimpleTypeCircularArrow', 'XSDSimpleTypeFan', 'XSDSimpleTypeHandbellValue',
           'XSDSimpleTypeHarmonClosedLocation', 'XSDSimpleTypeHarmonClosedValue',
           'XSDSimpleTypeHoleClosedLocation', 'XSDSimpleTypeHoleClosedValue',
           'XSDSimpleTypeNoteTypeValue', 'XSDSimpleTypeNoteheadValue', 'XSDSimpleTypeOctave',
           'XSDSimpleTypeSemitones', 'XSDSimpleTypeShowTuplet', 'XSDSimpleTypeStemValue',
           'XSDSimpleTypeStep', 'XSDSimpleTypeSyllabic', 'XSDSimpleTypeTapHand',
           'XSDSimpleTypeTremoloMarks', 'XSDSimpleTypeGroupBarlineValue',
           'XSDSimpleTypeGroupSymbolValue', 'XSDSimpleTypeMeasureText',
           'XSDSimpleTypeSwingTypeValue', 'XSDSimpleTypeName', 'XSDSimpleTypeNCName',
           'XSDSimpleTypeID', 'XSDSimpleTypeIDREF']
