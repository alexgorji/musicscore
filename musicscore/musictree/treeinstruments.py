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


class Violin(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Violin', abbreviation='vln.', number=number, *args, **kwargs)
        self.id = 'vln' + str(uuid.uuid4())


class Viola(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Viola', abbreviation='vla.', number=number, *args, **kwargs)
        self.id = 'vla' + str(uuid.uuid4())


class Cello(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Cello', abbreviation='vc.', number=number, *args, **kwargs)
        self.id = 'vc' + str(uuid.uuid4())


class Accordion(TreeInstrument):
    def __init__(self, number=None, *args, **kwargs):
        super().__init__(name='Accordion', abbreviation='acc.', number=number, *args, **kwargs)
        self.id = 'acc' + str(uuid.uuid4())
