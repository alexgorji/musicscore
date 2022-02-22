import copy
from unittest import TestCase

from musicxml.util.core import convert_to_xml_class_name, show_force_valid
from musicxml.xmlelement.exceptions import XMLChildContainerWrongElementError, XMLChildContainerMaxOccursError, \
    XMLChildContainerChoiceHasAnotherChosenChild, XMLChildContainerFactoryError
from musicxml.xmlelement.xmlchildcontainer import XMLChildContainer, DuplicationXSDSequence, XMLChildContainerFactory
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdelement import XSDElement
from musicxml.xsd.xsdindicator import *
from musicxml.xsd.xsdtree import XSDTree
import xml.etree.ElementTree as ET


class TestChildContainer(TestCase):
    def setUp(self) -> None:
        element_xsd = '<xs:element xmlns:xs="http://www.w3.org/2001/XMLSchema" name="alter" type="semitones" minOccurs="0"/>'
        sequence_xsd = """
                <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <xs:element name="step" type="step"/>
                    <xs:element name="alter" type="semitones" minOccurs="0"/>
                    <xs:element name="octave" type="octave"/>
                </xs:sequence>
        """
        choice_xsd = """<xs:choice xmlns:xs="http://www.w3.org/2001/XMLSchema">
                <xs:element name="pitch" type="pitch"/>
                <xs:element name="unpitched" type="unpitched"/>
                <xs:element name="rest" type="rest"/>
            </xs:choice>
        """
        self.element = XSDElement(XSDTree(ET.fromstring(element_xsd)))
        self.sequence = XSDSequence(XSDTree(ET.fromstring(sequence_xsd)))
        self.choice = XSDChoice(XSDTree(ET.fromstring(choice_xsd)))

    def test_children_container_node_type(self):
        """
        Test that an XMLChildContainer must initiate with an XSDElement, XSDGroup, XSDSequence or
        XSDChoice instances.
        """

        XMLChildContainer(self.element)
        XMLChildContainer(self.sequence)
        XMLChildContainer(self.choice)
        XMLChildContainer(XSDGroupEditorial())
        with self.assertRaises(TypeError):
            XMLChildContainer()
        with self.assertRaises(TypeError):
            XMLChildContainer(3)

    def test_min_max_occurrences(self):
        container = XMLChildContainer(self.element)
        assert container.min_occurrences == 1
        assert container.max_occurrences == 1
        container = XMLChildContainer(self.element, min_occurrences='0')
        assert container.min_occurrences == 0
        container = XMLChildContainer(self.element, max_occurrences='2')
        assert container.max_occurrences == 2
        container = XMLChildContainer(self.element, max_occurrences='unbounded')
        assert container.max_occurrences == 'unbounded'

    def test_that_all_complex_types_can_create_child_container(self):
        from musicxml.xsd.xsdcomplextype import __all__
        complex_types_with_child_container = []
        complex_types_without_child_container = []
        for complex_type_name in __all__[1:]:
            complex_type = eval(complex_type_name)
            try:
                XMLChildContainerFactory(complex_type).get_child_container()
                complex_types_with_child_container.append(complex_type_name)
            except XMLChildContainerFactoryError:
                complex_types_without_child_container.append(complex_type_name)
                # print(complex_type.get_xsd())

        assert set(complex_types_with_child_container) == {'XSDComplexTypeDynamics', 'XSDComplexTypeMidiInstrument',
                                                           'XSDComplexTypeNameDisplay', 'XSDComplexTypePlay', 'XSDComplexTypeAttributes',
                                                           'XSDComplexTypeBeatRepeat', 'XSDComplexTypeClef', 'XSDComplexTypeForPart',
                                                           'XSDComplexTypeInterchangeable', 'XSDComplexTypeKey',
                                                           'XSDComplexTypeMeasureStyle',
                                                           'XSDComplexTypePartClef', 'XSDComplexTypePartTranspose', 'XSDComplexTypeSlash',
                                                           'XSDComplexTypeStaffDetails', 'XSDComplexTypeStaffTuning', 'XSDComplexTypeTime',
                                                           'XSDComplexTypeTranspose', 'XSDComplexTypeBarline', 'XSDComplexTypeAccord',
                                                           'XSDComplexTypeAccordionRegistration', 'XSDComplexTypeBass',
                                                           'XSDComplexTypeBeatUnitTied', 'XSDComplexTypeDegree', 'XSDComplexTypeDirection',
                                                           'XSDComplexTypeDirectionType', 'XSDComplexTypeFrame', 'XSDComplexTypeFrameNote',
                                                           'XSDComplexTypeGrouping', 'XSDComplexTypeHarmony', 'XSDComplexTypeHarpPedals',
                                                           'XSDComplexTypeInstrumentChange', 'XSDComplexTypeListening',
                                                           'XSDComplexTypeMetronome', 'XSDComplexTypeMetronomeNote',
                                                           'XSDComplexTypeMetronomeTuplet', 'XSDComplexTypeNumeral',
                                                           'XSDComplexTypeNumeralKey', 'XSDComplexTypePedalTuning',
                                                           'XSDComplexTypePercussion',
                                                           'XSDComplexTypePrint', 'XSDComplexTypeRoot', 'XSDComplexTypeScordatura',
                                                           'XSDComplexTypeSound', 'XSDComplexTypeStick', 'XSDComplexTypeSwing',
                                                           'XSDComplexTypeEncoding', 'XSDComplexTypeIdentification',
                                                           'XSDComplexTypeMiscellaneous', 'XSDComplexTypeAppearance',
                                                           'XSDComplexTypeMeasureLayout', 'XSDComplexTypePageLayout',
                                                           'XSDComplexTypePageMargins', 'XSDComplexTypeScaling',
                                                           'XSDComplexTypeStaffLayout',
                                                           'XSDComplexTypeSystemDividers', 'XSDComplexTypeSystemLayout',
                                                           'XSDComplexTypeSystemMargins', 'XSDComplexTypeArticulations',
                                                           'XSDComplexTypeArrow',
                                                           'XSDComplexTypeBackup', 'XSDComplexTypeBend', 'XSDComplexTypeFigure',
                                                           'XSDComplexTypeFiguredBass', 'XSDComplexTypeForward', 'XSDComplexTypeHarmonMute',
                                                           'XSDComplexTypeHarmonic', 'XSDComplexTypeHole', 'XSDComplexTypeListen',
                                                           'XSDComplexTypeLyric', 'XSDComplexTypeNotations', 'XSDComplexTypeNote',
                                                           'XSDComplexTypeNoteheadText', 'XSDComplexTypeOrnaments', 'XSDComplexTypePitch',
                                                           'XSDComplexTypeRest', 'XSDComplexTypeTechnical',
                                                           'XSDComplexTypeTimeModification',
                                                           'XSDComplexTypeTuplet', 'XSDComplexTypeTupletPortion', 'XSDComplexTypeUnpitched',
                                                           'XSDComplexTypeCredit', 'XSDComplexTypeDefaults', 'XSDComplexTypePartGroup',
                                                           'XSDComplexTypePartLink', 'XSDComplexTypePartList', 'XSDComplexTypePlayer',
                                                           'XSDComplexTypeScoreInstrument', 'XSDComplexTypeScorePart',
                                                           'XSDComplexTypeVirtualInstrument', 'XSDComplexTypeWork',
                                                           'XSDComplexTypeScorePartwise', 'XSDComplexTypePart', 'XSDComplexTypeMeasure',
                                                           }
        assert complex_types_without_child_container == ['XSDComplexTypeDirective', 'XSDComplexTypeAccidentalText', 'XSDComplexTypeCoda',
                                                         'XSDComplexTypeEmpty', 'XSDComplexTypeEmptyPlacement',
                                                         'XSDComplexTypeEmptyPlacementSmufl', 'XSDComplexTypeEmptyPrintStyle',
                                                         'XSDComplexTypeEmptyPrintStyleAlign', 'XSDComplexTypeEmptyPrintStyleAlignId',
                                                         'XSDComplexTypeEmptyPrintObjectStyleAlign', 'XSDComplexTypeEmptyTrillSound',
                                                         'XSDComplexTypeHorizontalTurn', 'XSDComplexTypeFermata', 'XSDComplexTypeFingering',
                                                         'XSDComplexTypeFormattedSymbol', 'XSDComplexTypeFormattedSymbolId',
                                                         'XSDComplexTypeFormattedText', 'XSDComplexTypeFormattedTextId',
                                                         'XSDComplexTypeFret', 'XSDComplexTypeLevel', 'XSDComplexTypeMidiDevice',
                                                         'XSDComplexTypeOtherPlay', 'XSDComplexTypeSegno', 'XSDComplexTypeString',
                                                         'XSDComplexTypeTypedText', 'XSDComplexTypeWavyLine', 'XSDComplexTypeCancel',
                                                         'XSDComplexTypeDouble', 'XSDComplexTypeKeyAccidental', 'XSDComplexTypeKeyOctave',
                                                         'XSDComplexTypeLineDetail', 'XSDComplexTypeMeasureRepeat',
                                                         'XSDComplexTypeMultipleRest', 'XSDComplexTypePartSymbol',
                                                         'XSDComplexTypeStaffSize', 'XSDComplexTypeBarStyleColor', 'XSDComplexTypeEnding',
                                                         'XSDComplexTypeRepeat', 'XSDComplexTypeBarre', 'XSDComplexTypeHarmonyAlter',
                                                         'XSDComplexTypeBassStep', 'XSDComplexTypeBeater', 'XSDComplexTypeBracket',
                                                         'XSDComplexTypeDashes', 'XSDComplexTypeDegreeAlter', 'XSDComplexTypeDegreeType',
                                                         'XSDComplexTypeDegreeValue', 'XSDComplexTypeEffect', 'XSDComplexTypeFeature',
                                                         'XSDComplexTypeFirstFret', 'XSDComplexTypeGlass', 'XSDComplexTypeImage',
                                                         'XSDComplexTypeInversion', 'XSDComplexTypeKind', 'XSDComplexTypeMeasureNumbering',
                                                         'XSDComplexTypeMembrane', 'XSDComplexTypeMetal', 'XSDComplexTypeMetronomeBeam',
                                                         'XSDComplexTypeMetronomeTied', 'XSDComplexTypeNumeralRoot',
                                                         'XSDComplexTypeOctaveShift', 'XSDComplexTypeOffset',
                                                         'XSDComplexTypeOtherDirection', 'XSDComplexTypeOtherListening',
                                                         'XSDComplexTypePedal', 'XSDComplexTypePerMinute', 'XSDComplexTypePitched',
                                                         'XSDComplexTypePrincipalVoice', 'XSDComplexTypeRootStep',
                                                         'XSDComplexTypeStaffDivide', 'XSDComplexTypeStringMute', 'XSDComplexTypeSync',
                                                         'XSDComplexTypeTimpani', 'XSDComplexTypeWedge', 'XSDComplexTypeWood',
                                                         'XSDComplexTypeMiscellaneousField', 'XSDComplexTypeSupports',
                                                         'XSDComplexTypeDistance', 'XSDComplexTypeGlyph', 'XSDComplexTypeLineWidth',
                                                         'XSDComplexTypeNoteSize', 'XSDComplexTypeOtherAppearance',
                                                         'XSDComplexTypeBookmark', 'XSDComplexTypeLink', 'XSDComplexTypeAccidental',
                                                         'XSDComplexTypeAccidentalMark', 'XSDComplexTypeArpeggiate', 'XSDComplexTypeAssess',
                                                         'XSDComplexTypeBeam', 'XSDComplexTypeBreathMark', 'XSDComplexTypeCaesura',
                                                         'XSDComplexTypeElision', 'XSDComplexTypeEmptyLine', 'XSDComplexTypeExtend',
                                                         'XSDComplexTypeGlissando', 'XSDComplexTypeGrace', 'XSDComplexTypeHammerOnPullOff',
                                                         'XSDComplexTypeHandbell', 'XSDComplexTypeHarmonClosed', 'XSDComplexTypeHeelToe',
                                                         'XSDComplexTypeHoleClosed', 'XSDComplexTypeInstrument', 'XSDComplexTypeMordent',
                                                         'XSDComplexTypeNonArpeggiate', 'XSDComplexTypeNoteType', 'XSDComplexTypeNotehead',
                                                         'XSDComplexTypeOtherNotation', 'XSDComplexTypeOtherPlacementText',
                                                         'XSDComplexTypeOtherText', 'XSDComplexTypePlacementText', 'XSDComplexTypeRelease',
                                                         'XSDComplexTypeSlide', 'XSDComplexTypeSlur', 'XSDComplexTypeStem',
                                                         'XSDComplexTypeStrongAccent', 'XSDComplexTypeStyleText', 'XSDComplexTypeTap',
                                                         'XSDComplexTypeTextElementData', 'XSDComplexTypeTie', 'XSDComplexTypeTied',
                                                         'XSDComplexTypeTremolo', 'XSDComplexTypeTupletDot', 'XSDComplexTypeTupletNumber',
                                                         'XSDComplexTypeTupletType', 'XSDComplexTypeWait', 'XSDComplexTypeEmptyFont',
                                                         'XSDComplexTypeGroupBarline', 'XSDComplexTypeGroupName',
                                                         'XSDComplexTypeGroupSymbol', 'XSDComplexTypeInstrumentLink',
                                                         'XSDComplexTypeLyricFont', 'XSDComplexTypeLyricLanguage', 'XSDComplexTypeOpus',
                                                         'XSDComplexTypePartName']

    def test_complex_type_with_complex_content_child_container(self):
        """
        complexType@name=metronome-tuplet
            complexContent
                extension@base=time-modification
                    attribute@name=type@type=start-stop@use=required
                    attribute@name=bracket@type=yes-no
                    attribute@name=show-number@type=show-tuplet
        """
        container = XMLChildContainerFactory(XSDComplexTypeMetronomeTuplet).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=actual-notes@minOccurs=1@maxOccurs=1
    Element@name=normal-notes@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=0@maxOccurs=1
        Element@name=normal-type@minOccurs=1@maxOccurs=1
        Element@name=normal-dot@minOccurs=0@maxOccurs=unbounded
