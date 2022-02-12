from musicxml.xmlelement.xmlelement import XMLNotations, XMLTuplet, XMLTimeModification, XMLBeam
from quicktions import Fraction

from musictree.chord import split_copy, group_chords
from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError, ChordHasNoQuarterDurationError, \
    ChordHasNoMidisError
from musictree.musictree import MusicTree
from musictree.quarterduration import QuarterDurationMixin, QuarterDuration
from musictree.util import lcm


class Beat(MusicTree, QuarterDurationMixin):
    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0
        self.left_over_chord = None

    def _add_child(self, child):
        child._parent = self
        self._children.append(child)
        if self.up.up.up.up:
            self.up.up.up.up.set_current_measure(staff_number=self.up.up.value, voice_number=self.up.value, measure=self.up.up.up)

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    @staticmethod
    def _split_chord(chord, quarter_durations):
        output = [chord]
        chord.quarter_duration = quarter_durations[0]
        offset = chord.offset + chord.quarter_duration
        for qd in quarter_durations[1:]:
            copied = split_copy(chord, qd)
            copied.offset = offset
            offset += qd
            output.append(copied)
        for index, ch in enumerate(output[:-1]):
            next_ch = output[index + 1]
            chord.add_tie('start')
            next_ch.add_tie('stop')
            for midi in next_ch.midis:
                midi.accidental.show = False
        return output

    def _split_not_writable(self, chord):
        if chord.offset == QuarterDuration(1, 8) and chord.quarter_duration > QuarterDuration(3, 8):
            return self._split_chord(chord, [QuarterDuration(3, 8), chord.quarter_duration - QuarterDuration(3, 8)])
        elif chord.offset == QuarterDuration(2, 8) and chord.quarter_duration == QuarterDuration(3, 8):
            return self._split_chord(chord, [QuarterDuration(2, 8), QuarterDuration(1, 8)])
        if chord.offset == QuarterDuration(3, 8) and chord.quarter_duration > QuarterDuration(1, 8):
            return self._split_chord(chord, [QuarterDuration(1, 8), chord.quarter_duration - QuarterDuration(1, 8)])

        elif chord.quarter_duration.numerator == 5:
            denom = chord.quarter_duration.denominator
            if denom == 6 and chord.offset != 0:
                return self._split_chord(chord, [QuarterDuration(2, 6), QuarterDuration(3, 6)])
            elif denom == 8 and chord.offset in [0, QuarterDuration(1, 4)]:
                return self._split_chord(chord, [QuarterDuration(4, 8), QuarterDuration(1, 8)])
            else:
                return self._split_chord(chord, [QuarterDuration(3, denom), QuarterDuration(2, denom)])
        elif chord.quarter_duration.numerator == 9:
            denom = chord.quarter_duration.denominator
            return self._split_chord(chord, [QuarterDuration(5, denom), QuarterDuration(4, denom)])
        else:
            return None

    def _update_dots(self, chord_group, actual_notes):
        for note in [n for ch in chord_group for n in ch.get_children()]:
            if note.number_of_dots is None:
                if note.quarter_duration != 0:
                    if note.quarter_duration.numerator % 3 == 0:
                        note.set_dots(number_of_dots=1)
                    elif note.quarter_duration == Fraction(1, 2) and actual_notes == 6:
                        note.set_dots(number_of_dots=1)
                    elif True in [note.quarter_duration == x for x in [7, 7 / 2, 7 / 4, 7 / 8, 7 / 16, 7 / 32, 7 / 64]]:
                        note.set_dots(number_of_dots=2)
                    else:
                        note.set_dots(number_of_dots=0)

    def _update_tuplets(self, chord_group, actual_notes, factor=1):
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

        actual_notes *= factor
        if int(actual_notes) != actual_notes:
            raise ValueError
        actual_notes = int(actual_notes)

        if actual_notes in normals:
            normal = normals[actual_notes]
            type_ = types[normal / factor]
            for chord in chord_group:
                for note in chord.notes:
                    note.xml_time_modification = XMLTimeModification()
                    note.xml_time_modification.xml_actual_notes = actual_notes
                    note.xml_time_modification.xml_normal_notes = normal
                    note.xml_time_modification.xml_normal_type = type_
                if chord == chord_group[0]:
                    add_bracket_to_notes(chord, type_='start')
                elif chord == chord_group[-1]:
                    add_bracket_to_notes(chord, type_='stop')
                else:
                    pass

    @staticmethod
    def _get_actual_notes(chords):
        denominators = list(dict.fromkeys([ch.quarter_duration.denominator for ch in chords]))
        if len(denominators) > 1:
            l_c_m = lcm(denominators)
            if l_c_m not in denominators:
                return None
            else:
                return l_c_m
        else:
            return next(iter(denominators))

    def _update_note_tuplets_dots(self):
        actual_notes = self._get_actual_notes(self.get_children())
        if not actual_notes:
            if self.quarter_duration == 1:
                grouped_chords = group_chords(self.get_children(), [1 / 2, 1 / 2])
                if grouped_chords:
                    for g in grouped_chords:
                        actual_notes = self._get_actual_notes(g)
                        self._update_tuplets(g, actual_notes, 1 / 2)
                        self._update_dots(g, actual_notes)
                    return
                else:
                    raise NotImplementedError('Beat cannot be halved. It cannot manage the necessary grouping of chords.')
            else:
                raise NotImplementedError('Beat with quarter_duration other than one cannot manage more than one group of chords.')
        self._update_tuplets(self.get_children(), actual_notes)
        self._update_dots(self.get_children(), actual_notes)

    def _update_note_beams(self):
        if self.get_children():
            beam_chord_group(chord_group=self.get_children())

    def _update_xml_notes(self):
        if self.get_children():
            for chord in self.get_children():
                chord._update_notes()
            self._update_note_tuplets_dots()
            self._update_note_beams()

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


