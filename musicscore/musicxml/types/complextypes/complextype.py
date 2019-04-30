from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyle, PrintStyleAlign
from musicscore.musicxml.elements.xml_element import XMLElement


class ComplexType(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# TODO: add exception for attributes
class Empty(ComplexType, XMLElement):
    """
    Empty is a type of XMLElement with no children, no text and no attributes.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

    def add_child(self, child):
        raise Exception('Empty cannot have children.')

    @XMLElement.text.setter
    def text(self, value):
        if value is not None:
            raise Exception('Empty cannot have text.')


class EmptyPlacement(Empty, PrintStyle, Placement):
    """
    The empty-placement type represents an empty element with print-style and placement attributes.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class EmptyPrintStyleAlignId(Empty, PrintStyleAlign, OptionalUniqueId):
    """
    The empty-print-style-align-id type represents an empty element with print-style-align and optional-unique-id 
    attribute groups.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
