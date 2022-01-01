from unittest import TestCase

from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import XSDAttribute, xml_attribute_group_class_names
from musicxml.xsd.xsdtree import XSDTree
from xml.etree import ElementTree as ET

from musicxml.util.helperclasses import MusicXmlTestCase
from musicxml.xsd.xsdattribute import *


class TestXSDAttribute(TestCase):
    def test_xsd_attribute_from_xsd_tree(self):
        """
        Test that an XSDAttribute can be created out of a XSDTree with tag attribute.
        """
        el = ET.fromstring('<xs:attribute xmlns:xs="http://www.w3.org/2001/XMLSchema" name="type" type="xs:token" />')
        xsd_tree = XSDTree(el)
        attribute = XSDAttribute(xsd_tree)
        assert attribute.name == 'type'
        assert attribute.type_ == XSDSimpleTypeToken
        assert attribute.is_required is False
        assert isinstance(attribute('Hi'), XSDSimpleTypeToken)
        with self.assertRaises(TypeError):
            attribute(1)


class TestXSDAttributeGroup(MusicXmlTestCase):
    def test_xsd_attribute_group_list(self):
        """
        Test if xml_attribute_group_class_names in module musicxml.xsdattribute return all attribute group
        """
        assert xml_attribute_group_class_names == ['XSDAttributeGroupBendSound', 'XSDAttributeGroupBezier', 'XSDAttributeGroupColor',
                                                   'XSDAttributeGroupDashedFormatting', 'XSDAttributeGroupDirective',
                                                   'XSDAttributeGroupDocumentAttributes', 'XSDAttributeGroupEnclosure',
                                                   'XSDAttributeGroupFont', 'XSDAttributeGroupHalign', 'XSDAttributeGroupJustify',
                                                   'XSDAttributeGroupLetterSpacing', 'XSDAttributeGroupLevelDisplay',
                                                   'XSDAttributeGroupLineHeight', 'XSDAttributeGroupLineLength',
                                                   'XSDAttributeGroupLineShape', 'XSDAttributeGroupLineType',
                                                   'XSDAttributeGroupOptionalUniqueId', 'XSDAttributeGroupOrientation',
                                                   'XSDAttributeGroupPlacement', 'XSDAttributeGroupPosition',
                                                   'XSDAttributeGroupPrintObject', 'XSDAttributeGroupPrintSpacing',
                                                   'XSDAttributeGroupPrintStyle', 'XSDAttributeGroupPrintStyleAlign',
                                                   'XSDAttributeGroupPrintout', 'XSDAttributeGroupSmufl', 'XSDAttributeGroupSystemRelation',
                                                   'XSDAttributeGroupSymbolFormatting', 'XSDAttributeGroupTextDecoration',
                                                   'XSDAttributeGroupTextDirection', 'XSDAttributeGroupTextFormatting',
                                                   'XSDAttributeGroupTextRotation', 'XSDAttributeGroupTrillSound',
                                                   'XSDAttributeGroupValign', 'XSDAttributeGroupValignImage', 'XSDAttributeGroupXPosition',
                                                   'XSDAttributeGroupYPosition', 'XSDAttributeGroupImageAttributes',
                                                   'XSDAttributeGroupPrintAttributes', 'XSDAttributeGroupElementPosition',
                                                   'XSDAttributeGroupLinkAttributes', 'XSDAttributeGroupGroupNameText',
                                                   'XSDAttributeGroupMeasureAttributes', 'XSDAttributeGroupPartAttributes',
                                                   'XSDAttributeGroupPartNameText']

    def test_attribute_group_get_attributes(self):
        """
        attributeGroup@name=position

        attribute@name=default-x@type=tenths
        attribute@name=default-y@type=tenths
        attribute@name=relative-x@type=tenths
        attribute@name=relative-y@type=tenths
        """
        [attribute_1, attribute_2, attribute_3, attribute_4] = XSDAttributeGroupPosition.get_xsd_attributes()
        assert str(attribute_1) == 'XSDAttribute@name=default-x@type=tenths'
        assert str(attribute_2) == 'XSDAttribute@name=default-y@type=tenths'
        assert str(attribute_3) == 'XSDAttribute@name=relative-x@type=tenths'
        assert str(attribute_4) == 'XSDAttribute@name=relative-y@type=tenths'

        for attribute in XSDAttributeGroupPosition.get_xsd_attributes():
            assert isinstance(attribute, XSDAttribute)
            assert isinstance(attribute(10), XSDSimpleTypeTenths)

    def test_print_style_attribute_group(self):
        """
        attributeGroup@name=print-style
            attributeGroup@ref=position
            attributeGroup@ref=font
            attributeGroup@ref=color

        attributeGroup@name=position
            attribute@name=default-x@type=tenths
            attribute@name=default-y@type=tenths
            attribute@name=relative-x@type=tenths
            attribute@name=relative-y@type=tenths

        attributeGroup@name=font
            attribute@name=font-family@type=font-family
            attribute@name=font-style@type=font-style
            attribute@name=font-size@type=font-size
            attribute@name=font-weight@type=font-weight

        attributeGroup@name=color
            attribute@name=color@type=color
        """
        [attribute_1, attribute_2, attribute_3, attribute_4, attribute_5, attribute_6, attribute_7, attribute_8, attribute_9] = \
            XSDAttributeGroupPrintStyle.get_xsd_attributes()
        assert str(attribute_1) == 'XSDAttribute@name=default-x@type=tenths'
        assert str(attribute_2) == 'XSDAttribute@name=default-y@type=tenths'
        assert str(attribute_3) == 'XSDAttribute@name=relative-x@type=tenths'
        assert str(attribute_4) == 'XSDAttribute@name=relative-y@type=tenths'
        assert str(attribute_5) == 'XSDAttribute@name=font-family@type=font-family'
        assert str(attribute_6) == 'XSDAttribute@name=font-style@type=font-style'
        assert str(attribute_7) == 'XSDAttribute@name=font-size@type=font-size'
        assert str(attribute_8) == 'XSDAttribute@name=font-weight@type=font-weight'
        assert str(attribute_9) == 'XSDAttribute@name=color@type=color'