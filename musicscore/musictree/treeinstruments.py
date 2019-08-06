from musicscore.musicxml.types.complextypes.midiinstrument import ComplexTypeMidiInstrument
from musicscore.musicxml.types.complextypes.scorepart import PartName, PartAbbreviation


class TreeInstrument(ComplexTypeMidiInstrument):
    def __init__(self, name, number=None, *args, **kwargs):
        super().__init__(id='tmp_id', *args, **kwargs)
        self._number = None
        self.number = number
        self._part_name = PartName(name=name)
        self._part_abbreviation = PartAbbreviation()

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Violine'
        self.abbreviation = 'vln'
        self.id = 'vln'
        if self.number is not None:
            self.id += str(self.number)
            self.name += ' ' + str(self.number)
            self.abbreviation += ' ' + str(self.number)
