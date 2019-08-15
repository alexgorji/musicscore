from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeHoleClosedValue, TypeHoleClosedLocation


class ComplexTypeHoleClosed(ComplexType, TypeHoleClosedValue):
    """The hole-closed type represents whether the hole is closed, open, or half-open. The optional location attribute
    indicates which portion of the hole is filled in when the element value is half.
    """

    def __init__(self, tag, value, location=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
        self.location = location

    @property
    def location(self):
        return self.get_attribute('location')

    @location.setter
    def location(self, value):
        if value is None:
            self.remove_attribute('location')
        else:
            TypeHoleClosedLocation(value)
            self._ATTRIBUTES.insert(0, 'location')
            self.set_attribute('location', value)