"""
        assert container.tree_representation() == expected

    def test_complex_type_with_group_child_container(self):
        """
        complexType@name=system-margins
            group@ref=left-right-margins
        """
        container = XMLChildContainerFactory(XSDComplexTypeSystemMargins).get_child_container()
        expected = """Group@name=left-right-margins@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=1@maxOccurs=1
        Element@name=left-margin@minOccurs=1@maxOccurs=1
        Element@name=right-margin@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_complex_type_measure_child_container(self):
        """
        element@name=measure@maxOccurs=unbounded
            complexType
                group@ref=music-data
                attributeGroup@ref=measure-attributes
        """
        container = XMLChildContainerFactory(XSDComplexTypeMeasure).get_child_container()
        expected = """Group@name=music-data@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=1@maxOccurs=1
        Choice@minOccurs=0@maxOccurs=unbounded
            Element@name=note@minOccurs=1@maxOccurs=1
            Element@name=backup@minOccurs=1@maxOccurs=1
            Element@name=forward@minOccurs=1@maxOccurs=1
            Element@name=direction@minOccurs=1@maxOccurs=1
            Element@name=attributes@minOccurs=1@maxOccurs=1
            Element@name=harmony@minOccurs=1@maxOccurs=1
            Element@name=figured-bass@minOccurs=1@maxOccurs=1
            Element@name=print@minOccurs=1@maxOccurs=1
            Element@name=sound@minOccurs=1@maxOccurs=1
            Element@name=listening@minOccurs=1@maxOccurs=1
            Element@name=barline@minOccurs=1@maxOccurs=1
            Element@name=grouping@minOccurs=1@maxOccurs=1
            Element@name=link@minOccurs=1@maxOccurs=1
            Element@name=bookmark@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_children_container_compact_repr(self):
        """
        Test that children container has a compact_repr attribute
        """
        container = XMLChildContainer(self.element, min_occurrences=0)
        assert container.compact_repr == 'Element@name=alter@minOccurs=0@maxOccurs=1'
        container = XMLChildContainer(self.sequence)
        assert container.compact_repr == 'Sequence@minOccurs=1@maxOccurs=1'
        container = XMLChildContainer(self.choice, min_occurrences=0, max_occurrences='unbounded')
        assert container.compact_repr == 'Choice@minOccurs=0@maxOccurs=unbounded'
        container = XMLChildContainer(XSDGroupEditorial(), min_occurrences=1, max_occurrences=2)
        assert container.compact_repr == 'Group@name=editorial@minOccurs=1@maxOccurs=2'

    def test_child_container_simple_sequence(self):
        """
        Test a complex type with a simple sequence of elements
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePitch).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=step@minOccurs=1@maxOccurs=1
    Element@name=alter@minOccurs=0@maxOccurs=1
    Element@name=octave@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

        container.add_element(XMLStep('A'))
        container.add_element(XMLOctave(2))

        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=step@minOccurs=1@maxOccurs=1
        XMLStep
    Element@name=alter@minOccurs=0@maxOccurs=1
    Element@name=octave@minOccurs=1@maxOccurs=1
        XMLOctave
