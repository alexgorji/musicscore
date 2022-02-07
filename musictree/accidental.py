from typing import Optional

from musicxml.xmlelement.xmlelement import XMLAccidental

from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper

STANDARD = {
    0: ('C', 0, 0),
    0.5: ('C', 0.5, 0),
    1: ('C', 1, 0),
    1.5: ('D', -0.5, 0),
    2: ('D', 0, 0),
    2.5: ('D', 0.5, 0),
    3: ('E', -1, 0),
    3.5: ('E', -0.5, 0),
    4: ('E', 0, 0),
    4.5: ('E', 0.5, 0),
    5: ('F', 0, 0),
    5.5: ('F', 0.5, 0),
    6: ('F', 1, 0),
    6.5: ('G', -0.5, 0),
    7: ('G', 0, 0),
    7.5: ('G', 0.5, 0),
    8: ('A', -1, 0),
    8.5: ('A', -0.5, 0),
    9: ('A', 0, 0),
    9.5: ('A', 0.5, 0),
    10: ('B', -1, 0),
    10.5: ('B', -0.5, 0),
    11: ('B', 0, 0),
    11.5: ('C', -0.5, 1)
}

FLAT = {
    0: ('C', 0, 0),
    0.5: ('D', -1.5, 0),
    1: ('D', -1, 0),
    1.5: ('D', -0.5, 0),
    2: ('D', 0, 0),
    2.5: ('E', -1.5, 0),
    3: ('E', -1, 0),
    3.5: ('E', -0.5, 0),
    4: ('E', 0, 0),
    4.5: ('F', -0.5, 0),
    5: ('F', 0, 0),
    5.5: ('G', -1.5, 0),
    6: ('G', -1, 0),
    6.5: ('G', -0.5, 0),
    7: ('G', 0, 0),
    7.5: ('A', -1.5, 0),
    8: ('A', -1, 0),
    8.5: ('A', -0.5, 0),
    9: ('A', 0, 0),
    9.5: ('B', -1.5, 0),
    10: ('B', -1, 0),
    10.5: ('B', -0.5, 0),
    11: ('B', 0, 0),
    11.5: ('C', -0.5, 1)
}

SHARP = {
    0: ('C', 0, 0),
    0.5: ('C', 0.5, 0),
    1: ('C', 1, 0),
    1.5: ('C', 1.5, 0),
    2: ('D', 0, 0),
    2.5: ('D', 0.5, 0),
    3: ('D', 1, 0),
    3.5: ('D', 1.5, 0),
    4: ('E', 0, 0),
    4.5: ('E', 0.5, 0),
    5: ('F', 0, 0),
    5.5: ('F', 0.5, 0),
    6: ('F', 1, 0),
    6.5: ('F', 1.5, 0),
    7: ('G', 0, 0),
    7.5: ('G', 0.5, 0),
    8: ('G', 1, 0),
    8.5: ('G', 1.5, 0),
    9: ('A', 0, 0),
    9.5: ('A', 0.5, 0),
    10: ('A', 1, 0),
    10.5: ('A', 1.5, 0),
    11: ('B', 0, 0),
    11.5: ('B', 0.5, 0)
}

ENHARMONIC1 = {
    0: ('B', 1, -1),
    0.5: ('D', -1.5, 0),
    1: ('D', -1, 0),
    1.5: ('C', 1.5, 0),
    2: ('C', 2, 0),
    2.5: ('E', -1.5, 0),
    3: ('D', 1, 0),
    3.5: ('D', 1.5, 0),
    4: ('F', -1, 0),
    4.5: ('F', -0.5, 0),
    5: ('E', 1, 0),
    5.5: ('G', -1.5, 0),
    6: ('G', -1, 0),
    6.5: ('F', 1.5, 0),
    7: ('F', 2, 0),
    7.5: ('A', -1.5, 0),
    8: ('G', 1, 0),
    8.5: ('G', 1.5, 0),
    9: ('G', 2, 0),
    9.5: ('B', -1.5, 0),
    10: ('A', 1, 0),
    10.5: ('A', 1.5, 0),
    11: ('C', -1, 1),
    11.5: ('B', 0.5, 0)
}

