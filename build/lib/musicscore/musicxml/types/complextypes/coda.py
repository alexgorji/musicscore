from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeSmuflCodaGlyphNameType


class ComplexTypeCoda(ComplexType, PrintStyleAlign, OptionalUniqueId):
    """The coda type is the visual indicator of a coda sign. The exact glyph can be specified with the smufl attribute.
    A sound element is also needed to guide playback applications reliably.
    		<xs:attribute name="smufl" type="smufl-coda-glyph-name"/>"""

    def __init__(self, tag, smufl=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.smufl = smufl

    @property
    def smufl(self):
        return self.get_attribute('smufl')

    @smufl.setter
    def smufl(self, value):
        if value is None:
            self.remove_attribute('smufl')
        else:
            TypeSmuflCodaGlyphNameType(value)
            self._ATTRIBUTES.insert(0, 'smufl')
            self.set_attribute('smufl', value)
