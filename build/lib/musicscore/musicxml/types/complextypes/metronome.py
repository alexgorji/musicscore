from musicscore.dtd.dtd import Choice, Sequence, GroupReference, Element
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.leveldisplay import Parentheses
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.complextypes.timemodification import ComplexTypeTimeModification
from musicscore.musicxml.types.complextypes.tuplet import Bracket, ShowNumber
from musicscore.musicxml.types.simple_type import String, TypeNoteTypeValue, TypeBeamValue, TypeBeamLevel, TypeStartStop


class PerMinute(ComplexType, String, Font):
    """The per-minute type can be a number, or a text description including numbers. If a font is specified, it
    overrides the font specified for the overall metronome element. This allows separate specification of a music font
    for the beat-unit and a text font for the numeric value, in cases where a single metronome font is not used."""

    _TAG = 'per-minute'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class BeatUnit(XMLElement, TypeNoteTypeValue):
    """The beat-unit element indicates the graphical note type to use in a metronome mark."""

    _TAG = 'beat-unit'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class BeatUnitDot(Empty):
    """The beat-unit-dot element is used to specify any augmentation dots for a metronome mark note.."""

    _TAG = 'beat-unit'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


"""
The beat-unit group combines elements used repeatedly in the metronome element to specify a note within a metronome 
mark.
"""
GroupBeatUnit = Sequence(
    Element(BeatUnit),
    Element(BeatUnitDot, min_occurrence=0, max_occurrence=None)
)


class BeatUnitTied(ComplexType):
    """The beat-unit-tied type indicates a beat-unit within a metronome mark that is tied to the preceding beat-unit.
    This allows or two or more tied notes to be associated with a per-minute value in a metronome mark, whereas the
    metronome-tied element is restricted to metric relationship marks."""
    _TAG = 'beat-unit-tied'
    _DTD = GroupBeatUnit

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MetronomeArrows(Empty):
    """If the metronome-arrows element is present, it indicates that metric modulation arrows are displayed on both
    sides of the metronome mark."""

    _TAG = 'metronome-arrows'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MetronomeType(XMLElement, TypeNoteTypeValue):
    """The metronome-type element works like the type element in defining metric relationships."""

    _TAG = 'metronome-type'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class MetronomeDot(Empty):
    """The metronome-dot element works like the dot element in defining metric relationships."""

    _TAG = 'metronome-dot'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MetronomeBeam(ComplexType, TypeBeamValue):
    """The metronome-beam type works like the beam type in defining metric relationships, but does not include all the
    attributes available in the beam type."""

    _TAG = 'metronome-beam'

    def __init__(self, value=None, number=1, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeBeamLevel(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)


class MetronomeTied(ComplexType):
    """The metronome-tied indicates the presence of a tie within a metric relationship mark. As with the tied element,
    both the start and stop of the tie should be specified, in this case within separate metronome-note elements."""

    _TAG = 'metronome-tied'

    def __init__(self, type_='start', *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        self.type = type_

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


class MetronomeTuplet(ComplexTypeTimeModification, Bracket, ShowNumber):
    """The metronome-tuplet type uses the same element structure as the time-modification element along with some
    attributes from the tuplet element."""

    _TAG = 'metronome-tuplet'

    def __init__(self, type_='start', *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        self.type = type_

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


class MetronomeNote(ComplexType):
    """The metronome-note type defines the appearance of a note within a metric relationship mark."""
    _DTD = Sequence(
        Element(MetronomeType),
        Element(MetronomeDot, min_occurrence=0, max_occurrence=None),
        Element(MetronomeBeam, min_occurrence=0, max_occurrence=None),
        Element(MetronomeTied, min_occurrence=0),
        Element(MetronomeTuplet, min_occurrence=0)
    )
    _TAG = 'metronome-note'

    def __init__(self, args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MetronomeRelation(XMLElement, String):
    """The metronome-relation element describes the relationship symbol that goes between the two sets of
    metronome-note elements. The currently allowed value is equals, but this may expand in future versions. If the
    element is empty, the equals value is used."""

    _TAG = 'metronome-relation'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeMetronome(ComplexType, PrintStyleAlign, Justify, Parentheses, OptionalUniqueId):
    """
    The metronome type represents metronome marks and other metric relationships. The beat-unit group and per-minute
    element specify regular metronome marks. The metronome-note and metronome-relation elements allow for the
    specification of metric modulations and other metric relationships, such as swing tempo marks where two eighths are
    equated to a quarter note / eighth note triplet. Tied notes can be represented in both types of metronome marks by
    using the beat-unit-tied and metronome-tied elements. The parentheses attribute indicates whether or not to put
    the metronome mark in parentheses; its value is no if not specified.
    """
    _DTD = Choice(
        Sequence(
            GroupReference(GroupBeatUnit),
            Element(BeatUnitTied, min_occurrence=0, max_occurrence=None),
            Choice(
                Element(PerMinute),
                Sequence(
                    GroupReference(GroupBeatUnit),
                    Element(BeatUnitTied, min_occurrence=0, max_occurrence=None),
                )
            )
        ),
        Sequence(
            Element(MetronomeArrows, min_occurrence=0),
            Element(MetronomeNote, max_occurrence=None),
            Sequence(
                Element(MetronomeRelation),
                Element(MetronomeNote),
                min_occurrence=0
            )
        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
