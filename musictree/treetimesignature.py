import math

from common.helpers import _check_type, _check_permitted_value


class TreeTimeSignature(object):
    PERMITTED_BEAT_TYPES = [1, 2, 4, 8, 16, 32, 64]

    def __init__(self, beat=4, beat_type=4, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._beat = None
        self._beat_type = None
        self.beat = beat
        self.beat_type = beat_type

    @property
    def beat(self):
        return self._beat

    @beat.setter
    def beat(self, value):
        _check_type('beat_type', value, int, False)
        self._beat = value

    @property
    def beat_type(self):
        return self._beat_type

    @beat_type.setter
    def beat_type(self, value):
        _check_type('beat_type', value, int, False)
        _check_permitted_value('beat_type', value, self.PERMITTED_BEAT_TYPES)
        self._beat_type = value
