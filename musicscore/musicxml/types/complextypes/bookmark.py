from musicscore.musicxml.attributes.elementposition import ElementPosition
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import ID, Token


class ComplexTypeBookmark(ComplexType, ElementPosition):
    """The bookmark type serves as a well-defined target for an incoming simple XLink."""

    def __init__(self, id_, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id_
        self.name = name

    @property
    def id(self):
        return self.get_attribute('id')

    @id.setter
    def id(self, value):
        if value is None:
            self.remove_attribute('id')
        else:
            ID(value)
            self._ATTRIBUTES.insert(0, 'id')
            self.set_attribute('id', value)

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