ENHARMONIC2 = {
    0: ('D', -2, 0),
    1: ('B', 2, -1),
    2: ('E', 2, 0),
    3: ('F', -2, 0),
    4: ('D', 2, 0),
    5: ('G', -2, 0),
    6: ('E', 2, 0),
    7: ('A', -2, 0),
    9: ('B', -2, 0),
    10: ('C', -2, 1),
    11: ('A', 2, 0)
}
SIGNS = {-2: 'flat-flat',
         -1.5: 'three-quarters-flat',
         -1: 'flat',
         -0.5: 'quarter-flat',
         0: 'natural',
         0.5: 'quarter-sharp',
         1: 'sharp',
         1.5: 'three-quarters-sharp',
         2: 'double-sharp'
         }


class Accidental(MusicTree, XMLWrapper):
    """
    Accidental can be of different modes: standard, flat, sharp, enharmonic_1 or enharmonic_2. It accepts furthermore two parameters:
    force_show and force_hide.
    """
    _ATTRIBUTES = {'mode', 'show', 'parent_midi'}

    # (stem, alter, octaveAdd)

    def __init__(self, mode='standard', show=True, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLAccidental(*args, **kwargs)
        self._mode = None
        self._parent_midi = None
        self._show = None
        self.show = show
        self.mode = mode

    def _update_parent_midi(self):
        if self.parent_midi and self.parent_midi.value != 0:
            self.parent_midi._update_pitch_parameters()

    def _update_xml_object(self):
        if self.sign:
            self._xml_object.value = self.sign

    @XMLWrapper.xml_object.getter
    def xml_object(self):
        if self.parent_midi and self.parent_midi.value == 0:
            return None
        if self.show is True:
            return self._xml_object
        elif self.show is False:
            return None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        permitted = ('standard', 'flat', 'sharp', 'enharmonic_1', 'enharmonic_2')
        if value not in permitted:
            raise TypeError(f'accidental_mode.value {value} must be in {permitted}')
        self._mode = value
        self._update_xml_object()
        self._update_parent_midi()

    @property
    def parent_midi(self):
        return self._parent_midi

    @parent_midi.setter
    def parent_midi(self, val):
        self._parent_midi = val
        self._update_xml_object()
        self._update_parent_midi()
        self._parent = val

    @property
    def sign(self):
        try:
            alter = self.get_pitch_parameters()[1]
            return SIGNS[alter]
        except TypeError:
            return None

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError
        if val != self._show:
            self._show = val
            try:
                self.up.up._update_xml_accidental()
            except AttributeError:
                pass

    def get_pitch_parameters(self, midi_value: Optional[float] = None) -> Optional[tuple]:
        """
        :return: a tuple consisting of pitch stem name, alter value and octave value. A midi_value 0 returns None. If midi_value is None
        and parent_midi exists, its value will be used.
        """
        if midi_value is None:
            if self.parent_midi:
                midi_value = self.parent_midi.value
            else:
                return None
        if midi_value == 0:
            return None

        if self.mode == 'standard':
            output = STANDARD[midi_value % 12]

        elif self.mode == 'enharmonic_1':
            output = ENHARMONIC1[midi_value % 12]

        elif self.mode == 'enharmonic_2':
            output = ENHARMONIC2[midi_value % 12]

        elif self.mode == 'flat':
            output = FLAT[midi_value % 12]

        elif self.mode == 'sharp':
            output = SHARP[midi_value % 12]

        else:
            raise ValueError
        return output[0], output[1], output[2] + (int(midi_value // 12)) - 1

    def __copy__(self):
        return self.__class__(mode=self.mode, show=self.show)
