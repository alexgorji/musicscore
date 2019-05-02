from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeMillimeters, TypeTenths


class Millimeters(XMLElement, TypeMillimeters):
    _TAG = 'millimeters'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Tenths(XMLElement, TypeTenths):
    _TAG = 'tenths'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeScaling(ComplexType):
    """
    Margins, page sizes, and distances are all measured in tenths to keep MusicXML data in a consistent coordinate
    system as much as possible. The translation to absolute units is done with the scaling type, which specifies how
    many millimeters are equal to how many tenths. For a staff height of 7mm, millimeters would be set to 7 while tenths
    is set to 40. The ability to set a formula rather than a single scaling factor helps avoid roundoff errors.
    """
    _DTD = Sequence(
        Element(Millimeters),
        Element(Tenths)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)