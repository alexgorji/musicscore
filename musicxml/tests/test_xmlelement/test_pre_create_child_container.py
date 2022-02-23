import copy
from unittest import TestCase
from musicxml.xmlelement.containers import containers
from musicxml.xmlelement.xmlchildcontainer import XMLChildContainerFactory
from musicxml.xsd.xsdcomplextype import XSDComplexTypeNote


class TestPrecreatingXMLChildContainer(TestCase):
    def test_xml_note(self):
        container = copy.deepcopy(containers['XSDComplexTypeNote'])
        manually = XMLChildContainerFactory(XSDComplexTypeNote).get_child_container()
        assert manually.tree_representation() == container.tree_representation()
