from musicscore.dtd.dtd import Element, GroupReference, Sequence, Choice
from musicscore.musicxml.attributes.grace_attributes import StealTimePrevious, StealTimeFollowing, MakeTime, Slash
from musicscore.musicxml.elements.fullnote import FullNote
from musicscore.musicxml.elements.xml_element import XMLElement
import copy

from musicscore.musicxml.types.complex_type import EmptyPlacement
from musicscore.musicxml.types.simple_type import PositiveDivisions, NoteTypeValue


class Grace(XMLElement, StealTimePrevious, StealTimeFollowing, MakeTime, Slash):
    """
    documentation>The grace type indicates the presence of a grace note. The slash attribute for a grace note is yes
    for slashed eighth notes. The other grace note attributes come from MuseData sound suggestions. The
    steal-time-previous attribute indicates the percentage of time to steal from the previous note for the grace note.
    The steal-time-following attribute indicates the percentage of time to steal from the following note for the grace
    note, as for appoggiaturas. The make-time attribute indicates to make time, not steal time; the units are in
    real-time divisions for the grace note.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='grace', *args, **kwargs)


# type="semitones"


class Tie(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='tie', *args, **kwargs)


class Cue(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='cue', *args, **kwargs)


class Duration(XMLElement, PositiveDivisions):
    """
    Duration is a positive number specified in division units. This is the intended duration vs. notated duration
    (for instance, swing eighths vs. even eighths, or differences in dotted notes in Baroque-era music). Differences
    in duration specific to an interpretation or performance should use the note element's attack and release
    attributes
    """

    def __init__(self, value=1, *args, **kwargs):
        super().__init__(tag='duration', value=value, *args, **kwargs)


"""The duration element is defined within a group due to its uses within the note, figure-bass, backup, and
forward elements.
"""
DurationGroup = Sequence(

    Element(Duration)
)


class Instrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='instrument', *args, **kwargs)


EditorialVoice = Sequence()


class Type(XMLElement, NoteTypeValue):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='type', *args, **kwargs)


class Dot(EmptyPlacement):
    """
    One dot element is used for each dot of prolongation. The placement element is used to specify whether the dot
    should appear above or below the staff line. It is ignored for notes that appear on a staff space.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='dot', *args, **kwargs)


class Accidental(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='accidental', *args, **kwargs)


class TimeModification(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='time-modification', *args, **kwargs)


class Stem(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='stem', *args, **kwargs)


