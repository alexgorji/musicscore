from unittest import TestCase
from musicxml.types.complextype import *


class TestImportSimpleTypes(TestCase):
    def test_import_all_imports_only_xml_classes(self):
        XMLComplexTypeFingering
        with self.assertRaises(NameError):
            XMLComplexType
