from unittest import TestCase

from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdtree import XSDTree
from xml.etree import ElementTree as ET

from musicxml.tests.util import MusicXmlTestCase


class TestXSDAttribute(TestCase):
    def test_xsd_attribute_from_XSD_TREE(self):
        """
        Test that an XSDAttribute can be created out of a XSDTree with tag attribute.
        """
        el = ET.fromstring('<xs:attribute xmlns:xs="http://www.w3.org/2001/XMLSchema" name="type" type="xs:token" />')
        XSD_TREE = XSDTree(el)
        attribute = XSDAttribute(XSD_TREE)
        assert attribute.name == 'type'
        assert attribute.type_ == XSDSimpleTypeToken
        assert attribute.is_required is False
        assert isinstance(attribute('Hi'), XSDSimpleTypeToken)
        with self.assertRaises(TypeError):
            attribute(1)

    def test_attributes_with_ref(self):
        """
        There are a few attributes with ref instead of name:
        <xs:attribute ref="xml:lang"/>
        used in:
            <xs:element name="directive">
            <xs:complexType name="text-element-data">
            <xs:complexType name="lyric-language">
            <xs:attributeGroup name="text-formatting">
        <xs:attribute ref="xml:space"/>
        used in:
            <xs:attributeGroup name="text-formatting">

        <xs:attribute ref="xlink:href" use="required"/>
        <xs:attribute ref="xlink:type" fixed="simple"/>
        <xs:attribute ref="xlink:role"/>
        <xs:attribute ref="xlink:title"/>
        <xs:attribute ref="xlink:show" default="replace"/>
        <xs:attribute ref="xlink:actuate" default="onRequest"/>
        used in:
            <xs:attributeGroup name="link-attributes">
        """
        """
        Test lang and space
        """
        tf = XSDAttributeGroupTextFormatting()
        assert [a.name for a in tf.get_xsd_attributes()] == ['justify', 'default-x', 'default-y', 'relative-x', 'relative-y', 'font-family',
                                                             'font-style', 'font-size', 'font-weight', 'color', 'halign', 'valign',
                                                             'underline', 'overline', 'line-through', 'rotation', 'letter-spacing',
                                                             'line-height', 'lang', 'space', 'dir', 'enclosure']

        """
        Test xlink
        """
    #
    # self.fail('Incomplete')


class TestXSDAttributeGroup(MusicXmlTestCase):

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
