from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class VirtualLibrary(XMLElement, String):
    """
    The virtual-library element indicates the virtual instrument library name.
    """
    _TAG = 'virtual-library'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class VirtualName(XMLElement, String):
    """
    The virtual-name element indicates the library-specific name for the virtual instrument.
    """
    _TAG = 'virtual-name'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeVirtualInstrument(ComplexType):
    """
    The virtual-instrument element defines a specific virtual instrument used for an instrument sound.
    """
    _DTD = Sequence(
        Element(VirtualLibrary, min_occurrence=0),
        Element(VirtualName, min_occurrence=0)

    )

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
