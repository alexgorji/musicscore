from typing import Optional, List

from musicxml.xmlelement.xmlelement import XMLNotations, XMLTuplet, XMLTimeModification, XMLBeam
from quicktions import Fraction

from musictree.chord import split_copy, group_chords, Chord
from musictree.exceptions import BeatWrongDurationError, BeatIsFullError, BeatHasNoParentError, ChordHasNoQuarterDurationError, \
    ChordHasNoMidisError, AlreadyFinalUpdated, BeatNotFullError
from musictree.core import MusicTree
from musictree.quarterduration import QuarterDuration, QuarterDurationMixin
from musictree.util import lcm

__all__ = ['SPLITTABLES', 'Beat', 'beam_chord_group']

#: {offset : {chord.quarter_duration: split quarter_durations, ...}, ...}
SPLITTABLES = {
    QuarterDuration(0): {
        QuarterDuration(5, 6): [QuarterDuration(3, 6), QuarterDuration(2, 6)],
        QuarterDuration(5, 7): [QuarterDuration(3, 7), QuarterDuration(2, 7)],
        QuarterDuration(5, 8): [QuarterDuration(4, 8), QuarterDuration(1, 8)],
        QuarterDuration(5, 9): [QuarterDuration(3, 9), QuarterDuration(2, 9)],
        QuarterDuration(5, 11): [QuarterDuration(4, 11), QuarterDuration(1, 11)],

        QuarterDuration(7, 8): [QuarterDuration(4, 8), QuarterDuration(3, 8)],
        QuarterDuration(7, 9): [QuarterDuration(4, 9), QuarterDuration(3, 9)],
        QuarterDuration(7, 10): [QuarterDuration(5, 10), QuarterDuration(2, 10)],
        QuarterDuration(7, 11): [QuarterDuration(4, 11), QuarterDuration(3, 11)],
    },
    QuarterDuration(1, 8): {
        QuarterDuration(4, 8): [QuarterDuration(3, 8), QuarterDuration(1, 8)],
        QuarterDuration(5, 8): [QuarterDuration(3, 8), QuarterDuration(2, 8)],
        QuarterDuration(6, 8): [QuarterDuration(3, 8), QuarterDuration(3, 8)],
        QuarterDuration(7, 8): [QuarterDuration(3, 8), QuarterDuration(4, 8)],
    },
    QuarterDuration(2, 8): {
        QuarterDuration(3, 8): [QuarterDuration(2, 8), QuarterDuration(1, 8)],
        QuarterDuration(5, 8): [QuarterDuration(2, 8), QuarterDuration(3, 8)],
    },
    QuarterDuration(3, 8): {
        QuarterDuration(2, 8): [QuarterDuration(1, 8), QuarterDuration(1, 8)],
        QuarterDuration(3, 8): [QuarterDuration(1, 8), QuarterDuration(2, 8)],
        QuarterDuration(4, 8): [QuarterDuration(1, 8), QuarterDuration(3, 8)],
        QuarterDuration(5, 8): [QuarterDuration(1, 8), QuarterDuration(4, 8)],
    },
    QuarterDuration(1, 7): {
        QuarterDuration(5, 7): [QuarterDuration(3, 7), QuarterDuration(2, 7)],
        QuarterDuration(6, 7): [QuarterDuration(3, 7), QuarterDuration(3, 7)],
    },
    QuarterDuration(2, 7): {
        QuarterDuration(5, 7): [QuarterDuration(3, 7), QuarterDuration(2, 7)],
    },
    QuarterDuration(1, 6): {
        QuarterDuration(4, 6): [QuarterDuration(2, 6), QuarterDuration(2, 6)],
        QuarterDuration(5, 6): [QuarterDuration(2, 6), QuarterDuration(3, 6)],
    },
    QuarterDuration(2, 6): {
        QuarterDuration(3, 6): [QuarterDuration(2, 6), QuarterDuration(1, 6)],
        QuarterDuration(5, 6): [QuarterDuration(2, 6), QuarterDuration(3, 6)],
    },
}


def _find_nearest_quantized_value(quantized_values, values):
    output = []
    for value in values:
        nearest_quantized = min(enumerate(quantized_values), key=lambda x: abs(x[1] - value))[1]
        delta = nearest_quantized - value
        output.append((nearest_quantized, delta))
    return output


