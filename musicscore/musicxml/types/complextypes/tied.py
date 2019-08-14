from musicscore.musicxml.attributes.bezier import Bezier
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.orientation import Orientation
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeTiedType, TypeNumberLevel


class ComplexTypeTied(ComplexType, LineType, DashedFormatting, Position, Placement, Orientation, Bezier, Color,
                      OptionalUniqueId):
    """
    The tied element represents the notated tie. The tie element represents the tie sound.
    The number attribute is rarely needed to disambiguate ties, since note pitches will usually suffice. The attribute
    is implied rather than defaulting to 1 as with most elements. It is available for use in more complex tied notation
    situations.
    Ties that join two notes of the same pitch together should be represented with a tied element on the first note with
    type="start" and a tied element on the second note with type="stop".  This can also be done if the two notes being
    tied are enharmonically equivalent, but have different step values. It is not recommended to use tied elements to
    join two notes with enharmonically inequivalent pitches.
    Ties that indicate that an instrument should be undamped are specified with a single tied element with
    type="let-ring".
    Ties that are visually attached to only one note, other than undamped ties, should be specified with two tied
    elements on the same note, first type="start" then type="stop". This can be used to represent ties into or out of
    repeated sections or codas.
    """

    def __init__(self, type, number=1, *args, **kwargs):
        super().__init__(tag='tied', *args, **kwargs)
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
            TypeNumberLevel(value)
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
            TypeTiedType(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
