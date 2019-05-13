from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printattributes import PrintAttributes
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.groups.layout import Layout
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.scorepart import PartNameDisplay, PartAbbreviationDisplay


class MeasureLayout(XMLElement):
    _TAG = 'measure-layout'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class MeasureNumbering(XMLElement):
    _TAG = 'measure-numbering'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class ComplexTypePrint(ComplexType, PrintAttributes, OptionalUniqueId):
    """
    The print type contains general printing parameters, including the layout elements defined in the layout.mod file.
    The part-name-display and part-abbreviation-display elements used in the score.mod file may also be used here to
    change how a part name or abbreviation is displayed over the course of a piece. They take effect when the current
    measure or a succeeding measure starts a new system.

    Layout elements in a print statement only apply to the current page, system, staff, or measure. Music that follows
    continues to take the default values from the layout included in the defaults element.
    """
    _DTD = Sequence(
        GroupReference(Layout),
        Element(MeasureLayout,
                min_occurrence=0),
        Element(MeasureNumbering,
                min_occurrence=0),
        Element(PartNameDisplay,
                min_occurrence=0),
        Element(PartAbbreviationDisplay,
                min_occurrence=0)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
