from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.xmlelement.xmlelement import *

from musicxml.xsd.xsdtree import XSDTree
from musicxml.xsd.xsdindicator import XSDSequence, XSDChoice


class TestSequence(TestCase):
    def setUp(self) -> None:
        xsd = """
                <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <xs:element name="midi-channel" type="midi-16" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The midi-channel element specifies a MIDI 1.0 channel numbers ranging from 1 to 16.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="midi-name" type="xs:string" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The midi-name element corresponds to a ProgramName meta-event within a Standard MIDI File.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="midi-bank" type="midi-16384" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The midi-bank element specifies a MIDI 1.0 bank number ranging from 1 to 16,384.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="midi-program" type="midi-128" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The midi-program element specifies a MIDI 1.0 program number ranging from 1 to 128.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="midi-unpitched" type="midi-128" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>For unpitched instruments, the midi-unpitched element specifies a MIDI 1.0 note number ranging from 1 to 128. It is usually used with MIDI banks for percussion. Note that MIDI 1.0 note numbers are generally specified from 0 to 127 rather than the 1 to 128 numbering used in this element.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="volume" type="percent" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The volume element value is a percentage of the maximum ranging from 0 to 100, with decimal values allowed. This corresponds to a scaling value for the MIDI 1.0 channel volume controller.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="pan" type="rotation-degrees" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The pan and elevation elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For pan, 0 is straight ahead, -90 is hard left, 90 is hard right, and -180 and 180 are directly behind the listener.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                    <xs:element name="elevation" type="rotation-degrees" minOccurs="0">
                        <xs:annotation>
                            <xs:documentation>The elevation and pan elements allow placing of sound in a 3-D space relative to the listener. Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly above, and -90 is directly below.</xs:documentation>
                        </xs:annotation>
                    </xs:element>
                </xs:sequence>
        """
        et = ET.fromstring(xsd)
        sequence_xsd_tree = XSDTree(et)
        self.sequence = XSDSequence(sequence_xsd_tree)

    def test_sequence_elements(self):
        assert self.sequence.elements == [('XMLMidiChannel', '0', '1'), ('XMLMidiName', '0', '1'), ('XMLMidiBank', '0', '1'),
                                          ('XMLMidiProgram', '0', '1'), ('XMLMidiUnpitched', '0', '1'), ('XMLVolume', '0', '1'),
                                          ('XMLPan', '0', '1'), ('XMLElevation', '0', '1')]

    def test_sequence_min_occurrences(self):
        xsd = """
                <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <xs:element name="step" type="step"/>
                    <xs:element name="alter" type="semitones" minOccurs="0"/>
                    <xs:element name="octave" type="octave"/>
                </xs:sequence>
        """
        et = ET.fromstring(xsd)
        sequence_xsd_tree = XSDTree(et)
        sequence = XSDSequence(sequence_xsd_tree)
        assert sequence.elements == [('XMLStep', '1', '1'), ('XMLAlter', '0', '1'), ('XMLOctave', '1', '1')]

    def test_sequence_group_elements(self):
        xsd = """
        <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:element name="group-name" type="group-name" minOccurs="0"/>
            <xs:element name="group-name-display" type="name-display" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>Formatting specified in the group-name-display element overrides formatting specified in the group-name element.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="group-abbreviation" type="group-name" minOccurs="0"/>
            <xs:element name="group-abbreviation-display" type="name-display" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>Formatting specified in the group-abbreviation-display element overrides formatting specified in the group-abbreviation element.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="group-symbol" type="group-symbol" minOccurs="0"/>
            <xs:element name="group-barline" type="group-barline" minOccurs="0"/>
            <xs:element name="group-time" type="empty" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>The group-time element indicates that the displayed time signatures should stretch across all parts and staves in the group.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:group ref="editorial"/>
        </xs:sequence>
                """
        et = ET.fromstring(xsd)
        sequence_xsd_tree = XSDTree(et)
        sequence = XSDSequence(sequence_xsd_tree)
        assert sequence.elements == [('XMLGroupName', '0', '1'), ('XMLGroupNameDisplay', '0', '1'), ('XMLGroupAbbreviation', '0', '1'),
                                     ('XMLGroupAbbreviationDisplay', '0', '1'), ('XMLGroupSymbol', '0', '1'), ('XMLGroupBarline', '0', '1'),
                                     ('XMLGroupTime', '0', '1'),
                                     ('XMLFootnote', '0', '1'), ('XMLLevel', '0', '1')]
