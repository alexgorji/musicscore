from musicscore.musicxml.attributes.accidental import Smulf
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printstyle import PrintStyle, PrintStyleAlign
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import String


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


class EmptyPrintObjectStyleAlign(Empty, PrintObject, PrintStyleAlign):
    """
    The empty-print-style-align-object type represents an empty element with print-object and print-style-align
    attribute groups.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class EmptyPlacementSmulf(Empty, Placement, Smulf):
    """
    The empty-placement-smufl type represents an empty element with print-style, placement, and smufl attributes.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class EmptyFont(Empty, Font):
    """
    >The empty-font type represents an empty element with font attributes.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class PlacementText(ComplexType, String, PrintStyle, Placement):
    """
    The placement-text type represents a text element with print-style and placement attribute groups.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class OtherPlacementText(ComplexType, String, PrintStyle, Placement, Smulf):
    """
    The other-placement-text type represents a text element with print-style, placement, and smufl attribute groups.
    This type is used by MusicXML notation extension elements to allow specification of specific SMuFL glyphs without
    needed to add every glyph as a MusicXML element.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
