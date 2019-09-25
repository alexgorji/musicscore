from musicscore.musicxml.attributes.bendsound import BendSound
from musicscore.musicxml.attributes.dahsedformatting import DashedFormatting
from musicscore.musicxml.attributes.linetype import LineType
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import Empty
from musicscore.musicxml.types.simple_type import TypeStartStop, TypeNumberLevel


class ComplexTypeSlide(Empty, LineType, DashedFormatting, PrintStyle, BendSound, OptionalUniqueId):
    """Glissando and slide types both indicate rapidly moving from one pitch to the other so that individual notes are
    not discerned. The distinction is similar to that between NIFF's glissando and portamento elements. A slide is
    continuous between two notes and defaults to a solid line. The optional text for a is printed alongside the line."""

    def __init__(self, tag, type, number=1, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type
        self.number = number

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
