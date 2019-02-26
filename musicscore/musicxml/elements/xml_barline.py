from musicscore.musicxml.attributes.barline import BarlineAttributes
from musicscore.musicxml.types.simple_type import BarStyleType
from musicscore.musicxml.elements.xml_element import XMLElement


class XMLBarStyle(XMLElement, BarStyleType):
    """Bar-style contains style information. Choices are regular, dotted, dashed, heavy, light-light, light-heavy,
    heavy-light, heavy-heavy, tick (a short stroke through the top line), short (a partial barline between the 2nd
    and 4th lines), and none.
    <!ELEMENT bar-style (#PCDATA)>
    <!ATTLIST bar-style
        %color;
    >
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='bar-style', value=value, *args, **kwargs)


class XMLBarline(XMLElement, BarlineAttributes):
    """If a barline is other than a normal single barline, it should be represented by a barline type that describes it.
    This includes information about repeats and multiple endings, as well as line style. Barline data is on the same
    level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise
    score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters. The two
    fermata elements allow for fermatas on both sides of the barline (the lower one inverted). If no location is
    specified, the right barline is the default.
    <!ELEMENT barline (bar-style?, %editorial;, wavy-line?, segno?, coda?, (fermata, fermata?)?, ending?, repeat?)>
    <!ATTLIST barline
        location (right | left | middle) "right"
        segno CDATA #IMPLIED
        coda CDATA #IMPLIED
        divisions CDATA #IMPLIED
        %optional-unique-id;
     >
    """
    _ATTRIBUTES = BarlineAttributes._ATTRIBUTES
    _CHILDREN_TYPES = [XMLBarStyle]
    _CHILDREN_ORDERED = True

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)
