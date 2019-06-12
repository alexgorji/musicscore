from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeTenths, TypeStaffNumber


class StaffDistance(XMLElement, TypeTenths):
    _TAG = 'staff-distance'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeStaffLayout(ComplexType):
    """
    Staff layout includes the vertical distance from the bottom line of the previous staff in this system to the top
    line of the staff specified by the number attribute. The optional number attribute refers to staff numbers within
    the part, from top to bottom on the system. A value of 1 is assumed if not present. When used in the defaults
    element, the values apply to all parts. This value is ignored for the first staff in a system.
    """
    _DTD = Sequence(
        Element(StaffDistance,
                min_occurrence=0)

    )

    def __init__(self, tag, number=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeStaffNumber(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)
