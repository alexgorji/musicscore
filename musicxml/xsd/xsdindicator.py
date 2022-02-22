from musicxml.util.core import cap_first, convert_to_xml_class_name
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
import xml.etree.ElementTree as ET


class XSDSequence:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self._elements = None
        self.xsd_tree = xsd_tree

    @property
    def elements(self):
        if not self._elements:
            self._elements = []
            for child in self.xsd_tree.get_children():
                if child.tag == 'element':
                    element = convert_to_xml_class_name(child.name)
                    min_occurrence = child.get_attributes().get('minOccurs')
                    if min_occurrence is None: min_occurrence = '1'
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if max_occurrence is None: max_occurrence = '1'
                    self._elements.append((element, min_occurrence, max_occurrence))

                elif child.tag == 'group':
                    xsd_group_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in child.get_attributes()['ref'].split('-')])
                    elements = eval(xsd_group_name)().sequence.elements
                    min_occurrence = child.get_attributes().get('minOccurs')
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if min_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[1] = min_occurrence
                        elements[0] = tuple(list_el)
                    if max_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[2] = max_occurrence
                        elements[0] = tuple(list_el)
                    self._elements.extend(elements)
                else:
                    raise NotImplementedError(child.tag)
        return self._elements

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'sequence':
            raise ValueError
        self._xsd_tree = value


class XSDChoice:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self.xsd_tree = xsd_tree

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'choice':
            raise ValueError
        self._xsd_tree = value


class XSDGroup(XSDTreeElement):

    def __init__(self):
        self._sequence = None
        self._name = None

    @property
    def name(self):
        return self.XSD_TREE.name

    @property
    def sequence(self):
        if not self._sequence:
            for child in self.XSD_TREE.get_children():
                if child.tag == 'sequence':
                    self._sequence = XSDSequence(child)
        return self._sequence


# -----------------------------------------------------
# AUTOMATICALLY GENERATED WITH generate_indicators.py
# -----------------------------------------------------


