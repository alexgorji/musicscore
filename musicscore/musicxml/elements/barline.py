from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.barline import BarlineAttributes
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.common.common import Editorial
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeBarStyle
from musicscore.musicxml.elements.xml_element import XMLElement


class BarStyleColor(ComplexType, TypeBarStyle, Color):
    """
    The bar-style-color type contains barline style and color information.
    """

    def __init__(self, tag, value, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)


class BarStyle(BarStyleColor):
    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='bar-style', value=value, *args, **kwargs)


class WavyLine(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='wavy-line', *args, **kwargs)
        raise NotImplementedError('WavyLine')


class Segno(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='segno', *args, **kwargs)
        raise NotImplementedError('Segno')


class Coda(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='coda', *args, **kwargs)
        raise NotImplementedError()


class Fermata(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='fermata', *args, **kwargs)
        raise NotImplementedError('Fermata')


class Ending(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='ending', *args, **kwargs)
        raise NotImplementedError('Ending')


class Repeat(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='repeat', *args, **kwargs)
        raise NotImplementedError('Repeat')


class Barline(XMLElement, BarlineAttributes):
    """
    If a barline is other than a normal single barline, it should be represented by a barline type that describes it.
    This includes information about repeats and multiple endings, as well as line style. Barline data is on the same
    level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise
    score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters.
    The two fermata elements allow for fermatas on both sides of the barline (the lower one inverted).

 Barlines have a location attribute to make it easier to process barlines independently of the other musical data in a
 score. It is often easier to set up measures separately from entering notes. The location attribute must match where
 the barline element occurs within the rest of the musical data in the score. If location is left, it should be the
 first element in the measure, aside from the print, bookmark, and link elements. If location is right, it should be
 the last element, again with the possible exception of the print, bookmark, and link elements. If no location is
 specified, the right barline is the default. The segno, coda, and divisions attributes work the same way as in the
 sound element. They are used for playback when barline elements contain segno or coda child elements.
    """
    _DTD = Sequence(
        Element(BarStyle, min_occurrence=0),
        GroupReference(Editorial),
        Element(WavyLine, min_occurrence=0),
        Element(Segno, min_occurrence=0),
        Element(Coda, min_occurrence=0),
        Element(Fermata, min_occurrence=0, max_occurrence=2),
        Element(Ending, min_occurrence=0),
        Element(Repeat, min_occurrence=0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)
