'''
    <xs:complexType name="system-layout">
        <xs:sequence>
            <xs:element name="system-margins" type="system-margins" minOccurs="0"/>
            <xs:element name="system-dividers" type="system-dividers" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
'''
from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.systemdividers import ComplexTypeSystemDividers
from musicscore.musicxml.types.complextypes.systemmargins import ComplexTypeSystemMargins
from musicscore.musicxml.types.simple_type import TypeTenths


class SystemMargins(ComplexTypeSystemMargins):
    _TAG = 'system-margins'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SystemDistance(XMLElement, TypeTenths):
    _TAG = 'system-distance'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class TopSystemDistance(XMLElement, TypeTenths):
    _TAG = 'top-system-distance'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class SystemDividers(ComplexTypeSystemDividers):
    _TAG = 'system-dividers'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeSystemLayout(ComplexType):
    """A system is a group of staves that are read and played simultaneously. System layout includes left and right
    margins and the vertical distance from the previous system. The system distance is measured from the bottom line
    of the previous system to the top line of the current system. It is ignored for the first system on a page. The top
    system distance is measured from the page's top margin to the top line of the first system. It is ignored for all
    but the first system on a page.

    Sometimes the sum of measure widths in a system may not equal the system width specified by the layout elements due
    to roundoff or other errors. The behavior when reading MusicXML files in these cases is application-dependent. For
    instance, applications may find that the system layout data is more reliable than the sum of the measure widths,
    and adjust the measure widths accordingly."""

    _DTD = Sequence(
        Element(SystemMargins, min_occurrence=0),
        Element(SystemDistance, min_occurrence=0),
        Element(TopSystemDistance, min_occurrence=0),
        Element(SystemDividers, min_occurrence=0),
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
