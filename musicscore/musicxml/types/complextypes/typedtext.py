from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String, Token


class ComplexTypeTypedText(ComplexType, String):
    """
    The typed-text type represents a text element with a type attributes.
    """

    def __init__(self, tag, type=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.name = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
