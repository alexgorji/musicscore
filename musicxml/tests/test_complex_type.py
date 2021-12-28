import importlib

from musicxml.util.helperclasses import MusicXmlTestCase

from musicxml.types.simpletype import *
from musicxml.types.complextype import xsd_complex_type_class_names, XSDComplexType
from musicxml.types.complextype import *
from musicxml.xsdattribute import XSDAttribute


class TestComplexTypes(MusicXmlTestCase):
    def test_complex_types_list(self):
        """
        Test if SIMPLE_TYPES in module musicxml.types.simpletype return all simple types
        """
        assert xsd_complex_type_class_names == ['XSDComplexTypeAccidentalText', 'XSDComplexTypeCoda', 'XSDComplexTypeDynamics',
                                                'XSDComplexTypeEmpty', 'XSDComplexTypeEmptyPlacement', 'XSDComplexTypeEmptyPlacementSmufl',
                                                'XSDComplexTypeEmptyPrintStyle', 'XSDComplexTypeEmptyPrintStyleAlign',
                                                'XSDComplexTypeEmptyPrintStyleAlignId', 'XSDComplexTypeEmptyPrintObjectStyleAlign',
                                                'XSDComplexTypeEmptyTrillSound', 'XSDComplexTypeHorizontalTurn', 'XSDComplexTypeFermata',
                                                'XSDComplexTypeFingering', 'XSDComplexTypeFormattedSymbol',
                                                'XSDComplexTypeFormattedSymbolId', 'XSDComplexTypeFormattedText',
                                                'XSDComplexTypeFormattedTextId', 'XSDComplexTypeFret', 'XSDComplexTypeLevel',
                                                'XSDComplexTypeMidiDevice', 'XSDComplexTypeMidiInstrument', 'XSDComplexTypeNameDisplay',
                                                'XSDComplexTypeOtherPlay', 'XSDComplexTypePlay', 'XSDComplexTypeSegno',
                                                'XSDComplexTypeString', 'XSDComplexTypeTypedText', 'XSDComplexTypeWavyLine',
                                                'XSDComplexTypeAttributes', 'XSDComplexTypeBeatRepeat', 'XSDComplexTypeCancel',
                                                'XSDComplexTypeClef', 'XSDComplexTypeDouble', 'XSDComplexTypeForPart',
                                                'XSDComplexTypeInterchangeable', 'XSDComplexTypeKey', 'XSDComplexTypeKeyAccidental',
                                                'XSDComplexTypeKeyOctave', 'XSDComplexTypeLineDetail', 'XSDComplexTypeMeasureRepeat',
                                                'XSDComplexTypeMeasureStyle', 'XSDComplexTypeMultipleRest', 'XSDComplexTypePartClef',
                                                'XSDComplexTypePartSymbol', 'XSDComplexTypePartTranspose', 'XSDComplexTypeSlash',
                                                'XSDComplexTypeStaffDetails', 'XSDComplexTypeStaffSize', 'XSDComplexTypeStaffTuning',
                                                'XSDComplexTypeTime', 'XSDComplexTypeTranspose', 'XSDComplexTypeBarStyleColor',
                                                'XSDComplexTypeBarline', 'XSDComplexTypeEnding', 'XSDComplexTypeRepeat',
                                                'XSDComplexTypeAccord', 'XSDComplexTypeAccordionRegistration', 'XSDComplexTypeBarre',
                                                'XSDComplexTypeBass', 'XSDComplexTypeHarmonyAlter', 'XSDComplexTypeBassStep',
                                                'XSDComplexTypeBeater', 'XSDComplexTypeBeatUnitTied', 'XSDComplexTypeBracket',
                                                'XSDComplexTypeDashes', 'XSDComplexTypeDegree', 'XSDComplexTypeDegreeAlter',
                                                'XSDComplexTypeDegreeType', 'XSDComplexTypeDegreeValue', 'XSDComplexTypeDirection',
                                                'XSDComplexTypeDirectionType', 'XSDComplexTypeEffect', 'XSDComplexTypeFeature',
                                                'XSDComplexTypeFirstFret', 'XSDComplexTypeFrame', 'XSDComplexTypeFrameNote',
                                                'XSDComplexTypeGlass', 'XSDComplexTypeGrouping', 'XSDComplexTypeHarmony',
                                                'XSDComplexTypeHarpPedals', 'XSDComplexTypeImage', 'XSDComplexTypeInstrumentChange',
                                                'XSDComplexTypeInversion', 'XSDComplexTypeKind', 'XSDComplexTypeListening',
                                                'XSDComplexTypeMeasureNumbering', 'XSDComplexTypeMembrane', 'XSDComplexTypeMetal',
                                                'XSDComplexTypeMetronome', 'XSDComplexTypeMetronomeBeam', 'XSDComplexTypeMetronomeNote',
                                                'XSDComplexTypeMetronomeTied', 'XSDComplexTypeMetronomeTuplet', 'XSDComplexTypeNumeral',
                                                'XSDComplexTypeNumeralKey', 'XSDComplexTypeNumeralRoot', 'XSDComplexTypeOctaveShift',
                                                'XSDComplexTypeOffset', 'XSDComplexTypeOtherDirection', 'XSDComplexTypeOtherListening',
                                                'XSDComplexTypePedal', 'XSDComplexTypePedalTuning', 'XSDComplexTypePerMinute',
                                                'XSDComplexTypePercussion', 'XSDComplexTypePitched', 'XSDComplexTypePrincipalVoice',
                                                'XSDComplexTypePrint', 'XSDComplexTypeRoot', 'XSDComplexTypeRootStep',
                                                'XSDComplexTypeScordatura', 'XSDComplexTypeSound', 'XSDComplexTypeStaffDivide',
                                                'XSDComplexTypeStick', 'XSDComplexTypeStringMute', 'XSDComplexTypeSwing',
                                                'XSDComplexTypeSync', 'XSDComplexTypeTimpani', 'XSDComplexTypeWedge', 'XSDComplexTypeWood',
                                                'XSDComplexTypeEncoding', 'XSDComplexTypeIdentification', 'XSDComplexTypeMiscellaneous',
                                                'XSDComplexTypeMiscellaneousField', 'XSDComplexTypeSupports', 'XSDComplexTypeAppearance',
                                                'XSDComplexTypeDistance', 'XSDComplexTypeGlyph', 'XSDComplexTypeLineWidth',
                                                'XSDComplexTypeMeasureLayout', 'XSDComplexTypeNoteSize', 'XSDComplexTypeOtherAppearance',
                                                'XSDComplexTypePageLayout', 'XSDComplexTypePageMargins', 'XSDComplexTypeScaling',
                                                'XSDComplexTypeStaffLayout', 'XSDComplexTypeSystemDividers', 'XSDComplexTypeSystemLayout',
                                                'XSDComplexTypeSystemMargins', 'XSDComplexTypeBookmark', 'XSDComplexTypeLink',
                                                'XSDComplexTypeAccidental', 'XSDComplexTypeAccidentalMark', 'XSDComplexTypeArpeggiate',
                                                'XSDComplexTypeArticulations', 'XSDComplexTypeArrow', 'XSDComplexTypeAssess',
                                                'XSDComplexTypeBackup', 'XSDComplexTypeBeam', 'XSDComplexTypeBend',
                                                'XSDComplexTypeBreathMark', 'XSDComplexTypeCaesura', 'XSDComplexTypeElision',
                                                'XSDComplexTypeEmptyLine', 'XSDComplexTypeExtend', 'XSDComplexTypeFigure',
                                                'XSDComplexTypeFiguredBass', 'XSDComplexTypeForward', 'XSDComplexTypeGlissando',
                                                'XSDComplexTypeGrace', 'XSDComplexTypeHammerOnPullOff', 'XSDComplexTypeHandbell',
                                                'XSDComplexTypeHarmonClosed', 'XSDComplexTypeHarmonMute', 'XSDComplexTypeHarmonic',
                                                'XSDComplexTypeHeelToe', 'XSDComplexTypeHole', 'XSDComplexTypeHoleClosed',
                                                'XSDComplexTypeInstrument', 'XSDComplexTypeListen', 'XSDComplexTypeLyric',
                                                'XSDComplexTypeMordent', 'XSDComplexTypeNonArpeggiate', 'XSDComplexTypeNotations',
                                                'XSDComplexTypeNote', 'XSDComplexTypeNoteType', 'XSDComplexTypeNotehead',
                                                'XSDComplexTypeNoteheadText', 'XSDComplexTypeOrnaments', 'XSDComplexTypeOtherNotation',
                                                'XSDComplexTypeOtherPlacementText', 'XSDComplexTypeOtherText', 'XSDComplexTypePitch',
                                                'XSDComplexTypePlacementText', 'XSDComplexTypeRelease', 'XSDComplexTypeRest',
                                                'XSDComplexTypeSlide', 'XSDComplexTypeSlur', 'XSDComplexTypeStem',
                                                'XSDComplexTypeStrongAccent', 'XSDComplexTypeStyleText', 'XSDComplexTypeTap',
                                                'XSDComplexTypeTechnical', 'XSDComplexTypeTextElementData', 'XSDComplexTypeTie',
                                                'XSDComplexTypeTied', 'XSDComplexTypeTimeModification', 'XSDComplexTypeTremolo',
                                                'XSDComplexTypeTuplet', 'XSDComplexTypeTupletDot', 'XSDComplexTypeTupletNumber',
                                                'XSDComplexTypeTupletPortion', 'XSDComplexTypeTupletType', 'XSDComplexTypeUnpitched',
                                                'XSDComplexTypeWait', 'XSDComplexTypeCredit', 'XSDComplexTypeDefaults',
                                                'XSDComplexTypeEmptyFont', 'XSDComplexTypeGroupBarline', 'XSDComplexTypeGroupName',
                                                'XSDComplexTypeGroupSymbol', 'XSDComplexTypeInstrumentLink', 'XSDComplexTypeLyricFont',
                                                'XSDComplexTypeLyricLanguage', 'XSDComplexTypeOpus', 'XSDComplexTypePartGroup',
                                                'XSDComplexTypePartLink', 'XSDComplexTypePartList', 'XSDComplexTypePartName',
                                                'XSDComplexTypePlayer', 'XSDComplexTypeScoreInstrument', 'XSDComplexTypeScorePart',
                                                'XSDComplexTypeVirtualInstrument', 'XSDComplexTypeWork']

    def test_generated_complex_type_xsd_snippet(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class can show corresponding xsd
        """
        expected = """<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fingering">\n\t\t<xs:annotation>\n\t\t\t<xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>\n\t\t</xs:annotation>\n\t\t<xs:simpleContent>\n\t\t\t<xs:extension base="xs:string">\n\t\t\t\t<xs:attribute name="substitution" type="yes-no" />\n\t\t\t\t<xs:attribute name="alternate" type="yes-no" />\n\t\t\t\t<xs:attributeGroup ref="print-style" />\n\t\t\t\t<xs:attributeGroup ref="placement" />\n\t\t\t</xs:extension>\n\t\t</xs:simpleContent>\n\t</xs:complexType>\n"""
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
            module = importlib.import_module('musicxml.types.complextype')
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
        ct = XSDComplexTypeMetronomeTuplet
        """
            attribute@name=default-x@type=tenths
            attribute@name=default-y@type=tenths
            attribute@name=relative-x@type=tenths
            attribute@name=relative-y@type=tenths
        """
        [attribute_1, attribute_2, attribute_3, attribute_4, attribute_5, attribute_6, attribute_7, attribute_8, attribute_9] = \
            ct.get_xsd_attributes()
        assert str(attribute_1) == 'XSDAttribute@name=default-x@type=tenths'
        assert str(attribute_2) == 'XSDAttribute@name=default-y@type=tenths'
        assert str(attribute_3) == 'XSDAttribute@name=relative-x@type=tenths'
        assert str(attribute_4) == 'XSDAttribute@name=relative-y@type=tenths'
        assert str(attribute_5) == 'XSDAttribute@name=font-family@type=font-family'
        assert str(attribute_6) == 'XSDAttribute@name=font-style@type=font-style'
        assert str(attribute_7) == 'XSDAttribute@name=font-size@type=font-size'
        assert str(attribute_8) == 'XSDAttribute@name=font-weight@type=font-weight'
        assert str(attribute_9) == 'XSDAttribute@name=substitution@type=yes-no'
