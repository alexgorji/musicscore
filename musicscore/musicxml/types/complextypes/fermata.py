from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeFermataShape, TypeUprightInverted


class ComplexTypeFermata(ComplexType, TypeFermataShape, PrintStyle, OptionalUniqueId):
    """The fermata text content represents the shape of the fermata sign. An empty fermata element represents a normal
    fermata. The fermata type is upright if not specified."""

    def __init__(self, tag, value, type=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeUprightInverted(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
