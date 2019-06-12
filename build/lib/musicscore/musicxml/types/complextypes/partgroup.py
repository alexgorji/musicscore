from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class GroupName(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-name', *args, **kwargs)
        raise NotImplementedError('GroupName')


class GroupNameDisplay(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-name-display', *args, **kwargs)
        raise NotImplementedError('GroupNameDisplay')


class GroupAbbreviation(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-abbreviation', *args, **kwargs)
        raise NotImplementedError('GroupAbbreviation')


class GroupAbbreviationDisplay(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-abbreviation-display', *args, **kwargs)
        raise NotImplementedError('GroupAbbreviationDisplay')


class GroupSymbol(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-symbol', *args, **kwargs)
        raise NotImplementedError('GroupSymbol')


class GroupTime(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group-time', *args, **kwargs)
        raise NotImplementedError('GroupTime')


class ComplexTypePartGroup(ComplexType):
    """
    The part-group element indicates groupings of parts in the score, usually indicated by braces and brackets. Braces
    that are used for multi-staff parts should be defined in the attributes element for that part. The part-group start
    element appears before the first score-part in the group. The part-group stop element appears after the last
    score-part in the group.

    The number attribute is used to distinguish overlapping and nested part-groups, not the sequence of groups. As with
    parts, groups can have a name and abbreviation. Values for the child elements are ignored at the stop of a group.

    A part-group element is not needed for a single multi-staff part. By default, multi-staff parts include a brace
    symbol and (if appropriate given the bar-style) common barlines. The symbol formatting for a multi-staff part can
    be more fully specified using the part-symbol element.

		<xs:sequence>
			<xs:element name="group-name" type="group-name" minOccurs="0"/>
			<xs:element name="group-name-display" type="name-display" minOccurs="0">
				<xs:annotation>
					<xs:documentation>Formatting specified in the group-name-display element overrides formatting specified in the group-name element.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="group-abbreviation" type="group-name" minOccurs="0"/>
			<xs:element name="group-abbreviation-display" type="name-display" minOccurs="0">
				<xs:annotation>
					<xs:documentation>Formatting specified in the group-abbreviation-display element overrides formatting specified in the group-abbreviation element.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="group-symbol" type="group-symbol" minOccurs="0"/>
			<xs:element name="group-barline" type="group-barline" minOccurs="0"/>
			<xs:element name="group-time" type="empty" minOccurs="0">
				<xs:annotation>
					<xs:documentation>The group-time element indicates that the displayed time signatures should stretch across all parts and staves in the group.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:group ref="editorial"/>
		</xs:sequence>
		<xs:attribute name="type" type="start-stop" use="required"/>
		<xs:attribute name="number" type="xs:token" default="1"/>
	</xs:complexType>
    """
    _DTD = Sequence(
        Element(GroupName, min_occurrence=0),
        Element(GroupNameDisplay, min_occurrence=0),
        Element(GroupAbbreviation, min_occurrence=0),
        Element(GroupAbbreviationDisplay, min_occurrence=0),
        Element(GroupSymbol, min_occurrence=0),
        Element(GroupTime, min_occurrence=0),
        GroupReference(Editorial)

    )

    def __init__(self, type_, number=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = None
        self.type_ = type_
        self._number = None
        self.number = number
        raise NotImplementedError()