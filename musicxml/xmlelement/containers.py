from musicxml.xmlelement.xmlchildcontainer import XMLChildContainerFactory
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdcomplextype import __all__

containers = {}

for ct in __all__[1:]:
    cls = eval(ct)
    if cls.get_xsd_indicator():
        containers[ct] = XMLChildContainerFactory(complex_type=cls).get_child_container()
