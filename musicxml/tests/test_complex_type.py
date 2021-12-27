import importlib

from musicxml.types.complextype import xsd_complex_type_class_names
from musicxml.util.helperclasses import MusicXmlTestCase

from musicxml.types.complextype import XSDComplexType, XSDComplexTypeFingering


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
        print(XSDComplexTypeFingering.get_xsd())
        expected = """<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="fingering">\n\t\t<xs:annotation>\n\t\t\t<xs:documentation>Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.</xs:documentation>\n\t\t</xs:annotation>\n\t\t<xs:simpleContent>\n\t\t\t<xs:extension base="xs:string">\n\t\t\t\t<xs:attribute name="substitution" type="yes-no" />\n\t\t\t\t<xs:attribute name="alternate" type="yes-no" />\n\t\t\t\t<xs:attributeGroup ref="print-style" />\n\t\t\t\t<xs:attributeGroup ref="placement" />\n\t\t\t</xs:extension>\n\t\t</xs:simpleContent>\n\t</xs:complexType>\n"""
        assert XSDComplexTypeFingering.get_xsd() == expected

    def test_generated_simple_type_doc_string_from_annotation(self):
        """
        Test that the instance of an in module musicxml.types.complextype generated class has a documentation string
        matching its xsd annotation
        """
        assert isinstance(XSDComplexTypeFingering, type(XSDComplexType))
        assert XSDComplexTypeFingering.__doc__ == 'Fingering is typically indicated 1,2,3,4,5. Multiple fingerings may be given, typically to substitute fingerings in the middle of a note. The substitution and alternate values are "no" if the attribute is not present. For guitar and other fretted instruments, the fingering element represents the fretting finger; the pluck element represents the plucking finger.'

    def test_complex_type_xsd_is_converted_to_classes(self):
        """
        Test that all XSDComplexType classes are generated
        """
        for complex_type in self.all_complex_type_xsd_elements:
            module = importlib.import_module('musicxml.types.complextype')
            complex_type_class = getattr(module, complex_type.xsd_tree_class_name)
            assert complex_type.xsd_tree_class_name == complex_type_class.__name__
