from musicscore.musicxml.types.complextypes.complextype import EmptyPlacement
from musicscore.musicxml.types.simple_type import TypeUpDown


class ComplexTypeStrongAccent(EmptyPlacement):
    """The strong-accent type indicates a vertical accent mark. The type attribute indicates if the point of the
    accent is down or up."""

    def __init__(self, tag, type, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeUpDown(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
