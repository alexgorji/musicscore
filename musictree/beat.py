from musictree.chord import Chord
from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError
from musictree.musictree import MusicTree
from musictree.quarterduration import QuarterDurationMixin


class Beat(MusicTree, QuarterDurationMixin):
    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0
        self.left_over_chord = None

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    @property
    def is_filled(self):
        if self.filled_quarter_duration == self.quarter_duration:
            return True
        else:
            return False

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
        if self.is_filled:
            raise BeatIsFullError()
        child.offset = self.filled_quarter_duration
        diff = child.quarter_duration - (self.quarter_duration - self.filled_quarter_duration)
        if diff <= 0:
            self._filled_quarter_duration += child.quarter_duration
        else:
            if child.split:
                remaining_quarter_duration = child.quarter_duration
                current_beat = self
                while remaining_quarter_duration and current_beat:
                    if current_beat.quarter_duration < remaining_quarter_duration:
                        current_beat._filled_quarter_duration += current_beat.quarter_duration
                        remaining_quarter_duration -= current_beat.quarter_duration
                        current_beat = current_beat.next
                    else:
                        current_beat._filled_quarter_duration += remaining_quarter_duration
                        break
            else:
                beats = self.up.get_children()[self.up.get_children().index(self):]
                child.split_beatwise(beats)
                return child

        return super().add_child(child)
