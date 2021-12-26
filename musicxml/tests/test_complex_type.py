import importlib

from musicxml.types.complextype import xml_complex_type_class_names
from musicxml.util.helperclasses import MusicXmlTestCase

from musicxml.types.complextype import XMLComplexType, XMLComplexTypeFingering


class TestComplexTypes(MusicXmlTestCase):
    def test_complex_types_list(self):
        """
        Test if SIMPLE_TYPES in module musicxml.types.simpletype return all simple types
        """
        assert xml_complex_type_class_names == ['XMLComplexTypeAccidentalText', 'XMLComplexTypeCoda', 'XMLComplexTypeDynamics',
                                                'XMLComplexTypeEmpty', 'XMLComplexTypeEmptyPlacement', 'XMLComplexTypeEmptyPlacementSmufl',
                                                'XMLComplexTypeEmptyPrintStyle', 'XMLComplexTypeEmptyPrintStyleAlign',
                                                'XMLComplexTypeEmptyPrintStyleAlignId', 'XMLComplexTypeEmptyPrintObjectStyleAlign',
                                                'XMLComplexTypeEmptyTrillSound', 'XMLComplexTypeHorizontalTurn', 'XMLComplexTypeFermata',
                                                'XMLComplexTypeFingering', 'XMLComplexTypeFormattedSymbol',
                                                'XMLComplexTypeFormattedSymbolId', 'XMLComplexTypeFormattedText',
                                                'XMLComplexTypeFormattedTextId', 'XMLComplexTypeFret', 'XMLComplexTypeLevel',
                                                'XMLComplexTypeMidiDevice', 'XMLComplexTypeMidiInstrument', 'XMLComplexTypeNameDisplay',
                                                'XMLComplexTypeOtherPlay', 'XMLComplexTypePlay', 'XMLComplexTypeSegno',
                                                'XMLComplexTypeString', 'XMLComplexTypeTypedText', 'XMLComplexTypeWavyLine',
                                                'XMLComplexTypeAttributes', 'XMLComplexTypeBeatRepeat', 'XMLComplexTypeCancel',
                                                'XMLComplexTypeClef', 'XMLComplexTypeDouble', 'XMLComplexTypeForPart',
                                                'XMLComplexTypeInterchangeable', 'XMLComplexTypeKey', 'XMLComplexTypeKeyAccidental',
                                                'XMLComplexTypeKeyOctave', 'XMLComplexTypeLineDetail', 'XMLComplexTypeMeasureRepeat',
                                                'XMLComplexTypeMeasureStyle', 'XMLComplexTypeMultipleRest', 'XMLComplexTypePartClef',
                                                'XMLComplexTypePartSymbol', 'XMLComplexTypePartTranspose', 'XMLComplexTypeSlash',
                                                'XMLComplexTypeStaffDetails', 'XMLComplexTypeStaffSize', 'XMLComplexTypeStaffTuning',
                                                'XMLComplexTypeTime', 'XMLComplexTypeTranspose', 'XMLComplexTypeBarStyleColor',
                                                'XMLComplexTypeBarline', 'XMLComplexTypeEnding', 'XMLComplexTypeRepeat',
                                                'XMLComplexTypeAccord', 'XMLComplexTypeAccordionRegistration', 'XMLComplexTypeBarre',
                                                'XMLComplexTypeBass', 'XMLComplexTypeHarmonyAlter', 'XMLComplexTypeBassStep',
                                                'XMLComplexTypeBeater', 'XMLComplexTypeBeatUnitTied', 'XMLComplexTypeBracket',
                                                'XMLComplexTypeDashes', 'XMLComplexTypeDegree', 'XMLComplexTypeDegreeAlter',
                                                'XMLComplexTypeDegreeType', 'XMLComplexTypeDegreeValue', 'XMLComplexTypeDirection',
                                                'XMLComplexTypeDirectionType', 'XMLComplexTypeEffect', 'XMLComplexTypeFeature',
                                                'XMLComplexTypeFirstFret', 'XMLComplexTypeFrame', 'XMLComplexTypeFrameNote',
                                                'XMLComplexTypeGlass', 'XMLComplexTypeGrouping', 'XMLComplexTypeHarmony',
                                                'XMLComplexTypeHarpPedals', 'XMLComplexTypeImage', 'XMLComplexTypeInstrumentChange',
                                                'XMLComplexTypeInversion', 'XMLComplexTypeKind', 'XMLComplexTypeListening',
                                                'XMLComplexTypeMeasureNumbering', 'XMLComplexTypeMembrane', 'XMLComplexTypeMetal',
                                                'XMLComplexTypeMetronome', 'XMLComplexTypeMetronomeBeam', 'XMLComplexTypeMetronomeNote',
                                                'XMLComplexTypeMetronomeTied', 'XMLComplexTypeMetronomeTuplet', 'XMLComplexTypeNumeral',
                                                'XMLComplexTypeNumeralKey', 'XMLComplexTypeNumeralRoot', 'XMLComplexTypeOctaveShift',
                                                'XMLComplexTypeOffset', 'XMLComplexTypeOtherDirection', 'XMLComplexTypeOtherListening',
                                                'XMLComplexTypePedal', 'XMLComplexTypePedalTuning', 'XMLComplexTypePerMinute',
                                                'XMLComplexTypePercussion', 'XMLComplexTypePitched', 'XMLComplexTypePrincipalVoice',
                                                'XMLComplexTypePrint', 'XMLComplexTypeRoot', 'XMLComplexTypeRootStep',
                                                'XMLComplexTypeScordatura', 'XMLComplexTypeSound', 'XMLComplexTypeStaffDivide',
                                                'XMLComplexTypeStick', 'XMLComplexTypeStringMute', 'XMLComplexTypeSwing',
                                                'XMLComplexTypeSync', 'XMLComplexTypeTimpani', 'XMLComplexTypeWedge', 'XMLComplexTypeWood',
                                                'XMLComplexTypeEncoding', 'XMLComplexTypeIdentification', 'XMLComplexTypeMiscellaneous',
                                                'XMLComplexTypeMiscellaneousField', 'XMLComplexTypeSupports', 'XMLComplexTypeAppearance',
                                                'XMLComplexTypeDistance', 'XMLComplexTypeGlyph', 'XMLComplexTypeLineWidth',
                                                'XMLComplexTypeMeasureLayout', 'XMLComplexTypeNoteSize', 'XMLComplexTypeOtherAppearance',
                                                'XMLComplexTypePageLayout', 'XMLComplexTypePageMargins', 'XMLComplexTypeScaling',
                                                'XMLComplexTypeStaffLayout', 'XMLComplexTypeSystemDividers', 'XMLComplexTypeSystemLayout',
                                                'XMLComplexTypeSystemMargins', 'XMLComplexTypeBookmark', 'XMLComplexTypeLink',
                                                'XMLComplexTypeAccidental', 'XMLComplexTypeAccidentalMark', 'XMLComplexTypeArpeggiate',
                                                'XMLComplexTypeArticulations', 'XMLComplexTypeArrow', 'XMLComplexTypeAssess',
                                                'XMLComplexTypeBackup', 'XMLComplexTypeBeam', 'XMLComplexTypeBend',
                                                'XMLComplexTypeBreathMark', 'XMLComplexTypeCaesura', 'XMLComplexTypeElision',
                                                'XMLComplexTypeEmptyLine', 'XMLComplexTypeExtend', 'XMLComplexTypeFigure',
                                                'XMLComplexTypeFiguredBass', 'XMLComplexTypeForward', 'XMLComplexTypeGlissando',
                                                'XMLComplexTypeGrace', 'XMLComplexTypeHammerOnPullOff', 'XMLComplexTypeHandbell',
                                                'XMLComplexTypeHarmonClosed', 'XMLComplexTypeHarmonMute', 'XMLComplexTypeHarmonic',
                                                'XMLComplexTypeHeelToe', 'XMLComplexTypeHole', 'XMLComplexTypeHoleClosed',
                                                'XMLComplexTypeInstrument', 'XMLComplexTypeListen', 'XMLComplexTypeLyric',
                                                'XMLComplexTypeMordent', 'XMLComplexTypeNonArpeggiate', 'XMLComplexTypeNotations',
                                                'XMLComplexTypeNote', 'XMLComplexTypeNoteType', 'XMLComplexTypeNotehead',
                                                'XMLComplexTypeNoteheadText', 'XMLComplexTypeOrnaments', 'XMLComplexTypeOtherNotation',
                                                'XMLComplexTypeOtherPlacementText', 'XMLComplexTypeOtherText', 'XMLComplexTypePitch',
                                                'XMLComplexTypePlacementText', 'XMLComplexTypeRelease', 'XMLComplexTypeRest',
                                                'XMLComplexTypeSlide', 'XMLComplexTypeSlur', 'XMLComplexTypeStem',
                                                'XMLComplexTypeStrongAccent', 'XMLComplexTypeStyleText', 'XMLComplexTypeTap',
                                                'XMLComplexTypeTechnical', 'XMLComplexTypeTextElementData', 'XMLComplexTypeTie',
                                                'XMLComplexTypeTied', 'XMLComplexTypeTimeModification', 'XMLComplexTypeTremolo',
                                                'XMLComplexTypeTuplet', 'XMLComplexTypeTupletDot', 'XMLComplexTypeTupletNumber',
                                                'XMLComplexTypeTupletPortion', 'XMLComplexTypeTupletType', 'XMLComplexTypeUnpitched',
                                                'XMLComplexTypeWait', 'XMLComplexTypeCredit', 'XMLComplexTypeDefaults',
                                                'XMLComplexTypeEmptyFont', 'XMLComplexTypeGroupBarline', 'XMLComplexTypeGroupName',
                                                'XMLComplexTypeGroupSymbol', 'XMLComplexTypeInstrumentLink', 'XMLComplexTypeLyricFont',
                                                'XMLComplexTypeLyricLanguage', 'XMLComplexTypeOpus', 'XMLComplexTypePartGroup',
                                                'XMLComplexTypePartLink', 'XMLComplexTypePartList', 'XMLComplexTypePartName',
                                                'XMLComplexTypePlayer', 'XMLComplexTypeScoreInstrument', 'XMLComplexTypeScorePart',
                                                'XMLComplexTypeVirtualInstrument', 'XMLComplexTypeWork']

    def test_generated_complex_type_xsd_snippet(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class can show corresponding xsd
        """
        print(XMLComplexTypeFingering.get_xsd())
        expected = """<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fingering">\n\t\t<xs:annotation>\n\t\t\t<xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>\n\t\t</xs:annotation>\n\t\t<xs:simpleContent>\n\t\t\t<xs:extension base="xs:string">\n\t\t\t\t<xs:attribute name="substitution" type="yes-no" />\n\t\t\t\t<xs:attribute name="alternate" type="yes-no" />\n\t\t\t\t<xs:attributeGroup ref="print-style" />\n\t\t\t\t<xs:attributeGroup ref="placement" />\n\t\t\t</xs:extension>\n\t\t</xs:simpleContent>\n\t</xs:complexType>\n"""
        assert XMLComplexTypeFingering.get_xsd() == expected

    def test_generated_simple_type_doc_string_from_annotation(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class has a documentation string
        matching its xsd annotation
        """
        assert isinstance(XMLComplexTypeFingering, type(XMLComplexType))
        assert XMLComplexTypeFingering.__doc__ == 'Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.'

    def test_complex_type_xsd_is_converted_to_classes(self):
        """
        Test that all XMLComplexType classes are generated
        """
        for complex_type in self.all_complex_type_xsd_elements:
            module = importlib.import_module('musicxml.types.complextype')
            complex_type_class = getattr(module, complex_type.xml_tree_class_name)
            assert complex_type.xml_tree_class_name == complex_type_class.__name__
