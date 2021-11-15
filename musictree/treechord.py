from common.helpers import _check_type, _check_types


class TreeChord(object):
    """
    This class represents a chord as the third layer ?? of musical score's tree structure.
    """

    def __init__(self, midis=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._midis = None
        self.midis = midis

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, values):
        if not values:
            values = [71]
        else:
            _check_types('midis', values, (int, float,), none=False)

        self._midis = values

    def add_midi(self, value):
        _check_type('midi', value, (int, float), none=False)
        self.midis.append(value)
