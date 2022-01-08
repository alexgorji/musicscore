from musicxml.xmlelement.xmlelement import XMLChildContainerFactory
from musicxml.xsd.xsdcomplextype import XSDComplexTypeKey

container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
