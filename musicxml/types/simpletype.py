from musicxml.util.helperfunctions import get_simple_format_all_base_classes, find_all_xsd_children
from musicxml.xmlelement import MusicXMLElement, XMLElementTreeElement


class XsType:
    pass


class XsToken(XsType):
    pass


class XsPositiveInteger(XsType):
    pass


class XsDecimal(XsType):
    pass


class XsString(XsType):
    pass


class XsNonNegativeInteger(XsType):
    pass


class XsNMTOKEN(XsType):
    pass


class XsDate(XsType):
    pass


class XsInteger(XsType):
    pass


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
    base_classes = f"({', '.join(get_simple_format_all_base_classes(xml_element_tree_element))}, )"
    attributes = """
    {
    '__doc__': xml_element_tree_element.get_doc(), 
    'XML_ET_ELEMENT':xml_element_tree_element
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