def _find_q_delta(quantized_locations, values):
    qs = _find_nearest_quantized_value(quantized_locations, values)
    d = 0
    for q in qs:
        d += abs(q[1])
    return d


def _find_quantized_locations(duration, subdivision):
    output = range(subdivision + 1)
    fr = duration / subdivision
    output = [x * fr for x in output]
    return output


class Beat(MusicTree, QuarterDurationMixin):
    """
    Beat is the direct ancestor of chords. Each :obj:`~musictree.chord.Chord` is placed with an offset between 0 and beat's
    quarter duration inside the beat as its child .

    Quarter duration of a beat's :obj:`~musictree.chord.Chord` child can exceed its own quarter duration. If a
    :obj:`~musictree.chord.Chord` is longer than the quarter duration of beat's parent :obj:`~musictree.voice.Voice`,
    a leftover :obj:`~musictree.chord.Chord` will be added as leftover property to the :obj:`~musictree.voice.Voice` which will be added
    to next measure's appropriate voice .

    Beat manages splitting of each child :obj:`~musictree.chord.Chord` into appropriate tied :obj:`~musictree.chord.Chord` s if needed,
    for example if this chord has a non-writable quarter duration like 5/6.

    The dots and tuplets are also added here to :obj:`~musictree.chord.Chord` or directly to their :obj:`~musictree.note.Note` children.

    Beaming and quantization are also further important tasks of a beat.
    """

    _PERMITTED_DURATIONS = {4, 2, 1, 0.5}

    def __init__(self, quarter_duration=1):
        super().__init__(quarter_duration=quarter_duration)
        self._filled_quarter_duration = 0
        self.leftover_chord = None
        self._final_updated = False

    def _add_child(self, child):
        child._parent = self
        self._children.append(child)
        if self.up.up.up.up:
            self.up.up.up.up.set_current_measure(staff_number=self.up.up.number, voice_number=self.up.number, measure=self.up.up.up)

    def _change_children_quarter_durations(self, quarter_durations):
        if len(quarter_durations) != len(self.get_children()):
            raise ValueError
        if sum(quarter_durations) != self.quarter_duration:
            raise ValueError
        for qd, ch in zip(quarter_durations, self.get_children()):
            ch._quarter_duration = qd

    def _check_permitted_duration(self, val):
        for d in self._PERMITTED_DURATIONS:
            if val == d:
                return
        raise BeatWrongDurationError(f"Beat's quarter duration {val} is not allowed.")

    def _get_quantized_locations(self, subdivision):
        return _find_quantized_locations(self.quarter_duration, subdivision)

    def _get_quantized_quarter_durations(self, quarter_durations):
        if sum(quarter_durations) != self.quarter_duration:
            raise ValueError(
                f"Sum of quarter_durations '{quarter_durations}: {sum(quarter_durations)}' is not equal to beat quarter_duration "
                f"'{self.quarter_duration}'")

        def _get_positions():
            output = [0]
            for i, qd in enumerate(quarter_durations):
                output.append(output[i] + qd)
            return output

        positions = _get_positions()
        permitted_divs = self.get_possible_subdivisions()[:]
        best_div = permitted_divs.pop(0)
        last_q_delta = _find_q_delta(self._get_quantized_locations(subdivision=best_div), positions)

        for div in permitted_divs:
            current_q_delta = _find_q_delta(self._get_quantized_locations(subdivision=div), positions)

            if current_q_delta < last_q_delta:
                best_div = div
                last_q_delta = current_q_delta

            elif (current_q_delta == last_q_delta) and (div < best_div):
                best_div = div

        quantized_positions = [f[0] for f in
                               _find_nearest_quantized_value(self._get_quantized_locations(subdivision=best_div),
                                                             positions)]

        quantized_durations = []

        for i in range(len(quarter_durations)):
            fr = Fraction(
                quantized_positions[i + 1] - quantized_positions[i]).limit_denominator(
                int(best_div / self.quarter_duration))
            quantized_durations.append(QuarterDuration(fr))
        return quantized_durations

    @staticmethod
    def _split_chord(chord, quarter_durations):
        output = [chord]
        chord._quarter_duration = quarter_durations[0]
        for qd in quarter_durations[1:]:
            copied = split_copy(chord, qd)
            output.append(copied)
        for index, ch in enumerate(output[:-1]):
            next_ch = output[index + 1]
            chord.add_tie('start')
            next_ch.add_tie('stop')
            for midi in next_ch.midis:
                midi.accidental.show = False
        return output

    def _split_not_writable(self, chord, offset):
        if SPLITTABLES.get(offset):
            quarter_durations = SPLITTABLES.get(offset).get(chord.quarter_duration)
            if quarter_durations:
                return self._split_chord(chord, quarter_durations)

    def _update_dots(self, chord_group, actual_notes):
        for note in [n for ch in chord_group for n in ch.get_children()]:
            if note.number_of_dots is None:
                if note.quarter_duration != 0:
                    if note.quarter_duration.numerator % 3 == 0:
                        note.update_dots(number_of_dots=1)
                    elif note.quarter_duration == Fraction(1, 2) and actual_notes == 6:
                        note.update_dots(number_of_dots=1)
                    elif True in [note.quarter_duration == x for x in [7, 7 / 2, 7 / 4, 7 / 8, 7 / 16, 7 / 32, 7 / 64]]:
                        note.update_dots(number_of_dots=2)
                    else:
                        note.update_dots(number_of_dots=0)

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

    def _update_note_tuplets_and_dots(self):
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

    def _remove_zero_quarter_durations(self):
        zeros = [ch for ch in self.get_children() if ch.quarter_duration == 0]
        for ch in zeros:
            if 'start' in ch._ties:
                pass
            elif 'stop' in ch._ties:
                ch.up.remove(ch)
            else:
                pass

    @property
    def is_filled(self) -> bool:
        """
        :return: ``True`` if no children can be added anymore. If ``False`` there is still room for further child or children.
        :rtype: bool
        """
        if self.filled_quarter_duration == self.quarter_duration:
            return True
        else:
            return False

    @property
    def filled_quarter_duration(self):
        """
        :return: How much of beat's quarter duration is already filled.
        :rtype: QuarterDuration
        """
        return self._filled_quarter_duration

    @property
    def number(self) -> int:
        """
        :return: Beat's number inside its parent's :obj:`musictree.voice.Voice`
        :rtype: int
        """
        return self.up.get_children().index(self) + 1

    @property
    def offset(self) -> QuarterDuration:
        """
        :return: Offset in Beat's parent :obj:`musictree.voice.Voice`
        :rtype: QuarterDuration
        """
        if not self.up:
            return None
        elif self.previous is None:
            return 0
        else:
            return self.previous.offset + self.previous.quarter_duration

    def add_child(self, child: Chord) -> List['Chord']:
        """
        If child's quarter duration is less than beat's remaining quarter duration: child is added to the beat.

        If child's quarter duration is greater than beat's remaining quarter duration: :obj:`~musictree.chord.Chord.split_and_add_beatwise` is
        called. It is possible to add a chord with a quarter duration exceeding the beat's quarter duration without splitting the chord.
        For example if the first beat in a 4/4 measure gets a chord with quarter duration 3, the chord will be added to this first beat as a
        child and the following two beats will be set to filled without having a child themselves and the parent
        :obj:`~musictree.voice.Voice` return the fourth beat if its :obj:`~musictree.voice.Voice.get_current_beat` is called.

        If child's quarter duration exceeds the voice's remaining quarter duration a leftover chord will be added to the voice and can be
        accessed when the next measure is created.

        :param child: Chord to be added as child
        :return: added chord or a list of split chords
        """
        self._check_child_to_be_added(child)
        if not self.up:
            raise BeatHasNoParentError('A child Chord can only be added to a beat if it has a voice parent.')
        if child.quarter_duration is None:
            raise ChordHasNoQuarterDurationError('Chord with no quarter_duration cannot be added to Beat.')
        if not child.midis:
            raise ChordHasNoMidisError('Chord with no midis cannot be added to Beat.')
        if self.is_filled:
            raise BeatIsFullError()
        diff = child.quarter_duration - (self.quarter_duration - self.filled_quarter_duration)
        if diff <= 0:
            self._filled_quarter_duration += child.quarter_duration
            self._add_child(child)
            return [child]
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
                return [child]
            else:
                beats = self.up.get_children()[self.up.get_children().index(self):]
                return child.split_and_add_beatwise(beats)

    def add_chord(self, chord: Optional[Chord] = None) -> List['Chord']:
        """
        :param chord: if None chord is set to a :obj:`~musictree.chord.Chord` with quarter_duration 1 and midis set to 60
        :return: added chord or a list of split chords
        """
        if chord is None:
            chord = Chord(midis=60, quarter_duration=self.quarter_duration)
        return self.add_child(chord)

    def final_updates(self):
        """
        final_updates can only be called once.

        - It calls :obj:`~musictree.chord.Chord.final_updates()` method of all :obj:`~musictree.chord.Chord` children.
        - Following updates are triggered: update_note_tuplets_and_dots, update_note_beams, quantize_quarter_durations (if quantize is
          True), split_not_writable_chords
        """
        if self._final_updated:
            raise AlreadyFinalUpdated(self)

        if self.is_filled is False:
            BeatNotFullError()

        if self.get_children():
            for chord in self.get_children():
                chord.final_updates()
            self._update_note_tuplets_and_dots()
            self._update_note_beams()

        self._final_updated = True

    def get_children(self) -> List[Chord]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musictree.chord.Chord`]
        """
        return super().get_children()

    def get_parent(self) -> 'Voice':
        """
        :return: parent
        :rtype: :obj:`~musictree.voice.Voice`
        """
        return super().get_parent()

    def split_not_writable_chords(self) -> None:
        """
        This method checks if the quarter duration of all children chords must be split according to :obj:`~musictree.beat.SPLITTABLES`
        dictionary. If chord's offset and its quarter duration exist in the dictionary a list of splitting quarter durations can be
        accessed like this: ``SPLITTABLES[chord.offset[chord.quarter_duration]]`` This dictionary can be manipulated by user during runtime
        if needed. Be careful with not writable quarter durations which have to be split (for example 5/6 must be split to 3/6,
        2/6 or some other writable quarter durations).

        :obj:`~musictree.measure.Measure.final_updates()` loops over all its beats calls this method.
        """
        for chord in self.get_children()[:]:
            split = self._split_not_writable(chord, chord.offset)
            if split:
                for ch in split:
                    ch._parent = self
                if chord == self.get_children()[-1]:
                    self._children = self.get_children()[:-1] + split
                else:
                    index = self.get_children().index(chord)
                    self._children = self.get_children()[:index] + split + self.get_children()[index + 1:]

    def quantize_quarter_durations(self):
        """
        When called the positioning of children will be quantized according to :obj:`musictree.core.MusicTree.get_possible_subdivisions()`
        """
        if self.get_possible_subdivisions() and self.get_children():
            if self._get_actual_notes(self.get_children()) in self.get_possible_subdivisions():
                pass
            else:
                quarter_durations = [chord.quarter_duration for chord in self.get_children()]
                if len([d for d in quarter_durations if d != 0]) > 1:
                    self._change_children_quarter_durations(self._get_quantized_quarter_durations(quarter_durations))
                    self._remove_zero_quarter_durations()


def beam_chord_group(chord_group: List['Chord']) -> None:
    """
    Function for setting beams of a list of chords (chord_group). This function is used to create or update beams inside a beat.

    :param chord_group:
    :return: None
    """
    chord_group = [ch for ch in chord_group if ch.quarter_duration != 0]

    def add_beam(chord, number, value):
        if value == 'hook':
            if chord.quarter_duration == QuarterDuration(1, 6) and chord.offset == QuarterDuration(1, 3):
                value = 'backward hook'
            else:
                value = 'forward hook'
        for note in chord.notes:
            note.xml_object.add_child(XMLBeam(number=number, value_=value))

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
        t1, t2 = chord.notes[0].xml_type.value_, next_chord.notes[0].xml_type.value_
        b1, b2 = beams.get(t1), beams.get(t2)
        types = []
        if b1 and b2:
            if next_chord.offset == QuarterDuration(1, 2) \
                    and current_beams != 0 \
                    and (b1 == 3 or b2 == 3
                         or current_beams == 3
                         or chord.quarter_duration == QuarterDuration(3, 8)
                         or next_chord.quarter_duration == QuarterDuration(3, 8)):
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
