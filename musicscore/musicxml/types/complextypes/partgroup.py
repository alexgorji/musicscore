from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.complextypes.groupbarline import ComplexTypeGroupBarline
from musicscore.musicxml.types.complextypes.groupname import ComplexTypeGroupName
from musicscore.musicxml.types.complextypes.groupsymbol import ComplexTypeGroupSymbol
from musicscore.musicxml.types.complextypes.namedisplay import ComplexTypeNameDisplay
from musicscore.musicxml.types.simple_type import TypeStartStop, Token


class GroupName(ComplexTypeGroupName):
    _TAG = 'group-name'

    def __init__(self, value='', *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class GroupNameDisplay(ComplexTypeNameDisplay):
    _TAG = 'group-name-display'
    """Formatting specified in the group-name-display element overrides formatting specified in the group-name 
    element."""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class GroupAbbreviation(ComplexTypeGroupName):
    _TAG = 'group-abbreviation'

    def __init__(self, value='', *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class GroupAbbreviationDisplay(ComplexTypeNameDisplay):
    """
    Formatting specified in the group-abbreviation-display element overrides formatting specified in the
    group-abbreviation element.
    """
    _TAG = 'group-abbreviation-display'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class GroupSymbol(ComplexTypeGroupSymbol):
    _TAG = 'group-symbol'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class GroupBarline(ComplexTypeGroupBarline):
    _TAG = 'group-barline'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class GroupTime(Empty):
    """The group-time element indicates that the displayed time signatures should stretch across all parts and
    staves in the group."""

    _TAG = 'group-time'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


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
    """
    _DTD = Sequence(
        Element(GroupName, min_occurrence=0),
        Element(GroupNameDisplay, min_occurrence=0),
        Element(GroupAbbreviation, min_occurrence=0),
        Element(GroupAbbreviationDisplay, min_occurrence=0),
        Element(GroupSymbol, min_occurrence=0),
        Element(GroupBarline, min_occurrence=0),
        Element(GroupTime, min_occurrence=0),
        GroupReference(Editorial)

    )
    _ATTRIBUTES = []

    def __init__(self, type, number='1', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = type
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeStartStop(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