class Notehead(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead', *args, **kwargs)


class NotheadText(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead-text', *args, **kwargs)


Staff = Sequence()


class Beam(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='beam', *args, **kwargs)


class Notations(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notations', *args, **kwargs)


class Lyric(XMLElement):
    """
    The lyric type represents text underlays for lyrics, based on Humdrum with support for other formats. Two text
    elements that are not separated by an elision element are part of the same syllable, but may have different text
    formatting. The MusicXML XSD is more strict than the DTD in enforcing this by disallowing a second syllabic element
    unless preceded by an elision element. The lyric number indicates multiple lines, though a name can be used as well
    (as in Finale's verse / chorus / section specification).

    Justification is center by default; placement is below by default. The print-object attribute can override a note's
    print-lyric attribute in cases where only some lyrics on a note are printed, as when lyrics for later verses are printed
    in a block of text rather than with each note. The time-only attribute precisely specifies which lyrics are to be sung
    which time through a repeated section.
    	<xs:complexType name="lyric">
		<xs:sequence>
			<xs:choice>
				<xs:sequence>
					<xs:element name="syllabic" type="syllabic" minOccurs="0"/>
					<xs:element name="text" type="text-element-data"/>
					<xs:sequence minOccurs="0" maxOccurs="unbounded">
						<xs:sequence minOccurs="0">
							<xs:element name="elision" type="elision"/>
							<xs:element name="syllabic" type="syllabic" minOccurs="0"/>
						</xs:sequence>
						<xs:element name="text" type="text-element-data"/>
					</xs:sequence>
					<xs:element name="extend" type="extend" minOccurs="0"/>
				</xs:sequence>
				<xs:element name="extend" type="extend"/>
				<xs:element name="laughing" type="empty">
					<xs:annotation>
						<xs:documentation>The laughing element is taken from Humdrum.</xs:documentation>
					</xs:annotation>
				</xs:element>
				<xs:element name="humming" type="empty">
					<xs:annotation>
						<xs:documentation>The humming element is taken from Humdrum.</xs:documentation>
					</xs:annotation>
				</xs:element>
			</xs:choice>
			<xs:element name="end-line" type="empty" minOccurs="0">
				<xs:annotation>
					<xs:documentation>The end-line element comes from RP-017 for Standard MIDI File Lyric meta-events. It facilitates lyric display for Karaoke and similar applications.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="end-paragraph" type="empty" minOccurs="0">
				<xs:annotation>
					<xs:documentation>The end-paragraph element comes from RP-017 for Standard MIDI File Lyric meta-events. It facilitates lyric display for Karaoke and similar applications.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:group ref="editorial"/>
		</xs:sequence>
		<xs:attribute name="number" type="xs:NMTOKEN"/>
		<xs:attribute name="name" type="xs:token"/>
		<xs:attributeGroup ref="justify"/>
		<xs:attributeGroup ref="position"/>
		<xs:attributeGroup ref="placement"/>
		<xs:attributeGroup ref="color"/>
		<xs:attributeGroup ref="print-object"/>
		<xs:attribute name="time-only" type="time-only"/>
		<xs:attributeGroup ref="optional-unique-id"/>
	</xs:complexType>
    """

    def __init__(self, text, *args, **kwargs):
        super().__init__(tag='lyric', *args, **kwargs)
        self.text = text


class Play(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='play', *args, **kwargs)


class Note(XMLElement):
    """
    Notes are the most common type of MusicXML data. The MusicXML format keeps the MuseData distinction between
    elements used for sound information and elements used for notation information (e.g., tie is used for sound,
    tied for notation). Thus grace notes do not have a duration element. Cue notes have a duration element, as do
    forward elements, but no tie elements. Having these two types of information available can make interchange
    considerably easier, as some programs handle one type of information much more readily than the other.

    The print-leger attribute is used to indicate whether leger lines are printed. Notes without leger lines are
    used to indicate indeterminate high and low notes. By default, it is set to yes. If print-object is set to no,
    print-leger is interpreted to also be set to no if not present. This attribute is ignored for rests.

    The dynamics and end-dynamics attributes correspond to MIDI 1.0's Note On and Note Off velocities, respectively.
    They are expressed in terms of percentages of the default forte value (90 for MIDI 1.0).

    The attack and release attributes are used to alter the starting and stopping time of the note from when it
    would otherwise occur based on the flow of durations - information that is specific to a performance. They are
    expressed in terms of divisions, either positive or negative. A note that starts a tie should not have a
    release attribute, and a note that stops a tie should not have an attack attribute. The attack and release
    attributes are independent of each other. The attack attribute only changes the starting time of a note, and
    the release attribute only changes the stopping time of a note.

    If a note is played only particular times through a repeat, the time-only attribute shows which times to
    play the note.

    The pizzicato attribute is used when just this note is sounded pizzicato, vs. the pizzicato element which
    changes overall playback between pizzicato and arco.
    """
    _DTD = Sequence(
        Choice(
            Sequence(
                Element(Grace),
                Choice(
                    Sequence(
                        GroupReference(FullNote)
                    ),
                    Sequence(
                        GroupReference(FullNote),
                        Element(Tie, 0, 2)
                    ),
                    Sequence(
                        Element(Cue),
                        GroupReference(FullNote)
                    )
                )
            ),
            Sequence(
                Element(Cue),
                GroupReference(FullNote),
                GroupReference(DurationGroup)
            ),
            Sequence(
                GroupReference(FullNote),
                GroupReference(DurationGroup),
                Element(Tie, 0, 2)
            )
        ),
        Element(Instrument, 0),
        GroupReference(EditorialVoice, 0),
        Element(Type, 0),
        Element(Dot, 0, None),
        Element(Accidental, 0),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        Element(Notehead, 0),
        Element(NotheadText, 0),
        GroupReference(Staff, 0),
        Element(Beam, 0, 8),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
        Element(Play, 0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='note', *args, **kwargs)
        self.dtd = copy.copy(self._DTD)
