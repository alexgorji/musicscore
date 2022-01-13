import xml.etree.ElementTree as ET

from musicxml.generate_classes.utils import musicxml_xsd_et_root, ns
from musicxml.xmlelement.core import XMLElement
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdtree import XSDTree

# xml score partwise
xsd_tree_score_partwise_part = XSDTree(musicxml_xsd_et_root.find(f".//{ns}element[@name='score-partwise']"))


class XMLScorePartwise(XMLElement):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.find(f".//{ns}element[@name='score-partwise']"))

    def write(self, path, intelligent_choice=False):
        with open(path, 'w') as file:
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            file.write(self.to_string(intelligent_choice=intelligent_choice))

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypeScorePartwise
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


class XMLPart(XMLElement):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.findall(f".//{ns}element[@name='score-partwise']//{ns}element")[0])

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypePart
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


class XMLMeasure(XMLElement):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.findall(f".//{ns}element[@name='score-partwise']//{ns}element")[1])

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypeMeasure
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()


class XMLDirective(XMLElement):
    XSD_TREE = XSDTree(musicxml_xsd_et_root.find(".//{*}complexType[@name='attributes']//{*}element[@name='directive']"))

    @property
    def type_(self):
        if self._type is None:
            self._type = XSDComplexTypeDirective
        return self._type

    @property
    def __doc__(self):
        return self.XSD_TREE.get_doc()
# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_xml_elements.py
# -----------------------------------------------------