"""
        assert container.tree_representation() == expected
        with self.assertRaises(XMLChildContainerWrongElementError):
            container.add_element(XMLAccent())
        with self.assertRaises(XMLChildContainerMaxOccursError):
            container.add_element(XMLStep('B'))

    def test_child_container_sequence_with_sequence(self):
        """
        Test a complex type with a sequence which has elements and sequences
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeStaffDetails).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=staff-type@minOccurs=0@maxOccurs=1
    Sequence@minOccurs=0@maxOccurs=1
        Element@name=staff-lines@minOccurs=1@maxOccurs=1
        Element@name=line-detail@minOccurs=0@maxOccurs=unbounded
    Element@name=staff-tuning@minOccurs=0@maxOccurs=unbounded
    Element@name=capo@minOccurs=0@maxOccurs=1
    Element@name=staff-size@minOccurs=0@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_child_container_sequence_with_group(self):
        """
        Test a complex type with a sequence of groups an elements
        """

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeInterchangeable).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=time-relation@minOccurs=0@maxOccurs=1
    Group@name=time-signature@minOccurs=1@maxOccurs=unbounded
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=beats@minOccurs=1@maxOccurs=1
            Element@name=beat-type@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_child_container_sequence_with_choice(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Choice@minOccurs=1@maxOccurs=1
        Group@name=traditional-key@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=cancel@minOccurs=0@maxOccurs=1
                Element@name=fifths@minOccurs=1@maxOccurs=1
                Element@name=mode@minOccurs=0@maxOccurs=1
        Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=key-step@minOccurs=1@maxOccurs=1
                Element@name=key-alter@minOccurs=1@maxOccurs=1
                Element@name=key-accidental@minOccurs=0@maxOccurs=1
    Element@name=key-octave@minOccurs=0@maxOccurs=unbounded
"""
        assert container.tree_representation() == expected

    def test_child_container_complex_sequence_with_group_and_choice(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeAttributes).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Group@name=editorial@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Group@name=footnote@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=footnote@minOccurs=1@maxOccurs=1
            Group@name=level@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=level@minOccurs=1@maxOccurs=1
    Element@name=divisions@minOccurs=0@maxOccurs=1
    Element@name=key@minOccurs=0@maxOccurs=unbounded
    Element@name=time@minOccurs=0@maxOccurs=unbounded
    Element@name=staves@minOccurs=0@maxOccurs=1
    Element@name=part-symbol@minOccurs=0@maxOccurs=1
    Element@name=instruments@minOccurs=0@maxOccurs=1
    Element@name=clef@minOccurs=0@maxOccurs=unbounded
    Element@name=staff-details@minOccurs=0@maxOccurs=unbounded
    Choice@minOccurs=1@maxOccurs=1
        Element@name=transpose@minOccurs=0@maxOccurs=unbounded
        Element@name=for-part@minOccurs=0@maxOccurs=unbounded
    Element@name=directive@minOccurs=0@maxOccurs=unbounded
    Element@name=measure-style@minOccurs=0@maxOccurs=unbounded
"""
        assert container.tree_representation() == expected

    def test_child_container_simple_choice(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasureStyle).get_child_container()
        expected = """Choice@minOccurs=1@maxOccurs=1
    Element@name=multiple-rest@minOccurs=1@maxOccurs=1
    Element@name=measure-repeat@minOccurs=1@maxOccurs=1
    Element@name=beat-repeat@minOccurs=1@maxOccurs=1
    Element@name=slash@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_child_container_simple_choice_adding_child(self):
        """
        Test a complex type with a simple choice of elements can manage children.
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasureStyle).get_child_container()
        container.add_element(XMLMultipleRest(1))

        expected = """Choice@minOccurs=1@maxOccurs=1
    Element@name=multiple-rest@minOccurs=1@maxOccurs=1
        XMLMultipleRest
    Element@name=measure-repeat@minOccurs=1@maxOccurs=1
    Element@name=beat-repeat@minOccurs=1@maxOccurs=1
    Element@name=slash@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected
        with self.assertRaises(XMLChildContainerWrongElementError):
            container.add_element(XMLAccent())
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLBeatRepeat())

    def test_score_partwise_child_container(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeScorePartwise).get_child_container()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Group@name=score-header@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=work@minOccurs=0@maxOccurs=1
            Element@name=movement-number@minOccurs=0@maxOccurs=1
            Element@name=movement-title@minOccurs=0@maxOccurs=1
            Element@name=identification@minOccurs=0@maxOccurs=1
            Element@name=defaults@minOccurs=0@maxOccurs=1
            Element@name=credit@minOccurs=0@maxOccurs=unbounded
            Element@name=part-list@minOccurs=1@maxOccurs=1
    Element@name=part@minOccurs=1@maxOccurs=unbounded
"""
        assert container.tree_representation() == expected
        container.add_element(XMLPartList())

        with self.assertRaises(XMLChildContainerMaxOccursError):
            container.add_element(XMLPartList())
        container.add_element(XMLPart())
        container.add_element(XMLPart())
        container.check_required_elements()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Group@name=score-header@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=work@minOccurs=0@maxOccurs=1
            Element@name=movement-number@minOccurs=0@maxOccurs=1
            Element@name=movement-title@minOccurs=0@maxOccurs=1
            Element@name=identification@minOccurs=0@maxOccurs=1
            Element@name=defaults@minOccurs=0@maxOccurs=1
            Element@name=credit@minOccurs=0@maxOccurs=unbounded
            Element@name=part-list@minOccurs=1@maxOccurs=1
                XMLPartList
    Element@name=part@minOccurs=1@maxOccurs=unbounded
        XMLPart
        XMLPart
