from musicscore.musictree.midi import Midi
from musicscore.musictree.treechord import TreeChord


class ChordDictError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class AttributeIsNeededError(ChordDictError):
    def __init__(self, attribute):
        msg = f'ChordDict: Attribute {attribute} must be set '
        super().__init__(msg)


class ChordDict:
    def __init__(self, chord_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chord_dict = None
        self.chord_dict = chord_dict

    @staticmethod
    def _check_dict(val):
        needed_attributes = ['quarter_duration', 'midis']
        for needed_attribute in needed_attributes:
            if not val.get(needed_attribute):
                raise AttributeIsNeededError(needed_attribute)

    @staticmethod
    def _translate_midis(val):
        output = []
        try:
            raw_midis = list(val)
        except TypeError:
            raw_midis = [val]

        for raw_midi in raw_midis:
            if isinstance(raw_midi, int) or isinstance(raw_midi, float):
                midi = Midi(raw_midi)
                output.append(midi)
            else:
                raise TypeError(f'{val} must be of type int or float not {type(val)}')
        return output

    @property
    def chord_dict(self):
        return self._chord_dict

    @chord_dict.setter
    def chord_dict(self, val):
        if not isinstance(val, dict):
            raise TypeError(f"chord_dict.value must be of type dict not{type(val)}")
        self._check_dict(val)
        self._chord_dict = val

    def get_chord(self):
        midis = self._translate_midis(self.chord_dict.get('midis'))
        chord = TreeChord(quarter_duration=self.chord_dict.get('quarter_duration'), midis=midis)
        return chord

    def import_chord(self):
        raise NotImplementedError()
