from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import Token


class ComplexTypeLyricFont(ComplexType, Font):
    """The lyric-font type specifies the default font for a particular name and number of lyric.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

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
