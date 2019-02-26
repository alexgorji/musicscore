from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.attribute_example import AttibuteExample


class XMLExample(XMLElement, AttibuteExample):
    """
    some documenation
    """
    _ATTRIBUTES = ('attribute-example')

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