"""
        assert container.tree_representation() == expected

    def test_part_and_measure_child_container(self):
        part_expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=measure@minOccurs=1@maxOccurs=unbounded
"""
        measure_expected = """Group@name=music-data@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=1@maxOccurs=1
        Choice@minOccurs=0@maxOccurs=unbounded
            Element@name=note@minOccurs=1@maxOccurs=1
            Element@name=backup@minOccurs=1@maxOccurs=1
            Element@name=forward@minOccurs=1@maxOccurs=1
            Element@name=direction@minOccurs=1@maxOccurs=1
            Element@name=attributes@minOccurs=1@maxOccurs=1
            Element@name=harmony@minOccurs=1@maxOccurs=1
            Element@name=figured-bass@minOccurs=1@maxOccurs=1
            Element@name=print@minOccurs=1@maxOccurs=1
            Element@name=sound@minOccurs=1@maxOccurs=1
            Element@name=listening@minOccurs=1@maxOccurs=1
            Element@name=barline@minOccurs=1@maxOccurs=1
            Element@name=grouping@minOccurs=1@maxOccurs=1
            Element@name=link@minOccurs=1@maxOccurs=1
            Element@name=bookmark@minOccurs=1@maxOccurs=1
"""
        part_container = XMLChildContainerFactory(complex_type=XSDComplexTypePart).get_child_container()
        measure_container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasure).get_child_container()
        assert part_container.tree_representation() == part_expected
        assert measure_container.tree_representation() == measure_expected

    def test_metronome_child_container(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMetronome).get_child_container()
        expected = """Choice@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=1@maxOccurs=1
        Group@name=beat-unit@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=beat-unit@minOccurs=1@maxOccurs=1
                Element@name=beat-unit-dot@minOccurs=0@maxOccurs=unbounded
        Element@name=beat-unit-tied@minOccurs=0@maxOccurs=unbounded
        Choice@minOccurs=1@maxOccurs=1
            Element@name=per-minute@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Group@name=beat-unit@minOccurs=1@maxOccurs=1
                    Sequence@minOccurs=1@maxOccurs=1
                        Element@name=beat-unit@minOccurs=1@maxOccurs=1
                        Element@name=beat-unit-dot@minOccurs=0@maxOccurs=unbounded
                Element@name=beat-unit-tied@minOccurs=0@maxOccurs=unbounded
    Sequence@minOccurs=1@maxOccurs=1
        Element@name=metronome-arrows@minOccurs=0@maxOccurs=1
        Element@name=metronome-note@minOccurs=1@maxOccurs=unbounded
        Sequence@minOccurs=0@maxOccurs=1
            Element@name=metronome-relation@minOccurs=1@maxOccurs=1
            Element@name=metronome-note@minOccurs=1@maxOccurs=unbounded
"""
        assert container.tree_representation() == expected

    def test_add_child_lyric(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        container.check_required_elements()
        choice = container.get_children()[0]
        assert choice.requirements_not_fulfilled is True
        container.add_element(XMLHumming())
        assert choice.requirements_not_fulfilled is False
        assert choice.chosen_child == choice.get_children()[3]
        with self.assertRaises(XMLChildContainerMaxOccursError):
            container.add_element(XMLHumming())
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLLaughing())
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLText('huhu'))
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLSyllabic('begin'))

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        choice = container.get_children()[0]
        container.check_required_elements()
        container.add_element(XMLElision('something'))
        assert choice.chosen_child == choice.get_children()[0]
        container.add_element(XMLText('something'))
        container.add_element(XMLText('something'))
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLLaughing())

        container.add_element(XMLText('something'))
        container.add_element(XMLSyllabic('end'), forward=1)
        expected = """        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Element@name=syllabic@minOccurs=0@maxOccurs=1
            Element@name=text@minOccurs=1@maxOccurs=1
                XMLText
            Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                Sequence@minOccurs=0@maxOccurs=unbounded: !!!FORCED!!!
                    Sequence@minOccurs=0@maxOccurs=1: !!!FORCED!!!
                        Element@name=elision@minOccurs=1@maxOccurs=1
                            XMLElision
                        Element@name=syllabic@minOccurs=0@maxOccurs=1
                            XMLSyllabic
                    Element@name=text@minOccurs=1@maxOccurs=1
                        XMLText
                Sequence@minOccurs=0@maxOccurs=unbounded: !!!FORCED!!!
                    Sequence@minOccurs=0@maxOccurs=1
                        Element@name=elision@minOccurs=1@maxOccurs=1
                        Element@name=syllabic@minOccurs=0@maxOccurs=1
                    Element@name=text@minOccurs=1@maxOccurs=1
                        XMLText
            Element@name=extend@minOccurs=0@maxOccurs=1
"""
        assert choice.chosen_child.tree_representation(show_force_valid) == expected

    def test_add_child_note(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
        container.check_required_elements()
        choice = container.get_children()[0]
        selected = container.add_element(XMLPitch())
        assert selected.get_parent().chosen_child == selected
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Choice@minOccurs=1@maxOccurs=1: !!Chosen Child!!
        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=chord@minOccurs=0@maxOccurs=1
                    Choice@minOccurs=1@maxOccurs=1: !!Chosen Child!!
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                            XMLPitch
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=duration@minOccurs=1@maxOccurs=1
                        !Required!
            Element@name=tie@minOccurs=0@maxOccurs=2
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=cue@minOccurs=1@maxOccurs=1
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=chord@minOccurs=0@maxOccurs=1
                    Choice@minOccurs=1@maxOccurs=1
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=duration@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=grace@minOccurs=1@maxOccurs=1
            Choice@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
                    Element@name=tie@minOccurs=0@maxOccurs=2
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=cue@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
    Element@name=instrument@minOccurs=0@maxOccurs=unbounded
    Group@name=editorial-voice@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Group@name=footnote@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=footnote@minOccurs=1@maxOccurs=1
            Group@name=level@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=level@minOccurs=1@maxOccurs=1
            Group@name=voice@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=voice@minOccurs=1@maxOccurs=1
    Element@name=type@minOccurs=0@maxOccurs=1
    Element@name=dot@minOccurs=0@maxOccurs=unbounded
    Element@name=accidental@minOccurs=0@maxOccurs=1
    Element@name=time-modification@minOccurs=0@maxOccurs=1
    Element@name=stem@minOccurs=0@maxOccurs=1
    Element@name=notehead@minOccurs=0@maxOccurs=1
    Element@name=notehead-text@minOccurs=0@maxOccurs=1
    Group@name=staff@minOccurs=0@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=staff@minOccurs=1@maxOccurs=1
    Element@name=beam@minOccurs=0@maxOccurs=8
    Element@name=notations@minOccurs=0@maxOccurs=unbounded
    Element@name=lyric@minOccurs=0@maxOccurs=unbounded
    Element@name=play@minOccurs=0@maxOccurs=1
    Element@name=listen@minOccurs=0@maxOccurs=1
"""
        container.check_required_elements()
        assert container.tree_representation(function=show_force_valid) == expected
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLUnpitched())
        container.add_element(XMLChord())
        container.check_required_elements()
        expected = """        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=chord@minOccurs=0@maxOccurs=1
                        XMLChord
                    Choice@minOccurs=1@maxOccurs=1: !!Chosen Child!!
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                            XMLPitch
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=duration@minOccurs=1@maxOccurs=1
                        !Required!
            Element@name=tie@minOccurs=0@maxOccurs=2
"""
        assert choice.chosen_child.tree_representation(function=show_force_valid) == expected
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLRest())
        container.add_element(XMLDuration(2))
        container.check_required_elements()
        expected = """        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=chord@minOccurs=0@maxOccurs=1
                        XMLChord
                    Choice@minOccurs=1@maxOccurs=1: !!Chosen Child!!
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                            XMLPitch
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=duration@minOccurs=1@maxOccurs=1
                        XMLDuration
            Element@name=tie@minOccurs=0@maxOccurs=2
"""
        assert choice.chosen_child.tree_representation(function=show_force_valid) == expected
        assert container.get_children()[0].requirements_not_fulfilled is False
        container.add_element(XMLVoice('1'))
        assert container.get_children()[0].requirements_not_fulfilled is False

    def test_container_with_unbounded_choice(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeDynamics).get_child_container()
        assert container.min_occurrences == 0
        assert container.max_occurrences == 'unbounded'

    def test_container_part_list(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePartList).get_child_container()
        container.check_required_elements()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Group@name=part-group@minOccurs=0@maxOccurs=unbounded
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=part-group@minOccurs=1@maxOccurs=1
    Group@name=score-part@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=score-part@minOccurs=1@maxOccurs=1
                !Required!
    Choice@minOccurs=0@maxOccurs=unbounded
        Group@name=part-group@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=part-group@minOccurs=1@maxOccurs=1
        Group@name=score-part@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=score-part@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation(show_force_valid) == expected
        container.check_required_elements()
        element = XMLScorePart()
        container.add_element(element)

        expected = """Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
    Group@name=part-group@minOccurs=0@maxOccurs=unbounded
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=part-group@minOccurs=1@maxOccurs=1
    Group@name=score-part@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Element@name=score-part@minOccurs=1@maxOccurs=1
                XMLScorePart
    Choice@minOccurs=0@maxOccurs=unbounded
        Group@name=part-group@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=part-group@minOccurs=1@maxOccurs=1
        Group@name=score-part@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=score-part@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation(show_force_valid) == expected

    def test_xsd_element_parent_content(self):
        """
        Test that if an xsd element is content of a child_container it can return parent_container.
        """

        container = XMLChildContainer(content=self.element)
        assert container.content.parent_container == container
        container = XMLChildContainer(content=self.sequence)
        for node in container.traverse():
            assert node.content.parent_container == node
        container = XMLChildContainer(content=self.choice)
        for node in container.traverse():
            assert node.content.parent_container == node
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePitch).get_child_container()
        for node in container.traverse():
            assert node.content.parent_container == node