class XSDGroupEditorial(XSDGroup):
    """The editorial group specifies editorial information for a musical element."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="editorial">
    <xs:annotation>
        <xs:documentation>The editorial group specifies editorial information for a musical element.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:group ref="footnote" minOccurs="0" />
        <xs:group ref="level" minOccurs="0" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupEditorialVoice(XSDGroup):
    """The editorial-voice group supports the common combination of editorial and voice information for a musical element."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="editorial-voice">
    <xs:annotation>
        <xs:documentation>The editorial-voice group supports the common combination of editorial and voice information for a musical element.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:group ref="footnote" minOccurs="0" />
        <xs:group ref="level" minOccurs="0" />
        <xs:group ref="voice" minOccurs="0" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupEditorialVoiceDirection(XSDGroup):
    """The editorial-voice-direction group supports the common combination of editorial and voice information for a direction element. It is separate from the editorial-voice element because extensions and restrictions might be different for directions than for the note and forward elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="editorial-voice-direction">
    <xs:annotation>
        <xs:documentation>The editorial-voice-direction group supports the common combination of editorial and voice information for a direction element. It is separate from the editorial-voice element because extensions and restrictions might be different for directions than for the note and forward elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:group ref="footnote" minOccurs="0" />
        <xs:group ref="level" minOccurs="0" />
        <xs:group ref="voice" minOccurs="0" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupFootnote(XSDGroup):
    """The footnote element specifies editorial information that appears in footnotes in the printed score. It is defined within a group due to its multiple uses within the MusicXML schema."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="footnote">
    <xs:annotation>
        <xs:documentation>The footnote element specifies editorial information that appears in footnotes in the printed score. It is defined within a group due to its multiple uses within the MusicXML schema.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="footnote" type="formatted-text" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupLevel(XSDGroup):
    """The level element specifies editorial information for different MusicXML elements. It is defined within a group due to its multiple uses within the MusicXML schema."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="level">
    <xs:annotation>
        <xs:documentation>The level element specifies editorial information for different MusicXML elements. It is defined within a group due to its multiple uses within the MusicXML schema.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="level" type="level" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupStaff(XSDGroup):
    """The staff element is defined within a group due to its use by both notes and direction elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="staff">
    <xs:annotation>
        <xs:documentation>The staff element is defined within a group due to its use by both notes and direction elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="staff" type="xs:positiveInteger">
            <xs:annotation>
                <xs:documentation>Staff assignment is only needed for music notated on multiple staves. Used by both notes and directions. Staff values are numbers, with 1 referring to the top-most staff in a part.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupTuning(XSDGroup):
    """The tuning group contains the sequence of elements common to the staff-tuning and accord elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="tuning">
    <xs:annotation>
        <xs:documentation>The tuning group contains the sequence of elements common to the staff-tuning and accord elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="tuning-step" type="step">
            <xs:annotation>
                <xs:documentation>The tuning-step element is represented like the step element, with a different name to reflect its different function in string tuning.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="tuning-alter" type="semitones" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The tuning-alter element is represented like the alter element, with a different name to reflect its different function in string tuning.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="tuning-octave" type="octave">
            <xs:annotation>
                <xs:documentation>The tuning-octave element is represented like the octave element, with a different name to reflect its different function in string tuning.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupVirtualInstrumentData(XSDGroup):
    """Virtual instrument data can be part of either the score-instrument element at the start of a part, or an instrument-change element within a part."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="virtual-instrument-data">
    <xs:annotation>
        <xs:documentation>Virtual instrument data can be part of either the score-instrument element at the start of a part, or an instrument-change element within a part.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="instrument-sound" type="xs:string" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The instrument-sound element describes the default timbre of the score-instrument. This description is independent of a particular virtual or MIDI instrument specification and allows playback to be shared more easily between applications and libraries.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:choice minOccurs="0">
            <xs:element name="solo" type="empty">
                <xs:annotation>
                    <xs:documentation>The solo element is present if performance is intended by a solo instrument.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="ensemble" type="positive-integer-or-empty">
                <xs:annotation>
                    <xs:documentation>The ensemble element is present if performance is intended by an ensemble such as an orchestral section. The text of the ensemble element contains the size of the section, or is empty if the ensemble size is not specified.</xs:documentation>
                </xs:annotation>
            </xs:element>
        </xs:choice>
        <xs:element name="virtual-instrument" type="virtual-instrument" minOccurs="0" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupVoice(XSDGroup):
    """A voice is a sequence of musical events (e.g. notes, chords, rests) that proceeds linearly in time. The voice element is used to distinguish between multiple voices in individual parts. It is defined within a group due to its multiple uses within the MusicXML schema."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="voice">
    <xs:annotation>
        <xs:documentation>A voice is a sequence of musical events (e.g. notes, chords, rests) that proceeds linearly in time. The voice element is used to distinguish between multiple voices in individual parts. It is defined within a group due to its multiple uses within the MusicXML schema.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="voice" type="xs:string" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupClef(XSDGroup):
    """Clefs are represented by a combination of sign, line, and clef-octave-change elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="clef">
    <xs:annotation>
        <xs:documentation>Clefs are represented by a combination of sign, line, and clef-octave-change elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="sign" type="clef-sign">
            <xs:annotation>
                <xs:documentation>The sign element represents the clef symbol.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="line" type="staff-line-position" minOccurs="0">
            <xs:annotation>
                <xs:documentation>Line numbers are counted from the bottom of the staff. They are only needed with the G, F, and C signs in order to position a pitch correctly on the staff. Standard values are 2 for the G sign (treble clef), 4 for the F sign (bass clef), and 3 for the C sign (alto clef). Line values can be used to specify positions outside the staff, such as a C clef positioned in the middle of a grand staff.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="clef-octave-change" type="xs:integer" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The clef-octave-change element is used for transposing clefs. A treble clef for tenors would have a value of -1.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupNonTraditionalKey(XSDGroup):
    """The non-traditional-key group represents a single alteration within a non-traditional key signature. A sequence of these groups makes up a non-traditional key signature"""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="non-traditional-key">
    <xs:annotation>
        <xs:documentation>The non-traditional-key group represents a single alteration within a non-traditional key signature. A sequence of these groups makes up a non-traditional key signature</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="key-step" type="step">
            <xs:annotation>
                <xs:documentation>Non-traditional key signatures are represented using a list of altered tones. The key-step element indicates the pitch step to be altered, represented using the same names as in the step element.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="key-alter" type="semitones">
            <xs:annotation>
                <xs:documentation>Non-traditional key signatures are represented using a list of altered tones. The key-alter element represents the alteration for a given pitch step, represented with semitones in the same manner as the alter element.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="key-accidental" type="key-accidental" minOccurs="0">
            <xs:annotation>
                <xs:documentation>Non-traditional key signatures are represented using a list of altered tones. The key-accidental element indicates the accidental to be displayed in the key signature, represented in the same manner as the accidental element. It is used for disambiguating microtonal accidentals.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupSlash(XSDGroup):
    """The slash group combines elements used for more complete specification of the slash and beat-repeat measure-style elements. They have the same values as the type and dot elements, and define what the beat is for the display of repetition marks. If not present, the beat is based on the current time signature."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="slash">
    <xs:annotation>
        <xs:documentation>The slash group combines elements used for more complete specification of the slash and beat-repeat measure-style elements. They have the same values as the type and dot elements, and define what the beat is for the display of repetition marks. If not present, the beat is based on the current time signature.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:sequence minOccurs="0">
            <xs:element name="slash-type" type="note-type-value">
                <xs:annotation>
                    <xs:documentation>The slash-type element indicates the graphical note type to use for the display of repetition marks.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="slash-dot" type="empty" minOccurs="0" maxOccurs="unbounded">
                <xs:annotation>
                    <xs:documentation>The slash-dot element is used to specify any augmentation dots in the note type used to display repetition marks.</xs:documentation>
                </xs:annotation>
            </xs:element>
        </xs:sequence>
        <xs:element name="except-voice" type="xs:string" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
                <xs:documentation>The except-voice element is used to specify a combination of slash notation and regular notation. Any note elements that are in voices specified by the except-voice elements are displayed in normal notation, in addition to the slash notation that is always displayed.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupTimeSignature(XSDGroup):
    """Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="time-signature">
    <xs:annotation>
        <xs:documentation>Time signatures are represented by the beats element for the numerator and the beat-type element for the denominator.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="beats" type="xs:string">
            <xs:annotation>
                <xs:documentation>The beats element indicates the number of beats, as found in the numerator of a time signature.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="beat-type" type="xs:string">
            <xs:annotation>
                <xs:documentation>The beat-type element indicates the beat unit, as found in the denominator of a time signature.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupTraditionalKey(XSDGroup):
    """The traditional-key group represents a traditional key signature using the cycle of fifths."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="traditional-key">
    <xs:annotation>
        <xs:documentation>The traditional-key group represents a traditional key signature using the cycle of fifths.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="cancel" type="cancel" minOccurs="0" />
        <xs:element name="fifths" type="fifths" />
        <xs:element name="mode" type="mode" minOccurs="0" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupTranspose(XSDGroup):
    """The transpose group represents what must be added to a written pitch to get a correct sounding pitch."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="transpose">
    <xs:annotation>
        <xs:documentation>The transpose group represents what must be added to a written pitch to get a correct sounding pitch.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="diatonic" type="xs:integer" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The diatonic element specifies the number of pitch steps needed to go from written to sounding pitch. This allows for correct spelling of enharmonic transpositions. This value does not include octave-change values; the values for both elements need to be added to the written pitch to get the correct sounding pitch.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="chromatic" type="semitones">
            <xs:annotation>
                <xs:documentation>The chromatic element represents the number of semitones needed to get from written to sounding pitch. This value does not include octave-change values; the values for both elements need to be added to the written pitch to get the correct sounding pitch.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="octave-change" type="xs:integer" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The octave-change element indicates how many octaves to add to get from written pitch to sounding pitch. The octave-change element should be included when using transposition intervals of an octave or more, and should not be present for intervals of less than an octave.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="double" type="double" minOccurs="0">
            <xs:annotation>
                <xs:documentation>If the double element is present, it indicates that the music is doubled one octave from what is currently written.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupBeatUnit(XSDGroup):
    """The beat-unit group combines elements used repeatedly in the metronome element to specify a note within a metronome mark."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="beat-unit">
    <xs:annotation>
        <xs:documentation>The beat-unit group combines elements used repeatedly in the metronome element to specify a note within a metronome mark.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="beat-unit" type="note-type-value">
            <xs:annotation>
                <xs:documentation>The beat-unit element indicates the graphical note type to use in a metronome mark.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="beat-unit-dot" type="empty" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
                <xs:documentation>The beat-unit-dot element is used to specify any augmentation dots for a metronome mark note.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupHarmonyChord(XSDGroup):
    """A harmony element can contain many stacked chords (e.g. V of II). A sequence of harmony-chord groups is used for this type of secondary function, where V of II would be represented by a harmony-chord with a 5 numeral followed by a harmony-chord with a 2 numeral.

