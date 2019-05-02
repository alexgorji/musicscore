from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeDivisions


class Sound(AttributeAbstract):

    def __init__(self, sound=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('sound', sound, 'TypeYesNo')


class ComplexTypeOffset(ComplexType, TypeDivisions, Sound):
    """
    An offset is represented in terms of divisions, and indicates where the direction will appear relative to the
    current musical location. This affects the visual appearance of the direction. If the sound attribute is "yes", then
    the offset affects playback too. If the sound attribute is "no", then any sound associated with the direction takes
    effect at the current location. The sound attribute is "no" by default for compatibility with earlier versions of
    the MusicXML format. If an element within a direction includes a default-x attribute, the offset value will be
    ignored when determining the appearance of that element
    """

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
