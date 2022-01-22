from musicxml.exceptions import XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *
from typing import Union, List
from quicktions import Fraction

from musictree.exceptions import MusicTreeDurationError
from musictree.midi import Midi
from tree.tree import Tree


class MusicTree(Tree):
    """
    MusicTree is the parent class of all music tree objects: Score (root), Part (first layer), Measure (second layer),
    Chord (third layer). An abstract grid-like layer of TreeBeats can be imagined as a quantity between Measure and
    Chord depending on measures time signature.
    """
    _ATTRIBUTES = []

    def _check_child_to_be_added(self, child):
        if isinstance(self, Score) and not isinstance(child, Part):
            raise TypeError('Score accepts only children of type Part')

        if isinstance(self, Part) and not isinstance(child, Measure):
            raise TypeError('Part accepts only children of type Measure')

        if isinstance(self, Measure) and not isinstance(child, Chord):
            raise TypeError('Measure accepts only children of type Chord')

    @property
    def xml_object(self):
        return self._xml_object

    def _convert_attribute_to_child(self, name, value=None):
        setattr(self.xml_object, name, value)

    def to_string(self):
        if self._xml_object:
            return self.xml_object.to_string()
        else:
            raise ValueError(f'{self.__class__.__name__} has no xml object.')

    def __setattr__(self, key, value):
        if '_xml_object' in self.__dict__ and key not in self._ATTRIBUTES and key not in [f'_{attr}' for attr in self._ATTRIBUTES] and \
                key not in self.__dict__:
            setattr(self.xml_object, key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if item == 'xml_object':
            return super().__getattribute__(item)
        try:
            return self.xml_object.__getattr__(item)
        except AttributeError:
            return super().__getattribute__(item)


class Score(MusicTree):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLScorePartwise(*args, **kwargs)
        self._xml_part_list = self._xml_object.add_child(XMLPartList())


class Part(MusicTree):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLPart(*args, **kwargs)


class Measure(MusicTree):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLMeasure(*args, **kwargs)
        xattr = self._xml_object.add_child(XMLAttributes())
        xattr.add_child(XMLDivisions(1))

    def add_child(self, child):
        super().add_child(child)
        for note in child.get_notes():
            self.xml_object.add_child(note.xml_object)


class Note(MusicTree):
    _ATTRIBUTES = ['midi', 'duration', 'voice']

    def __init__(self, midi=None, duration=None, voice=1, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLNote(*args, **kwargs)
        self._midi = None
        self._duration = None
        self._voice = None

        self.duration = duration
        self.midi = midi
        self.voice = voice

    def _add_duration_to_note(self, duration: int):
        if duration == 0:
            self._xml_object.add_child(XMLGrace())
        else:
            self._xml_object.add_child(XMLDuration(duration))

    def _convert_midi_to_pitch(self, midi: Midi):
        if not isinstance(midi, Midi):
            raise TypeError
        if midi.value == 0:
            raise ValueError()

        if not self.xml_object.xml_pitch:
            self.xml_object.xml_pitch = midi.get_pitch_or_rest()
        else:
            step, alter, octave = midi.get_pitch_parameters()
            self.xml_object.xml_pitch.xml_step = step
            self.xml_object.xml_pitch.xml_alter = alter
            self.xml_object.xml_pitch.xml_octave = octave

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if self._duration is None:
            self._add_duration_to_note(value)
            self._duration = value
        else:
            raise AttributeError('duration can only be set by initiation.')

    @property
    def midi(self):
        return self._midi

    @midi.setter
    def midi(self, value):
        if self._midi is None:
            self._convert_midi_to_pitch(value)
            self._midi = value
        else:
            raise AttributeError('midi can only be set by initiation.')

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, val):
        self.xml_object.xml_voice = str(val)
        self._voice = val


class QuarterDuration:
    """
    Type for tree chord's duration. It has a quicktions.Fraction with limited denominator 1000 as its core.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, Fraction):
            try:
                val = Fraction(val)
            except TypeError as err:
                msg = err.args[0]
                msg += f' not {val.__class__.__name__} {val}'
                raise TypeError(msg)
        self._value = val.limit_denominator(1000)

    def __repr__(self):
        return f"{self.__class__.__name__}:value={self.value} at {id(self)}"

    def __str__(self):
        return f"{self.__class__.__name__}:value={self.value}"

    def __eq__(self, other):
        if other is not None:
            if not isinstance(other, QuarterDuration):
                other = self.__class__(other)
            return self.value.as_integer_ratio() == other.value.as_integer_ratio()
        else:
            return False

    def __ne__(self, other):
        if other is not None:
            if not isinstance(other, QuarterDuration):
                other = self.__class__(other)
            return self.value.as_integer_ratio() != other.value.as_integer_ratio()
        else:
            return True

    def __gt__(self, other):
        if other is None:
            raise TypeError("'>' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() > other.value.as_integer_ratio()

    def __ge__(self, other):
        if other is None:
            raise TypeError("'>=' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() >= other.value.as_integer_ratio()

    def __lt__(self, other):
        if other is None:
            raise TypeError("'<' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() < other.value.as_integer_ratio()

    def __le__(self, other):
        if other is None:
            raise TypeError("'<=' not supported between instances of 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.value.as_integer_ratio() <= other.value.as_integer_ratio()

    def __add__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for +: 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.__class__(self.value + other.value)

    def __mul__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for *: 'QuarterDuration' and 'NoneType'")
        if not isinstance(other, QuarterDuration):
            other = self.__class__(other)
        return self.__class__(self.value * other.value)

    def __truediv__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for /: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value / other.value)

    def __floordiv__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for //: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value // other.value)

    def __mod__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for %: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value % other.value)

    def __sub__(self, other):
        if other is None:
            raise TypeError("unsupported operand type(s) for -: 'QuarterDuration' and 'NoneType'")
        other = self.__class__(other)
        return self.__class__(self.value - other.value)

    def __pow__(self, power, modulo=None):
        return self.__class__(self.value.__pow__(power, modulo))

    def __float__(self):
        return float(self.value)


class Chord(MusicTree):
    """
    Chord is a sequence of one or more XMLNotes which occur at the same time in a XMLMeasure of a XMLPart.
    :param midis: midi, midis, midi value or midi values. 0 or [0] for a rest.
    :param quarter_duration: int or float for duration counted in quarters (crotchets). 0 for grace note (or chord).
    """
    _ATTRIBUTES = ['midis', 'quarter_duration', 'voice']

    def __init__(self, midis: Union[List[Union[float, int]], List[Midi], float, int, Midi],
                 quarter_duration: Union[float, int, Fraction, QuarterDuration], voice=1, **kwargs):
        super().__init__()
        self._quarter_duration = None
        self._voice = None
        self._midis = None
        self._notes = []

        self.note_attributes = kwargs
        self.voice = voice
        self.quarter_duration = quarter_duration
        self._set_midis(midis)

    @property
    def is_rest(self):
        if self._midis[0].value == 0:
            return True
        else:
            return False

    def _get_duration(self):
        if self.get_parent() is None:
            raise MusicTreeDurationError(f"Chord without measure as parent cannot determine its music xml duration.")
        duration = float(self.quarter_duration) * self.get_parent().xml_object.find_child(XMLAttributes).find_child(
            XMLDivisions).value
        if duration != int(duration):
            raise ValueError(f'xml duration {duration} must be an integer.')
        return int(duration)

    def _set_midis(self, midis):
        if isinstance(midis, str):
            raise TypeError
        if hasattr(midis, '__iter__'):
            pass
        else:
            midis = [midis]
        if len(midis) > 1 and 0 in midis:
            raise ValueError('Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.')

        if midis == [0] and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note')

        self._midis = [Midi(v) if not isinstance(v, Midi) else v for v in midis]

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, val):
        self._voice = val
        for note in self.get_notes():
            note.xml_voice = val

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, val):
        if not isinstance(val, int) and not isinstance(val, float) and not isinstance(val, Fraction) and not isinstance(val,
                                                                                                                        QuarterDuration):
            raise TypeError

        if val < 0:
            raise ValueError()
        old_q_d = self.quarter_duration
        if not isinstance(self.quarter_duration, QuarterDuration):
            self._quarter_duration = QuarterDuration(val)
        if old_q_d != self.quarter_duration:
            self._notes = []

    def get_notes(self):
        if self.get_parent():
            if not self._notes:
                for midi in self._midis:
                    new_note = Note(midi, self._get_duration())
                    if self.voice:
                        new_note.xml_voice = str(self.voice)
                    self._notes.append(new_note)
        return self._notes

    #
    # def get_xml_elements(self):
    #     output = []
    #     first_midi = True
    #     for midi in self.midis:
    #         note = XMLNote()

    @property
    def xml_object(self):
        raise AttributeError('TreeChord has not xml_object. Use get_elements() instead.')
