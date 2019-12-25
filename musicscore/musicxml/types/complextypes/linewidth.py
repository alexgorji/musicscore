from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeLineWidthType, TypeTenths


class ComplexTypeLineWidth(ComplexType, TypeTenths):
    """The line-width type indicates the width of a line type in tenths. The type attribute defines what type of line
    is being defined. Values include beam, bracket, dashes, enclosure, ending, extend, heavy barline, leger, light
    barline, octave shift, pedal, slur middle, slur tip, staff, stem, tie middle, tie tip, tuplet bracket, and wedge.
    The text content is expressed in tenths."""

    _ATTRIBUTES = []

    def __init__(self, tag, type, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeLineWidthType(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
