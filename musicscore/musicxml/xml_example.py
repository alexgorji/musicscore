from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.print_style import Position


class XMLExample(XMLElement, Position):
    """"""

    def __init__(self, default_x=10, *args, **kwargs):
        super().__init__(tag='example', default_x=default_x, *args, **kwargs)
