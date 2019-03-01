'''
<!ELEMENT note
	(
	    (
	        (grace,
	            (
	                (%full-note;, (tie, tie?)?)
	                |
	                (cue, %full-note;)
	            )
	        )
	        |
	        (cue, %full-note;, duration)
	        |
	        (%full-note;, duration, (tie, tie?)?)
	        ),
	    instrument?,
	    %editorial-voice;,
	    type?,
	    dot*,
	    accidental?,
	    time-modification?,
	    stem?,
	    notehead?,
	    notehead-text?,
	    staff?,
	    beam*,
	    notations*,
	    lyric*,
	    play?
	)>
'''
from musicscore.musicxml.elements.xml_element import XMLElement, XMLElementGroup

'''
<xs:group name="editorial-voice">
    <xs:annotation>
		<xs:documentation>The editorial-voice group supports the common combination of editorial and voice information 
		for a musical element.</xs:documentation>
	</xs:annotation>		
	<xs:sequence>
		<xs:group ref="footnote" minOccurs="0"/>
		<xs:group ref="level" minOccurs="0"/>
		<xs:group ref="voice" minOccurs="0"/>
	</xs:sequence>
</xs:group>

<xs:group name="full-note">
		<xs:annotation>
			<xs:documentation>The full-note group is a sequence of the common note elements between cue/grace notes and 
			regular (full) notes: pitch, chord, and rest information, but not duration (cue and grace notes do not have 
			duration encoded). Unpitched elements are used for unpitched percussion, speaking voice, and other musical 
			elements lacking determinate pitch.</xs:documentation>
		</xs:annotation>
		<xs:sequence>
			<xs:element name="chord" type="empty" minOccurs="0">
				<xs:annotation>
					<xs:documentation>The chord element indicates that this note is an additional chord tone with the 
					preceding note. The duration of this note can be no longer than the preceding note. In MuseData, 
					a missing duration indicates the same length as the previous note, but the MusicXML format requires 
					ma duration for chord notes too.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:choice>
				<xs:element name="pitch" type="pitch"/>
				<xs:element name="unpitched" type="unpitched"/>
				<xs:element name="rest" type="rest"/>
			</xs:choice>
		</xs:sequence>
	</xs:group>

<xs:complexType name="note">
    <xs:annotation>
        <xs:documentation>
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
        </xs:documentation>
    </xs:annotation>
    <xs:sequence>
        <xs:choice>
            <xs:sequence>
                <xs:element name="grace" type="grace"/>
                <xs:choice>
                    <xs:sequence>
                        <xs:group ref="full-note"/>
                        <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2"/>
                    </xs:sequence>
                    <xs:sequence>
                        <xs:element name="cue" type="empty"/>
                        <xs:group ref="full-note"/>
                    </xs:sequence>
                </xs:choice>
            </xs:sequence>
            <xs:sequence>
                <xs:element name="cue" type="empty">
                    <xs:annotation>
                        <xs:documentation>
                        The cue element indicates the presence of a cue note. In MusicXML, a cue note is a silent note 
                        with no playback. Normal notes that play can be specified as cue size using the type element. A 
                        cue note that is specified as full size using the type element will still remain silent.
                        </xs:documentation>
                    </xs:annotation>
                </xs:element>
                <xs:group ref="full-note"/>
                <xs:group ref="duration"/>
            </xs:sequence>
            <xs:sequence>
                <xs:group ref="full-note"/>
                <xs:group ref="duration"/>
                <xs:element name="tie" type="tie" minOccurs="0" maxOccurs="2"/>
            </xs:sequence>
        </xs:choice>
        <xs:element name="instrument" type="instrument" minOccurs="0"/>
        <xs:group ref="editorial-voice"/>
        <xs:element name="type" type="note-type" minOccurs="0"/>
        <xs:element name="dot" type="empty-placement" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
                <xs:documentation>One dot element is used for each dot of prolongation. The placement element is used 
                to specify whether the dot should appear above or below the staff line. It is ignored for notes that 
                appear on a staff space.</xs:documentation>
            </xs:annotation>
        </xs:element>
        <xs:element name="accidental" type="accidental" minOccurs="0"/>
        <xs:element name="time-modification" type="time-modification" minOccurs="0"/>
        <xs:element name="stem" type="stem" minOccurs="0"/>
        <xs:element name="notehead" type="notehead" minOccurs="0"/>
        <xs:element name="notehead-text" type="notehead-text" minOccurs="0"/>
        <xs:group ref="staff" minOccurs="0"/>
        <xs:element name="beam" type="beam" minOccurs="0" maxOccurs="8"/>
        <xs:element name="notations" type="notations" minOccurs="0" maxOccurs="unbounded"/>
        <xs:element name="lyric" type="lyric" minOccurs="0" maxOccurs="unbounded"/>
        <xs:element name="play" type="play" minOccurs="0"/>
    </xs:sequence>
    <xs:attributeGroup ref="x-position"/>
    <xs:attributeGroup ref="font"/>
    <xs:attributeGroup ref="color"/>
    <xs:attributeGroup ref="printout"/>
    <xs:attribute name="print-leger" type="yes-no"/>
    <xs:attribute name="dynamics" type="non-negative-decimal"/>
    <xs:attribute name="end-dynamics" type="non-negative-decimal"/>
    <xs:attribute name="attack" type="divisions"/>
    <xs:attribute name="release" type="divisions"/>
    <xs:attribute name="time-only" type="time-only"/>
    <xs:attribute name="pizzicato" type="yes-no"/>
    <xs:attributeGroup ref="optional-unique-id"/>
</xs:complexType>
'''


class Grace(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='grace', *args, **kwargs)


class FullNote(XMLElementGroup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tie(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='tie', *args, **kwargs)


class Cue(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='cue', *args, **kwargs)


class Duration(XMLElementGroup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Instrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='instrument', *args, **kwargs)


class EditorialVoice(XMLElementGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='instrument', *args, **kwargs)


class Type(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='type', *args, **kwargs)


class Dot(XMLElement):
    """"""

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


class Staff(XMLElementGroup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Beam(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='beam', *args, **kwargs)


class Notations(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notations', *args, **kwargs)


class Lyric(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='lyric', *args, **kwargs)


class Play(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='play', *args, **kwargs)

# bla = (
#     Sequence(
#         Choice(
#             Sequence(
#                 Element(Grace),
#                 Choice(
#                     Sequence(
#                         Group(FullNote)
#                     ),
#                     Sequence(
#                         Group(FullNote),
#                         Element(Tie, 0, 2)
#                     ),
#                     Sequence(
#                         Element(Cue),
#                         Group(FullNote)
#                     )
#                 )
#             ),
#             Sequence(
#                 Element(Cue),
#                 Group(FullNote),
#                 Group(Duration)
#             ),
#             Sequence(
#                 Group(FullNote),
#                 Group(Duration),
#                 Element(Tie, 0, 2)
#             )
#         ),
#         Element(Instrument, 0),
#         Group(EditorialVoice),
#         Element(Type, 0),
#         Element(Dot, 0, None),
#         Element(Accidental, 0),
#         Element(TimeModification, 0, None),
#         Element(Stem, 0),
#         Element(Notehead, 0),
#         Element(NotheadText, 0),
#         Group(Staff, 0),
#         Element(Beam, 0, 8),
#         Element(Notations, 0, None),
#         Element(Lyric, 0, None),
#         Element(Play, 0)
#     )
# )