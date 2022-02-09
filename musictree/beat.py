from quicktions import Fraction

from musictree.chord import Chord, split_copy
from musicxml.xmlelement.xmlelement import XMLNotations, XMLTuplet, XMLTimeModification
from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError, ChordHasNoQuarterDurationError, \
    ChordHasNoMidisError, BeatHasWrongTupletError
from musictree.musictree import MusicTree
from musictree.quarterduration import QuarterDurationMixin, QuarterDuration
from musictree.util import lcm


class Beat(MusicTree, QuarterDurationMixin):
    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0
        self._divisions = None
        self.left_over_chord = None

    def _add_child(self, child):
        child._parent = self
        self._children.append(child)
        if self.up.up.up.up:
            self.up.up.up.up.set_current_measure(staff=self.up.up.value, voice=self.up.value, measure=self.up.up.up)

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    @property
    def divisions(self):
        return self._divisions

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

    def _split_not_writable(self, chord):
        if chord.quarter_duration == QuarterDuration(5, 6):
            if chord.offset == 0:
                chord.quarter_duration = QuarterDuration(1, 2)
                copied = split_copy(chord, QuarterDuration(1, 3))
            elif chord.offset == QuarterDuration(1, 6):
                chord.quarter_duration = QuarterDuration(1, 3)
                copied = split_copy(chord, QuarterDuration(1, 2))
            else:
                raise NotImplementedError
            chord.add_tie('start')
            copied.add_tie('stop')
            for midi in copied.midis:
                midi.accidental.show = False
            return [chord, copied]
        return None

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
            children = self._split_not_writable(child)
            if children:
                for ch in children:
                    self._add_child(ch)
                return children
            else:
                self._add_child(child)
                return child
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
                self._add_child(child)
                return child
            else:
                beats = self.up.get_children()[self.up.get_children().index(self):]
                return child.split_beatwise(beats)

    def _update_dots(self):
        for note in [n for ch in self.get_children() for n in ch.get_children()]:
            if note.number_of_dots is None:
                if note.quarter_duration != 0:
                    if note.quarter_duration.numerator % 3 == 0:
                        note.set_dots(number_of_dots=1)
                    elif note.quarter_duration == Fraction(1, 2) and self.divisions == 6:
                        note.set_dots(number_of_dots=1)
                    elif True in [note.quarter_duration == x for x in [7, 7 / 2, 7 / 4, 7 / 8, 7 / 16, 7 / 32, 7 / 64]]:
                        note.set_dots(number_of_dots=2)
                    else:
                        note.set_dots(number_of_dots=0)

    def update_notes(self):
        for chord in self.get_children():
            chord.update_notes()
        self.update_tuplets()
        self._update_dots()

    def _update_time_modification(self):
        def add_bracket_to_notes(chord, type_, number=1):
            for note in chord.notes:
                if not note.xml_notations:
                    note.xml_notations = XMLNotations()
                t = note.xml_notations.xml_tuplet = XMLTuplet()
                if type_ == 'start':
                    t.bracket = 'yes'
                t.number = number
                t.type = type_

        normals = {3: 2, 5: 4, 6: 4, 7: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8}
        types = {8: '32nd', 4: '16th', 2: 'eighth'}
        denominators = list(dict.fromkeys([ch.quarter_duration.denominator for ch in self.get_children()]))
        if len(denominators) > 1:
            l_c_m = lcm(denominators)
            if l_c_m not in denominators:
                raise NotImplementedError()
            else:
                actual_notes = l_c_m
        else:
            actual_notes = next(iter(denominators))
        if actual_notes in normals:
            self._divisions = actual_notes
            normal = normals[actual_notes]
            type_ = types[normal]
            for chord in self.get_children():
                for note in chord.notes:
                    note.xml_time_modification = XMLTimeModification()
                    note.xml_time_modification.xml_actual_notes = actual_notes
                    note.xml_time_modification.xml_normal_notes = normal
                    note.xml_time_modification.xml_normal_type = type_
                if chord == self.get_children()[0]:
                    add_bracket_to_notes(chord, type_='start')
                elif chord == self.get_children()[-1]:
                    add_bracket_to_notes(chord, type_='stop')
                else:
                    pass

    def update_tuplets(self):
        if self.get_children():
            self._update_time_modification()
