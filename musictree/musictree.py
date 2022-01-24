from musicxml.exceptions import XSDWrongAttribute
from musicxml.xmlelement.xmlelement import *
from typing import Union, List, Optional
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
    _ATTRIBUTES = {}

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
    _ATTRIBUTES = {'divisions'}

    def __init__(self, divisions=1, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLMeasure(*args, **kwargs)
        self.xml_object.xml_attributes = XMLAttributes()
        self._divisions = None
        self.divisions = divisions

    @property
    def divisions(self):
        return self._divisions

    @divisions.setter
    def divisions(self, val):
        self._divisions = val
        self.xml_object.xml_attributes.xml_divisions = val
        for child in self.get_children():
            child._update_duration()

    def add_child(self, child):
        super().add_child(child)
        for note in child.notes:
            self.xml_object.add_child(note.xml_object)
            note.parent_measure = self
        child._update_duration()


class Note(MusicTree):
    _ATTRIBUTES = {'midi', 'duration', 'voice', 'parent_measure'}

    def __init__(self, midi=None, duration=None, voice=1, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLNote(*args, **kwargs)
        self._midi = None
        self._duration = None
        self._voice = None

        self.duration = duration
        self.midi = midi
        self.voice = voice
        self.parent_measure = None

    def _add_xml_duration_to_note(self, duration: int):
        if duration is None:
            self.xml_object.xml_duration = None
            self.xml_object.xml_grace = None
        else:
            if not isinstance(duration, int):
                raise TypeError
            if duration < 0:
                raise ValueError
            if duration == 0:
                if self.midi and self.midi.value == 0:
                    raise ValueError('A rest cannot be a grace note.')
                self.xml_object.xml_duration = None
                if not self.xml_object.xml_grace:
                    self.xml_object.xml_grace = XMLGrace()
            else:
                self.xml_object.xml_grace = None
                self.xml_object.xml_duration = duration

    def update_midi(self):
        midi = self.midi
        if midi is None:
            self.xml_object.xml_pitch = None
            self.xml_object.xml_rest = None
        else:
            if not isinstance(midi, Midi):
                raise TypeError
            if self.midi.value == 0 and self.duration == 0:
                raise ValueError('A rest cannot be a grace note.')
            pitch_or_rest = midi.get_pitch_or_rest()
            if isinstance(pitch_or_rest, XMLRest):
                if self.xml_object.xml_pitch:
                    self.xml_object.xml_pitch = None
                self.xml_object.xml_rest = pitch_or_rest
                self.xml_object.xml_notehead = None
            else:
                if self.xml_object.xml_rest:
                    self.xml_object.xml_rest = None
                self.xml_object.xml_pitch = pitch_or_rest

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._add_xml_duration_to_note(value)
        self._duration = value

    @property
    def midi(self):
        return self._midi

    @midi.setter
    def midi(self, value):
        self._midi = value if isinstance(value, Midi) or value is None else Midi(value)
        self.update_midi()
        if value is not None:
            self.midi.parent_note = self

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
    _ATTRIBUTES = {'midis', 'quarter_duration', 'voice', 'notes', '_note_attributes'}

    def __init__(self, midis: Union[List[Union[float, int]], List[Midi], float, int, Midi],
                 quarter_duration: Union[float, int, Fraction, QuarterDuration], voice=1, **kwargs):
        super().__init__()
        self._quarter_duration = None
        self._voice = None
        self._midis = None
        self._notes = []

        self._note_attributes = kwargs
        self.voice = voice
        self.quarter_duration = quarter_duration
        self._set_midis(midis)

    def _get_duration(self):
        if self.get_parent() is None:
            raise MusicTreeDurationError(f"Chord without measure as parent cannot determine its music xml duration.")
        duration = float(self.quarter_duration) * self.get_parent().xml_object.find_child(XMLAttributes).find_child(
            XMLDivisions).value
        if duration != int(duration):
            raise ValueError(f'xml duration {duration} must be an integer.')
        return int(duration)

    def _update_duration(self):
        if self._quarter_duration is not None and self.get_parent():
            for note in self.notes:
                note.duration = self._get_duration()

    def _update_voice(self):
        if self.voice:
            for note in self.notes:
                note.xml_voice = str(self.voice)

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
        self._notes = [Note(midi, **self._note_attributes) for midi in self._midis]
        self._update_duration()
        self._update_voice()

    @property
    def is_rest(self):
        if self._midis[0].value == 0:
            return True
        else:
            return False

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, val):
        self._set_midis(val)

    @property
    def notes(self):
        return self._notes

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
        if not isinstance(self.quarter_duration, QuarterDuration):
            self._quarter_duration = QuarterDuration(val)
        else:
            self._quarter_duration.value = val
        self._update_duration()

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, val):
        self._voice = val
        self._update_voice()

    @property
    def xml_object(self):
        raise AttributeError("object 'Chord' has no xml_object. Use 'notes' property instead.")

    def to_string(self):
        raise AttributeError("object 'Chord' cannot return a string.")

    def __setattr__(self, key, value):
        if key not in self._ATTRIBUTES.union(self.PROPERTIES) and key not in [f'_{attr}' for attr in self._ATTRIBUTES.union(
                self.PROPERTIES)] and key not in self.__dict__:
            try:
                value = list(value)
            except TypeError:
                value = [value] * len(self.notes)
            for n, v in zip(self.notes, value):
                setattr(n, key, v)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        return [getattr(n, item) for n in self.notes]