A root is a pitch name like C, D, E, while a numeral is a scale degree like 1, 2, 3. The root element is generally used with pop chord symbols, while the numeral element is generally used with classical functional harmony and Nashville numbers. It is an either/or choice to avoid data inconsistency. The function element, which represents Roman numerals with roman numeral text, has been deprecated as of MusicXML 4.0."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="harmony-chord">
    <xs:annotation>
        <xs:documentation>A harmony element can contain many stacked chords (e.g. V of II). A sequence of harmony-chord groups is used for this type of secondary function, where V of II would be represented by a harmony-chord with a 5 numeral followed by a harmony-chord with a 2 numeral.

A root is a pitch name like C, D, E, while a numeral is a scale degree like 1, 2, 3. The root element is generally used with pop chord symbols, while the numeral element is generally used with classical functional harmony and Nashville numbers. It is an either/or choice to avoid data inconsistency. The function element, which represents Roman numerals with roman numeral text, has been deprecated as of MusicXML 4.0.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:choice>
            <xs:element name="root" type="root" />
            <xs:element name="numeral" type="numeral" />
            <xs:element name="function" type="style-text">
                <xs:annotation>
                    <xs:documentation>The function element represents classical functional harmony with an indication like I, II, III rather than C, D, E. It represents the Roman numeral part of a functional harmony rather than the complete function itself. It has been deprecated as of MusicXML 4.0 in favor of the numeral element.</xs:documentation>
                </xs:annotation>
            </xs:element>
        </xs:choice>
        <xs:element name="kind" type="kind" />
        <xs:element name="inversion" type="inversion" minOccurs="0" />
        <xs:element name="bass" type="bass" minOccurs="0" />
        <xs:element name="degree" type="degree" minOccurs="0" maxOccurs="unbounded" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupAllMargins(XSDGroup):
    """The all-margins group specifies both horizontal and vertical margins in tenths."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="all-margins">
    <xs:annotation>
        <xs:documentation>The all-margins group specifies both horizontal and vertical margins in tenths.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:group ref="left-right-margins" />
        <xs:element name="top-margin" type="tenths" />
        <xs:element name="bottom-margin" type="tenths" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupLayout(XSDGroup):
    """The layout group specifies the sequence of page, system, and staff layout elements that is common to both the defaults and print elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="layout">
    <xs:annotation>
        <xs:documentation>The layout group specifies the sequence of page, system, and staff layout elements that is common to both the defaults and print elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="page-layout" type="page-layout" minOccurs="0" />
        <xs:element name="system-layout" type="system-layout" minOccurs="0" />
        <xs:element name="staff-layout" type="staff-layout" minOccurs="0" maxOccurs="unbounded" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupLeftRightMargins(XSDGroup):
    """The left-right-margins group specifies horizontal margins in tenths."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="left-right-margins">
    <xs:annotation>
        <xs:documentation>The left-right-margins group specifies horizontal margins in tenths.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="left-margin" type="tenths" />
        <xs:element name="right-margin" type="tenths" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupDuration(XSDGroup):
    """The duration element is defined within a group due to its uses within the note, figured-bass, backup, and forward elements."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="duration">
    <xs:annotation>
        <xs:documentation>The duration element is defined within a group due to its uses within the note, figured-bass, backup, and forward elements.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="duration" type="positive-divisions">
            <xs:annotation>
                <xs:documentation>Duration is a positive number specified in division units. This is the intended duration vs. notated duration (for instance, differences in dotted notes in Baroque-era music). Differences in duration specific to an interpretation or performance should be represented using the note element's attack and release attributes.

