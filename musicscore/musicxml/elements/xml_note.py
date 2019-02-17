from musicscore.musicxml.types.complex_type import Empty, EmptyPlacement
from musicscore.musicxml.types.simple_type import Step, Octave, Alter, PositiveDevisions, NoteTypeValue
from musicscore.musicxml.elements.xml_element import XMLElement, XMLElementGroup
from musicscore.musicxml.elements.xml_music_data import XMLMusicData

"""
Notes are the most common type of MusicXML musicxml. The
MusicXML format keeps the MuseData distinction between
elements used for sound information and elements used for
notation information (e.g., tie is used for sound, tied for
notation). Thus grace notes do not have a duration element.
Cue notes have a duration element, as do forward elements,
but no tie elements. Having these two types of information
available can make interchange considerably easier, as
some programs handle one type of information much more
readily than the other.
"""

"""
%full-note; --> (chord?, (pitch | unpitched | rest))
(
    (
        (grace, ((%full-note;, (tie, tie?)?) | (cue, %full-note;))) |
        (cue, %full-note;, duration) |
        (%full-note;, duration, (tie, tie?)?)
    ), instrument?, %editorial-voice;, type?, dot*, accidental?, time-modification?, stem?, notehead?, notehead-text?, staff?, beam*, notations*, lyric*, play?
)
"""


class XMLEvent(XMLElement):
    def __init__(self, tag):
        super().__init__(tag=tag)


class XMLStep(XMLElement, Step):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='step', value=value, *args, **kwargs)
        self.text = value


class XMLAlter(XMLElement, Alter):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='alter', value=value, *args, **kwargs)
        self.text = value


class XMLOctave(XMLElement, Octave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='octave', value=value, *args, **kwargs)
        self.text = value


class XMLPitch(XMLEvent):
    """
    pitch(step, alter?, octave)
    """
    _CHILDREN_TYPES = [XMLStep, XMLAlter, XMLOctave]
    _CHILDREN_ORDERED = True

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


class XMLDisplayStep(XMLElement, Step):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-step', value=value, *args, **kwargs)
        self.text = value


class XMLDisplayOctave(XMLElement, Octave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-octave', value=value, *args, **kwargs)
        self.text = value


class XMLRest(XMLEvent):
    """
    The rest element indicates notated rests or silences.
    Rest elements are usually empty, but placement on the staff can be specified using display-step and
    display-octave elements.
    If the measure attribute is set to yes, this indicates this is a complete measure rest.
    """
    _CHILDREN_TYPES = [XMLDisplayStep, XMLDisplayOctave]
    _CHILDREN_ORDERED = True

    def __init__(self, display_step=None, display_octave=None):
        super().__init__(tag='rest')
        self._display_step = None
        self.display_step = display_step
        self._display_octave = None
        self.display_octave = display_octave

    @property
    def display_step(self):
        return self._display_step

    @display_step.setter
    def display_step(self, value):
        self._set_child(XMLDisplayStep, 'display-step', value)

    @property
    def display_octave(self):
        return self._display_octave

    @display_octave.setter
    def display_octave(self, value):
        self._set_child(XMLDisplayOctave, 'display-octave', value)


class XMLChord(Empty):
    def __init__(self):
        super().__init__(tag='chord')


class XMLDuration(XMLElement, PositiveDevisions):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='duration', value=value, *args, **kwargs)
        self.text = value


class XMLType(XMLElement, NoteTypeValue):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='type', value=value, *args, **kwargs)
        self.text = value


class XMLDot(EmptyPlacement):
    """
    One dot element is used for each dot of prolongation.
    The placement element is used to specify whether the dot should appear above or below the staff line.
    It is ignored for notes that appear on a staff space
    """

    def __init__(self):
        super().__init__(tag='dot')


class XMLDotGroup(XMLElementGroup):
    def __init__(self):
        super().__init__(tag='dot')


class XMLLyric(XMLElement):
    def __init__(self, text):
        super().__init__(tag='lyric')
        self.text = text


class XMLLyricGroup(XMLElementGroup):
    # TODO: LYRIC is still a dummy
    def __init__(self):
        super().__init__(tag='lyric')


class XMLNoteAbstract(XMLElement, XMLMusicData):
    # _CHILDREN_TYPES_ORDER = [XMLFullNote, XMLDuration, XMLTie, XMLType, XMLDots, XMLAccidental, XMLTimeModification, XMLNoteHead, XMLNotations, XMLLyrics]
    _CHILDREN_TYPES = [XMLChord, XMLEvent, XMLDuration, XMLType, XMLLyricGroup]
    _CHILDREN_ORDERED = True

    def __init__(self, event):
        XMLElement.__init__(self, tag='note')
        self._event = None
        self.event = event
        self._type = None
        self._chord = None
        self._lyric = None

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        if isinstance(value, XMLPitch) or isinstance(value, XMLRest):
            self.replace_old_child_by_type(type=XMLEvent, new_child=value)
            self._event = value
        else:
            raise TypeError('event must be of type XMLEvent and not {}'.format(type(value)))

    @property
    def chord(self):
        return self._chord

    @chord.setter
    def chord(self, value):
        if value is False:
            value = None
        elif value is True:
            value = XMLChord()
        self._set_child(XMLChord, 'chord', value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._set_child(XMLType, 'type', value)

    @property
    def lyric(self):
        return self._lyric

    @lyric.setter
    def lyric(self, value):
        self._set_child(XMLLyricGroup, 'lyric', value)


class XMLNote(XMLNoteAbstract):
    def __init__(self, event, duration):
        XMLNoteAbstract.__init__(self, event=event)
        self._duration = None
        self.duration = duration

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._set_child(XMLDuration, 'duration', value)
