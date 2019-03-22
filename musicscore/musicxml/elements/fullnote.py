from musicscore.dtd.dtd import Sequence, Element, Choice, GroupReference
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import Empty
from musicscore.musicxml.types.simple_type import TypeStep, TypeSemitones, TypeOctave


class Step(XMLElement, TypeStep):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='step', value=value, *args, **kwargs)


class Alter(XMLElement, TypeSemitones):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='alter', value=value, *args, **kwargs)


class Octave(XMLElement, TypeOctave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='octave', value=value, *args, **kwargs)


class DisplayStep(XMLElement, TypeStep):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-step', value=value, *args, **kwargs)


class DisplayOctave(XMLElement, TypeOctave):
    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='display-octave', value=value, *args, **kwargs)


"""
The display-step-octave group contains the sequence of elements used by both the rest and unpitched elements. This
group is used to place rests and unpitched elements on the staff without implying that these elements have pitch.
Positioning follows the current clef. If percussion clef is used, the display-step and display-octave elements are
interpreted as if in treble clef, with a G in octave 4 on line 2. If not present, the note is placed on the middle
line"""
DisplayStepOctave = Sequence(
    Element(DisplayStep),
    Element(DisplayOctave)
)


class Event(XMLElement):
    """"""

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class Pitch(Event):
    """
    Pitch is represented as a combination of the step of the diatonic scale, the chromatic alteration, and the octave.
    """
    _DTD = Sequence(
        Element(Step),
        Element(Alter, min_occurrence=0),
        Element(Octave)
    )

    def __init__(self, step=Step('C'), alter=None, octave=Octave(4)):
        super().__init__(tag='pitch')
        self._step = None
        self.step = step
        self.alter = alter
        self._octave = None
        self.octave = octave

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._set_child(Step, 'step', value)

    @property
    def alter(self):
        alter = self.get_children_by_type(Alter)
        if alter:
            return alter[0]
        else:
            return None

    @alter.setter
    def alter(self, value):
        self._set_child(Alter, 'alter', value)

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):
        self._set_child(Octave, 'octave', value)


class Unpitched(Event):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='unpitched', *args, **kwargs)


class Measure(AttributeAbstract):
    def __init__(self, measure=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('measure', measure, 'TypeYesNo')


class Rest(Event, Measure):
    """
    The rest element indicates notated rests or silences. Rest elements are usually empty, but placement on the staff
    can be specified using display-step and  display-octave elements. If the measure attribute is set to yes, this
    indicates this is a complete measure rest.
    """

    _DTD = Sequence(
        GroupReference(DisplayStepOctave, min_occurrence=0)
    )

    def __init__(self, measure=None, *args, **kwargs):
        super().__init__(tag='rest', measure=measure, *args, **kwargs)


class Chord(Empty):
    """
    The chord element indicates that this note is an additional chord tone with the preceding note. The duration of
    this note can be no longer than the preceding note. In MuseData, a missing duration indicates the same length as
    the previous note, but the MusicXML format requires a duration for chord notes too
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='chord', *args, **kwargs)


"""
The full-note group is a sequence of the common note elements between cue/grace notes and regular (full) notes:
pitch, chord, and rest information, but not duration (cue and grace notes do not have duration encoded). Unpitched
elements are used for unpitched percussion, speaking voice, and other musical elements lacking determinate pitch.
"""

FullNote = Sequence(
    Element(Chord, min_occurrence=0),
    Choice(
        Element(Pitch),
        Element(Unpitched),
        Element(Rest)
    )
)
