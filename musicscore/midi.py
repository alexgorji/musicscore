from musicscore.musicxml.elements.xml_note import XMLRest, XMLPitch


class Midi(object):
    """"""
    # (stem, alter, octaveAdd)
    standard = {
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

    flat = {
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

    sharp = {
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

    enharmonic_1 = {
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

    enharmonic_2 = {
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

    def __init__(self, value, accidental_mode='standard', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._accidental_mode = None
        self.value = value
        self.accidental_mode = accidental_mode

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):

        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError('midi.value must be of type float or int not{}'.format(type(v)))
        if v < 16 and v != 0:
            raise ValueError('midi.value must be greater than 16')
        self._value = v

    @property
    def accidental_mode(self):
        return self._accidental_mode

    @accidental_mode.setter
    def accidental_mode(self, value):
        permitted = ('standard', 'flat', 'sharp', 'enharmonic_1', 'enharmonic_2')
        if value not in permitted:
            raise TypeError('accidental_mode.value {} must be in {}'.format(value, permitted))
        self._accidental_mode = value

    def get_pitch_name(self):
        if self.accidental_mode == 'standard':
            output = self.standard[self.value % 12]

        elif self.accidental_mode == 'enharmonic_1':
            output = self.enharmonic_1[self.value % 12]

        elif self.accidental_mode == 'enharmonic_2':
            output = self.enharmonic_2[self.value % 12]

        elif self.accidental_mode == 'flat':
            output = self.flat[self.value % 12]

        elif self.accidental_mode == 'sharp':
            output = self.sharp[self.value % 12]

        output = list(output)
        output[2] += (self.value // 12) - 1
        return output

    def get_pitch_rest(self):
        if self.value == 0:
            return XMLRest()
        else:
            return XMLPitch(*self.get_pitch_name())
