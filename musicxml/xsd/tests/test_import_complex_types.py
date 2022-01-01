from unittest import TestCase
from musicxml.xsd.xsdcomplextype import *

class TestImportSimpleTypes(TestCase):
    def test_import_all_imports_only_xml_classes(self):
        XSDComplexTypeFingering
        with self.assertRaises(NameError):
            XSDComplexType
