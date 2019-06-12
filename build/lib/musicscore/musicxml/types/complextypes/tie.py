from musicscore.musicxml.attributes.timeonly import TimeOnly
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeStartStop


class ComplexTypeTie(ComplexType, TimeOnly):
    """
    The tie element indicates that a tie begins or ends with this note. If the tie element applies only particular times
    through a repeat, the time-only attribute indicates which times to apply it. The tie element indicates sound; the
    tied element indicates notation
    """

    def __init__(self, type='start', *args, **kwargs):
        super().__init__(tag='tie', *args, **kwargs)
        self.type = type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeStartStop(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
