from musicxml.generate_classes.utils import musicxml_xsd_et_root
from musicxml.util.core import convert_to_xsd_class_name
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdindicator import *
from musicxml.xsd.xsdtree import XSDTreeElement, XSDTree
import xml.etree.ElementTree as ET


class XSDComplexType(XSDTreeElement):
    _SIMPLE_CONTENT = None
    _SEARCH_FOR_ELEMENT = ''

    def __init__(self, value=None, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.value = value
        self._value = None

    def _get_error_class(self):
        if self.parent:
            return self.parent.__class__.__name__
        else:
            return self.__class__.__name__

    def _check_value(self, val):
        if self._SIMPLE_CONTENT:
            try:
                self._SIMPLE_CONTENT(val)
            except TypeError as err:
                raise TypeError(f"{self._get_error_class()}: " + err.args[0])
            except ValueError as err:
                raise ValueError(f"{self._get_error_class()}: " + err.args[0])

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._check_value(v)
        self._value = v

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        if cls.get_xsd_tree().get_simple_content_extension():
            for child in cls.get_xsd_tree().get_simple_content_extension().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        elif cls.get_xsd_tree().get_complex_content():
            complex_content_extension = cls.get_xsd_tree().get_complex_content_extension()
            complex_type_extension_base_class_name = convert_to_xsd_class_name(complex_content_extension.get_attributes()['base'],
                                                                               'complex_type')
            extension_base = eval(complex_type_extension_base_class_name)
            output.extend(extension_base.get_xsd_attributes())
            for child in complex_content_extension.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
            return output
        else:
            for child in cls.get_xsd_tree().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

    @classmethod
    def get_xsd_indicator(cls):
        def get_occurrences(ch):
            min_ = ch.get_attributes().get('minOccurs')
            max_ = ch.get_attributes().get('maxOccurs')
            return 1 if not min_ else int(min_), 1 if not max_ else 'unbounded' if max_ == 'unbounded' else int(max_)

        for child in cls.get_xsd_tree().get_children():
            if child.tag == 'sequence':
                return XSDSequence(child), *get_occurrences(child)
            if child.tag == 'choice':
                return XSDChoice(child), *get_occurrences(child)
            if child.tag == 'group':
                return eval(convert_to_xsd_class_name(child.get_attributes()['ref'], 'group'))(), *get_occurrences(child)
            if child.tag == 'complexContent':
                return eval(convert_to_xsd_class_name(child.get_children()[0].get_attributes()['base'],
                                                      'complex_type')).get_xsd_indicator()


class XSDComplexTypeScorePartwise(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType"


class XSDComplexTypePart(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType//{*}complexType"


class XSDComplexTypeMeasure(XSDComplexType):
    _SEARCH_FOR_ELEMENT = ".//{*}element[@name='score-partwise']//{*}complexType//{*}complexType//{*}complexType"


class XSDComplexTypeDirective(XSDComplexType):
    _SIMPLE_CONTENT = XSDSimpleTypeString
    _SEARCH_FOR_ELEMENT = ".//{*}complexType[@name='attributes']//{*}complexType"


# Note's choice is being manually reordered to avoid using intelligent choice for each Note without grace.
class XSDComplexTypeNote(XSDComplexType):
    """Notes are the most common type of MusicXML data. The MusicXML format distinguishes between elements used for sound information and elements used for notation information (e.g., tie is used for sound, tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do forward elements, but no tie elements. Having these two types of information available can make interchange easier, as some programs handle one type of information more readily than the other.

The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no, print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.

The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively. They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).

The attack and release attributes are used to alter the starting and stopping time of the note from when it would otherwise occur based on the flow of durations - information that is specific to a performance. They are expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a release attribute, and a note that stops a tie should not have an attack attribute. The attack and release attributes are independent of each other. The attack attribute only changes the starting time of a note, and the release attribute only changes the stopping time of a note.

If a note is played only particular times through a repeat, the time-only attribute shows which times to play the note.

The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which changes overall playback between pizzicato and arco.
"""

    _XSD_TREE = XSDTree(ET.fromstring("""
<xs:complexType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="note">
    <xs:annotation>
        <xs:documentation>Notes are the most common type of MusicXML data. The MusicXML format distinguishes between elements used for sound information and elements used for notation information (e.g., tie is used for sound, tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do forward elements, but no tie elements. Having these two types of information available can make interchange easier, as some programs handle one type of information more readily than the other.

The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no, print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.

The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively. They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).

The attack and release attributes are used to alter the starting and stopping time of the note from when it would otherwise occur based on the flow of durations - information that is specific to a performance. They are expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a release attribute, and a note that stops a tie should not have an attack attribute. The attack and release attributes are independent of each other. The attack attribute only changes the starting time of a note, and the release attribute only changes the stopping time of a note.

If a note is played only particular times through a repeat, the time-only attribute shows which times to play the note.

The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which changes overall playback between pizzicato and arco.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:choice>
            <xs:sequence>
                <xs:group ref="full-note" />
                <xs:group ref="duration" />
                <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2" />
            </xs:sequence>
            <xs:sequence>
                <xs:element name="cue" type="empty">
                    <xs:annotation>
                        <xs:documentation>The cue element indicates the presence of a cue note. In MusicXML, a cue note is a silent note with no playback. Normal notes that play can be specified as cue size using the type element. A cue note that is specified as full size using the type element will still remain silent.</xs:documentation>
                    </xs:annotation>
                </xs:element>
                <xs:group ref="full-note" />
                <xs:group ref="duration" />
            </xs:sequence>
            <xs:sequence>
                <xs:element name="grace" type="grace" />
                <xs:choice>
                    <xs:sequence>
                        <xs:group ref="full-note" />
                        <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2" />
                    </xs:sequence>
                    <xs:sequence>
                        <xs:element name="cue" type="empty" />
                        <xs:group ref="full-note" />
                    </xs:sequence>
                </xs:choice>
            </xs:sequence>
        </xs:choice>
        <xs:element name="instrument" type="instrument" minOccurs="0" maxOccurs="unbounded" />
        <xs:group ref="editorial-voice" />
        <xs:element name="type" type="note-type" minOccurs="0" />
        <xs:element name="dot" type="empty-placement" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
                <xs:documentation>One dot element is used for each dot of prolongation. The placement attribute is used to specify whether the dot should appear above or below the staff line. It is ignored for notes that appear on a staff space.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="accidental" type="accidental" minOccurs="0" />
        <xs:element name="time-modification" type="time-modification" minOccurs="0" />
        <xs:element name="stem" type="stem" minOccurs="0" />
        <xs:element name="notehead" type="notehead" minOccurs="0" />
        <xs:element name="notehead-text" type="notehead-text" minOccurs="0" />
        <xs:group ref="staff" minOccurs="0" />
        <xs:element name="beam" type="beam" minOccurs="0" maxOccurs="8" />
        <xs:element name="notations" type="notations" minOccurs="0" maxOccurs="unbounded" />
        <xs:element name="lyric" type="lyric" minOccurs="0" maxOccurs="unbounded" />
        <xs:element name="play" type="play" minOccurs="0" />
        <xs:element name="listen" type="listen" minOccurs="0" />
    </xs:sequence>
    <xs:attributeGroup ref="x-position" />
    <xs:attributeGroup ref="font" />
    <xs:attributeGroup ref="color" />
    <xs:attributeGroup ref="printout" />
    <xs:attribute name="print-leger" type="yes-no" />
    <xs:attribute name="dynamics" type="non-negative-decimal" />
    <xs:attribute name="end-dynamics" type="non-negative-decimal" />
    <xs:attribute name="attack" type="divisions" />
    <xs:attribute name="release" type="divisions" />
    <xs:attribute name="time-only" type="time-only" />
    <xs:attribute name="pizzicato" type="yes-no" />
    <xs:attributeGroup ref="optional-unique-id" />
</xs:complexType>
"""
                                      ))
# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_complex_types.py
# -----------------------------------------------------
