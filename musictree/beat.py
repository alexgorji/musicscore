from musictree.chord import Chord
from musicxml.xmlelement.xmlelement import XMLNotations
from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError, ChordHasNoQuarterDurationError, \
    ChordHasNoMidisError
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
        self._check_child_to_be_added(child)
        if not self.up:
            raise BeatHasNoParentError('A child Chord can only be added to a beat if it has a voice parent.')
        if child.quarter_duration is None:
            raise ChordHasNoQuarterDurationError('Chord with no quarter_duration cannot be added to Beat.')
        if not child.midis:
            raise ChordHasNoMidisError('Chord with no midis cannot be added to Beat.')
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
                return child.split_beatwise(beats)
        child._parent = self
        self._children.append(child)
        if self.up.up.up.up:
            self.up.up.up.up.set_current_measure(staff=self.up.up.value, voice=self.up.value, measure=self.up.up.up)
        return child

    def update_xml_brackets(self):
        def add_bracket_to_notes(chord, mode):
            for note in chord.notes:
                if not note.xml_notations:
                    note.xml_notations = XMLNotations()
                    note.xml_notations.xml_tuplet = mode
        start = False
        for index, chord in enumerate(self.get_children()[:-1]):
            if chord.xml_time_modification:
                if not start:
                    start = True
                add_bracket_to_notes(chord, 'start')
            if start and self.get_children()[index + 1].xml_time_modification is None:
                start = False
                add_bracket_to_notes(chord, 'stop')

