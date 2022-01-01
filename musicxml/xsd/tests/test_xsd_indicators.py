from unittest import TestCase
import xml.etree.ElementTree as ET

from musicxml.xmlelement.xmlelement import XMLElement
from musicxml.xsd.xsdtree import XSDTree, XSDSequence, XSDChoice
from musicxml.xsd.xsdsimpletype import *


class TestSequence(TestCase):
    def test_sequence_initialization(self):
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
        s = XSDSequence(sequence_xsd_tree)
        assert s._element_names_order == ['midi-channel', 'midi-name', 'midi-bank', 'midi-program', 'midi-unpitched', 'volume', 'pan',
                                          'elevation']

        s.order_elements(elements=XMLElement(name='midi-channel', type_=XSDSimpleTypeMidi16))
