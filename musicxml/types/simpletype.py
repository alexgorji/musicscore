from musicxml.xmlelement import MusicXMLElement, XMLElementTreeElement, find_all_xsd_children


class XMLSimpleType(MusicXMLElement):
    """
    Parent Class for all SimpleType classes
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate(value)
        self._value = value

    def _validate(self, value):
        return True

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return str(self.value)


for simple_type in find_all_xsd_children(tag='simpleType'):
    xml_element_tree_element = XMLElementTreeElement(simple_type)

    class_name = xml_element_tree_element.class_name
    parent_class = 'XMLSimpleType'
    attributes = """
    {
    '__doc__': xml_element_tree_element.get_doc(), 
    'XML_ET_ELEMENT':xml_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', ({parent_class},), {attributes})")
