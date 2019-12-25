"""
    <xs:complexType name="appearance">
        <xs:sequence>
            <xs:element name="line-width" type="line-width" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="note-size" type="note-size" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="distance" type="distance" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="glyph" type="glyph" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element name="other-appearance" type="other-appearance" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
"""
from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.distance import ComplexTypeDistance
from musicscore.musicxml.types.complextypes.glyph import ComplexTypeGlyph
from musicscore.musicxml.types.complextypes.linewidth import ComplexTypeLineWidth
from musicscore.musicxml.types.complextypes.notesize import ComplexTypeNoteSize
from musicscore.musicxml.types.complextypes.otherappearance import ComplexTypeOtherAppearance


class LineWidth(ComplexTypeLineWidth):
    """"""

    _TAG = 'line-width'

    def __init__(self, type, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class NoteSize(ComplexTypeNoteSize):
    """"""

    _TAG = 'note-size'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Distance(ComplexTypeDistance):
    """"""

    _TAG = 'distance'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Glyph(ComplexTypeGlyph):
    """"""

    _TAG = 'glyph'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OtherAppearance(ComplexTypeOtherAppearance):
    """"""

    _TAG = 'other-appearance'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeAppearance(ComplexType):
    """The appearance type controls general graphical settings for the music's final form appearance on a printed page
    of display. This includes support for line widths, definitions for note sizes, and standard distances between
    notation elements, plus an extension element for other aspects of appearance."""

    _DTD = Sequence(
        Element(LineWidth, 0, None),
        Element(NoteSize, 0, None),
        Element(Distance, 0, None),
        Element(Glyph, 0, None),
        Element(OtherAppearance, 0, None)

    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
