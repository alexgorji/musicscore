from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, String
from musicscore.musicxml.attributes.leveldisplay import LevelDisplay
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class Reference(AttributeAbstract):
    def __init__(self, reference=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('reference', reference, 'TypeYesNo')


class ComplexTypeLevel(ComplexType, String, Reference, LevelDisplay):
    """The level type is used to specify editorial information for different MusicXML elements. If the reference
    attribute for the level element is yes, this indicates editorial information that is for display only and should
    not affect playback. For instance, a modern edition of older music may set reference="yes" on the attributes
    containing the music's original clef, key, and time signature. It is no by default.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
