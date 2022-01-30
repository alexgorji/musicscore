from fractions import Fraction

from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError
from musictree.musictree import MusicTree
from musictree.quarterduration import _check_quarter_duration, QuarterDurationMixin


class Beat(MusicTree, QuarterDurationMixin):
    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    @property
    def filled_quarter_duration(self):
        return self._filled_quarter_duration

    @property
    def offset(self):
        if not self.up:
            return None
        elif self.previous is None:
            return 0
        else:
            return self.previous.offset + self.previous.quarter_duration

    def add_child(self, child):
        if not self.up:
            raise BeatHasNoParentError('A child Chord can only be added to a beat if it has a voice parent.')
        if self.filled_quarter_duration == self.quarter_duration:
            raise BeatIsFullError()
        diff = child.quarter_duration - (self.quarter_duration - self.filled_quarter_duration)
        if diff <= 0:
            child._offset = self.filled_quarter_duration
            self._filled_quarter_duration += child.quarter_duration
        else:
            raise NotImplementedError

        return super().add_child(child)
