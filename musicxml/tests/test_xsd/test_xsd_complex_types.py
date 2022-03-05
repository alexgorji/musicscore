import importlib

from musicxml.tests.util import MusicXmlTestCase
from musicxml.xsd.xsdindicator import XSDSequence, XSDChoice

from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdcomplextype import XSDComplexType
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdtree import XSDTree


class TestComplexTypes(MusicXmlTestCase):

    def test_generated_complex_type_xsd_snippet(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class can show corresponding xsd
        """
        expected = """<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fingering">
		<xs:annotation>
			<xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>
		</xs:annotation>
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="substitution" type="yes-no" />
				<xs:attribute name="alternate" type="yes-no" />
				<xs:attributeGroup ref="print-style" />
				<xs:attributeGroup ref="placement" />
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
"""
        assert XSDComplexTypeFingering.get_xsd() == expected

    def test_generate_complex_type_is_descendent_of_complex_type(self):
        assert isinstance(XSDComplexTypeFingering('2'), XSDComplexType)

    def test_generated_complex_type_doc_string_from_annotation(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class has a documentation string
        matching its xsd annotation
        """
        assert XSDComplexTypeFingering.__doc__ == 'Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.'

    def test_complex_type_xsd_is_converted_to_classes(self):
        """
        Test that all XSDComplexType classes are generated
        """
        for complex_type in self.all_complex_type_xsd_elements:
            module = importlib.import_module('musicxml.xsd.xsdcomplextype')
            complex_type_class = getattr(module, complex_type.xsd_element_class_name)
            assert complex_type.xsd_element_class_name == complex_type_class.__name__

    def test_complex_type_get_attributes_simple_content(self):
        """
        Test that complex type's get_attributes method returns XSDAttribute classes according to:
        simpleContext's extention
        """
        """
        complexType@name=typed-text
            simpleContent
                extension@base=xs:string
                    attribute@name=type@type=xs:token
        """
        ct = XSDComplexTypeTypedText
        attribute = ct.get_xsd_attributes()[0]
        assert isinstance(attribute, XSDAttribute)
        assert attribute.name == 'type'
        assert attribute.type_ == XSDSimpleTypeToken
        attribute('hello')
        with self.assertRaises(TypeError):
            attribute(2)
        assert str(attribute) == 'XSDAttribute@name=type@type=xs:token'
        assert not attribute.is_required
        """
        complexType@name=cancel
            simpleContent
                extension@base=fifths
                    attribute@name=location@type=cancel-location
        """
        ct = XSDComplexTypeCancel
        attribute = ct.get_xsd_attributes()[0]
        assert isinstance(attribute, XSDAttribute)
        assert attribute.name == 'location'
        assert attribute.type_ == XSDSimpleTypeCancelLocation
        attribute('left')
        with self.assertRaises(TypeError):
            attribute(2)
        with self.assertRaises(ValueError):
            attribute('something')
        assert not attribute.is_required
        assert str(attribute) == 'XSDAttribute@name=location@type=cancel-location'

    def test_complex_type_get_attributes_simple_content_attribute_group(self):
        """
        complexType@name=part-symbol
            simpleContent
                extension@base=group-symbol-value
                    attribute@name=top-staff@type=staff-number
                    attribute@name=bottom-staff@type=staff-number
                    attributeGroup@ref=position
                    attributeGroup@ref=color
        """
        ct = XSDComplexTypePartSymbol
        attribute_1 = ct.get_xsd_attributes()[0]
        attribute_2 = ct.get_xsd_attributes()[1]
        attribute_3 = ct.get_xsd_attributes()[2]
        attribute_4 = ct.get_xsd_attributes()[3]
        attribute_5 = ct.get_xsd_attributes()[4]
        attribute_6 = ct.get_xsd_attributes()[5]
        attribute_7 = ct.get_xsd_attributes()[6]
        assert attribute_1.type_ == XSDSimpleTypeStaffNumber
        assert attribute_2.type_ == XSDSimpleTypeStaffNumber
        assert attribute_3.type_ == XSDSimpleTypeTenths
        assert attribute_4.type_ == XSDSimpleTypeTenths
        assert attribute_5.type_ == XSDSimpleTypeTenths
        assert attribute_6.type_ == XSDSimpleTypeTenths
        assert attribute_7.type_ == XSDSimpleTypeColor
        assert str(attribute_1) == 'XSDAttribute@name=top-staff@type=staff-number'
        assert str(attribute_2) == 'XSDAttribute@name=bottom-staff@type=staff-number'
        assert str(attribute_3) == 'XSDAttribute@name=default-x@type=tenths'
        assert str(attribute_4) == 'XSDAttribute@name=default-y@type=tenths'
        assert str(attribute_5) == 'XSDAttribute@name=relative-x@type=tenths'
        assert str(attribute_6) == 'XSDAttribute@name=relative-y@type=tenths'
        assert str(attribute_7) == 'XSDAttribute@name=color@type=color'

    def test_complex_type_get_attributes_direct_children(self):
        """
        Test that complex type's get_attributes method returns XSDAttribute classes according to:
        direct attributes
        """

        """
        complexType@name=beat-repeat
            annotation
                documentation
            group@ref=slash@minOccurs=0
            attribute@name=type@type=start-stop@use=required
            attribute@name=slashes@type=xs:positiveInteger
            attribute@name=use-dots@type=yes-no
        """
        ct = XSDComplexTypeBeatRepeat
        attribute_1 = ct.get_xsd_attributes()[0]
        attribute_2 = ct.get_xsd_attributes()[1]
        attribute_3 = ct.get_xsd_attributes()[2]
        assert attribute_1.type_ == XSDSimpleTypeStartStop
        assert attribute_2.type_ == XSDSimpleTypePositiveInteger
        assert attribute_3.type_ == XSDSimpleTypeYesNo
        assert attribute_1.is_required
        assert not attribute_2.is_required
        assert not attribute_3.is_required
        assert str(attribute_1) == 'XSDAttribute@name=type@type=start-stop@use=required'
        assert str(attribute_2) == 'XSDAttribute@name=slashes@type=xs:positiveInteger'
        assert str(attribute_3) == 'XSDAttribute@name=use-dots@type=yes-no'

    def test_complex_type_get_attributes_direct_children_attribute_groups(self):
        """
        Test that complex type's get_attributes method returns XSDAttribute classes according to:
        direct attributes and attribute groups
        """
        """
        complexType@name=transpose
            annotation
                documentation
            group@ref=transpose
            attribute@name=number@type=staff-number
            attributeGroup@ref=optional-unique-id
        """
        ct = XSDComplexTypeTranspose
        attribute_1 = ct.get_xsd_attributes()[0]
        attribute_2 = ct.get_xsd_attributes()[1]
        assert attribute_1.type_ == XSDSimpleTypeStaffNumber
        assert attribute_2.type_ == XSDSimpleTypeID
        assert str(attribute_1) == 'XSDAttribute@name=number@type=staff-number'
        assert str(attribute_2) == 'XSDAttribute@name=id@type=xs:ID'

    def test_complex_type_get_attributes_complexContent(self):
        """
        Test that complex type's get_attributes method returns XSDAttribute classes according to:
        complexContent
        """
        """
        complexType@name=heel-toe
            complexContent
                extension@base=empty-placement
                    attribute@name=substitution@type=yes-no
                    
        complexType@name=empty-placement
            attributeGroup@ref=print-style
            attributeGroup@ref=placement
        
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

        """
        attributeGroup@name=placement
            attribute@name=placement@type=above-below
        """

        ct = XSDComplexTypeHeelToe
        [attribute_1, attribute_2, attribute_3, attribute_4, attribute_5, attribute_6, attribute_7, attribute_8, attribute_9,
         attribute_10, attribute_11] = ct.get_xsd_attributes()
        assert str(attribute_1) == 'XSDAttribute@name=default-x@type=tenths'
        assert str(attribute_2) == 'XSDAttribute@name=default-y@type=tenths'
        assert str(attribute_3) == 'XSDAttribute@name=relative-x@type=tenths'
        assert str(attribute_4) == 'XSDAttribute@name=relative-y@type=tenths'
        assert str(attribute_5) == 'XSDAttribute@name=font-family@type=font-family'
        assert str(attribute_6) == 'XSDAttribute@name=font-style@type=font-style'
        assert str(attribute_7) == 'XSDAttribute@name=font-size@type=font-size'
        assert str(attribute_8) == 'XSDAttribute@name=font-weight@type=font-weight'
        assert str(attribute_9) == 'XSDAttribute@name=color@type=color'
        assert str(attribute_10) == 'XSDAttribute@name=placement@type=above-below'
        assert str(attribute_11) == 'XSDAttribute@name=substitution@type=yes-no'

    def test_get_xsd_indicator(self):
        """
        Test if complex type's method get_xsd_indicator return XSDSequence, XSDChoice or None
        """
        assert XSDComplexTypeEmpty().get_xsd_indicator() is None
        assert isinstance(XSDComplexTypeMidiInstrument().get_xsd_indicator()[0], XSDSequence)
        assert XSDComplexTypeMidiInstrument().get_xsd_indicator()[1:] == (1, 1)
        assert isinstance(XSDComplexTypeDynamics().get_xsd_indicator()[0], XSDChoice)
        assert XSDComplexTypeDynamics().get_xsd_indicator()[1:] == (0, 'unbounded')

    def test_complex_type_barline_sequence_elements(self):
        """
        Test sequence with group and elements
        """
        assert XSDComplexTypeBarline.get_xsd_indicator()[0].elements == [('XMLBarStyle', '0', '1'), ('XMLFootnote', '0', '1'), ('XMLLevel',
                                                                                                                                '0', '1'),
                                                                         ('XMLWavyLine', '0', '1'), ('XMLSegno', '0', '1'),
                                                                         ('XMLCoda', '0', '1'), ('XMLFermata', '0', '2'),
                                                                         ('XMLEnding', '0', '1'), ('XMLRepeat', '0', '1')]

    def test_complex_type_print_elements(self):
        """
        Test sequence with group and elements
        """
        assert XSDComplexTypePrint.get_xsd_indicator()[0].elements == [('XMLPageLayout', '0', '1'), ('XMLSystemLayout', '0', '1'),
                                                                       ('XMLStaffLayout', '0', 'unbounded'), ('XMLMeasureLayout', '0', '1'),
                                                                       ('XMLMeasureNumbering', '0', '1'), ('XMLPartNameDisplay', '0', '1'),
                                                                       ('XMLPartAbbreviationDisplay', '0', '1')]

    def test_simple_content_value(self):
        """
        Test if value of a complex type is checked according to the core simple type
        """
        with self.assertRaises(ValueError):
            XSDSimpleTypeNoteTypeValue('bla')

        with self.assertRaises(TypeError):
            XSDComplexTypeNoteType()
        with self.assertRaises(ValueError):
            XSDComplexTypeNoteType(value='bla')
        XSDComplexTypeNoteType('half')
