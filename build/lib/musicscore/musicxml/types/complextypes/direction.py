from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.attributes.directive import Directive
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.groups.common import EditorialVoiceDirection, Staff
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.directiontype import ComplexTypeDirectionType
from musicscore.musicxml.types.complextypes.offset import ComplexTypeOffset
from musicscore.musicxml.types.complextypes.sound import ComplexTypeSound


class DirectionType(ComplexTypeDirectionType):
    _TAG = 'direction-type'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Offset(ComplexTypeOffset):
    _TAG = 'offset'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Sound(ComplexTypeSound):
    _TAG = 'sound'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeDirection(ComplexType, Placement, Directive, OptionalUniqueId):
    """A direction is a musical indication that is not necessarily attached to a specific note. Two or more may be
    combined to indicate starts and stops of wedges, dashes, etc. For applications where a specific direction is indeed
    attached to a specific note, the direction element can be associated with the note element that follows it in score
    order that is not in a different voice.

    By default, a series of direction-type elements and a series of child elements of a direction-type within a single
    direction element follow one another in sequence visually. For a series of direction-type children, non-positional
    formatting attributes are carried over from the previous element by default."""

    _DTD = Sequence(
        Element(DirectionType, max_occurrence=None),
        Element(Offset, min_occurrence=0),
        GroupReference(EditorialVoiceDirection),
        GroupReference(Staff, min_occurrence=0),
        Element(Sound, min_occurrence=0)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
