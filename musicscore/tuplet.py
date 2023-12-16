from typing import Optional

from musicscore.exceptions import TupletNormalTypeError
from musicxml import XMLTimeModification, XMLTuplet

TUPLETACTUALTONORMALNOTES = {3: 2, 5: 4, 6: 4, 7: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8}
TUPLETNORMALTYPES = {8: '32nd', 4: '16th', 2: 'eighth', 1: 'quarter', 0.5: 'half'}


class Tuplet:
    def __init__(self, actual_notes=3, normal_notes=None, normal_type=None, bracket_type=None, bracket_number=None,
                 quarter_duration=1):
        self._actual_notes = None
        self._normal_notes = None
        self._normal_type = None
        self._bracket_type = None
        self._bracket_number = None
        self._quarter_duration = None
        self.actual_notes = actual_notes
        self.normal_notes = normal_notes
        self.normal_type = normal_type
        self.bracket_type = bracket_type
        self.bracket_number = bracket_number
        self.quarter_duration = quarter_duration

    @property
    def actual_notes(self) -> int:
        return self._actual_notes

    @actual_notes.setter
    def actual_notes(self, val):
        if not isinstance(val, int):
            raise TypeError
        if val < 2:
            raise ValueError
        self._actual_notes = val

    @property
    def normal_notes(self) -> int:
        if self._normal_notes is None:
            return TUPLETACTUALTONORMALNOTES.get(self.actual_notes)
        return self._normal_notes

    @normal_notes.setter
    def normal_notes(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise TypeError
            if val < 2:
                raise ValueError
        self._normal_notes = val

    @property
    def normal_type(self) -> str:
        if self._normal_type is None:
            try:
                return TUPLETNORMALTYPES[self.normal_notes / self.quarter_duration]
            except KeyError:
                raise TupletNormalTypeError(
                    f'Cannot find normal type of normal_notes {self.normal_notes} with quarter_duration {self.quarter_duration}. You can set normal_type manually.')
        return self._normal_type

    @normal_type.setter
    def normal_type(self, val):
        permitted = [None, '1024th', '512th', '256th', '128th', '64th', '32nd', '16th', 'eighth', 'quarter', 'half',
                     'whole', 'breve', 'long', 'maxima']
        if val not in permitted:
            raise ValueError(f'Permitted type values are: {permitted}')
        self._normal_type = val

    @property
    def bracket_type(self) -> Optional[str]:
        return self._bracket_type

    @bracket_type.setter
    def bracket_type(self, val):
        permitted = [None, 'start', 'stop']
        if val not in permitted:
            raise ValueError(f'Permitted bracket_type values are: {permitted}')
        self._bracket_type = val

    @property
    def bracket_number(self) -> int:
        if self._bracket_number is None and self.bracket_type:
            return 1
        return self._bracket_number

    @bracket_number.setter
    def bracket_number(self, val):
        if val is not None:
            if not isinstance(val, int):
                raise TypeError
            if val < 1:
                raise ValueError
        self._bracket_number = val

    @property
    def ratio(self):
        return (self.actual_notes, self.normal_notes)

    def get_xml_time_modification(self) -> 'XMLTimeModification':
        output = XMLTimeModification()
        output.xml_actual_notes = self.actual_notes
        output.xml_normal_notes = self.normal_notes
        output.xml_normal_type = self.normal_type
        return output

    def get_xml_tuplet(self) -> XMLTuplet:
        if self.bracket_type:
            output = XMLTuplet(type=self.bracket_type, number=self.bracket_number)
            if self.bracket_type == 'start':
                output.bracket = 'yes'
            return output
