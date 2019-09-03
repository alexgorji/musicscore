from musicscore.musictree.midi import G, D, A, E, C, MidiNote, Midi, B, F
from musicscore.musicxml.types.complextypes.midiinstrument import ComplexTypeMidiInstrument
from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation
import uuid


class TreeInstrument(ComplexTypeMidiInstrument):
    _TAG = 'midi-instrument'

    def __init__(self, name, abbreviation=None, number=None, *args, **kwargs):
        super().__init__(tag=self._TAG, id_='inst' + str(uuid.uuid4()), *args, **kwargs)
        self._part_name = PartName(name=name)
        self._part_abbreviation = PartAbbreviation()
        self.abbreviation = abbreviation
        self._number = None
        self.number = number

    @property
    def part_name(self):
        return self._part_name

    @property
    def part_abbreviation(self):
        return self._part_abbreviation

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
    def name(self):
        return self._part_name.name

    @name.setter
    def name(self, val):
        self._part_name.name = val

    @property
    def abbreviation(self):
        return self._part_abbreviation.value

    @abbreviation.setter
    def abbreviation(self, val):
        self._part_abbreviation.value = val


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
        if not isinstance(val, MidiNote):
            raise TypeError('tuning.value must be of type MidiNote not{}'.format(type(val)))
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


class Viola(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Viola', abbreviation='vla.', number=number, *args, **kwargs)
        self.strings = {4: String(4, C(3)),
                        3: String(3, G(3)),
                        2: String(2, D(4)),
                        1: String(1, A(4))
                        }


class Cello(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Cello', abbreviation='vc.', number=number, *args, **kwargs)
        self.strings = {4: String(4, C(2)),
                        3: String(3, G(2)),
                        2: String(2, D(3)),
                        1: String(1, A(3))
                        }


class ViolaDamore(StringInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Viola d\'more', abbreviation='vla.', number=number, *args, **kwargs)
        # skordatura
        self.strings = {1: String(1, B(4)),
                        2: String(2, B(4)),
                        3: String(3, F(4, '#')),
                        4: String(4, C(4)),
                        5: String(5, G(3)),
                        6: String(6, D(3)),
                        7: String(7, A(2))
                        }


class Accordion(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Accordion', abbreviation='acc.', number=number, *args, **kwargs)


class Horn(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Horn', abbreviation='hrn.', number=number, *args, **kwargs)


class TamTam(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Tam-tam', abbreviation='Tam-t.', number=number, *args, **kwargs)
        self.midi = B(3)
        self.midi.notehead = 'x'


class Percussion(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Percussion', abbreviation='perc.', number=number, *args, **kwargs)
        self.tamtam = TamTam()
