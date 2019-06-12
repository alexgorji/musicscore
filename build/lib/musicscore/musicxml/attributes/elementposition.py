from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Element(AttributeAbstract):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('element', element, "Token")


class ElementPosition(Element, Position):
    """
    The element and position attributes are new as of Version 2.0. They allow for bookmarks and links to be positioned
    at higher resolution than the level of music-data elements. When no element and position attributes are present,
    the bookmark or link element refers to the next sibling element in the MusicXML file. The element attribute
    specifies an element type for a descendant of the next sibling element that is not a link or bookmark. The position
    attribute specifies the position of this descendant element, where the first position is 1. The position attribute
    is ignored if the element attribute is not present. For instance, an element value of "beam" and a position value
    of "2" defines the link or bookmark to refer to the second beam descendant of the next sibling element that is not
    a link or bookmark. This is equivalent to an XPath test of [.//beam[2]] done in the context of the sibling element.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
