from unittest import TestCase

from musicxml.exceptions import XMLElementChildrenRequired, XMLElementValueRequiredError, XSDAttributeRequiredException
from musicxml.xmlelement.tests.test_child_container import show_force_valid
from musicxml.xmlelement.xmlelement import *
from musicxml.xsd.xsdcomplextype import *
from musicxml.xsd.xsdindicators import XSDSequence, XSDChoice
from musicxml.xsd.xsdsimpletype import *
from musicxml.xmlelement.xmlelement import xml_element_class_names


class TestXMLElements(TestCase):
    def test_xml_element_list(self):
        assert sorted(xml_element_class_names) == ['XMLAccent', 'XMLAccidental', 'XMLAccidentalMark', 'XMLAccidentalText', 'XMLAccord',
                                                   'XMLAccordionHigh', 'XMLAccordionLow', 'XMLAccordionMiddle', 'XMLAccordionRegistration',
                                                   'XMLActualNotes', 'XMLAlter', 'XMLAppearance', 'XMLArpeggiate', 'XMLArrow',
                                                   'XMLArrowDirection', 'XMLArrowStyle', 'XMLArrowhead', 'XMLArticulations',
                                                   'XMLArtificial', 'XMLAssess', 'XMLAttributes', 'XMLBackup', 'XMLBarStyle', 'XMLBarline',
                                                   'XMLBarre', 'XMLBasePitch', 'XMLBass', 'XMLBassAlter', 'XMLBassSeparator', 'XMLBassStep',
                                                   'XMLBeam', 'XMLBeatRepeat', 'XMLBeatType', 'XMLBeatUnit', 'XMLBeatUnitDot',
                                                   'XMLBeatUnitTied', 'XMLBeater', 'XMLBeats', 'XMLBend', 'XMLBendAlter', 'XMLBookmark',
                                                   'XMLBottomMargin', 'XMLBracket', 'XMLBrassBend', 'XMLBreathMark', 'XMLCaesura',
                                                   'XMLCancel', 'XMLCapo', 'XMLChord', 'XMLChromatic', 'XMLCircularArrow', 'XMLClef',
                                                   'XMLClefOctaveChange', 'XMLCoda', 'XMLConcertScore', 'XMLCreator', 'XMLCredit',
                                                   'XMLCreditImage', 'XMLCreditSymbol', 'XMLCreditType', 'XMLCreditWords', 'XMLCue',
                                                   'XMLDamp', 'XMLDampAll', 'XMLDashes', 'XMLDefaults', 'XMLDegree', 'XMLDegreeAlter',
                                                   'XMLDegreeType', 'XMLDegreeValue', 'XMLDelayedInvertedTurn', 'XMLDelayedTurn',
                                                   'XMLDetachedLegato', 'XMLDiatonic', 'XMLDirection', 'XMLDirectionType',
                                                   'XMLDisplayOctave', 'XMLDisplayStep', 'XMLDisplayText', 'XMLDistance', 'XMLDivisions',
                                                   'XMLDoit', 'XMLDot', 'XMLDouble', 'XMLDoubleTongue', 'XMLDownBow', 'XMLDuration',
                                                   'XMLDynamics', 'XMLEffect', 'XMLElevation', 'XMLElision', 'XMLEncoder', 'XMLEncoding',
                                                   'XMLEncodingDate', 'XMLEncodingDescription', 'XMLEndLine', 'XMLEndParagraph',
                                                   'XMLEnding', 'XMLEnsemble', 'XMLExceptVoice', 'XMLExtend', 'XMLEyeglasses', 'XMLF',
                                                   'XMLFalloff', 'XMLFeature', 'XMLFermata', 'XMLFf', 'XMLFff', 'XMLFfff', 'XMLFffff',
                                                   'XMLFfffff', 'XMLFifths', 'XMLFigure', 'XMLFigureNumber', 'XMLFiguredBass',
                                                   'XMLFingering', 'XMLFingernails', 'XMLFirst', 'XMLFirstFret', 'XMLFlip', 'XMLFootnote',
                                                   'XMLForPart', 'XMLForward', 'XMLFp', 'XMLFrame', 'XMLFrameFrets', 'XMLFrameNote',
                                                   'XMLFrameStrings', 'XMLFret', 'XMLFunction', 'XMLFz', 'XMLGlass', 'XMLGlissando',
                                                   'XMLGlyph', 'XMLGolpe', 'XMLGrace', 'XMLGroup', 'XMLGroupAbbreviation',
                                                   'XMLGroupAbbreviationDisplay', 'XMLGroupBarline', 'XMLGroupLink', 'XMLGroupName',
                                                   'XMLGroupNameDisplay', 'XMLGroupSymbol', 'XMLGroupTime', 'XMLGrouping', 'XMLHalfMuted',
                                                   'XMLHammerOn', 'XMLHandbell', 'XMLHarmonClosed', 'XMLHarmonMute', 'XMLHarmonic',
                                                   'XMLHarmony', 'XMLHarpPedals', 'XMLHaydn', 'XMLHeel', 'XMLHole', 'XMLHoleClosed',
                                                   'XMLHoleShape', 'XMLHoleType', 'XMLHumming', 'XMLIdentification', 'XMLImage',
                                                   'XMLInstrument', 'XMLInstrumentAbbreviation', 'XMLInstrumentChange', 'XMLInstrumentLink',
                                                   'XMLInstrumentName', 'XMLInstrumentSound', 'XMLInstruments', 'XMLInterchangeable',
                                                   'XMLInversion', 'XMLInvertedMordent', 'XMLInvertedTurn', 'XMLInvertedVerticalTurn',
                                                   'XMLIpa', 'XMLKey', 'XMLKeyAccidental', 'XMLKeyAlter', 'XMLKeyOctave', 'XMLKeyStep',
                                                   'XMLKind', 'XMLLaughing', 'XMLLeftDivider', 'XMLLeftMargin', 'XMLLevel', 'XMLLine',
                                                   'XMLLineDetail', 'XMLLineWidth', 'XMLLink', 'XMLListen', 'XMLListening', 'XMLLyric',
                                                   'XMLLyricFont', 'XMLLyricLanguage', 'XMLMeasure', 'XMLMeasureDistance',
                                                   'XMLMeasureLayout', 'XMLMeasureNumbering', 'XMLMeasureRepeat', 'XMLMeasureStyle',
                                                   'XMLMembrane', 'XMLMetal', 'XMLMetronome', 'XMLMetronomeArrows', 'XMLMetronomeBeam',
                                                   'XMLMetronomeDot', 'XMLMetronomeNote', 'XMLMetronomeRelation', 'XMLMetronomeTied',
                                                   'XMLMetronomeTuplet', 'XMLMetronomeType', 'XMLMf', 'XMLMidiBank', 'XMLMidiChannel',
                                                   'XMLMidiDevice', 'XMLMidiInstrument', 'XMLMidiName', 'XMLMidiProgram',
                                                   'XMLMidiUnpitched', 'XMLMillimeters', 'XMLMiscellaneous', 'XMLMiscellaneousField',
                                                   'XMLMode', 'XMLMordent', 'XMLMovementNumber', 'XMLMovementTitle', 'XMLMp',
                                                   'XMLMultipleRest', 'XMLMusicFont', 'XMLMute', 'XMLN', 'XMLNatural', 'XMLNonArpeggiate',
                                                   'XMLNormalDot', 'XMLNormalNotes', 'XMLNormalType', 'XMLNotations', 'XMLNote',
                                                   'XMLNoteSize', 'XMLNotehead', 'XMLNoteheadText', 'XMLNumeral', 'XMLNumeralAlter',
                                                   'XMLNumeralFifths', 'XMLNumeralKey', 'XMLNumeralMode', 'XMLNumeralRoot', 'XMLOctave',
                                                   'XMLOctaveChange', 'XMLOctaveShift', 'XMLOffset', 'XMLOpen', 'XMLOpenString', 'XMLOpus',
                                                   'XMLOrnaments', 'XMLOtherAppearance', 'XMLOtherArticulation', 'XMLOtherDirection',
                                                   'XMLOtherDynamics', 'XMLOtherListen', 'XMLOtherListening', 'XMLOtherNotation',
                                                   'XMLOtherOrnament', 'XMLOtherPercussion', 'XMLOtherPlay', 'XMLOtherTechnical', 'XMLP',
                                                   'XMLPageHeight', 'XMLPageLayout', 'XMLPageMargins', 'XMLPageWidth', 'XMLPan', 'XMLPart',
                                                   'XMLPartAbbreviation', 'XMLPartAbbreviationDisplay', 'XMLPartClef', 'XMLPartGroup',
                                                   'XMLPartLink', 'XMLPartList', 'XMLPartName', 'XMLPartNameDisplay', 'XMLPartSymbol',
                                                   'XMLPartTranspose', 'XMLPedal', 'XMLPedalAlter', 'XMLPedalStep', 'XMLPedalTuning',
                                                   'XMLPerMinute', 'XMLPercussion', 'XMLPf', 'XMLPitch', 'XMLPitched', 'XMLPlay',
                                                   'XMLPlayer', 'XMLPlayerName', 'XMLPlop', 'XMLPluck', 'XMLPp', 'XMLPpp', 'XMLPppp',
                                                   'XMLPpppp', 'XMLPppppp', 'XMLPreBend', 'XMLPrefix', 'XMLPrincipalVoice', 'XMLPrint',
                                                   'XMLPullOff', 'XMLRehearsal', 'XMLRelation', 'XMLRelease', 'XMLRepeat', 'XMLRest',
                                                   'XMLRf', 'XMLRfz', 'XMLRightDivider', 'XMLRightMargin', 'XMLRights', 'XMLRoot',
                                                   'XMLRootAlter', 'XMLRootStep', 'XMLScaling', 'XMLSchleifer', 'XMLScoop', 'XMLScordatura',
                                                   'XMLScoreInstrument', 'XMLScorePart', 'XMLScorePartwise', 'XMLSecond', 'XMLSegno',
                                                   'XMLSemiPitched', 'XMLSenzaMisura', 'XMLSf', 'XMLSffz', 'XMLSfp', 'XMLSfpp', 'XMLSfz',
                                                   'XMLSfzp', 'XMLShake', 'XMLSign', 'XMLSlash', 'XMLSlashDot', 'XMLSlashType', 'XMLSlide',
                                                   'XMLSlur', 'XMLSmear', 'XMLSnapPizzicato', 'XMLSoftAccent', 'XMLSoftware', 'XMLSolo',
                                                   'XMLSound', 'XMLSoundingPitch', 'XMLSource', 'XMLSpiccato', 'XMLStaccatissimo',
                                                   'XMLStaccato', 'XMLStaff', 'XMLStaffDetails', 'XMLStaffDistance', 'XMLStaffDivide',
                                                   'XMLStaffLayout', 'XMLStaffLines', 'XMLStaffSize', 'XMLStaffTuning', 'XMLStaffType',
                                                   'XMLStaves', 'XMLStem', 'XMLStep', 'XMLStick', 'XMLStickLocation', 'XMLStickMaterial',
                                                   'XMLStickType', 'XMLStopped', 'XMLStraight', 'XMLStress', 'XMLString', 'XMLStringMute',
                                                   'XMLStrongAccent', 'XMLSuffix', 'XMLSupports', 'XMLSwing', 'XMLSwingStyle',
                                                   'XMLSwingType', 'XMLSyllabic', 'XMLSymbol', 'XMLSync', 'XMLSystemDistance',
                                                   'XMLSystemDividers', 'XMLSystemLayout', 'XMLSystemMargins', 'XMLTap', 'XMLTechnical',
                                                   'XMLTenths', 'XMLTenuto', 'XMLText', 'XMLThumbPosition', 'XMLTie', 'XMLTied', 'XMLTime',
                                                   'XMLTimeModification', 'XMLTimeRelation', 'XMLTimpani', 'XMLToe', 'XMLTopMargin',
                                                   'XMLTopSystemDistance', 'XMLTouchingPitch', 'XMLTranspose', 'XMLTremolo', 'XMLTrillMark',
                                                   'XMLTripleTongue', 'XMLTuningAlter', 'XMLTuningOctave', 'XMLTuningStep', 'XMLTuplet',
                                                   'XMLTupletActual', 'XMLTupletDot', 'XMLTupletNormal', 'XMLTupletNumber', 'XMLTupletType',
                                                   'XMLTurn', 'XMLType', 'XMLUnpitched', 'XMLUnstress', 'XMLUpBow', 'XMLVerticalTurn',
                                                   'XMLVirtualInstrument', 'XMLVirtualLibrary', 'XMLVirtualName', 'XMLVoice', 'XMLVolume',
                                                   'XMLWait', 'XMLWavyLine', 'XMLWedge', 'XMLWithBar', 'XMLWood', 'XMLWordFont', 'XMLWords',
                                                   'XMLWork', 'XMLWorkNumber', 'XMLWorkTitle']

    def test_element_type(self):
        el = XMLOffset()
        assert el.type_ == XSDComplexTypeOffset

        el = XMLElevation()
        assert el.type_ == XSDSimpleTypeRotationDegrees

    def test_element_simple_content(self):
        """
        Test if complex types with a simple context (extension of a simple type) work properly in an XMLElement.
        A simple example is

        complexType@name=offset

        simpleContent
            extension@base=divisions
                attribute@name=sound@type=yes-no
        """
        el = XMLOffset(-2)
        assert el.to_string() == '<offset>-2</offset>\n'

        el = XMLOffset(-2, sound='yes')
        assert el.to_string() == '<offset sound="yes">-2</offset>\n'

        el = XMLOffset()
        with self.assertRaises(XMLElementValueRequiredError):
            el.to_string()

        with self.assertRaises(TypeError):
            XMLOffset('wrong', sound='yes')

        with self.assertRaises(TypeError):
            XMLOffset(-2, sound=3).to_string()

        with self.assertRaises(ValueError):
            XMLOffset(-2, sound='maybe').to_string()

    def test_element_name(self):
        el = XMLOffset(-2)
        assert el.name == 'offset'
        el = XMLElevation()
        assert el.name == 'elevation'

    def test_element_with_simple_type(self):
        """
        <xs:element name="elevation" type="rotation-degrees" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.</xs:documentation>
            </xs:annotation>
        </xs:element>
        """
        el = XMLElevation()
        assert el.type_ == XSDSimpleTypeRotationDegrees
        with self.assertRaises(TypeError):
            el.value = 'something'
        with self.assertRaises(ValueError):
            el.value = 200
        with self.assertRaises(XMLElementValueRequiredError):
            el.to_string()

        el.value = 170
        assert el.to_string() == '<elevation>170</elevation>\n'
        assert el.__doc__ == 'The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.'

    def test_element_doc(self):
        """
        Test if an element with complex type returns its type's __doc__ as its __doc__
        Test if an element with simple type returns its xsd tree documentation as its __doc__
        """
        assert XMLOffset().__doc__ == """An offset is represented in terms of divisions, and indicates where the direction will appear relative to the current musical location. The current musical location is always within the current measure, even at the end of a measure.

The offset affects the visual appearance of the direction. If the sound attribute is "yes", then the offset affects playback and listening too. If the sound attribute is "no", then any sound or listening associated with the direction takes effect at the current location. The sound attribute is "no" by default for compatibility with earlier versions of the MusicXML format. If an element within a direction includes a default-x attribute, the offset value will be ignored when determining the appearance of that element."""

        assert XMLElevation().__doc__ == 'The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.'

    def test_element_empty(self):
        """
        Test that empty complex type is created properly
        """
        el = XMLChord()
        assert el.to_string() == '<chord />\n'

    def test_all_element_tags(self):
        """
        Test that all element names are represented as elements tag.
        """
        for el in xml_element_class_names:
            element = eval(el)()
            assert element._et_xml_element.tag == element.name

    def test_get_class_name(self):
        assert XMLPitch.get_class_name() == 'XMLPitch'
        assert XMLPitch().get_class_name() == 'XMLPitch'

    def test_sequence_indicator_children_required(self):
        """
        Test that a sequence indicator with only elements as children can verify the behavior of its corresponding element
        """
        """
        complexType@name=pitch
        sequence
            element@name=step@type=step
            element@name=alter@type=semitones@minOccurs=0
            element@name=octave@type=octave
        """

        """
        Element Pitch must have one and only one child element step and one and only one child element octave. It can have only one child 
        alter. The sequence order will be automatically set according to the sequence (step, alter, octave)
        """

        el = XMLPitch()
        with self.assertRaises(XMLElementChildrenRequired):
            el.to_string()

    def test_sequence_add_children_to_string(self):
        """
        Test that to_string function of an element with complex type and sequence works properly
        """
        el = XMLPitch()
        el.add_child(XMLStep('A'))
        el.add_child(XMLOctave(4))
        expected = """<pitch>
    <step>A</step>
    <octave>4</octave>
</pitch>
"""
        assert el.to_string() == expected

    def test_xml_element_part_list(self):
        el = XMLPartList()
        with self.assertRaises(XMLElementChildrenRequired) as err:
            el.to_string()

        assert err.exception.args[0] == 'XMLPartList requires at least following children: XMLScorePart'
        sp = el.add_child(XMLScorePart())

        with self.assertRaises(XMLElementChildrenRequired) as err:
            el.to_string()
        assert err.exception.args[0] == 'XMLScorePart requires at least following children: XMLPartName'

        pn = sp.add_child(XMLPartName())
        with self.assertRaises(XSDAttributeRequiredException) as err:
            el.to_string()
        assert err.exception.args[0] == 'XSDComplexTypeScorePart requires attribute: id'
        sp.id = '1'
        with self.assertRaises(XMLElementValueRequiredError) as err:
            el.to_string()

        assert err.exception.args[0] == 'XMLPartName requires a value.'
        pn.value = 'part name 1'
        expected = """<part-list>
    <score-part>
        <part-name>part name 1</part-name>
    </score-part>
</part-list>
"""
        assert el.to_string() == expected
