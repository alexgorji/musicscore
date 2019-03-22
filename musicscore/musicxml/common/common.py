from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.types.complextypes.formattedtext import ComplexTypeFormattedText
from musicscore.musicxml.types.complextypes.level import ComplexTypeLevel


class FootNote(ComplexTypeFormattedText):
    """
    The footnote element specifies editorial information that appears in footnotes in the printed score. It is defined
    within a group due to its multiple uses within the MusicXML schema.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='footnote', value=value, *args, **kwargs)


class Level(ComplexTypeLevel):
    """
    The level element specifies editorial information for different MusicXML elements. It is defined within a group due
    to its multiple uses within the MusicXML schema.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


"""
The editorial group specifies editorial information for a musical element.
"""
Editorial = Sequence(
    Element(FootNote, min_occurrence=0),
    Element(Level, min_occurrence=0)
)
