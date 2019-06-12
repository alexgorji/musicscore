from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, String
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class Smulf(AttributeAbstract):
    def __init__(self, smulf=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('smulf', smulf, 'SmulfLyricsGlyphName')


class ComplexTypeElision(ComplexType, String, Font, Color, Smulf):
    """
    The elision type represents an elision between lyric syllables. The text content specifies the symbol used to
    display the elision. Common values are a no-break space (Unicode 00A0), an underscore (Unicode 005F), or an undertie
    (Unicode 203F). If the text content is empty, the smufl attribute is used to specify the symbol to use. Its value
    is a SMuFL canonical glyph name that starts with lyrics. The SMuFL attribute is ignored if the elision glyph is
    already specified by the text content. If neither text content nor a smufl attribute are present, the elision
    glyph is application-specific.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
