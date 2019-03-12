from musicscore.dtd.dtd import Element, Group, Sequence, Choice
from musicscore.musicxml.attributes.grace_attributes import StealTimePrevious, StealTimeFollowing, MakeTime, Slash
from musicscore.musicxml.elements.xml_element import XMLElementGroup, XMLElement2
import copy

from musicscore.musicxml.types.simple_type import PositiveDevisions, Step, Alter, Octave


class Grace(XMLElement2, StealTimePrevious, StealTimeFollowing, MakeTime, Slash):
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


class Chord(XMLElement2):
    """
    The chord element indicates that this note is an additional chord tone with the preceding note. The duration of
    this note can be no longer than the preceding note. In MuseData, a missing duration indicates the same length as
    the previous note, but the MusicXML format requires a duration for chord notes too
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='chord', *args, **kwargs)


class XMLStep(XMLElement2, Step):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='step', value=value, *args, **kwargs)


# type="semitones"
class XMLAlter(XMLElement2, Alter):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='alter', value=value, *args, **kwargs)


class XMLOctave(XMLElement2, Octave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='octave', value=value, *args, **kwargs)


class XMLPitch(XMLElement2):
    """
    Pitch is represented as a combination of the step of the diatonic scale, the chromatic alteration, and the octave.
    """
    _DTD = Sequence(
        Element(XMLStep),
        Element(XMLAlter, min_occurrence=0),
        Element(XMLOctave)
    )

    def __init__(self, step=XMLStep('C'), alter=None, octave=XMLOctave(4)):
        super().__init__(tag='pitch')
        self._step = None
        self.step = step
        self._alter = None
        self.alter = alter
        self._octave = None
        self.octave = octave

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._set_child(XMLStep, 'step', value)

    @property
    def alter(self):
        return self._alter

    @alter.setter
    def alter(self, value):
        self._set_child(XMLAlter, 'alter', value)

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):
        self._set_child(XMLOctave, 'octave', value)


class Unpitched(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='unpitched', *args, **kwargs)


class XMLDisplayStep(XMLElement2, Step):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-step', value=value, *args, **kwargs)


class XMLDisplayOctave(XMLElement2, Octave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-octave', value=value, *args, **kwargs)


class DisplayStepOctave(XMLElementGroup):
    """
    The display-step-octave group contains the sequence of elements used by both the rest and unpitched elements. This
    group is used to place rests and unpitched elements on the staff without implying that these elements have pitch.
    Positioning follows the current clef. If percussion clef is used, the display-step and display-octave elements are
    interpreted as if in treble clef, with a G in octave 4 on line 2. If not present, the note is placed on the middle
    line of the staff, generally used for a one-line staff.
    """
    _DTD = Sequence(
        Element(XMLDisplayStep),
        Element(XMLDisplayOctave)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class XMLRest(XMLElement2):
    """
    The rest element indicates notated rests or silences. Rest elements are usually empty, but placement on the staff
    can be specified using display-step and  display-octave elements. If the measure attribute is set to yes, this
    indicates this is a complete measure rest.
    """

    _DTD = Sequence(
        Group(DisplayStepOctave, min_occurrence=0)
    )

    def __init__(self):
        super().__init__(tag='rest')


class FullNote(XMLElementGroup):
    """The full-note group is a sequence of the common note elements between cue/grace notes and regular (full) notes:
    pitch, chord, and rest information, but not duration (cue and grace notes do not have duration encoded). Unpitched
    elements are used for unpitched percussion, speaking voice, and other musical elements lacking determinate pitch
    	<xs:group name="full-note">
		<xs:sequence>
			<xs:element name="chord" type="empty" minOccurs="0">
			</xs:element>
			<xs:choice>
				<xs:element name="pitch" type="pitch"/>
				<xs:element name="unpitched" type="unpitched"/>
				<xs:element name="rest" type="rest"/>
			</xs:choice>
		</xs:sequence>
	</xs:group>
    """
    _DTD = Sequence(
        Element(Chord, min_occurrence=0),
        Choice(
            Element(XMLPitch),
            Element(Unpitched),
            Element(XMLRest)
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tie(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='tie', *args, **kwargs)


class Cue(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='cue', *args, **kwargs)


# type="positive-divisions">
class Duration(XMLElement2, PositiveDevisions):
    """
    Duration is a positive number specified in division units. This is the intended duration vs. notated duration
    (for instance, swing eighths vs. even eighths, or differences in dotted notes in Baroque-era music). Differences
    in duration specific to an interpretation or performance should use the note element's attack and release
    attributes
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='duration', value=value, *args, **kwargs)


class DurationGroup(XMLElementGroup):
    """The duration element is defined within a group due to its uses within the note, figure-bass, backup, and
    forward elements.
    """

    _DTD = Sequence(
        Element(Duration)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Instrument(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='instrument', *args, **kwargs)


class EditorialVoice(XMLElementGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Type(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='type', *args, **kwargs)


class Dot(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='dot', *args, **kwargs)


class Accidental(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='accidental', *args, **kwargs)


class TimeModification(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='time-modification', *args, **kwargs)


class Stem(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='stem', *args, **kwargs)


class Notehead(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead', *args, **kwargs)


class NotheadText(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead-text', *args, **kwargs)


class Staff(XMLElementGroup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Beam(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='beam', *args, **kwargs)


class Notations(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notations', *args, **kwargs)


class Lyric(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='lyric', *args, **kwargs)


class Play(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='play', *args, **kwargs)


class Note(XMLElement2):
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
                        Group(FullNote)
                    ),
                    Sequence(
                        Group(FullNote),
                        Element(Tie, 0, 2)
                    ),
                    Sequence(
                        Element(Cue),
                        Group(FullNote)
                    )
                )
            ),
            Sequence(
                Element(Cue),
                Group(FullNote),
                Group(DurationGroup)
            ),
            Sequence(
                Group(FullNote),
                Group(DurationGroup),
                Element(Tie, 0, 2)
            )
        ),
        Element(Instrument, 0),
        Group(EditorialVoice, 0),
        Element(Type, 0),
        Element(Dot, 0, None),
        Element(Accidental, 0),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        Element(Notehead, 0),
        Element(NotheadText, 0),
        Group(Staff, 0),
        Element(Beam, 0, 8),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
        Element(Play, 0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='note', *args, **kwargs)
        self.dtd = copy.copy(self._DTD)
