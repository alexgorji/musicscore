from musicscore.dtd.dtd import Sequence, Element, GroupReference, Choice
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, String
from musicscore.musicxml.elements.editorial import Editorial
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.basic_functions import is_empty
from musicscore.musicxml.attributes.part_name_text import PartNameText
from musicscore.musicxml.types.complex_type import ComplexType


class Work(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='work', *args, **kwargs)
        raise NotImplementedError('Work')


class MovementNumber(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='movement-number', *args, **kwargs)
        raise NotImplementedError('MovementNumber')


class MovementTitle(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='movement-title', *args, **kwargs)
        raise NotImplementedError('MovementTitle')


class Identification(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='identification', *args, **kwargs)
        raise NotImplementedError('Identification')


class Defaults(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='defaults', *args, **kwargs)
        raise NotImplementedError('Defaults')


class Credit(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='credit', *args, **kwargs)
        raise NotImplementedError('Credit')


class TypePartName(ComplexType, PartNameText):
    """
    The part-name type describes the name or abbreviation of a score-part element. Formatting attributes for the
    part-name element are deprecated in Version 2.0 in favor of the new part-name-display and part-abbreviation-display
    elements.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class PartName(TypePartName):

    def __init__(self, name, *args, **kwargs):
        super().__init__(tag='part-name', *args, **kwargs)
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self.name is None or is_empty(self.name):
            self.text = 'none'
        else:
            self.text = self.name


class PartNameDisplay(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-name-display', *args, **kwargs)
        raise NotImplementedError('PartNameDisplay')


class PartAbbreviation(TypePartName, String):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='part-abbreviation', value=value, *args, **kwargs)


class PartAbbreviationDisplay(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-abbreviation-display', *args, **kwargs)
        raise NotImplementedError('PartAbbreviationDisplay')


class Group(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group', *args, **kwargs)
        raise NotImplementedError('Group')


class ScoreInstrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='score-instrument', *args, **kwargs)
        raise NotImplementedError('ScoreInstrument')


class MidiDevice(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='midi-device', *args, **kwargs)
        raise NotImplementedError('MidiDevice')


class MidiInstrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='midi-instrument', *args, **kwargs)
        raise NotImplementedError('MidiInstrument')


class Id(AttributeAbstract):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('id', id, "ID")


class TypeScorePart(ComplexType, Id):
    """
    Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used
    when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port
    assignment for the given track or specific MIDI instruments. Initial midi-instrument assignments may be made here
    as well.
    """

    _DTD = Sequence(
        Element(Identification, min_occurrence=0),
        Element(PartName),
        Element(PartNameDisplay, min_occurrence=0),
        Element(PartAbbreviation, min_occurrence=0),
        Element(PartAbbreviationDisplay, min_occurrence=0),
        Element(Group, min_occurrence=0, max_occurrence=None),
        Element(ScoreInstrument, min_occurrence=0, max_occurrence=None),
        Sequence(
            Element(MidiDevice, min_occurrence=0),
            Element(MidiInstrument, min_occurrence=0),
            min_occurrence=0,
            max_occurrence=None)
    )

    def __init__(self, tag, id, *args, **kwargs):
        super().__init__(tag=tag, id=id, *args, **kwargs)


class ScorePart(TypeScorePart):
    """
    The score-part element is defined within a group due to its multiple uses within the part-list element.
    Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used
    when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port
    assignment for the given track. Initial midi-instrument assignments may be made here as well.
    """

    def __init__(self, id, *args, **kwargs):
        super().__init__(tag='score-part', id=id, *args, **kwargs)


ScorePartGroup = Sequence(
    Element(ScorePart)
)


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


class TypePartGroup(ComplexType):
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


class PartGroup(TypePartGroup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-group', *args, **kwargs)


PartGroupGroup = Sequence(
    Element(PartGroup)
)


class TypePartList(ComplexType):
    """
    The part-list identifies the different musical parts in this movement. Each part has an ID that is used later within
    the musical data. Since parts may be encoded separately and combined later, identification elements are present at
    both the score and score-part levels. There must be at least one score-part, combined as desired with part-group
    elements that indicate braces and brackets. Parts are ordered from top to bottom in a score based on the order in
    which they appear in the part-list.
    """
    _DTD = Sequence(
        GroupReference(PartGroupGroup, min_occurrence=0, max_occurrence=None),
        GroupReference(ScorePartGroup),
        Choice(
            GroupReference(PartGroupGroup),
            GroupReference(ScorePartGroup),
            min_occurrence=0, max_occurrence=None
        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class PartList(TypePartList):

    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-list', *args, **kwargs)


"""
The score-header group contains basic score metadata about the work and movement, score-wide defaults for layout and 
fonts, credits that appear on the first or following pages, and the part list.
"""
ScoreHeader = Sequence(
    Element(Work, min_occurrence=0),
    Element(MovementNumber, min_occurrence=0),
    Element(MovementTitle, min_occurrence=0),
    Element(Identification, min_occurrence=0),
    Element(Defaults, min_occurrence=0),
    Element(Credit, min_occurrence=0, max_occurrence=None),
    Element(PartList)
)