def beam_chord_group(chord_group):
    def add_beam(chord, number, value):
        if value == 'hook':
            if chord.quarter_duration == QuarterDuration(1, 6) and chord.offset == QuarterDuration(1, 3):
                value = 'backward hook'
            else:
                value = 'forward hook'
        for note in chord.notes:
            note.xml_object.add_child(XMLBeam(number=number, value=value))

    def add_last_beam(chord, last_beam, current_beams, cont=False):
        if last_beam <= current_beams:
            if cont:
                add_beam(chord, 1, 'continue')
                for n in range(2, last_beam + 1):
                    add_beam(chord, n, 'end')
            else:
                for n in range(1, last_beam + 1):
                    add_beam(chord, n, 'end')
        else:
            if current_beams != 0:
                if cont:
                    add_beam(chord, 1, 'continue')
                    for n in range(2, current_beams + 1):
                        add_beam(chord, n, 'end')
                else:
                    for n in range(1, current_beams + 1):
                        add_beam(chord, n, 'end')
                for n in range(current_beams + 1, last_beam + 1):
                    add_beam(chord, n, 'backward hook')

    beams = {'eighth': 1, '16th': 2, '32nd': 3, '64th': 4, '128th': 5}
    current_beams = 0
    for index in range(len(chord_group) - 1):
        chord = chord_group[index]
        next_chord = chord_group[index + 1]
        t1, t2 = chord.notes[0].xml_type.value, next_chord.notes[0].xml_type.value
        b1, b2 = beams.get(t1), beams.get(t2)
        types = []
        if b1 and b2:
            if next_chord.offset == QuarterDuration(1, 2) and (b1 == 3 or b2 == 3 or current_beams == 3 or chord.quarter_duration ==
                                                               QuarterDuration(3, 8) or next_chord.quarter_duration == QuarterDuration(3,
                                                                                                                                       8)):
                add_last_beam(chord, b1, current_beams, True)
                current_beams = 1
            elif b2 < b1 <= current_beams:
                types.append(('continue', 0, b2))
                types.append(('end', b2, current_beams))
                current_beams = b1
            elif b2 < b1 > current_beams:
                if current_beams == 0:
                    types.append(('begin', 0, b2))
                else:
                    types.append(('continue', 0, current_beams))
                    types.append(('begin', current_beams, b2))
                    types.append(('hook', b2, b1))
                current_beams = b1
            elif b2 == b1 <= current_beams:
                types.append(('continue', 0, b1))
                current_beams = b1

            elif b2 == b1 > current_beams:
                if current_beams == 0:
                    types.append(('begin', 0, b2))
                else:
                    types.append(('continue', 0, current_beams))
                    types.append(('begin', current_beams, b2))
                current_beams = b1

            elif b2 > b1 <= current_beams:
                types.append(('continue', 0, b1))
                current_beams = b1

            elif b2 > b1 > current_beams:
                if current_beams == 0:
                    types.append(('begin', 0, b1))
                else:
                    types.append(('continue', 0, current_beams))
                    types.append(('begin', current_beams, b1))
                current_beams = b1
        elif b1 and not b2:
            add_last_beam(chord, b1, current_beams)
        else:
            pass
        for l in types:
            for n in range(l[1] + 1, l[2] + 1):
                add_beam(chord, n, l[0])
        if index == len(chord_group) - 2 and b2:
            add_last_beam(next_chord, b2, current_beams)