The duration element moves the musical position when used in backup elements, forward elements, and note elements that do not contain a chord child element.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupDisplayStepOctave(XSDGroup):
    """The display-step-octave group contains the sequence of elements used by both the rest and unpitched elements. This group is used to place rests and unpitched elements on the staff without implying that these elements have pitch. Positioning follows the current clef. If percussion clef is used, the display-step and display-octave elements are interpreted as if in treble clef, with a G in octave 4 on line 2."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="display-step-octave">
    <xs:annotation>
        <xs:documentation>The display-step-octave group contains the sequence of elements used by both the rest and unpitched elements. This group is used to place rests and unpitched elements on the staff without implying that these elements have pitch. Positioning follows the current clef. If percussion clef is used, the display-step and display-octave elements are interpreted as if in treble clef, with a G in octave 4 on line 2.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="display-step" type="step" />
        <xs:element name="display-octave" type="octave" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupFullNote(XSDGroup):
    """The full-note group is a sequence of the common note elements between cue/grace notes and regular (full) notes: pitch, chord, and rest information, but not duration (cue and grace notes do not have duration encoded). Unpitched elements are used for unpitched percussion, speaking voice, and other musical elements lacking determinate pitch."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="full-note">
    <xs:annotation>
        <xs:documentation>The full-note group is a sequence of the common note elements between cue/grace notes and regular (full) notes: pitch, chord, and rest information, but not duration (cue and grace notes do not have duration encoded). Unpitched elements are used for unpitched percussion, speaking voice, and other musical elements lacking determinate pitch.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="chord" type="empty" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The chord element indicates that this note is an additional chord tone with the preceding note.

