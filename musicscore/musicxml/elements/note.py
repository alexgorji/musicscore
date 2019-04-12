from musicscore.dtd.dtd import Element, GroupReference, Sequence, Choice
from musicscore.musicxml.attributes.accidental import Cautionary, Editorial, Smulf
from musicscore.musicxml.attributes.grace_attributes import StealTimePrevious, StealTimeFollowing, MakeTime, Slash
from musicscore.musicxml.attributes.leveldisplay import LevelDisplay
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.common.common import FootNote, Level, EditorialVoice, Staff
from musicscore.musicxml.elements.fullnote import FullNote
from musicscore.musicxml.elements.xml_element import XMLElement
import copy

from musicscore.musicxml.types.complextypes.complextype import EmptyPlacement, ComplexType
from musicscore.musicxml.types.complextypes.beam import ComplexTypeBeam
from musicscore.musicxml.types.complextypes.lyric import ComplexTypeLyric
from musicscore.musicxml.types.complextypes.notations import ComplexTypeNotations
from musicscore.musicxml.types.complextypes.tie import ComplexTypeTie
from musicscore.musicxml.types.complextypes.timemodification import ComplexTypeTimeModification
from musicscore.musicxml.types.simple_type import TypePositiveDivisions, TypeNoteTypeValue, TypeAccidentalValue


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


class Tie(ComplexTypeTie):
    """
    The tie element indicates that a tie begins or ends with this note. If the tie element applies only particular times
    through a repeat, the time-only attribute indicates which times to apply it. The tie element indicates sound; the
    tied element indicates notation.</xs:documentation>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Cue(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='cue', *args, **kwargs)


class Duration(XMLElement, TypePositiveDivisions):
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


class Type(XMLElement, TypeNoteTypeValue):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='type', value=value, *args, **kwargs)


class Dot(EmptyPlacement):
    """
    One dot element is used for each dot of prolongation. The placement element is used to specify whether the dot
    should appear above or below the staff line. It is ignored for notes that appear on a staff space.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='dot', *args, **kwargs)


class Accidental(ComplexType, TypeAccidentalValue, Cautionary, Editorial, LevelDisplay, PrintStyle, Smulf):
    """
    The accidental type represents actual notated accidentals. Editorial and cautionary indications are indicated by 
    attributes. Values for these attributes are "no" if not present. Specific graphic display such as parentheses, 
    brackets, and size are controlled by the level-display attribute group
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='accidental', value=value, *args, **kwargs)


class TimeModification(ComplexTypeTimeModification):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Stem(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='stem', *args, **kwargs)
        raise NotImplementedError()


class Notehead(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead', *args, **kwargs)
        raise NotImplementedError()


class NoteheadText(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notehead-text', *args, **kwargs)
        raise NotImplementedError()


class Beam(ComplexTypeBeam):
    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Notations(ComplexTypeNotations):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lyric(ComplexTypeLyric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Play(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='play', *args, **kwargs)
        raise NotImplementedError()


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
                GroupReference(FullNote),
                GroupReference(DurationGroup),
                Element(Tie, 0, 2)
            ),
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
        ),
        Element(Instrument, 0),
        GroupReference(EditorialVoice, 0),
        Element(Type, 0),
        Element(Dot, 0, None),
        Element(Accidental, 0),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        Element(Notehead, 0),
        Element(NoteheadText, 0),
        GroupReference(Staff, 0),
        Element(Beam, 0, 8),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
        Element(Play, 0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='note', *args, **kwargs)
