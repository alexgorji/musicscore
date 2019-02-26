from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.attribute_example import AttributeExample


class XMLExampleChild1(XMLElement):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-1', *args, **kwargs)


class XMLExampleChild2(XMLElement):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-2', *args, **kwargs)
        self.multiple = True


class XMLExample(XMLElement, AttributeExample):
    """
    some documentation
    """
    _ATTRIBUTES = ['attribute-example']
    _CHILDREN_TYPES = [XMLExampleChild1, XMLExampleChild2]
    _CHILDREN_ORDERED = True

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