The duration of a chord note does not move the musical position within a measure. That is done by the duration of the first preceding note without a chord element. Thus the duration of a chord note cannot be longer than the preceding note.
							
In most cases the duration will be the same as the preceding note. However it can be shorter in situations such as multiple stops for string instruments.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:choice>
            <xs:element name="pitch" type="pitch" />
            <xs:element name="unpitched" type="unpitched" />
            <xs:element name="rest" type="rest" />
        </xs:choice>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupMusicData(XSDGroup):
    """The music-data group contains the basic musical data that is either associated with a part or a measure, depending on whether the partwise or timewise hierarchy is used."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="music-data">
    <xs:annotation>
        <xs:documentation>The music-data group contains the basic musical data that is either associated with a part or a measure, depending on whether the partwise or timewise hierarchy is used.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:choice minOccurs="0" maxOccurs="unbounded">
            <xs:element name="note" type="note" />
            <xs:element name="backup" type="backup" />
            <xs:element name="forward" type="forward" />
            <xs:element name="direction" type="direction" />
            <xs:element name="attributes" type="attributes" />
            <xs:element name="harmony" type="harmony" />
            <xs:element name="figured-bass" type="figured-bass" />
            <xs:element name="print" type="print" />
            <xs:element name="sound" type="sound" />
            <xs:element name="listening" type="listening" />
            <xs:element name="barline" type="barline" />
            <xs:element name="grouping" type="grouping" />
            <xs:element name="link" type="link" />
            <xs:element name="bookmark" type="bookmark" />
        </xs:choice>
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupPartGroup(XSDGroup):
    """The part-group element is defined within a group due to its multiple uses within the part-list element."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="part-group">
    <xs:annotation>
        <xs:documentation>The part-group element is defined within a group due to its multiple uses within the part-list element.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="part-group" type="part-group" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupScoreHeader(XSDGroup):
    """The score-header group contains basic score metadata about the work and movement, score-wide defaults for layout and fonts, credits that appear on the first or following pages, and the part list."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="score-header">
    <xs:annotation>
        <xs:documentation>The score-header group contains basic score metadata about the work and movement, score-wide defaults for layout and fonts, credits that appear on the first or following pages, and the part list.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="work" type="work" minOccurs="0" />
        <xs:element name="movement-number" type="xs:string" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The movement-number element specifies the number of a movement.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="movement-title" type="xs:string" minOccurs="0">
            <xs:annotation>
                <xs:documentation>The movement-title element specifies the title of a movement, not including its number.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="identification" type="identification" minOccurs="0" />
        <xs:element name="defaults" type="defaults" minOccurs="0" />
        <xs:element name="credit" type="credit" minOccurs="0" maxOccurs="unbounded" />
        <xs:element name="part-list" type="part-list" />
    </xs:sequence>
</xs:group>
"""
                                     ))


class XSDGroupScorePart(XSDGroup):
    """The score-part element is defined within a group due to its multiple uses within the part-list element."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:group xmlns:xs="http://www.w3.org/2001/XMLSchema" name="score-part">
    <xs:annotation>
        <xs:documentation>The score-part element is defined within a group due to its multiple uses within the part-list element.</xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:element name="score-part" type="score-part">
            <xs:annotation>
                <xs:documentation>Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port assignment for the given track. Initial midi-instrument assignments may be made here as well.</xs:documentation>
            </xs:annotation>
        </xs:element>
    </xs:sequence>
</xs:group>
"""
                                     ))


__all__ = ['XSDSequence', 'XSDChoice', 'XSDGroup', 'XSDGroupEditorial', 'XSDGroupEditorialVoice', 'XSDGroupEditorialVoiceDirection',
           'XSDGroupFootnote', 'XSDGroupLevel', 'XSDGroupStaff', 'XSDGroupTuning', 'XSDGroupVirtualInstrumentData', 'XSDGroupVoice',
           'XSDGroupClef', 'XSDGroupNonTraditionalKey', 'XSDGroupSlash', 'XSDGroupTimeSignature', 'XSDGroupTraditionalKey',
           'XSDGroupTranspose', 'XSDGroupBeatUnit', 'XSDGroupHarmonyChord', 'XSDGroupAllMargins', 'XSDGroupLayout',
           'XSDGroupLeftRightMargins', 'XSDGroupDuration', 'XSDGroupDisplayStepOctave', 'XSDGroupFullNote', 'XSDGroupMusicData',
           'XSDGroupPartGroup', 'XSDGroupScoreHeader', 'XSDGroupScorePart']
