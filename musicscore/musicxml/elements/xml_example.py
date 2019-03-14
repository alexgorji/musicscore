from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement2
from musicscore.musicxml.attributes.attribute_example import AttributeExample


class XMLExampleChild1(XMLElement2):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-1', *args, **kwargs)


class XMLExampleChild2(XMLElement2):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-2', *args, **kwargs)


class XMLExample(XMLElement2, AttributeExample):
    """
    some documentation
    """
    _ATTRIBUTES = ['attribute-example']
    _DTD = Sequence(
        Element(XMLExampleChild1, min_occurrence=0),
        Element(XMLExampleChild2, min_occurrence=0, max_occurrence=None)

    )

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
