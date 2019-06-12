from musicscore.musicxml.attributes.elementposition import ElementPosition
from musicscore.musicxml.attributes.linkattributes import LinkAttributes
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import Token


class ComplexTypeLink(ComplexType, LinkAttributes, ElementPosition, Position):
    """The link type serves as an outgoing simple XLink. It is also used to connect a MusicXML score with a MusicXML
    opus. If a relative link is used within a document that is part of a compressed MusicXML file, the link is relative
    to the  root folder of the zip file."""

    def __init__(self, tag, name=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.name = name

    @property
    def name(self):
        return self.get_attribute('name')

    @name.setter
    def name(self, value):
        if value is None:
            self.remove_attribute('name')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'name')
            self.set_attribute('name', value)
