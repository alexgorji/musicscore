import uuid

from musicscore.musictree.midi import G, D, A, E, C, MidiNote, Midi, B, F, midi_to_frequency, frequency_to_midi
from musicscore.musictree.treeclef import TreeClef, TREBLE_CLEF, ALTO_CLEF, BASS_CLEF
from musicscore.musicxml.types.complextypes.midiinstrument import ComplexTypeMidiInstrument
from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation


class TreeInstrument(ComplexTypeMidiInstrument):
    _TAG = 'midi-instrument'

    def __init__(self, name, number_of_staves=None, abbreviation=None, number=None, *args, **kwargs):
        super().__init__(tag=self._TAG, id_='inst' + str(uuid.uuid4()), *args, **kwargs)
        self._part_name = PartName(name=name)
        self._part_abbreviation = PartAbbreviation()
        self._number_of_staves = None
        self._standard_clefs = None
        self._number = None

        self.number_of_staves = number_of_staves
        self.abbreviation = abbreviation
        self.number = number

    # public properties
    @property
    def abbreviation(self):
        return self._part_abbreviation.value

    @abbreviation.setter
    def abbreviation(self, val):
        self._part_abbreviation.value = val

    @property
    def name(self):
        return self._part_name.name

    @name.setter
    def name(self, val):
        self._part_name.name = val

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, val):
        if self._number is not None:
            raise AttributeError('number can only be set once')

        if val is not None and not isinstance(val, int):
            raise TypeError('number.value must be of type int not{}'.format(type(val)))
        self._number = val

        if self._number is not None:
            self.name += ' ' + str(self._number)
            self.abbreviation += ' ' + str(self._number)

    @property
    def part_name(self):
        return self._part_name

    @property
    def part_abbreviation(self):
        return self._part_abbreviation

    @property
    def standard_clefs(self):
        return self._standard_clefs

    @standard_clefs.setter
    def standard_clefs(self, vals):
        if not hasattr(vals, '__iter__'):
            vals = [vals]
        for index, val in enumerate(vals):
            if not isinstance(val, TreeClef):
                raise TypeError('standard_clef.value must be of type TreeClef not{}'.format(type(val)))
            vals[index] = val.__deepcopy__()

        if len(vals) > 1:
            for index, val in enumerate(vals):
                val.number = index + 1
        self._standard_clefs = vals

    @property
    def number_of_staves(self):
        return self._number_of_staves

    @number_of_staves.setter
    def number_of_staves(self, val):
        if val is not None and not isinstance(val, int):
            raise TypeError('number_of_staves.value must be of type int not{}'.format(type(val)))
        self._number_of_staves = val


# strings
class String(object):
    def __init__(self, number, tuning, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tuning = None
        self.number = number
        self.tuning = tuning

    @property
    def tuning(self):
        return self._tuning

    @tuning.setter
    def tuning(self, val):
        if not isinstance(val, Midi):
            raise TypeError('tuning.value must be of type Midi not{}'.format(type(val)))
        self._tuning = val

    def get_step(self, number):
        step = self.tuning.__deepcopy__()
        step.transpose(number)
        return step


class StringInstrument(TreeInstrument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strings = {}


class Violin(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Violin', abbreviation='vln.', number=number, *args, **kwargs)
        self.strings = {4: String(4, G(3)),
                        3: String(3, D(4)),
                        2: String(2, A(4)),
                        1: String(1, E(5))
                        }
        self.standard_clefs = TREBLE_CLEF


class Viola(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Viola', abbreviation='vla.', number=number, *args, **kwargs)
        self.strings = {4: String(4, C(3)),
                        3: String(3, G(3)),
                        2: String(2, D(4)),
                        1: String(1, A(4))
                        }
        self.standard_clefs = ALTO_CLEF


class Cello(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Cello', abbreviation='vc.', number=number, *args, **kwargs)
        self.strings = {4: String(4, C(2)),
                        3: String(3, G(2)),
                        2: String(2, D(3)),
                        1: String(1, A(3))
                        }
        self.standard_clefs = BASS_CLEF


class ViolaDamore(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Viola d\'amore\n430', abbreviation='vla.', number=number, *args, **kwargs)
        # skordatura
        self.strings = {1: String(1, B(4)),
                        2: String(2, B(4)),
                        3: String(3, F(4, '#')),
                        4: String(4, C(4)),
                        5: String(5, G(3)),
                        6: String(6, D(3)),
                        7: String(7, A(2))
                        }


# keyboards
class KeyboardInstrument(TreeInstrument):
    def __init__(self, number_of_staves=2, *args, **kwargs):
        super().__init__(number_of_staves=number_of_staves, *args, **kwargs)
        self.standard_clefs = [TREBLE_CLEF, BASS_CLEF]


class Accordion(KeyboardInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Accordion', abbreviation='acc.', number=number, *args, **kwargs)


class Piano(KeyboardInstrument):
    def __init__(self, *args, **kwargs):
        super().__init__(name='Piano', abbreviation='pno.', *args, **kwargs)


# brass
class NaturalInstrument(TreeInstrument):

    def __init__(self, key, a4=440, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._a4 = None
        self._key = None
        self._transposition = None
        self.a4 = a4
        self.key = key

    @property
    def a4(self):
        return self._a4

    @a4.setter
    def a4(self, val):
        try:
            float(val)
        except AttributeError:
            raise TypeError()
        self._a4 = val

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, val):
        if not isinstance(val, MidiNote):
            raise TypeError('key.value must be of type MidiNote not{}'.format(type(val)))
        self._key = val

    @property
    def transposition(self):
        return self._transposition

    @transposition.setter
    def transposition(self, val):
        self._transposition = val

    def get_fundamental_frequency(self):
        return midi_to_frequency(self.key, self.a4)

    def get_partial_midi_value(self, number):
        if not isinstance(number, int):
            return TypeError()
        if number <= 0:
            return ValueError()

        return frequency_to_midi(self.get_fundamental_frequency() * number, self.a4)


class Horn(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Horn', abbreviation='hrn.', number=number, *args, **kwargs)


class NaturalHorn(NaturalInstrument):
    def __init__(self, key=E(1, 'b'), a4=430, *args, **kwargs):
        super().__init__(name='Horn in E♭\n430', abbreviation='hrn.', key=key, a4=a4, *args, **kwargs)
        self.transposition = 9


# percussion
class Percussion(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Percussion', abbreviation='perc.', number=number, *args, **kwargs)
        self.tamtam = TamTam()
        self.cymbal_1 = Cymbal(1)
        self.cymbal_2 = Cymbal(2)
        self.cymbal_3 = Cymbal(3)
        self.cymbal_4 = Cymbal(4)
        self.cymbal_5 = Cymbal(5)


class TamTam(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Tam-tam', abbreviation='Tam-t.', number=number, *args, **kwargs)
        self.midi = B(3)
        self.midi.notehead = 'x'


class Cymbal(TreeInstrument):
    midis = {1: E(4), 2: G(4), 3: B(4), 4: D(5), 5: F(5)}

    def __init__(self, number=1, *args, **kwargs):
        super().__init__(name='cymbal-' + str(number), abbreviation='cym-' + str(number), number=number, *args,
                         **kwargs)

        self.midi = self.midis[self.number]
        self.midi.notehead = 'x'


# voice
class Voice(TreeInstrument):
    def __init__(self, *args, **kwargs):
        super().__init__(name='voice', abbreviation='v.', *args, **kwargs)