class TestDuplication(TestCase):
    def test_duplication_sequence(self):
        ds = DuplicationXSDSequence()
        container = XMLChildContainer(content=ds)
        child_container = XMLChildContainerFactory(complex_type=XSDComplexTypeDynamics).get_child_container()
        ch1 = container.add_child(child_container)
        ch2 = container.add_child(child_container._create_empty_copy())
        assert container.get_children() == [ch1, ch2]

    def test_create_empty_copy(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
        first_group = container.get_children()[0].get_children()[0]
        first_group.add_element(XMLCancel(0))
        copied_group = first_group._create_empty_copy()
        expected = """Group@name=traditional-key@minOccurs=1@maxOccurs=1
    Sequence@minOccurs=1@maxOccurs=1
        Element@name=cancel@minOccurs=0@maxOccurs=1
        Element@name=fifths@minOccurs=1@maxOccurs=1
        Element@name=mode@minOccurs=0@maxOccurs=1
"""
        assert copied_group.tree_representation() == expected
        first_sequence = container.get_children()[0].get_children()[0].get_children()[0]
        copied_sequence = first_sequence._create_empty_copy()
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=cancel@minOccurs=0@maxOccurs=1
    Element@name=fifths@minOccurs=1@maxOccurs=1
    Element@name=mode@minOccurs=0@maxOccurs=1
"""
        assert copied_sequence.tree_representation() == expected

        choice = container.get_children()[0]
        copied_choice = choice._create_empty_copy()
        expected = """Choice@minOccurs=1@maxOccurs=1
    Group@name=traditional-key@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=cancel@minOccurs=0@maxOccurs=1
            Element@name=fifths@minOccurs=1@maxOccurs=1
            Element@name=mode@minOccurs=0@maxOccurs=1
    Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=key-step@minOccurs=1@maxOccurs=1
            Element@name=key-alter@minOccurs=1@maxOccurs=1
            Element@name=key-accidental@minOccurs=0@maxOccurs=1
"""
        assert copied_choice.tree_representation() == expected

    def test_add_duplication_parent(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
        """
        No parent
        """
        container._add_duplication_parent()
        assert isinstance(container.get_parent().content, DuplicationXSDSequence)
        """
        With parent
        """
        group = container.get_children()[0].get_children()[1]
        parent = group.get_parent()
        index = parent.get_children().index(group)
        group._add_duplication_parent()
        assert isinstance(group.get_parent().content, DuplicationXSDSequence)
        assert group.get_parent().get_parent() == parent
        assert parent.get_children().index(group.get_parent()) == index

    def test_duplicate_node(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
        container.add_element(XMLKeyAccidental('sharp'))
        unbounded_group = container.get_children()[0].get_children()[1]
        duplicated = unbounded_group.duplicate()
        assert duplicated.get_parent() == unbounded_group.get_parent()
        assert container.get_leaves(lambda x: x.content.name) == [
            (['cancel', 'fifths', 'mode'], [['key-step', 'key-alter', 'key-accidental'], ['key-step', 'key-alter', 'key-accidental']]),
            'key-octave']
        container.add_element(XMLKeyAccidental('sharp'))
        other_duplicated = unbounded_group.duplicate()
        assert duplicated.get_parent() == unbounded_group.get_parent()
        assert other_duplicated.get_parent() == duplicated.get_parent() == unbounded_group.get_parent()
        assert container.get_leaves(lambda x: x.content.name) == [
            (['cancel', 'fifths', 'mode'], [['key-step', 'key-alter', 'key-accidental'], ['key-step', 'key-alter', 'key-accidental'],
                                            ['key-step', 'key-alter', 'key-accidental']]),
            'key-octave']
        container.check_required_elements()
        container.add_element(XMLKeyAlter(1), 2)
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Choice@minOccurs=1@maxOccurs=1: !!Chosen Child!!
        Group@name=traditional-key@minOccurs=1@maxOccurs=1
            Sequence@minOccurs=1@maxOccurs=1
                Element@name=cancel@minOccurs=0@maxOccurs=1
                Element@name=fifths@minOccurs=1@maxOccurs=1
                Element@name=mode@minOccurs=0@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=key-step@minOccurs=1@maxOccurs=1
                        !Required!
                    Element@name=key-alter@minOccurs=1@maxOccurs=1
                        !Required!
                    Element@name=key-accidental@minOccurs=0@maxOccurs=1
                        XMLKeyAccidental
            Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=key-step@minOccurs=1@maxOccurs=1
                        !Required!
                    Element@name=key-alter@minOccurs=1@maxOccurs=1
                        !Required!
                    Element@name=key-accidental@minOccurs=0@maxOccurs=1
                        XMLKeyAccidental
            Group@name=non-traditional-key@minOccurs=0@maxOccurs=unbounded
                Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
                    Element@name=key-step@minOccurs=1@maxOccurs=1
                        !Required!
                    Element@name=key-alter@minOccurs=1@maxOccurs=1
                        XMLKeyAlter
                    Element@name=key-accidental@minOccurs=0@maxOccurs=1
    Element@name=key-octave@minOccurs=0@maxOccurs=unbounded
"""
        container.check_required_elements()
        assert container.tree_representation(show_force_valid) == expected

    def test_duplicate_parent(self):
        """
        Test that duplicate parent method of XMLChildContainer duplicates a parent with max
        occurrences greater one if exists on the path to root if a XSDElement
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeDynamics).get_child_container()
        element = container.get_children()[0]
        duplicated_parent = element._duplicate_parent_in_path()
        assert isinstance(duplicated_parent.content, XSDChoice)
        assert duplicated_parent.get_parent() == container.get_parent()

    def test_add_child_to_unbounded_choice_dynamics(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeDynamics).get_child_container()
        container.add_element(XMLPp())
        container.add_element(XMLPp())
        container.add_element(XMLPp())
        container.get_parent().add_element(XMLPp())
        assert len(container.get_parent().get_children()) == 4
        assert [leaf.content.xml_elements[0].__class__.__name__ for leaf in container.get_parent().iterate_leaves() if
                leaf.content.xml_elements] == ['XMLPp', 'XMLPp', 'XMLPp', 'XMLPp']

        container.add_element(XMLMf())
        assert len(container.get_parent().get_children()) == 5
        assert [leaf.content.xml_elements[0].__class__.__name__ for leaf in container.get_parent().iterate_leaves() if
                leaf.content.xml_elements] == ['XMLPp', 'XMLPp', 'XMLPp', 'XMLPp', 'XMLMf']

    def test_add_child_to_unbounded_choice_articulations(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeArticulations).get_child_container()
        accent = XMLAccent()
        staccato = XMLStaccato()
        container.add_element(accent)
        container.add_element(staccato)
        assert container.up.get_attached_elements() == [accent, staccato]


class TestChildContainerCheckRequired(TestCase):
    def test_get_all_leaves(self):
        func = lambda l: convert_to_xml_class_name(l.content.name)
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePitch).get_child_container()
        assert container.get_leaves(func) == ['XMLStep', 'XMLAlter', 'XMLOctave']

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeStaffDetails).get_child_container()
        assert container.get_leaves(func) == ['XMLStaffType', ['XMLStaffLines', 'XMLLineDetail'], 'XMLStaffTuning', 'XMLCapo',
                                              'XMLStaffSize']

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeInterchangeable).get_child_container()
        assert container.get_leaves(func) == ['XMLTimeRelation', ['XMLBeats', 'XMLBeatType']]

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        assert container.get_leaves(func) == [
            (
                ['XMLSyllabic', 'XMLText', [['XMLElision', 'XMLSyllabic'], 'XMLText'], 'XMLExtend'],
                'XMLExtend', 'XMLLaughing', 'XMLHumming'
            ), 'XMLEndLine', 'XMLEndParagraph', ['XMLFootnote', 'XMLLevel']
        ]
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
        assert container.get_leaves(func) == [
            (
                [['XMLChord', ('XMLPitch', 'XMLUnpitched', 'XMLRest')], 'XMLDuration', 'XMLTie'],
                ['XMLCue', ['XMLChord', ('XMLPitch', 'XMLUnpitched', 'XMLRest')], 'XMLDuration'],
                ['XMLGrace', ([['XMLChord', ('XMLPitch', 'XMLUnpitched', 'XMLRest')], 'XMLTie'],
                              ['XMLCue', ['XMLChord', ('XMLPitch', 'XMLUnpitched', 'XMLRest')]])]
            ),
            'XMLInstrument', ['XMLFootnote', 'XMLLevel', 'XMLVoice'], 'XMLType', 'XMLDot',
            'XMLAccidental', 'XMLTimeModification', 'XMLStem', 'XMLNotehead', 'XMLNoteheadText',
            'XMLStaff', 'XMLBeam', 'XMLNotations', 'XMLLyric', 'XMLPlay', 'XMLListen']

    def test_get_required_elements(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasureStyle).get_child_container()
        container.check_required_elements()
        assert container.get_required_element_names() == ('XMLMultipleRest', 'XMLMeasureRepeat', 'XMLBeatRepeat', 'XMLSlash')
        container.add_element(XMLSlash())
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNameDisplay).get_child_container()
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeKey).get_child_container()
        assert container.get_required_element_names() == ('XMLFifths', ['XMLKeyStep', 'XMLKeyAlter'])
        container.add_element(XMLFifths(0))
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeAttributes).get_child_container()
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeScorePartwise).get_child_container()
        assert container.get_required_element_names() == ['XMLPartList', 'XMLPart']
        container.add_element(XMLPart())
        assert container.get_required_element_names() == 'XMLPartList'
        container.add_element(XMLPartList())
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypePart).get_child_container()
        assert container.get_required_element_names() == 'XMLMeasure'
        container.add_element(XMLMeasure())
        assert container.get_required_element_names() is None

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasure).get_child_container()
        assert container.get_required_element_names() is None

    def test_lyric_required_elements(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        assert container.get_required_element_names() == ('XMLText', 'XMLExtend', 'XMLLaughing', 'XMLHumming')

        container.add_element(XMLText('something'))
        assert container.get_required_element_names() is None
        container.add_element(XMLElision('Something'))
        assert container.get_required_element_names() == 'XMLText'

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        container.add_element(XMLText('something'))
        assert container.get_required_element_names() is None
        container.add_element(XMLSyllabic('end'))
        assert container.get_required_element_names() is None
        container.add_element(XMLSyllabic('end'))
        assert container.get_required_element_names() == ['XMLElision', 'XMLText']

    def test_note_required_elements(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()

        assert container.get_required_element_names() == (
            [('XMLPitch', 'XMLUnpitched', 'XMLRest'), 'XMLDuration'], ['XMLCue', ('XMLPitch', 'XMLUnpitched', 'XMLRest'), 'XMLDuration'],
            ['XMLGrace', (('XMLPitch', 'XMLUnpitched', 'XMLRest'), ['XMLCue', ('XMLPitch', 'XMLUnpitched', 'XMLRest')])]
        )

        container.add_element(XMLPitch())

        assert container.get_required_element_names() == 'XMLDuration'

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
        choice = container.get_children()[0]

        container.add_element(XMLGrace())
        container.check_required_elements()
        expected = """        Sequence@minOccurs=1@maxOccurs=1: !!!FORCED!!!
            Element@name=grace@minOccurs=1@maxOccurs=1
                XMLGrace
            Choice@minOccurs=1@maxOccurs=1
                !Required!
                Sequence@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
                    Element@name=tie@minOccurs=0@maxOccurs=2
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=cue@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
"""
        assert choice.chosen_child.tree_representation(show_force_valid) == expected
        container.add_element(XMLPitch())
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLRest())
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLCue(), intelligent_choice=False)
        with self.assertRaises(XMLChildContainerChoiceHasAnotherChosenChild):
            container.add_element(XMLDuration(1))

    def test_required_choice_not_fulfilled(self):
        """
        Test methode add_required will show in tree presentation that the element or the choice requirement is not fulfilled
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasureStyle).get_child_container()
        container.requirements_not_fulfilled = True
        expected = """Choice@minOccurs=1@maxOccurs=1
    !Required!
    Element@name=multiple-rest@minOccurs=1@maxOccurs=1
    Element@name=measure-repeat@minOccurs=1@maxOccurs=1
    Element@name=beat-repeat@minOccurs=1@maxOccurs=1
    Element@name=slash@minOccurs=1@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_required_element_not_fulfilled(self):
        """
        Test methode add_required will show in tree presentation that the element or the choice requirement is not fulfilled
        """
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePitch).get_child_container()
        container.get_children()[0].requirements_not_fulfilled = True
        container.get_children()[2].requirements_not_fulfilled = True
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Element@name=step@minOccurs=1@maxOccurs=1
        !Required!
    Element@name=alter@minOccurs=0@maxOccurs=1
    Element@name=octave@minOccurs=1@maxOccurs=1
        !Required!
"""
        assert container.tree_representation() == expected

    def test_check_choice(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeMeasureStyle).get_child_container()
        assert container.check_required_elements() is True
        assert container.requirements_not_fulfilled is True
        container.add_element(XMLMultipleRest(2))
        assert container.requirements_not_fulfilled is False
        assert container.check_required_elements() is False

    def test_check_sequence(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypePitch).get_child_container()
        assert container.check_required_elements() is True
        assert container.get_children()[0].requirements_not_fulfilled is True
        assert container.get_children()[2].requirements_not_fulfilled is True

    def test_check_score_child_container(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeScorePartwise).get_child_container()
        assert container.check_required_elements() is True
        container.add_element(XMLPartList())
        assert container.check_required_elements() is True
        container.add_element(XMLPart())
        assert container.check_required_elements() is False

    def test_check_lyric_child_container(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        assert container.check_required_elements() is True
        container.add_element(XMLLaughing())
        assert container.check_required_elements() is False

        container = XMLChildContainerFactory(complex_type=XSDComplexTypeLyric).get_child_container()
        container.add_element(XMLText('something'))
        assert container.check_required_elements() is False
        container.add_element(XMLElision('something'))
        assert container.check_required_elements() is True
        container.add_element(XMLText('something'))
        assert container.check_required_elements() is False

    #     def test_check_intelligent_choice(self):
    #         container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
    #         container.add_element(XMLPitch())
    #         container.add_element(XMLDuration(1))
    #         container.add_element(XMLCue())
    #         assert container.check_required_elements() is False
    #         expected = """Sequence@minOccurs=1@maxOccurs=1
    #     Choice@minOccurs=1@maxOccurs=1
    #         Sequence@minOccurs=1@maxOccurs=1
    #             Group@name=full-note@minOccurs=1@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=chord@minOccurs=0@maxOccurs=1
    #                     Choice@minOccurs=1@maxOccurs=1
    #                         Element@name=pitch@minOccurs=1@maxOccurs=1
    #                             XMLPitch
    #                         Element@name=unpitched@minOccurs=1@maxOccurs=1
    #                         Element@name=rest@minOccurs=1@maxOccurs=1
    #             Group@name=duration@minOccurs=1@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=duration@minOccurs=1@maxOccurs=1
    #                         XMLDuration
    #             Element@name=tie@minOccurs=0@maxOccurs=2
    #         Sequence@minOccurs=1@maxOccurs=1
    #             Element@name=cue@minOccurs=1@maxOccurs=1
    #             Group@name=full-note@minOccurs=1@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=chord@minOccurs=0@maxOccurs=1
    #                     Choice@minOccurs=1@maxOccurs=1
    #                         Element@name=pitch@minOccurs=1@maxOccurs=1
    #                         Element@name=unpitched@minOccurs=1@maxOccurs=1
    #                         Element@name=rest@minOccurs=1@maxOccurs=1
    #             Group@name=duration@minOccurs=1@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=duration@minOccurs=1@maxOccurs=1
    #         Sequence@minOccurs=1@maxOccurs=1
    #             Element@name=grace@minOccurs=1@maxOccurs=1
    #             Choice@minOccurs=1@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Group@name=full-note@minOccurs=1@maxOccurs=1
    #                         Sequence@minOccurs=1@maxOccurs=1
    #                             Element@name=chord@minOccurs=0@maxOccurs=1
    #                             Choice@minOccurs=1@maxOccurs=1
    #                                 Element@name=pitch@minOccurs=1@maxOccurs=1
    #                                 Element@name=unpitched@minOccurs=1@maxOccurs=1
    #                                 Element@name=rest@minOccurs=1@maxOccurs=1
    #                     Element@name=tie@minOccurs=0@maxOccurs=2
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=cue@minOccurs=1@maxOccurs=1
    #                     Group@name=full-note@minOccurs=1@maxOccurs=1
    #                         Sequence@minOccurs=1@maxOccurs=1
    #                             Element@name=chord@minOccurs=0@maxOccurs=1
    #                             Choice@minOccurs=1@maxOccurs=1
    #                                 Element@name=pitch@minOccurs=1@maxOccurs=1
    #                                 Element@name=unpitched@minOccurs=1@maxOccurs=1
    #                                 Element@name=rest@minOccurs=1@maxOccurs=1
    #     Element@name=instrument@minOccurs=0@maxOccurs=unbounded
    #     Group@name=editorial-voice@minOccurs=1@maxOccurs=1
    #         Sequence@minOccurs=1@maxOccurs=1
    #             Group@name=footnote@minOccurs=0@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=footnote@minOccurs=1@maxOccurs=1
    #             Group@name=level@minOccurs=0@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=level@minOccurs=1@maxOccurs=1
    #             Group@name=voice@minOccurs=0@maxOccurs=1
    #                 Sequence@minOccurs=1@maxOccurs=1
    #                     Element@name=voice@minOccurs=1@maxOccurs=1
    #     Element@name=type@minOccurs=0@maxOccurs=1
    #     Element@name=dot@minOccurs=0@maxOccurs=unbounded
    #     Element@name=accidental@minOccurs=0@maxOccurs=1
    #     Element@name=time-modification@minOccurs=0@maxOccurs=1
    #     Element@name=stem@minOccurs=0@maxOccurs=1
    #     Element@name=notehead@minOccurs=0@maxOccurs=1
    #     Element@name=notehead-text@minOccurs=0@maxOccurs=1
    #     Group@name=staff@minOccurs=0@maxOccurs=1
    #         Sequence@minOccurs=1@maxOccurs=1
    #             Element@name=staff@minOccurs=1@maxOccurs=1
    #     Element@name=beam@minOccurs=0@maxOccurs=8
    #     Element@name=notations@minOccurs=0@maxOccurs=unbounded
    #     Element@name=lyric@minOccurs=0@maxOccurs=unbounded
    #     Element@name=play@minOccurs=0@maxOccurs=1
    #     Element@name=listen@minOccurs=0@maxOccurs=1
    # """
    #
    #         print(container.tree_representation())
    #         assert container.tree_representation() == expected

    def test_note_with_voice_and_type(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
        container.add_element(XMLPitch())
        container.add_element(XMLDuration(1))
        container.add_element(XMLVoice('1'))
        container.add_element(XMLType('eighth'))
        expected = """Sequence@minOccurs=1@maxOccurs=1
    Choice@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=chord@minOccurs=0@maxOccurs=1
                    Choice@minOccurs=1@maxOccurs=1
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                            XMLPitch
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=duration@minOccurs=1@maxOccurs=1
                        XMLDuration
            Element@name=tie@minOccurs=0@maxOccurs=2
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=cue@minOccurs=1@maxOccurs=1
            Group@name=full-note@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=chord@minOccurs=0@maxOccurs=1
                    Choice@minOccurs=1@maxOccurs=1
                        Element@name=pitch@minOccurs=1@maxOccurs=1
                        Element@name=unpitched@minOccurs=1@maxOccurs=1
                        Element@name=rest@minOccurs=1@maxOccurs=1
            Group@name=duration@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=duration@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=grace@minOccurs=1@maxOccurs=1
            Choice@minOccurs=1@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
                    Element@name=tie@minOccurs=0@maxOccurs=2
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=cue@minOccurs=1@maxOccurs=1
                    Group@name=full-note@minOccurs=1@maxOccurs=1
                        Sequence@minOccurs=1@maxOccurs=1
                            Element@name=chord@minOccurs=0@maxOccurs=1
                            Choice@minOccurs=1@maxOccurs=1
                                Element@name=pitch@minOccurs=1@maxOccurs=1
                                Element@name=unpitched@minOccurs=1@maxOccurs=1
                                Element@name=rest@minOccurs=1@maxOccurs=1
    Element@name=instrument@minOccurs=0@maxOccurs=unbounded
    Group@name=editorial-voice@minOccurs=1@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Group@name=footnote@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=footnote@minOccurs=1@maxOccurs=1
            Group@name=level@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=level@minOccurs=1@maxOccurs=1
            Group@name=voice@minOccurs=0@maxOccurs=1
                Sequence@minOccurs=1@maxOccurs=1
                    Element@name=voice@minOccurs=1@maxOccurs=1
                        XMLVoice
    Element@name=type@minOccurs=0@maxOccurs=1
        XMLType
    Element@name=dot@minOccurs=0@maxOccurs=unbounded
    Element@name=accidental@minOccurs=0@maxOccurs=1
    Element@name=time-modification@minOccurs=0@maxOccurs=1
    Element@name=stem@minOccurs=0@maxOccurs=1
    Element@name=notehead@minOccurs=0@maxOccurs=1
    Element@name=notehead-text@minOccurs=0@maxOccurs=1
    Group@name=staff@minOccurs=0@maxOccurs=1
        Sequence@minOccurs=1@maxOccurs=1
            Element@name=staff@minOccurs=1@maxOccurs=1
    Element@name=beam@minOccurs=0@maxOccurs=8
    Element@name=notations@minOccurs=0@maxOccurs=unbounded
    Element@name=lyric@minOccurs=0@maxOccurs=unbounded
    Element@name=play@minOccurs=0@maxOccurs=1
    Element@name=listen@minOccurs=0@maxOccurs=1
"""
        assert container.tree_representation() == expected

    def test_copy_container(self):
        container = XMLChildContainerFactory(complex_type=XSDComplexTypeNote).get_child_container()
        before_tree = container.tree_representation(show_force_valid)
        container.add_element(XMLPitch())
        container.add_element(XMLDuration(2))
        container.add_element(XMLVoice('1'))
        container.add_element(XMLType('eighth'))
        copied = copy.copy(container)
        assert before_tree == copied.tree_representation()
